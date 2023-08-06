from collections import OrderedDict

import pytest

from clusterone.config import Config
from clusterone.clusterone_cli import Context
from clusterone.commands.create.job import base_cmd
from clusterone.client_exceptions import FailedCommitReference, NoProjectCommits


def test_python_version_aliases(mocker):
    base_cmd.client = mocker.Mock()
    base_cmd.path_to_project = mocker.Mock(return_value={'id': "project-id-123456", "commits": [OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1')]), OrderedDict([('id', '4a82d16c79elorapc7973af38f2f5ba4eac0cd2d1')])]})
    base_cmd.time_limit_to_minutes = mocker.Mock(return_value=123456)
    config = Config()
    config.load()
    context = Context(None, config, None)

    result = base_cmd.base(context, {'framework': 'tensorflow-130', 'project_path': 'mnist-demo', 'python_version': '3', 'requirements': None, 'commit': 'latest', 'name': 'old-morning-562', 'module': 'mymodule.py', 'package_manager': 'pip', 'package_path': '', 'description': '', 'time_limit': 2880, 'datasets': '',})


    assert result['parameters']['python_version'] == '3.5'

    result = base_cmd.base(context, {'framework': 'tensorflow-130', 'project_path': 'mnist-demo', 'python_version': '2', 'requirements': None, 'commit': 'latest', 'name': 'old-morning-562', 'module': 'mymodule.py', 'package_manager': 'pip', 'package_path': '', 'description': '', 'time_limit': 2880, 'datasets': '',})


    assert result['parameters']['python_version'] == '2.7'

def test_package_manager_aliases(mocker):
    base_cmd.client = mocker.Mock()
    base_cmd.path_to_project = mocker.Mock(return_value={'id': "project-id-123456", "commits": [OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1')]), OrderedDict([('id', '4a82d16c79elorapc7973af38f2f5ba4eac0cd2d1')])]})
    base_cmd.time_limit_to_minutes = mocker.Mock(return_value=123456)
    config = Config()
    config.load()
    context = Context(None, config, None)

    result = base_cmd.base(context, {'framework': 'tensorflow-130', 'project_path': 'mnist-demo', 'python_version': '3', 'requirements': None, 'commit': 'latest', 'name': 'old-morning-562', 'module': 'mymodule.py', 'package_manager': 'anaconda', 'package_path': '', 'description': '', 'time_limit': 2880, 'datasets': '',})


    assert result['parameters']['package_manager'] == 'conda'

def test_default_requirement_conda(mocker):
    base_cmd.client = mocker.Mock()
    base_cmd.path_to_project = mocker.Mock(return_value={'id': "project-id-123456", "commits": [OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1')]), OrderedDict([('id', '4a82d16c79elorapc7973af38f2f5ba4eac0cd2d1')])]})
    base_cmd.time_limit_to_minutes = mocker.Mock(return_value=123456)
    config = Config()
    config.load()
    context = Context(None, config, None)

    result = base_cmd.base(context, {'framework': 'tensorflow-1.3.0', 'project_path': 'mnist-demo', 'python_version': '3', 'requirements': None, 'commit': 'latest', 'name': 'old-morning-562', 'module': 'mymodule.py', 'package_manager': 'anaconda', 'package_path': '', 'description': '', 'time_limit': 2880, 'datasets': '',})


    assert result['parameters']['requirements'] == 'requirements.yml'

def test_no_project_commits(mocker):
    base_cmd.client = mocker.Mock()
    base_cmd.path_to_project = mocker.Mock(return_value={'id': "project-id-123456", "commits": []})
    base_cmd.time_limit_to_minutes = mocker.Mock(return_value=123456)
    config = Config()
    config.load()
    context = Context(None, config, None)


    with pytest.raises(NoProjectCommits):
        base_cmd.base(context, { 'framework': 'tensorflow-130', 'project_path': 'mnist-demo', 'python_version': '3', 'requirements': None, 'commit': 'latest', 'name': 'old-morning-562', 'module': 'mymodule.py', 'package_manager': 'anaconda', 'package_path': '', 'description': '', 'time_limit': 2880, 'datasets': '',})

def test_non_existant_commit(mocker):
    base_cmd.client = mocker.Mock()
    base_cmd.path_to_project = mocker.Mock(return_value={'id': "project-id-123456", "commits": [OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1')]), OrderedDict([('id', '4a82d16c79elorapc7973af38f2f5ba4eac0cd2d1')])]})
    base_cmd.time_limit_to_minutes = mocker.Mock(return_value=123456)
    config = Config()
    config.load()
    context = Context(None, config, None)


    with pytest.raises(FailedCommitReference):
        base_cmd.base(context, { 'framework': 'tensorflow-130', 'project_path': 'mnist-demo', 'python_version': '3', 'requirements': None, 'commit': 'non_existant_commit_hash', 'name': 'old-morning-562', 'module': 'mymodule.py', 'package_manager': 'anaconda', 'package_path': '', 'description': '', 'time_limit': 2880, 'datasets': '',})

