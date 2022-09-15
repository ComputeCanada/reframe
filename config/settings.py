#
# This file was first automatically generated by ReFrame based on '/home/oldeman/reframe/settings.py'.  # noqa: E501
# and then edited!
#
import os

serial_2016_environs = ['gcc-5.4.0', 'intel-2016.4']
serial_2018_environs = ['gcc-7.3.0', 'intel-2018.3']
serial_2020_environs = ['gcc-9.3.0', 'intel-2020.1']
parallel_2016_environs = [ 'gompi-2016.4.211', 'iompi-2016.4.211' ]
parallel_2018_environs = [ 'gompi-2018.3.312', 'iompi-2018.3.312' ]
parallel_2020_environs = [ 'gompi-2020a', 'iompi-2020a' ]
cuda_2016_environs = [ 'iccifortcuda-2016.4.100' ]
cuda_2018_environs = [ 'iccifortcuda-2018.3.100', 'iccifortcuda-2018.3.101' ]
cuda_2020_environs = [ 'iccifortcuda-2020.1.114' ]

arch = os.getenv("RSNT_ARCH")
if arch == "avx512":
    serial_environs = serial_2018_environs + serial_2020_environs
    parallel_environs = parallel_2018_environs + parallel_2020_environs
    cuda_environs = cuda_2018_environs + cuda_2020_environs
elif arch == "avx2":
    serial_environs = serial_2016_environs + serial_2018_environs + serial_2020_environs
    parallel_environs = parallel_2016_environs + parallel_2018_environs + parallel_2020_environs
    cuda_environs = cuda_2016_environs + cuda_2018_environs + cuda_2020_environs
else:
    serial_environs = serial_2016_environs
    parallel_environs = parallel_2016_environs
    cuda_environs = cuda_2016_environs

login_configuration = {
    'name': 'login',
    'scheduler': 'local',
    'environs': serial_environs,
    'descr': 'Login nodes',
    'launcher': 'local',
}
cpu_configuration = {
    'name': 'cpu',
    'scheduler': 'slurm',
    'environs': serial_environs + parallel_environs,
    'launcher': 'srun',
}
cpu_serial_configuration = {
    'name': 'cpu_serial',
    'scheduler': 'slurm',
    'environs': serial_environs,
    'launcher': 'srun',
}
cpu_parallel_configuration = {
    'name': 'cpu_parallel',
    'scheduler': 'slurm',
    'environs': parallel_environs,
    'launcher': 'srun',
}

site_configuration = {
    'systems': [
        {
            'name': 'build-node',
            'descr': 'Build node',
            'hostnames': [
                'build-node', '206-12-89-214.cloud.computecanada.ca',
            ],
            'modules_system': 'lmod',
            'resourcesdir': '/cvmfs/soft.computecanada.ca/custom/reframe/ressources',  # noqa: E501
            'partitions': [
                {
                    'name': 'serial',
                    'scheduler': 'local',
                    'environs': serial_environs,
                    'descr': 'Login nodes',
                    'launcher': 'local'
                },
                {
                    'name': 'parallel',
                    'scheduler': 'local',
                    'environs': parallel_environs,
                    'descr': 'Login nodes parallel',
                    'launcher': 'mpiexec'
                }
            ]
        },
        {
            'name': 'beluga',
            'descr': 'Beluga Compute Canada cluster',
            'hostnames': [
                'beluga',
                'blg'
                'bc'
                'bl'
                'bg'
            ],
            'partitions': [
                {
                    'name': 'gpu',
                    'scheduler': 'slurm',
                    'environs': cuda_environs,
                    'resources': [],
                    'launcher': 'srun'
                },
            ],
        },
        {
            'name': 'cedar',
            'descr': 'Cedar Compute Canada cluster',
            'hostnames': [
                'cedar',
                'cdr'
            ],
            'partitions': [
                {
                    'name': 'gpu',
                    'scheduler': 'slurm',
                    'environs': cuda_environs,
                    'resources': [
                        {
                            'name': 'lgpu',
                            'options': ['--gres=gpu:lgpu:{num_lgpu_per_node}']
                        },
                    ],
                    'launcher': 'srun'
                },
            ],
        },
        {
            'name': 'graham',
            'descr': 'Graham Compute Canada cluster',
            'hostnames': [
                'gra-login',
                'gra'
            ],
            'partitions': [
                {
                    'name': 'gpu',
                    'scheduler': 'slurm',
                    'environs': cuda_environs,
                    'resources': [
                        {
                            'name': 'v100',
                            'options': ['--gres=gpu:v100:{num_v100_per_node}']
                        },
                        {
                            'name': 'p100',
                            'options': ['--gres=gpu:p100:{num_p100_per_node}']
                        },
                        {
                            'name': 't4',
                            'options': ['--gres=gpu:t4:{num_t4_per_node}']
                        },
                    ],
                    'launcher': 'srun'
                },
            ],
        },
        {
            'name': 'helios',
            'descr': 'Helios Compute Canada clusters',
            'hostnames': [
                'helios',
                'hel'
            ],
            'partitions': [
                {
                    'name': 'gpu',
                    'scheduler': 'slurm',
                    'environs': cuda_environs,
                    'resources': [
                        {
                            'name': 'k20',
                            'options': ['--gres=gpu:k20:{num_k20_per_node}']
                        },
                        {
                            'name': 'k80',
                            'options': ['--gres=gpu:k80:{num_k80_per_node}']
                        },
                    ],
                    'launcher': 'srun'
                },
            ],
        },
        {
            'name': 'narval',
            'descr': 'Narval Compute Canada cluster',
            'hostnames': [
                'narval',
                'nc'
                'nl'
                'ng'
            ],
            'partitions': [
                {
                    'name': 'gpu',
                    'scheduler': 'slurm',
                    'environs': cuda_environs,
                    'resources': [],
                    'launcher': 'srun'
                },
            ],
        },
    ],
    'environments': [
        {
            'name': 'gcc-5.4.0',
            'modules': [
                'nixpkgs/16.09',
                'gcc/5.4.0'
            ],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'intel-2016.4',
            'modules': [
                'nixpkgs/16.09',
                'intel/2016.4'
            ],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'gcc-7.3.0',
            'modules': [
                'nixpkgs/16.09',
                'gcc/7.3.0'
            ],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'intel-2018.3',
            'modules': [
                'nixpkgs/16.09',
                'intel/2018.3'
            ],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'gcc-9.3.0',
            'modules': [
                'StdEnv/2020',
                'gcc/9.3.0'
            ],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'intel-2020.1',
            'modules': [
                'StdEnv/2020',
                'intel/2020.1'
            ],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'gompi-2016.4.211',
            'modules': [
                'nixpkgs/16.09',
                'gcc/5.4.0',
                'openmpi/2.1.1'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'iompi-2016.4.211',
            'modules': [
                'nixpkgs/16.09',
                'intel/2016.4',
                'openmpi/2.1.1'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'gompi-2018.3.312',
            'modules': [
                'nixpkgs/16.09',
                'gcc/7.3.0',
                'openmpi/3.1.2'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'iompi-2018.3.312',
            'modules': [
                'nixpkgs/16.09',
                'intel/2018.3',
                'openmpi/3.1.2'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'gompi-2020a',
            'modules': [
                'StdEnv/2020',
                'gcc/9.3.0',
                'openmpi/4.0.3'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'iompi-2020a',
            'modules': [
                'StdEnv/2020',
                'intel/2020.1',
                'openmpi/4.0.3'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'iccifortcuda-2016.4.100',
            'modules': [
                'nixpkgs/16.09',
                'intel/2016.4',
                'cuda/10.0'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'iccifortcuda-2018.3.100',
            'modules': [
                'nixpkgs/16.09',
                'intel/2018.3',
                'cuda/10.0'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'iccifortcuda-2018.3.101',
            'modules': [
                'nixpkgs/16.09',
                'intel/2018.3',
                'cuda/10.1'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'iccifortcuda-2020.1.114',
            'modules': [
                'StdEnv/2020',
                'intel/2020.1',
                'cuda/11.4'
            ],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        }
    ],
    'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'file',
                    'name': 'reframe.log',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',  # noqa: E501
                    'append': False
                },
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'name': 'reframe.out',
                    'level': 'info',
                    'format': '%(message)s',
                    'append': False
                }
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': '%(asctime)s|reframe %(version)s|%(check_info)s|jobid=%(check_jobid)s|%(check_perf_var)s=%(check_perf_value)s|ref=%(check_perf_ref)s (l=%(check_perf_lower_thres)s, u=%(check_perf_upper_thres)s)|%(check_perf_unit)s',  # noqa: E501
                    'append': True
                },
                {
                    'type': 'syslog',
                    'level': 'info',
                    'format': '%(asctime)s|reframe %(version)s|%(check_info)s|jobid=%(check_jobid)s|%(check_perf_var)s=%(check_perf_value)s|ref=%(check_perf_ref)s (l=%(check_perf_lower_thres)s, u=%(check_perf_upper_thres)s)|%(check_perf_unit)s',  # noqa: E501
                    'address': '/dev/log'
                }
            ]
        }
    ],
    'general': [
        {
            'check_search_path': [
                'checks/'
            ],
            'check_search_recursive': True
        }
    ]
}

# common configuration
for s in site_configuration['systems']:
    if s['name'] in ['graham', 'cedar', 'helios', 'beluga', 'narval']:
        s['modules_system'] = 'lmod'
        s['resourcesdir'] = '/cvmfs/soft.computecanada.ca/custom/reframe/ressources'
        s['partitions'].extend([login_configuration, cpu_configuration,
                                cpu_serial_configuration, cpu_parallel_configuration])
        for p in s['partitions']:
            if p['name'] == 'gpu':
                p['resources'].extend([
                    {
                        'name': 'gpu',
                        'options': ['--gres=gpu:{num_gpus_per_node}']
                    },
                    {
                        'name': 'mem-per-cpu',
                        'options': ['--mem-per-cpu={mem_per_cpu}']
                    }
                ])
