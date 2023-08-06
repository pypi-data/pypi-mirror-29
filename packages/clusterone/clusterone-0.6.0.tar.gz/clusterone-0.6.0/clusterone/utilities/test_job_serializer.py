import uuid

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import Context

from . import job_serializer, serialize_job

def test_job_id(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_job = mocker.Mock(return_value="some test job")
    job_serializer.UUID = mocker.spy(uuid, "UUID")
    context = Context(ClusteroneClient(), None, None)

    result = serialize_job("1c0a06e8-fb8c-454e-a018-29c41ef66cd6", context=context)

    job_serializer.UUID.assert_called_with("1c0a06e8-fb8c-454e-a018-29c41ef66cd6")
    ClusteroneClient.get_job.assert_called_with({"job_id": "1c0a06e8-fb8c-454e-a018-29c41ef66cd6"})
    assert result == "some test job"

def test_job_path(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_job = mocker.Mock(return_value="some test job")
    job_serializer.UUID = mocker.Mock(side_effect=ValueError)
    job_serializer.path_to_job_id = mocker.Mock(return_value="some id 12345")
    context = Context(ClusteroneClient(), None, None)

    result = serialize_job("username/project/job", context=context)

    job_serializer.UUID.assert_called_with("username/project/job")
    job_serializer.path_to_job_id.assert_called_with("username/project/job", context=context)
    ClusteroneClient.get_job.assert_called_with({"job_id": "some id 12345"})
    assert result == "some test job"
