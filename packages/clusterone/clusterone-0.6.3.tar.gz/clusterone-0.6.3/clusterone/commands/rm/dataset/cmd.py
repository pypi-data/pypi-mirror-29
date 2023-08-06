import click
from click import confirm

from clusterone import authenticate
from clusterone.client_exceptions import BussyDatasetRemoveAttempt
from clusterone.utilities import path_to_dataset


@click.command()
@click.pass_obj
@authenticate()
@click.argument(
    'dataset-path',
    )
def command(context, dataset_path):
    """
    Removes a dataset, confirmation required
    """

    client = context.client

    dataset = path_to_dataset(dataset_path, context=context)

    # test
    jobs_using_this_dataset = client.get_jobs({
        "datasets": dataset['id'],
    })
    dataset_used_by_running_job = any(
        map(lambda job: job['status'] in ['started', 'running'],
            jobs_using_this_dataset)
    )
    if dataset_used_by_running_job:
        raise BussyDatasetRemoveAttempt()

    confirm("Dummy?", abort=True)

    client.delete_dataset(dataset['name'], dataset['owner']['username'])
