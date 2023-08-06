import click

from clusterone import authenticate
from clusterone.utilities import path_to_job_id, make_table, serialize_job


HEADER = ['Property', 'Value']

HEADER_BASE = [
    'Name',
    'Status',
    'Project',
    'Module',
    'Package-path',
    'Datasets',
    'Python version',
    'Package manager',
    'Requirements',
    'Framework',
    'Framework version',
    'Mode',
    'Worker type',
    'Worker replicas',
    'Ps type',
    'Ps replicas',
    'Time limit',
    ]

#TODO: Test this thoughrilly in the future -> [], [dataset], [dataset] * 3
def displayable_data(datasets_list):
    return "".join(["{}:{}\n".format(dataset['mount_point'], dataset['hash']) for dataset in datasets_list])

def extract_data_from_job(job):

    mode = job['parameters']['mode']

    excluded_fields = \
        ["Ps type", "Worker replicas", "Ps replicas"] if mode == "single" \
        else []

    extracted_data = [
        job['display_name'],
        job['status'],
        job['repository_name'],
        job['parameters']['module'],
        job['parameters']['package_path'],
        displayable_data(job['parameters']['datasets']),
        job['parameters']['python_version'],
        job['parameters']['package_manager'],
        job['parameters']['requirements'],
        job['parameters']['framework']['name'],
        job['parameters']['framework']['version'],
        mode,
        job['parameters']['workers']['type'],
        job['parameters']['workers']['replicas'],
        job['parameters'].get('parameter_servers', {}).get('type'),
        job['parameters'].get('parameter_servers', {}).get('replicas'),
        "{} minutes".format(job['parameters']['time_limit']),
    ]

    key_value_pairs = zip(HEADER_BASE, extracted_data)

    #TODO: Redo this to namedtuples -> this pair[0] looks like shit...
    return [pair for pair in key_value_pairs if pair[0] not in excluded_fields]

@click.command()
@click.pass_obj
@authenticate()
@click.argument(
    'job-path-or-id',
    )
def command(context, job_path_or_id):
    """
    Get information about a job
    """

    job = serialize_job(job_path_or_id, context=context)

    click.echo(make_table(extract_data_from_job(job), header=HEADER))

    return job
