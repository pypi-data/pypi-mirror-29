from click.testing import CliRunner

from clusterone.utilities import main
from clusterone.clusterone_cli import cli
from clusterone import ClusteroneClient
from clusterone.commands.create.job import single


# client call is not explicitly tested as other tests depend on that call
# base_options call is not explicitly tested as other tests depend on that call

def test_passing_instance_type(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.create_job = mocker.Mock()
    single.base = mocker.Mock(return_value={'meta': {'name': 'late-moon-758', 'description': ''}, 'parameters': {'package_path': '', 'requirements': 'requirements.txt', 'time_limit': 2880, 'module': 'main', 'tf_version': '', 'framework': 'tensorflow', 'code_commit': '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1', 'code': 'aaf4de71-f506-48c0-855c-02c7c485c5a4', 'package_manager': 'pip', 'Clusterone_api_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9sZ2llcmRAa2FzcHJvd2ljei5wcm8iLCJ1c2VyX2lkIjo3OTUsImV4cCI6MTUxNzMxNjUzMCwidXNlcm5hbWUiOiJhbGxncmVlZCJ9.IJhEZWwMYf2sjHhoxUsjCj0Xll5CVX-RO3eUqvH7myU', 'python_version': 2.7}})

    CliRunner().invoke(cli, [
        'create',
        'job',
        'single',
        '--project', 'someproject',
        '--instance-type', 'p2.xlarge',
    ])

    args, kwargs = ClusteroneClient.create_job.call_args
    assert kwargs['parameters']['worker_type'] == 'p2.xlarge'

def test_default_instance_type(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.create_job = mocker.Mock()
    single.base = mocker.Mock(return_value={'meta': {'name': 'late-moon-758', 'description': ''}, 'parameters': {'package_path': '', 'requirements': 'requirements.txt', 'time_limit': 2880, 'module': 'main', 'tf_version': '', 'framework': 'tensorflow', 'code_commit': '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1', 'code': 'aaf4de71-f506-48c0-855c-02c7c485c5a4', 'package_manager': 'pip', 'Clusterone_api_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9sZ2llcmRAa2FzcHJvd2ljei5wcm8iLCJ1c2VyX2lkIjo3OTUsImV4cCI6MTUxNzMxNjUzMCwidXNlcm5hbWUiOiJhbGxncmVlZCJ9.IJhEZWwMYf2sjHhoxUsjCj0Xll5CVX-RO3eUqvH7myU', 'python_version': 2.7}})

    CliRunner().invoke(cli, [
        'create',
        'job',
        'single',
        '--project', 'someproject',
    ])

    args, kwargs = ClusteroneClient.create_job.call_args
    assert kwargs['parameters']['worker_type'] == 'c4.2xlarge'

def test_pytorch_invalid_framework_version(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.create_job = mocker.Mock()
    single.base = mocker.Mock(return_value={'meta': {'name': 'late-moon-758', 'description': ''}, 'parameters': {'package_path': '', 'requirements': 'requirements.txt', 'time_limit': 2880, 'module': 'main', 'tf_version': '1.2', 'framework': 'pytorch', 'code_commit': '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1', 'code': 'aaf4de71-f506-48c0-855c-02c7c485c5a4', 'package_manager': 'pip', 'Clusterone_api_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9sZ2llcmRAa2FzcHJvd2ljei5wcm8iLCJ1c2VyX2lkIjo3OTUsImV4cCI6MTUxNzMxNjUzMCwidXNlcm5hbWUiOiJhbGxncmVlZCJ9.IJhEZWwMYf2sjHhoxUsjCj0Xll5CVX-RO3eUqvH7myU', 'python_version': 2.7}})

    result = CliRunner().invoke(cli, [
        'create',
        'job',
        'single',
        '--project', 'someproject'
        '--framework', 'pytorch',
        '--framework_version', '1.2',
    ])

    # Click internal exception
    assert str(result.exception) == '2'

def test_call_to_base(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    single.base = mocker.Mock()
    CliRunner().invoke(cli, [
        'create',
        'job',
        'single',
        '--project', 'someproject',
    ])

    assert single.base.call_count == 1

def test_is_single(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.create_job = mocker.Mock()
    single.base = mocker.Mock(return_value={'meta': {'name': 'late-moon-758', 'description': ''}, 'parameters': {'package_path': '', 'requirements': 'requirements.txt', 'time_limit': 2880, 'module': 'main', 'tf_version': '', 'framework': 'tensorflow', 'code_commit': '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1', 'code': 'aaf4de71-f506-48c0-855c-02c7c485c5a4', 'package_manager': 'pip', 'Clusterone_api_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9sZ2llcmRAa2FzcHJvd2ljei5wcm8iLCJ1c2VyX2lkIjo3OTUsImV4cCI6MTUxNzMxNjUzMCwidXNlcm5hbWUiOiJhbGxncmVlZCJ9.IJhEZWwMYf2sjHhoxUsjCj0Xll5CVX-RO3eUqvH7myU', 'python_version': 2.7}})

    CliRunner().invoke(cli, [
        'create',
        'job',
        'single',
        '--project', 'someproject',
    ])

    args, kwargs = ClusteroneClient.create_job.call_args
    assert kwargs['parameters']['mode'] == 'single'
