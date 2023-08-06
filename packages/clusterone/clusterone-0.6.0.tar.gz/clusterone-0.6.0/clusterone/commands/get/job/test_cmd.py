from collections import OrderedDict

from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import cli
from clusterone.commands.get.job import cmd


def test_job_aquisition(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_job = mocker.Mock()
    cmd.serialize_job = mocker.Mock(return_value="12345678")

    CliRunner().invoke(cli, ['get', 'job', 'project/job_name'])

    cmd.serialize_job.assert_called_with('project/job_name', context=mocker.ANY)

def test_prop_stripping_single(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.serialize_job = mocker.Mock(return_value=OrderedDict([
    ('job_id', 'e144f11c-0207-47d6-b672-7efd692b0885'),
    ('repository', 'aaf4de71-f506-48c0-855c-02c7c485c5a4'),
    ('repository_owner', 'allgreed'),
    ('repository_name', 'mnist-demo'),
    ('repository_owner_photo_url',
     'https://clusterone-api-development.s3.amazonaws.com/images/empty_image_400_400.png'
     ),
    ('display_name', 'job'),
    ('description', 'Dummy job'),
    ('created_at', '2018-01-12T12:38:23.593018Z'),
    ('launched_at', '2018-01-24T16:33:19.411485Z'),
    ('terminated_at', '2018-01-24T16:41:41.557648Z'),
    ('modified_at', '2018-01-24T16:43:32.631078Z'),
    ('git_commit_hash', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'),
    ('status', 'stopped'),
    ('parameters', OrderedDict([
        ('debug', ''),
        ('ps_replicas', 1),
        ('package_manager', 'pip'),
        ('worker_type', 't2.small'),
        ('data_repos', []),
        ('code_repo', OrderedDict([('hash',
         '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'), ('url',
         'https://git.clusterone.com/allgreed/mnist-demo.git'),
         ('mount_point', 'code')])),
        ('python_version', '2.7'),
        ('package_path', ''),
        ('instance_type', 't2.small'),
        ('tf_version', '1.0.0'),
        ('requirements', 'requirements.txt'),
        ('code_repo_commit', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'
         ),
        ('ps_type', 't2.small'),
        ('time_limit', 2880),
        ('git_username', 'allgreed'),
        ('git_password', '584ed7f63b75c50ef3d38e9514d2cd14dc39eb14'),
        ('module', 'main'),
        ('worker_replicas', 2),
        ('framework', 'tensorflow'),
        ('mode', 'single-node-tf'),
        ])),
    ]))

    result = CliRunner().invoke(cli, ['get', 'job', 'project/job_name'])

    assert not any([(parameter in result.output) for parameter in ["Worker type", "Ps type", "Worker replicas", "Ps replicas"]])

def test_prop_stripping_distributed(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.serialize_job = mocker.Mock(return_value=OrderedDict([
    ('job_id', 'e144f11c-0207-47d6-b672-7efd692b0885'),
    ('repository', 'aaf4de71-f506-48c0-855c-02c7c485c5a4'),
    ('repository_owner', 'allgreed'),
    ('repository_name', 'mnist-demo'),
    ('repository_owner_photo_url',
     'https://clusterone-api-development.s3.amazonaws.com/images/empty_image_400_400.png'
     ),
    ('display_name', 'job'),
    ('description', 'Dummy job'),
    ('created_at', '2018-01-12T12:38:23.593018Z'),
    ('launched_at', '2018-01-24T16:33:19.411485Z'),
    ('terminated_at', '2018-01-24T16:41:41.557648Z'),
    ('modified_at', '2018-01-24T16:43:32.631078Z'),
    ('git_commit_hash', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'),
    ('status', 'stopped'),
    ('parameters', OrderedDict([
        ('debug', ''),
        ('ps_replicas', 1),
        ('package_manager', 'pip'),
        ('worker_type', 't2.small'),
        ('data_repos', []),
        ('code_repo', OrderedDict([('hash',
         '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'), ('url',
         'https://git.clusterone.com/allgreed/mnist-demo.git'),
         ('mount_point', 'code')])),
        ('python_version', '2.7'),
        ('package_path', ''),
        ('instance_type', 't2.small'),
        ('tf_version', '1.0.0'),
        ('requirements', 'requirements.txt'),
        ('code_repo_commit', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'
         ),
        ('ps_type', 't2.small'),
        ('time_limit', 2880),
        ('git_username', 'allgreed'),
        ('git_password', '584ed7f63b75c50ef3d38e9514d2cd14dc39eb14'),
        ('module', 'main'),
        ('worker_replicas', 2),
        ('framework', 'tensorflow'),
        ('mode', 'distributed'),
        ])),
    ]))

    result = CliRunner().invoke(cli, ['get', 'job', 'project/job_name'])

    assert "Instance type" not in result.output

def test_table_call(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.serialize_job = mocker.Mock(return_value=OrderedDict([
    ('job_id', 'e144f11c-0207-47d6-b672-7efd692b0885'),
    ('repository', 'aaf4de71-f506-48c0-855c-02c7c485c5a4'),
    ('repository_owner', 'allgreed'),
    ('repository_name', 'mnist-demo'),
    ('repository_owner_photo_url',
     'https://clusterone-api-development.s3.amazonaws.com/images/empty_image_400_400.png'
     ),
    ('display_name', 'job'),
    ('description', 'Dummy job'),
    ('created_at', '2018-01-12T12:38:23.593018Z'),
    ('launched_at', '2018-01-24T16:33:19.411485Z'),
    ('terminated_at', '2018-01-24T16:41:41.557648Z'),
    ('modified_at', '2018-01-24T16:43:32.631078Z'),
    ('git_commit_hash', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'),
    ('status', 'stopped'),
    ('parameters', OrderedDict([
        ('debug', ''),
        ('ps_replicas', 1),
        ('package_manager', 'pip'),
        ('worker_type', 't2.small'),
        ('data_repos', []),
        ('code_repo', OrderedDict([('hash',
         '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'), ('url',
         'https://git.clusterone.com/allgreed/mnist-demo.git'),
         ('mount_point', 'code')])),
        ('python_version', '2.7'),
        ('package_path', ''),
        ('instance_type', 't2.small'),
        ('tf_version', '1.0.0'),
        ('requirements', 'requirements.txt'),
        ('code_repo_commit', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'
         ),
        ('data_repos', [OrderedDict([('hash', 'hash'), ('mount_point', 'user/dataset')])]),
        ('ps_type', 't2.small'),
        ('time_limit', 2880),
        ('git_username', 'allgreed'),
        ('git_password', '584ed7f63b75c50ef3d38e9514d2cd14dc39eb14'),
        ('module', 'main'),
        ('worker_replicas', 2),
        ('framework', 'tensorflow'),
        ('mode', 'single-node-tf'),
        ])),
    ]))
    cmd.path_to_job_id = mocker.Mock(return_value="12345678")
    cmd.make_table = mocker.Mock(return_value="Example table string")

    CliRunner().invoke(cli, ['get', 'job', 'project/job_name'])

    cmd.make_table.assert_called_with([('Name', 'job'), ('Status', 'stopped'), ('Project', 'mnist-demo'), ('Module', 'main'), ('Package-path', ''),('Datasets', 'user/dataset:hash\n'), ('Python version', '2.7'), ('Package manager', 'pip'), ('Requirements', 'requirements.txt'), ('Framework', 'tensorflow'), ('Framework version', '1.0.0'), ('Mode', 'single-node-tf'), ('Instance type', 't2.small'), ('Time limit', '2880 minutes')], header=['Property', 'Value'])

def test_printing_out_table(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_job = mocker.Mock(return_value=OrderedDict([
    ('job_id', 'e144f11c-0207-47d6-b672-7efd692b0885'),
    ('repository', 'aaf4de71-f506-48c0-855c-02c7c485c5a4'),
    ('repository_owner', 'allgreed'),
    ('repository_name', 'mnist-demo'),
    ('repository_owner_photo_url',
     'https://clusterone-api-development.s3.amazonaws.com/images/empty_image_400_400.png'
     ),
    ('display_name', 'job'),
    ('description', 'Dummy job'),
    ('created_at', '2018-01-12T12:38:23.593018Z'),
    ('launched_at', '2018-01-24T16:33:19.411485Z'),
    ('terminated_at', '2018-01-24T16:41:41.557648Z'),
    ('modified_at', '2018-01-24T16:43:32.631078Z'),
    ('git_commit_hash', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'),
    ('status', 'stopped'),
    ('parameters', OrderedDict([
        ('debug', ''),
        ('ps_replicas', 1),
        ('package_manager', 'pip'),
        ('worker_type', 't2.small'),
        ('data_repos', []),
        ('code_repo', OrderedDict([('hash',
         '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'), ('url',
         'https://git.clusterone.com/allgreed/mnist-demo.git'),
         ('mount_point', 'code')])),
        ('python_version', '2.7'),
        ('package_path', ''),
        ('instance_type', 't2.small'),
        ('tf_version', '1.0.0'),
        ('requirements', 'requirements.txt'),
        ('code_repo_commit', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1'
         ),
        ('ps_type', 't2.small'),
        ('time_limit', 2880),
        ('git_username', 'allgreed'),
        ('git_password', '584ed7f63b75c50ef3d38e9514d2cd14dc39eb14'),
        ('module', 'main'),
        ('worker_replicas', 2),
        ('framework', 'tensorflow'),
        ('mode', 'single-node-tf'),
        ])),
    ]))
    cmd.path_to_job_id = mocker.Mock(return_value="12345678")
    cmd.make_table = mocker.Mock(return_value="Example table string")

    result = CliRunner().invoke(cli, ['get', 'job', 'project/job_name'])

    assert result.output == "Example table string\n"
