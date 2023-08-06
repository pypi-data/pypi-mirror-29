from collections import OrderedDict
import pytest
from click.exceptions import BadParameter

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import Context
from clusterone.client_exceptions import JobNameConflict, NonExistantJob
from clusterone.config import Config

from .path_to import path_to_job_id
from .path_to import path_to_project
from .path_to import path_to_dataset

def test_user_not_specified(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock(return_value={"id": ""})
    ClusteroneClient.get_jobs = mocker.Mock(return_value=[OrderedDict([('job_id', '6789-6789-6789')])])
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)

    path_to_job_id("my-tport-project/master", context)

    ClusteroneClient.get_project.assert_called_with("my-tport-project", "someuser")

def test_client_name_conflict(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock(return_value={"id": ""})
    ClusteroneClient.get_jobs = mocker.Mock(return_value=[OrderedDict([('job_id', '6789-6789-6789')]), OrderedDict([('job_id', '4567-4567-4567')])])
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)

    with pytest.raises(JobNameConflict) as exception:
        path_to_job_id("allgreed/my-tport-project/job", context)

        # Warning, this depends on the JobNameConflict implementation, see id field
        assert exception.ids == ['6789-6789-6789', '4567-4567-4567']

def test_job_not_exist(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.start_job = mocker.Mock()
    ClusteroneClient.get_project = mocker.Mock(return_value={"id": ""})
    ClusteroneClient.get_jobs = mocker.Mock(return_value=[])
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)

    with pytest.raises(NonExistantJob):
        path_to_job_id("allgreed/my-tport-project/very-not-existant-job-path", context)

def test_resolve_job_id(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.start_job = mocker.Mock()
    ClusteroneClient.get_project = mocker.Mock(return_value={"id": "12345"})
    ClusteroneClient.get_jobs = mocker.Mock(return_value=[OrderedDict([('job_id', '6789-6789-6789')])])
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)

    path_to_job_id("allgreed/my-tport-project/master", context)

    ClusteroneClient.get_jobs.assert_called_with({
        "repository": "12345",
        "display_name": "master"
        })

    ClusteroneClient.get_project.assert_called_with("my-tport-project", "allgreed")

def test_invalid_job_path(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)

    with pytest.raises(BadParameter):
        path_to_job_id("elorapmordeczko//////xd", context)

"""
Test path_to_project
"""

def test_basic_project_path(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)
    ClusteroneClient.get_project = mocker.Mock(return_value={"id": "12345"})

    assert path_to_project("username/project_name", context) == {"id": "12345"}
    ClusteroneClient.get_project.assert_called_with("project_name", "username")

def test_invalid_path(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)
    ClusteroneClient.get_project = mocker.Mock(return_value={"id": "12345"})

    with pytest.raises(BadParameter):
        path_to_project("elorapmordeczko//////xd", context)

def test_default_username(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)
    ClusteroneClient.get_project = mocker.Mock(return_value={"id": "12345"})

    assert path_to_project("project_name", context) == {"id": "12345"}
    ClusteroneClient.get_project.assert_called_with("project_name", "someuser")

"""
Test path_to_dataset
"""

def test_basic_dataset_path_d(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)
    ClusteroneClient.get_dataset = mocker.Mock(return_value={"id": "12345"})

    assert path_to_dataset("username/dataset_name", context) == {"id": "12345"}
    ClusteroneClient.get_dataset.assert_called_with("dataset_name", "username")

def test_invalid_path_d(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)
    ClusteroneClient.get_dataset = mocker.Mock(return_value={"id": "12345"})

    with pytest.raises(BadParameter):
        path_to_dataset("elorapmordeczko//////xd", context)

def test_default_username_d(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Config, 'get', autospec=True, return_value="someuser")
    client = ClusteroneClient()
    context = Context(client, Config(), None)
    ClusteroneClient.get_dataset = mocker.Mock(return_value={"id": "12345"})

    assert path_to_dataset("dataset_name", context) == {"id": "12345"}
    ClusteroneClient.get_dataset.assert_called_with("dataset_name", "someuser")
