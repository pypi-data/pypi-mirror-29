from collections import OrderedDict

from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import cli
from clusterone.commands.rm.job import cmd
from clusterone.client_exceptions import RunningJobRemoveAttempt


def test_deletion(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.delete_job = mocker.Mock()
    cmd.serialize_job = mocker.Mock(return_value=OrderedDict([
        ('job_id', 'some-dummy-id'),
        ('status', 'created'),
    ]))

    mocker.spy(cmd, 'confirm')

    CliRunner().invoke(cli, ['rm', 'job', 'project/job_name'], 'y')

    cmd.serialize_job.assert_called_with('project/job_name', context=mocker.ANY)
    cmd.confirm.assert_called_with(mocker.ANY, abort=True)
    ClusteroneClient.delete_job.assert_called_with('some-dummy-id')

def test_running_job(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.delete_job = mocker.Mock()
    cmd.serialize_job = mocker.Mock(return_value=OrderedDict([
        ('job_id', 'some-dummy-id'),
        ('status', 'running'),
    ]))

    result = CliRunner().invoke(cli, ['rm', 'job', 'project/job_name'], 'y')

    assert isinstance(result.exception, RunningJobRemoveAttempt)
