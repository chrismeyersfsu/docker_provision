import pytest
import imp
import mock
import os

from ansible.playbook.task import Task
import ansible.plugins.action as action


@pytest.fixture
def docker_provision():
    class TaskMock(object):
        args = dict()

    class ActionBaseMock(object):
        _task = TaskMock()
        def run(self, *args, **kwargs):
            return dict()

    action.ActionBase = ActionBaseMock

    dir_path = os.path.dirname(os.path.realpath(__file__))
    module = imp.load_source('docker_provision', os.path.join(dir_path, '../../', 'action_plugins/docker_provision.py'))

    obj = module.ActionModule()
    obj._execute_module = mock.Mock(name="_execute_module")
    obj._execute_module.return_value = dict()
    return obj

@pytest.fixture
def task_vars_minimal():
    return {
        'inventory_hostname': 'megatron'
    }

@pytest.fixture
def args_default():
    return {
        'name': None,
        'image': 'chrismeyers/centos6',
        'privileged': True,
        'state': "started",
        'restart': True,
        'tls': True,
        'stop_timeout': 1,
        'tty': True,
    }

def test_run_defaults(docker_provision, task_vars_minimal, args_default):
    args_default['name'] = 'megatron'

    res = docker_provision.run(task_vars=task_vars_minimal)
    docker_provision._execute_module.assert_called_with('docker_container',
                                                        module_args=args_default,
                                                        task_vars=task_vars_minimal)
    assert res == {'add_host': {'groups': [], 'host_name': 'megatron', 
                   'host_vars': {'ansible_connection': 'docker'}},
                   'changed': True}

def test_run_private_groups(docker_provision, task_vars_minimal, args_default):
    args_default['name'] = 'megatron'
    docker_provision._task.args['private'] = {
        'groups': ['g1', 'g2', 'g3'],
    }

    res = docker_provision.run(task_vars=task_vars_minimal)

    assert res['add_host']['groups'] == ['g1', 'g2', 'g3']

def test_run_private_hostvars(docker_provision, task_vars_minimal, args_default):
    args_default['name'] = 'megatron'
    docker_provision._task.args['private'] = {
        'hostvars': {
            'foo': {
                'bar': ['foo', 'bar']
            }
        }
    }

    res = docker_provision.run(task_vars=task_vars_minimal)

    assert res['add_host']['host_vars'] == {'ansible_connection': 'docker', 'foo': {'bar': ['foo', 'bar']}}

