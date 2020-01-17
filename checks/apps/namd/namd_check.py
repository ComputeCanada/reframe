import os

import reframe as rfm
import reframe.utility.sanity as sn


class NamdBaseCheck(rfm.RunOnlyRegressionTest):
    def __init__(self, arch, flavor):
        super().__init__()
        self.descr = 'NAMD check (%s)' % (arch)
        if flavor == 'multicore':
            self.valid_prog_environs = ['intel-2016.4', 'intel-2018.3']

        self.modules = ['namd-%s' % flavor]

        # Reset sources dir relative to the SCS apps prefix
        self.sourcesdir = os.path.join(self.current_system.resourcesdir, 'NAMD')
        self.executable = 'namd2'
        self.use_multithreading = True
        self.num_tasks_per_core = 2

        self.num_tasks = 6
        self.num_tasks_per_node = 1

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


@rfm.required_version('>=2.16')
@rfm.parameterized_test(*([f]
                          for f in ['multicore', 'verbs', 'verbs-smp']))
class NamdGPUCheck(NamdBaseCheck):
    def __init__(self, flavor):
        super().__init__('gpu', flavor)
        self.valid_systems = ['daint:gpu']
        self.executable_opts = ['+idlepoll', '+ppn 23', 'stmv.namd']
        self.num_cpus_per_task = 24
        self.num_gpus_per_node = 1
        self.reference = {
                'daint:gpu': {'days_ns': (0.11, None, 0.05, 'days/ns')}
        }


@rfm.required_version('>=2.16')
@rfm.parameterized_test(*([f]
                          for f in ['multicore', 'verbs', 'mpi']))
class NamdCPUCheck(NamdBaseCheck):
    def __init__(self, flavor):
        super().__init__('cpu', flavor)
        self.valid_systems = ['build-node:serial','build-node:parallel','computecanada:cpu_parallel']
        if self.current_system.name == "build-node":
            self.time_limit = (0, 40, 0)
        self.executable_opts = ['+idlepoll', '+ppn 5', 'stmv.namd']
        self.num_cpus_per_task = 6
        self.reference = {
                'build-node:parallel': {'days_ns': (0.57, None, 0.05, 'days/ns')},
        }

