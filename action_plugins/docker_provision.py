from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys

from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):

        self._supports_check_mode = False
        self._supports_async = False

        result = super(ActionModule, self).run(tmp, task_vars)
        task_vars = task_vars or dict()

        docker_container_module_args = self._task.args.copy()
        host_vars = docker_container_module_args.get('private', {}).copy()
        if 'private' in docker_container_module_args:
            del docker_container_module_args['private']

        inventory_hostname = task_vars.get('inventory_hostname')
        docker_container_defaults = {
            'name': inventory_hostname,
            'image': 'chrismeyers/centos6',
            'privileged': True,
            'state': "started",
            'restart': True,
            'tls': True,
            'stop_timeout': 1,
            'tty': True,
            'expose': ['1-65535'],
        }
        host_vars_defaults = {
            'ansible_connection': 'docker',
        }

        for k, v in docker_container_defaults.iteritems():
            docker_container_module_args.setdefault(k, v)

        result.update(self._execute_module('docker_container', 
                                           module_args=docker_container_module_args, 
                                           task_vars=task_vars))
        docker_container_facts = result.get('ansible_facts', {}).get('docker_container', dict())

        [host_vars.setdefault(k, v) for k, v in host_vars_defaults.iteritems()]

        result['add_host'] = dict(host_name=docker_container_module_args['name'], 
                                  groups=task_vars.get('group_names', []), 
                                  host_vars=host_vars)

        result['changed'] = True
        return result
