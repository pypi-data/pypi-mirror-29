from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import cli

from clusterone.commands.stop.job import cmd

def test_parameter_requirement(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)

    result = CliRunner().invoke(cli, ['stop', 'job'])

    # This is a fun way of saying internal Click Exception
    assert str(result.exception) == '2'

def test_both_parameters_sepcified(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)

    result = CliRunner().invoke(cli, ['stop', '--job-id', '12354', '--job-path', 'user/project/job'])

    # This is a fun way of saying internal Click Exception
    assert str(result.exception) == '2'

def test_calls_client_id(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.stop_job = mocker.Mock()

    CliRunner().invoke(cli, ['stop','--job-id', '1234-1234-1234'])

    ClusteroneClient.stop_job.assert_called_with('1234-1234-1234')

def test_calls_client_name(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.stop_job = mocker.Mock()
    cmd.path_to_job_id = mocker.Mock(return_value="6789-6789-6789")


    CliRunner().invoke(cli, ['stop', '--job-path', 'allgreed/my-tport-project/master'])

    cmd.path_to_job_id.assert_called_with('allgreed/my-tport-project/master', context=mocker.ANY)
    ClusteroneClient.stop_job.assert_called_with('6789-6789-6789')
