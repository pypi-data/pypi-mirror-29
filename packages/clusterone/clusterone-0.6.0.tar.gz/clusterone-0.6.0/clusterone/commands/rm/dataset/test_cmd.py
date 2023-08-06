from collections import OrderedDict

from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import cli
from clusterone.commands.rm.dataset import cmd
from clusterone.client_exceptions import BussyDatasetRemoveAttempt

def test_deletion(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.delete_dataset = mocker.Mock()
    ClusteroneClient.get_jobs = mocker.Mock(return_value=[])
    cmd.path_to_dataset = mocker.Mock(return_value=OrderedDict([
    ('id', 'c385c703-e928-42c6-a47c-383381c280ae'),
    ('name', 'some_dummy_dataset_name'),
    ('owner', OrderedDict([
        ('username', 'someDummyUsername'),
        ])),
    ]))
    mocker.spy(cmd, 'confirm')

    CliRunner().invoke(cli, ['rm', 'dataset', 'someDummyUsername/some_dummy_dataset_name'], 'y')

    cmd.path_to_dataset.assert_called_with(
        'someDummyUsername/some_dummy_dataset_name',
        context=mocker.ANY)

    cmd.confirm.assert_called_with(mocker.ANY, abort=True)

    ClusteroneClient.delete_dataset.assert_called_with(
        'some_dummy_dataset_name',
        'someDummyUsername')

def test_running_jobs(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.delete_dataset = mocker.Mock()
    ClusteroneClient.get_jobs = mocker.Mock(return_value=[OrderedDict([('status', 'started')])])
    cmd.path_to_dataset = mocker.Mock(return_value=OrderedDict([
    ('id', 'c385c703-e928-42c6-a47c-383381c280ae'),
    ('name', 'some_dummy_dataset_name'),
    ('owner', OrderedDict([
        ('username', 'someDummyUsername'),
        ])),
    ]))
    mocker.spy(cmd, 'confirm')

    result = CliRunner().invoke(cli, ['rm', 'dataset', 'dataset'])

    assert isinstance(result.exception, BussyDatasetRemoveAttempt)
