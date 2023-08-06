from collections import OrderedDict

from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import cli
from clusterone.commands.rm.project import cmd
from clusterone.client_exceptions import BussyProjectRemoveAttempt

def test_deletion(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.delete_project = mocker.Mock()
    ClusteroneClient.get_jobs = mocker.Mock(return_value=[])
    cmd.path_to_project = mocker.Mock(return_value=OrderedDict([
        ('id', 'some-dummy-id'),
        ('username', 'someDummyUsername'),
        ('name', 'some_dummy_project_name'),
    ]))
    mocker.spy(cmd, 'confirm')

    CliRunner().invoke(cli, ['rm', 'project', 'someDummyUsername/some_dummy_project_name'], 'y')

    cmd.path_to_project.assert_called_with(
        'someDummyUsername/some_dummy_project_name',
        context=mocker.ANY)

    cmd.confirm.assert_called_with(mocker.ANY, abort=True)

    ClusteroneClient.delete_project.assert_called_with(
        'some_dummy_project_name',
        'someDummyUsername')

def test_running_jobs(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.delete_project = mocker.Mock()
    ClusteroneClient.get_jobs = mocker.Mock(return_value=[OrderedDict([('status', 'started')])])
    cmd.path_to_project = mocker.Mock(return_value=OrderedDict([
        ('id', 'some-dummy-id'),
        ('username', 'someDummyUsername'),
        ('name', 'some_dummy_project_name'),
    ]))
    mocker.spy(cmd, 'confirm')

    result = CliRunner().invoke(cli, ['rm', 'project', 'project'])

    assert isinstance(result.exception, BussyProjectRemoveAttempt)
