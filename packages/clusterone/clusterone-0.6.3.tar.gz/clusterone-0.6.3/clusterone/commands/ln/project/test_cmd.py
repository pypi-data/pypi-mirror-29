import os
from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.config import Config
from clusterone.commands.ln.project import cmd
from clusterone.clusterone_cli import cli


def test_remote_from_stdin(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.main = mocker.Mock()

    CliRunner().invoke(cli, ['ln', 'project'], input="just.another.git.repo.link\n")

    cmd.main.assert_called_with(mocker.ANY, mocker.ANY, "just.another.git.repo.link")

def test_remote_from_project_name(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock(return_value={'git_auth_link': "my git auth link"})
    cmd.main = mocker.Mock()

    CliRunner().invoke(cli, ['ln', 'project', '--project-path', 'someuser/someProjectName'])

    cmd.main.assert_called_with(mocker.ANY, mocker.ANY, "my git auth link")

def test_no_stdin_no_name_err(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.main = mocker.Mock()

    result = CliRunner().invoke(cli, ['ln', 'project'])

    # This is a fun way of saying internal Clicks MissingParameter Exception
    assert str(result.exception) == '2'

def test_default_repo_path(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()
    cmd.main = mocker.Mock()

    CliRunner().invoke(cli, ['ln', 'project', '--project-path', 'someuser/someProjectName'])

    cmd.main.assert_called_with(mocker.ANY, os.getcwd(), mocker.ANY)

def test_user_provided_repo_path(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()
    cmd.main = mocker.Mock()

    CliRunner().invoke(
        cli,
        ['ln', 'project', '--project-path', 'someuser/someProjectName', '-r', '/some/path/to/git/repository'], input="")

    cmd.main.assert_called_with(mocker.ANY, '/some/path/to/git/repository', mocker.ANY)

def test_project_aquisition(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()
    cmd.main = mocker.Mock()

    CliRunner().invoke(
        cli,
        ['ln', 'project', '--project-path', 'someuser/someProjectName'], input="")

    ClusteroneClient.get_project.assert_called_with("someProjectName", username="someuser")

def test_default_username(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()
    cmd.main = mocker.Mock()
    mocker.patch.object(Config, 'get', autospec=True, return_value="defaultusername")

    CliRunner().invoke(
        cli,
        ['ln', 'project', '--project-path', 'someProjectName'], input="")

    ClusteroneClient.get_project.assert_called_with("someProjectName", username="defaultusername")

def test_invalid_project_path(mocker):
    cmd.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()
    cmd.main = mocker.Mock()

    result = CliRunner().invoke(
        cli,
        ['ln', 'project', '--project-path', 'elorapmordo/////////xd'], input="")

    # This is a fun way of saying internal Clicks Exception
    assert str(result.exception) == '2'
