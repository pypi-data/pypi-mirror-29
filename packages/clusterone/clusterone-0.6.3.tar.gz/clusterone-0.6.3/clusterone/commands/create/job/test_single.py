from collections import OrderedDict

from click.testing import CliRunner

from clusterone.utilities import main
from clusterone.clusterone_cli import cli
from clusterone import ClusteroneClient
from clusterone.commands.create.job import single


# client call is not explicitly tested as other tests depend on that call
# base_options call is not explicitly tested as other tests depend on that call

def test_passing_instance_type(mocker):
    single.client = mocker.Mock()
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    # This mock will propagate across the tests
    ClusteroneClient.get_frameworks = mocker.Mock(return_value=[
        OrderedDict([('slug', 'pytorch-1.0.0'), ('name', 'pytorch'),
                     ('version', '1.0.0'), ('description', '')]),
        OrderedDict([('slug', 'tensorflow-1.4.0'), ('name', 'tensorflow'),
                     ('version', '1.4.0'), ('description', '')]),
        OrderedDict([('slug', 'tensorflow-1.5.0'), ('name', 'tensorflow'),
                     ('version', '1.5.0'), ('description', '')]),
        OrderedDict([('slug', 'tensorflow-1.3.0'), ('name', 'tensorflow'),
                     ('version', '1.3.0'), ('description', '')]),
        OrderedDict([('slug', 'tensorflow-1.2.0'), ('name', 'tensorflow'),
                     ('version', '1.2.0'), ('description', '')]),
        OrderedDict([('slug', 'tensorflow-1.0.0'), ('name', 'tensorflow'),
                     ('version', '1.0.0'), ('description', '')]),
    ])
    ClusteroneClient.get_instance_types = mocker.Mock(return_value=[
        OrderedDict([
            ('slug', 'c4.2xlarge'),
            ('name', 'c4.2xlarge'),
            ('type', 'c4.2xlarge'),
            ('type_class', 'c'),
            ('cpu', 8),
            ('memory', 15),
            ('gpu', 0),
            ('description', ''),
            ('show_for_ps', True),
            ('show_for_workers', True),
            ('blessed', True),
            ('queue', 'tensorport-jobmaster-blessed'),
        ]),
        OrderedDict([
            ('slug', 'c4.2xlarge-spot'),
            ('name', 'c4.2xlarge Spot Instance'),
            ('type', 'c4.2xlarge'),
            ('type_class', 'c'),
            ('cpu', 8),
            ('memory', 61),
            ('gpu    ', 0),
            ('description', ''),
            ('show_for_ps', True),
            ('show_for_workers', True),
            ('blessed', False),
            ('queue', 'tensorport-jobmaster'),
        ]),
        OrderedDict([
            ('slug', 'p2.xlarge'),
            ('name', 'p2.xlarge'),
            ('type', 'p2.xlarge'),
            ('type_class', 'c'),
            ('cpu', 4),
            ('memory', 61),
            ('gpu', 1),
            ('description', ''),
            ('show_for_ps', False),
            ('show_for_workers', True),
            ('blessed', True),
            ('queue', 'tensorport-jobmaster-blessed'),
        ]),
        OrderedDict([
            ('slug', 'p3    .2xlarge'),
            ('name', 'p3.2xlarge'),
            ('type', 'p3.2xlarge'),
            ('type_class', 'p'),
            ('cpu', 8),
            ('memory', 61),
            ('gpu', 1),
            ('description', ''),
            ('sho    w_for_ps', False),
            ('show_for_workers', True),
            ('blessed', True),
            ('queue', 'tensorport-jobmaster-blessed'),
        ]),
        OrderedDict([
            ('slug', 't2.small'),
            ('name', 't2.small'),
            ('type', 't2.small'),
            ('type_class', 'c'),
            ('cpu', 1),
            ('memory', 2),
            ('gpu', 0),
            ('description', ''),
            ('show_for_ps', True),
            ('show_for_workers', True),
            ('blessed', True),
            ('queue', 'tensorport-jobmaster-blessed'),
        ]),
        OrderedDict([
            ('slug', 't2.small-spot'),
            ('name', 't2.sm    all Spot Instance'),
            ('type', 't2.small'),
            ('type_class', 'c'),
            ('cpu', 1),
            ('memory', 2),
            ('gpu', 0),
            ('description', ''),
            ('show_for_ps', True),
            ('show_for_workers', True),
            ('blessed', False),
            ('queue', 'tensorport-jobmaster'),
        ]),
    ])
    ClusteroneClient.create_job = mocker.Mock()
    single.base = mocker.Mock(return_value={'meta': {'name': 'late-moon-758', 'description': ''}, 'parameters': {'package_path': '', 'requirements': 'requirements.txt', 'time_limit': 2880, 'module': 'main', 'framework': 'tensorflow-1.3.0', 'code_commit': '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1', 'code': 'aaf4de71-f506-48c0-855c-02c7c485c5a4', 'package_manager': 'pip', 'Clusterone_api_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9sZ2llcmRAa2FzcHJvd2ljei5wcm8iLCJ1c2VyX2lkIjo3OTUsImV4cCI6MTUxNzMxNjUzMCwidXNlcm5hbWUiOiJhbGxncmVlZCJ9.IJhEZWwMYf2sjHhoxUsjCj0Xll5CVX-RO3eUqvH7myU', 'python_version': 2.7}})

    CliRunner().invoke(cli, [
        'create',
        'job',
        'single',
        '--project', 'someproject',
        '--instance-type', 'p2.xlarge',
    ])

    args, kwargs = ClusteroneClient.create_job.call_args


    assert kwargs['parameters']['workers']['slug'] == 'p2.xlarge'

def test_default_instance_type(mocker):
    single.client = mocker.Mock()
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
    assert kwargs['parameters']['workers']['slug'] == 't2.small'

def test_pytorch_invalid_framework_version(mocker):
    single.client = mocker.Mock()
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
    single.client = mocker.Mock()
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
    single.client = mocker.Mock()
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
