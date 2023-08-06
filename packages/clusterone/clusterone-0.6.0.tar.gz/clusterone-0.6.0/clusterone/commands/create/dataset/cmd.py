import time

import click

from clusterone import authenticate
from clusterone.messages import dataset_creation_in_progress_message
from clusterone.client_exceptions import RemoteAquisitionFailure


def aquire_remote(name, config, client):

    username = config['username']
    retry_count, retry_interval = config.retry_count, config.retry_interval

    #pytest.set_trace()

    for _ in range(retry_count):
        time.sleep(retry_interval)

        dataset = client.get_dataset(name, username)
        git_url = dataset['git_auth_link']

        # API response might be evaluated as None or ""
        if not (git_url is None or git_url == ""):
            return git_url

    raise RemoteAquisitionFailure()

@click.command()
@click.pass_obj
@authenticate()
@click.argument('name')
@click.option('--description', default='')
def command(context, name, description):
    """
    Create a new clusterone dataset and outputs it's git remote url
    """

    client, config = context.client, context.config

    click.echo(dataset_creation_in_progress_message)

    dataset_name = client.create_dataset(name, description)
    remote_url = aquire_remote(dataset_name, client=client, config=config)

    click.echo(remote_url)

    # Warning! This is untested!
    config['current_dataset'], config['current_dataset_name'] = [dataset_name] * 2
    config.save()

    return remote_url
