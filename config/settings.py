#
# ReFrame generic settings
#
import os

class ReframeSettings:
    job_poll_intervals = [1, 2, 3]
    job_submit_timeout = 60
    checks_path = ['checks/']
    checks_path_recurse = True

    serial_2016_environs = ['gcc-5.4.0', 'intel-2016.4']
    serial_2018_environs = ['gcc-7.3.0', 'intel-2018.3' ]
    parallel_2016_environs = [ 'gompi-2016.4.211', 'iompi-2016.4.211' ]
    parallel_2018_environs = [ 'gompi-2018.3.312', 'iompi-2018.3.312' ]
    cuda_2016_environs = [ 'iccifortcuda-2016.4.100' ]
    cuda_2018_environs = [ 'iccifortcuda-2018.3.100', 'iccifortcuda-2018.3.101' ]

    arch = os.getenv("RSNT_ARCH")
    if arch == "avx512":
        serial_environs = serial_2018_environs
        parallel_environs = parallel_2018_environs
        cuda_environs = cuda_2018_environs
    elif arch == "avx2":
        serial_environs = serial_2016_environs + serial_2018_environs
        parallel_environs = parallel_2016_environs + parallel_2018_environs
        cuda_environs = cuda_2016_environs + cuda_2018_environs
    else:
        serial_environs = serial_2016_environs
        parallel_environs = parallel_2016_environs

    login_configuration =   {
                                'scheduler': 'local',
                                'environs': serial_environs,
                                'descr': 'Login nodes'
                            }
    cpu_configuration =     {
                                'scheduler': 'nativeslurm',
                                'environs': serial_environs + parallel_environs,
                            }
    cpu_serial_configuration =     {
                                'scheduler': 'nativeslurm',
                                'environs': serial_environs,
                            }
    cpu_parallel_configuration =     {
                                'scheduler': 'nativeslurm',
                                'environs': parallel_environs,
                            }
    site_configuration = {}
    site_configuration['systems'] = {
            'build-node': {
                'descr': 'Build node',
                'hostnames': ['build-node'],
                'modules_system': 'lmod',
                'resourcesdir': '/cvmfs/soft.computecanada.ca/custom/reframe/ressources',
                'partitions': {
                    'serial': {
                        'scheduler': 'local',
                        'environs': serial_environs,
                        'descr': 'Login nodes'
                    },
                    'parallel': {
                        'scheduler': 'local+mpiexec',
                        'environs': parallel_environs,
                        'descr': 'Login nodes parallel'
                    }
                }
            },
            'beluga': {
                'descr': 'Beluga Compute Canada cluster',
                'hostnames': ['beluga', 'blg'],
                'partitions': {
                    'gpu': {
                        'scheduler': 'nativeslurm',
                        'environs': cuda_environs,
                        'resources': { }
                    }
                },
            },
            'cedar': {
                'descr': 'Cedar Compute Canada cluster',
                'hostnames': ['cedar', 'cdr'],
                'partitions': {
                    'gpu': {
                        'scheduler': 'nativeslurm',
                        'environs': cuda_environs,
                        'resources': {
                                'lgpu': ['--gres=gpu:lgpu:{num_lgpu_per_node}'],
                        }
                    }
                },
            },
            'graham': {
                'descr': 'Graham Compute Canada cluster',
                'hostnames': ['gra-login', 'gra'],
                'partitions': {
                    'gpu': {
                        'scheduler': 'nativeslurm',
                        'environs': cuda_environs,
                        'resources': {
                                'v100': ['--gres=gpu:v100:{num_v100_per_node}'],
                                'p100': ['--gres=gpu:p100:{num_p100_per_node}'],
                                't4': ['--gres=gpu:t4:{num_t4_per_node}'],
                        }
                    }
                },
            },
            'helios': {
                'descr': 'Helios Compute Canada clusters',
                'hostnames': ['helios', 'hel'],
                'partitions': {
                    'gpu': {
                        'scheduler': 'nativeslurm',
                        'environs': cuda_environs,
                        'resources': {
                                'k20': ['--gres=gpu:k20:{num_k20_per_node}'],
                                'k80': ['--gres=gpu:k80:{num_k80_per_node}'],
                        }
                    }
                }
            },
        }

    # common configuration
    for s in ['graham', 'cedar', 'helios', 'beluga']:
        site_configuration['systems'][s]['modules_system'] = 'lmod'
        site_configuration['systems'][s]['resourcesdir'] = '/cvmfs/soft.computecanada.ca/custom/reframe/ressources'
        site_configuration['systems'][s]['partitions']['login'] = login_configuration
        site_configuration['systems'][s]['partitions']['cpu'] = cpu_configuration
        site_configuration['systems'][s]['partitions']['cpu_serial'] = cpu_serial_configuration
        site_configuration['systems'][s]['partitions']['cpu_parallel'] = cpu_parallel_configuration
        site_configuration['systems'][s]['partitions']['gpu']['resources']['gpu'] = ['--gres=gpu:{num_gpus_per_node}']
        site_configuration['systems'][s]['partitions']['gpu']['resources']['mem-per-cpu'] = ['--mem-per-cpu={mem_per_cpu}']


    site_configuration['environments'] = {
            '*': {
                'gcc-5.4.0': {
                    'type': 'ProgEnvironment',
                    'modules': ['gcc/5.4.0'],
                    'cc':  'gcc',
                    'cxx': 'g++',
                    'ftn': 'gfortran',
                },
                'intel-2016.4': {
                    'type': 'ProgEnvironment',
                    'modules': ['intel/2016.4'],
                    'cc':  'gcc',
                    'cxx': 'g++',
                    'ftn': 'gfortran',
                },
                'gcc-7.3.0': {
                    'type': 'ProgEnvironment',
                    'modules': ['gcc/7.3.0'],
                    'cc':  'gcc',
                    'cxx': 'g++',
                    'ftn': 'gfortran',
                },
                'intel-2018.3': {
                    'type': 'ProgEnvironment',
                    'modules': ['intel/2018.3'],
                    'cc':  'gcc',
                    'cxx': 'g++',
                    'ftn': 'gfortran',
                },
                'gompi-2016.4.211': {
                    'type': 'ProgEnvironment',
                    'modules': ['gcc/5.4.0', 'openmpi/2.1.1'],
                    'cc':  'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpifort',
                },
                'iompi-2016.4.211': {
                    'type': 'ProgEnvironment',
                    'modules': ['intel/2016.4', 'openmpi/2.1.1'],
                    'cc':  'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpifort',
                },
                'gompi-2018.3.312': {
                    'type': 'ProgEnvironment',
                    'modules': ['gcc/7.3.0', 'openmpi/3.1.2'],
                    'cc':  'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpifort',
                },
                'iompi-2018.3.312': {
                    'type': 'ProgEnvironment',
                    'modules': ['intel/2018.3', 'openmpi/3.1.2'],
                    'cc':  'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpifort',
                },
                'iccifortcuda-2016.4.100': {
                    'type': 'ProgEnvironment',
                    'modules': ['intel/2016.4', 'cuda/10.0'],
                    'cc':  'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpifort',
                },
                'iccifortcuda-2018.3.100': {
                    'type': 'ProgEnvironment',
                    'modules': ['intel/2018.3', 'cuda/10.0'],
                    'cc':  'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpifort',
                },
                'iccifortcuda-2018.3.101': {
                    'type': 'ProgEnvironment',
                    'modules': ['intel/2018.3', 'cuda/10.1'],
                    'cc':  'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpifort',
                },
            }
        }

    logging_config = {
        'level': 'DEBUG',
        'handlers': [
            {
                'type': 'file',
                'name': 'reframe.log',
                'level': 'DEBUG',
                'format': '[%(asctime)s] %(levelname)s: '
                          '%(check_info)s: %(message)s',
                'append': False,
            },

            # Output handling
            {
                'type': 'stream',
                'name': 'stdout',
                'level': 'INFO',
                'format': '%(message)s'
            },
            {
                'type': 'file',
                'name': 'reframe.out',
                'level': 'INFO',
                'format': '%(message)s',
                'append': False,
            }
        ]
    }

    perf_logging_config = {
        'level': 'DEBUG',
        'handlers': [
            {
                'type': 'filelog',
                'prefix': '%(check_system)s/%(check_partition)s',
                'level': 'INFO',
                'format': (
                    '%(asctime)s|reframe %(version)s|'
                    '%(check_info)s|jobid=%(check_jobid)s|'
                    '%(check_perf_var)s=%(check_perf_value)s|'
                    'ref=%(check_perf_ref)s '
                    '(l=%(check_perf_lower_thres)s, '
                    'u=%(check_perf_upper_thres)s)|'
                    '%(check_perf_unit)s'
                ),
                'append': True
            },
            {
                'type': 'syslog',
                'level': 'INFO',
                'format': (
                    '%(asctime)s|reframe %(version)s|'
                    '%(check_info)s|jobid=%(check_jobid)s|'
                    '%(check_perf_var)s=%(check_perf_value)s|'
                    'ref=%(check_perf_ref)s '
                    '(l=%(check_perf_lower_thres)s, '
                    'u=%(check_perf_upper_thres)s)|'
                    '%(check_perf_unit)s'
                ),
                'address': '/dev/log'
            },
        ]
    }

    


settings = ReframeSettings()
