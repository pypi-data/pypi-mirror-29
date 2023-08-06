from collections import OrderedDict

from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import cli
from clusterone.commands.get.project import cmd


def test_passing_project_path(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.path_to_project = mocker.Mock()

    CliRunner().invoke(cli, ['get', 'project', 'some_user/some_project_name'])

    cmd.path_to_project.assert_called_with('some_user/some_project_name', context=mocker.ANY)

def test_table_call(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.path_to_project = mocker.Mock(return_value=OrderedDict([
        ('name', 'my-project-name'),
        ('owner', OrderedDict([
            ('username', 'someuser'),
            ])),
        ('created_at', '2020-06-12T11:35:56.364015Z'),
        ('modified_at', '2032-01-18T22:42:19.366416Z'),
        ('size', 123),
    ]))
    cmd.make_table = mocker.Mock(return_value="Example table string")

    CliRunner().invoke(cli, ['get', 'project', 'some_user/some_project_name'])

    cmd.make_table.assert_called_with([[
        'my-project-name',
        '2020-06-12T11:35:56.364015Z',
        'someuser',
        123,
        '2032-01-18T22:42:19.366416Z'
        ]], header=['Name', 'Created', 'Owner', 'Size [Mb]', 'Modified'])

def test_printing_out_table(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.path_to_project = mocker.Mock(return_value=OrderedDict([
        ('name', 'my-project-name'),
        ('owner', OrderedDict([
            ('username', 'someuser'),
            ])),
        ('created_at', '2020-06-12T11:35:56.364015Z'),
        ('modified_at', '2032-01-18T22:42:19.366416Z'),
        ('size', 123),
    ]))
    cmd.make_table = mocker.Mock(return_value="Example table string")

    result = CliRunner().invoke(cli, ['get', 'project', 'some_user/some_project_name'])

    assert result.output == "Example table string\n"
