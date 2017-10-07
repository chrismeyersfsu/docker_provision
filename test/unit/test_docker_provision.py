import pytest
import imp
import mock
import os

from ansible.playbook.task import Task
import ansible.plugins.action as action


@pytest.fixture
def provision_docker():
    class TaskMock(object):
        args = dict()

    class ActionBaseMock(object):
        _task = TaskMock()
        def run(self, *args, **kwargs):
            return dict()

    action.ActionBase = ActionBaseMock

    dir_path = os.path.dirname(os.path.realpath(__file__))
    module = imp.load_source('provision_docker', os.path.join(dir_path, '../../', 'action_plugins/docker_provision.py'))

    obj = module.ActionModule()
    obj._execute_module = mock.Mock(name="_execute_module")
    obj._execute_module.return_value = dict()
    return obj


def test_run_defaults(provision_docker):
    res = provision_docker.run()
    print(res)
    assert provision_docker._execute_module.call_count == 1
