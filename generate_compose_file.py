import os
import sys
import yaml
import base64
import random
import string
import argparse

from collections import OrderedDict


generate_secret = lambda length: base64.b64encode(
                        ''.join(
                            random.sample(string.lowercase+string.digits,length)
                        ))

def populate_config(master_host='master'):
    conf_in = OrderedDict()
    conf_in['version'] = '3.7'
    conf_in['services'] = {
        'master': {
            'hostname': master_host,
            'privileged': 'true',
            'cap_add': ['SYS_ADMIN'],
            'environment': {
                'container': 'docker'
            },
            'command': '/usr/sbin/init',
            'build': {
                'args': {
                    'MINION_IDS': ''
                },
                'context': 'saltstack/master'
            },
            'image': 'salt-master',
            'ports': ['4505:4505', '4506:4506'],
            'volumes': [
                '/sys/fs/cgroup:/sys/fs/cgroup:ro',
                './saltstack/salt:/srv/salt',
                './saltstack/pillar:/srv/pillar'
            ],
            'hostname': master_host,
            'networks': {
                'salt': {
                    'ipv4_address': '172.28.1.1'
                }
            },
            'container_name': master_host
            #'volumes': ['salt-volume:/etc/salt']
        } 
    }
    return conf_in


def minion_config(master_host='master', minions=1, minion_id=None):
    config = populate_config(master_host=master_host)
    i = 1
    while i <= minions:
        config['services']['master']['build']['args']['MINION_IDS'] += "{minion}_{num} ".format(minion=minion_id, num=i)
        config['services']['minion'+str(i)] = {
            'build': {
                'context': 'saltstack/minion'
            },
            'environment': ['MINION_ID='+"{minion}_{num}".format(minion=minion_id, num=i)],
            'privileged': 'true',
            'cap_add':['SYS_ADMIN'],
            'command': '/usr/sbin/init',
            'image': 'salt-minion',
            'volumes': ['/sys/fs/cgroup:/sys/fs/cgroup:ro'],
            'networks': ['salt'],
            'depends_on': ['master'],
            'links': ['master'],
            'hostname': "{minion}_{num}".format(minion=minion_id, num=i),
            'container_name': "{minion}_{num}".format(minion=minion_id, num=i)
        }
        i += 1
    config['networks'] = {
        'salt': {
            'ipam': {
                'driver': 'default',
                'config': [{'subnet': '172.28.0.0/16'}]
            }
        }
    }

    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manages docker-compose.yml files')
    parser.add_argument('--scale', '-s',
                        help='How many services you want to create',
                        default=1, type=int)
    parser.add_argument('--master', '-m',
                        help='Specify the hostname of the master',
                        default='salt-master')
    parser.add_argument('--hostname',
                        help='Specify the hostname of the service',
                        default=None)
    args = parser.parse_args()

    scale = args.scale
    master = args.master
    hostname = args.hostname

    def setup_yaml():
        """ https://stackoverflow.com/a/8661021 """
        represent_dict_order = lambda self, data:  self.represent_mapping('tag:yaml.org,2002:map', data.items())
        yaml.add_representer(OrderedDict, represent_dict_order)    
    setup_yaml()

    docker_compose = yaml.dump(minion_config(master, minions=scale, minion_id=hostname))
    with open('docker-compose.yml', 'w') as fh:
        fh.write(docker_compose)
    