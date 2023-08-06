import os
from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.config import Config
from clusterone.commands.ln.dataset import cmd
from clusterone.clusterone_cli import cli


def test_remote_from_dataset_name(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock(return_value={'git_auth_link': "my git auth link"})
    cmd.main = mocker.Mock()

    CliRunner().invoke(cli, ['ln', 'dataset', '--dataset-path', 'someuser/someProjectName'])

    cmd.main.assert_called_with(mocker.ANY, mocker.ANY, "my git auth link")


def test_default_repo_path(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock()
    cmd.main = mocker.Mock()

    CliRunner().invoke(cli, ['ln', 'dataset', '--dataset-path', 'someuser/someProjectName'])

    cmd.main.assert_called_with(mocker.ANY, os.getcwd(), mocker.ANY)

def test_user_provided_repo_path(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock()
    cmd.main = mocker.Mock()

    CliRunner().invoke(
        cli,
        ['ln', 'dataset', '--dataset-path', 'someuser/someProjectName', '-r', '/some/path/to/git/repository'], input="")

    cmd.main.assert_called_with(mocker.ANY, '/some/path/to/git/repository', mocker.ANY)

def test_dataset_aquisition(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock()
    cmd.main = mocker.Mock()

    CliRunner().invoke(
        cli,
        ['ln', 'dataset', '--dataset-path', 'someuser/someProjectName'])

    ClusteroneClient.get_dataset.assert_called_with("someProjectName", username="someuser")

def test_default_username(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock()
    cmd.main = mocker.Mock()
    mocker.patch.object(Config, 'get', autospec=True, return_value="defaultusername")

    CliRunner().invoke(
        cli,
        ['ln', 'dataset', '--dataset-path', 'someProjectName'])

    ClusteroneClient.get_dataset.assert_called_with("someProjectName", username="defaultusername")

def test_invalid_dataset_path(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock()
    cmd.main = mocker.Mock()

    result = CliRunner().invoke(
        cli,
        ['ln', 'dataset', '--dataset-path', 'elorapmordo/////////xd'], input="")

    # This is a fun way of saying internal Clicks Exception
    assert str(result.exception) == '2'
