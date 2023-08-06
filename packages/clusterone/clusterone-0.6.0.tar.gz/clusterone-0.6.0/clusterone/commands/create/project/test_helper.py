import pytest
from clusterone.client_exceptions import RemoteAquisitionFailure

from clusterone.config import Config
from clusterone import ClusteroneClient
from clusterone.clusterone_cli import Context

from . import helper
from .helper import main

def test_client_call(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()
    ClusteroneClient.create_project = mocker.Mock()

    helper.time.sleep = mocker.Mock()

    config = Config()
    config.load()
    client = ClusteroneClient(token=config.get('token'), username=config.get('username'))
    context = Context(client, config, None)

    ClusteroneClient.get_project.return_value = {'git_auth_link': "some text"}

    main(context, "ProjectName", "Description...")

    ClusteroneClient.create_project.assert_called_with("ProjectName", "Description...")

def test_remote_aquisition_failure(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()

    helper.time.sleep = mocker.Mock()
    config = Config()
    config.load()
    client = ClusteroneClient(token=config.get('token'), username=config.get('username'))
    context = Context(client, config, None)

    ClusteroneClient.get_project.return_value = {'git_auth_link': None}

    with pytest.raises(RemoteAquisitionFailure):
        main(context, "a1234567890", "sample text sample text")

def test_returns_remote_link(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()
    ClusteroneClient.create_project = mocker.Mock()

    helper.time.sleep = mocker.Mock()

    config = Config()
    config.load()
    client = ClusteroneClient(token=config.get('token'), username=config.get('username'))
    context = Context(client, config, None)

    ClusteroneClient.get_project.return_value = {'git_auth_link': "exceptional.remote.link.git"}

    assert main(context, "ProjectName", "Description...") == "exceptional.remote.link.git"

