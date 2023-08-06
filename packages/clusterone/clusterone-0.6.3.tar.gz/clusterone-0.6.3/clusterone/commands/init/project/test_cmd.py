# -*- coding: utf-8 -*-

from os import getcwd
from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import cli
from clusterone import commands

def test_create_project_all_args(mocker):

    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    commands.create.project.command = mocker.Mock()
    commands.ln.project.helper.main = mocker.Mock()

    CliRunner().invoke(
        cli,
        ['init', 'project', 'more-project-names', '--description', 'This is a sample project description'])

    commands.create.project.command.assert_called_with(name='more-project-names', description='This is a sample project description')


def test__create_project_name_only(mocker):

    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    commands.create.project.command = mocker.Mock()
    commands.ln.project.helper.main = mocker.Mock()

    CliRunner().invoke(cli, ['init', 'project', 'more-project-names'])

    commands.create.project.command.assert_called_with(name='more-project-names', description='')

def test_ln_project_all_params(mocker):

    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    commands.create.project.command = mocker.Mock(return_value="iam.tired.of.inventing.this.stuff.git")
    commands.ln.project.helper.main = mocker.Mock()

    CliRunner().invoke(cli, ['init', 'project', 'more-project-names', '-r', '/sample/repo/path/to/git/repository'])

    commands.ln.project.helper.main.assert_called_with(mocker.ANY, '/sample/repo/path/to/git/repository', "iam.tired.of.inventing.this.stuff.git")

def test_ln_default_repo_path(mocker):

    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    commands.create.project.command = mocker.Mock(return_value="iam.tired.of.inventing.this.stuff.git")
    commands.ln.project.helper.main = mocker.Mock()

    CliRunner().invoke(cli, ['init', 'project', 'more-project-names'])

    commands.ln.project.helper.main.assert_called_with(mocker.ANY, getcwd(), "iam.tired.of.inventing.this.stuff.git")

