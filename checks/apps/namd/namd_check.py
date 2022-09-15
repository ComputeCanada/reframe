import os

import reframe as rfm
import reframe.utility.sanity as sn


class NamdBaseCheck(rfm.RunOnlyRegressionTest):
    def __init__(self, arch, flavor):
        super().__init__()
        self.descr = 'NAMD check (%s)' % (arch)
        self.valid_prog_environs = []
        if flavor == 'multicore':
            self.valid_prog_environs = ['intel-2016.4', 'intel-2018.3']
        if flavor == 'verbs':
            self.valid_prog_environs = ['intel-2016.4', 'intel-2018.3']

        self.modules = ['namd-%s' % flavor]

        # Reset sources dir relative to the SCS apps prefix
        self.sourcesdir = os.path.join(self.current_system.resourcesdir, 'NAMD')
        self.executable = 'namd2'
        self.use_multithreading = True

        energy = sn.avg(sn.extractall(r'^ENERGY:(\s+\S+){10}\s+(?P<energy>\S+)',
                                      self.stdout, 'energy', float))
        energy_reference = -2451359.5
        energy_diff = sn.abs(energy - energy_reference)
        self.sanity_patterns = sn.all([
            sn.assert_eq(sn.count(sn.extractall(
                         r'TIMING: (?P<step_num>\S+)  CPU:',
                         self.stdout, 'step_num')), 25),
            sn.assert_lt(energy_diff, 2720)
        ])

        self.perf_patterns = {
            'days_ns': sn.avg(sn.extractall(
                'Info: Benchmark time: \S+ CPUs \S+ '
                's/step (?P<days_ns>\S+) days/ns \S+ MB memory',
                self.stdout, 'days_ns', float))
        }

        self.maintainers = ['CB', 'LM']
        self.tags = {'scs', 'external-resources'}
        self.strict_check = False
        self.extra_resources = {
            'switches': {
                'num_switches': 1
            }
        }


@rfm.simple_test
class NamdGPUCheck(NamdBaseCheck):
    require_version = '>=2.16.0'
    flavorgputype = parameter(
        [f,g]
        for f in ['multicore', 'verbs', 'verbs-smp']
        for g in ['any', 'k20', 'k80', 'p100', 'v100', 'lgpu', 't4'])
    def __init__(self):
        flavor, gputype = self.flavorgputype
        super().__init__(gputype, flavor)
        self.valid_systems = ['cedar:gpu', 'beluga:gpu', 'helios:gpu', 'graham:gpu']
        self.extra_resources = {'gpu': { 'num_gpus_per_node': 1 } }
        if gputype == 'k20':
            self.valid_systems = ['helios']
            self.extra_resources = {'k20': { 'num_k20_per_node': 1 } }
        elif gputype == 'k80':
            self.valid_systems = ['helios']
            self.extra_resources = {'k80': { 'num_k80_per_node': 1 } }
        elif gputype == 'p100':
            self.valid_systems = ['cedar:gpu', 'graham:gpu']
            self.extra_resources = {'p100': { 'num_p100_per_node': 1 } }
        elif gputype == 'v100':
            self.valid_systems = ['cedar:gpu', 'graham:gpu', 'beluga:gpu']
            self.extra_resources = {'v100': { 'num_v100_per_node': 1 } }
        elif gputype == 'lgpu':
            self.valid_systems = ['cedar:gpu']
            self.extra_resources = {'lgpu': { 'num_lgpu_per_node': 1 } }
        elif gputype == 't4':
            self.valid_systems = ['graham:gpu']
            self.extra_resources = {'t4': { 'num_t4_per_node': 1 } }

        self.extra_resources['mem-per-cpu'] = {'mem_per_cpu' : '512m'}

        if flavor == 'multicore':
            self.valid_prog_environs += ['iccifortcuda-2016.4.100', 'iccifortcuda-2018.3.100']

        cluster = os.environ['CC_CLUSTER']

        if cluster == "graham":
            if gputype in ['any','p100']:
                self.num_cpus_per_task = 16
            else:
                self.num_cpus_per_task = 4
            self.executable_opts = ['+idlepoll', '+ppn %s' % str(self.num_cpus_per_task - 1), 'stmv.namd']

        self.num_tasks = 1

        self.reference = {
                'daint:gpu': {'days_ns': (0.11, None, 0.05, 'days/ns')}
        }


@rfm.simple_test
class NamdCPUCheck(NamdBaseCheck):
    require_version = '>=2.16.0'
    flavor = parameter(('multicore', 'verbs', 'mpi'))
    def __init__(self):
        super().__init__('cpu', self.flavor)
        self.valid_systems = ['build-node:serial','build-node:parallel',
                              'beluga:cpu_parallel', 'cedar:cpu_parallel', 'graham:cpu_parallel']
        if self.current_system.name == "build-node":
            self.time_limit = "40m"
        self.executable_opts = ['+idlepoll', '+ppn 5', 'stmv.namd']
        self.num_cpus_per_task = 6
        self.reference = {
                'build-node:parallel': {'days_ns': (0.57, None, 0.05, 'days/ns')},
        }

