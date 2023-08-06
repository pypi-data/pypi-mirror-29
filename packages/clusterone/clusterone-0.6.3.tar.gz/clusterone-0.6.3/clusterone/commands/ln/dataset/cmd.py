import click
from click.exceptions import BadParameter

from clusterone import authenticate
from .helper import main

@click.command()
@click.option(
    '--dataset-path',
    '-p',
    help="Project identifier of format \"username/dataset\".",
    required=True
    )
@click.option(
    '--repo-path',
    '-r',
    help="Path to local git repository.")
@click.pass_obj
@authenticate()
def command(context, dataset_path, repo_path):
    """
    Links existing Clusterone dataset with a local git repository
    """

    client, config, cwd = context.client, context.config, context.cwd

    # since context cannot be referenced in the deault paramters
    repository_path = repo_path if repo_path is not None else cwd

    path_tokens = dataset_path.split('/')

    if not len(path_tokens) == 2:
        if len(path_tokens) == 1:
            path_tokens = [config.get("username")] + path_tokens
        else:
            raise BadParameter(param_hint="--dataset-path", message="Please provide a valid dataset-path. The format is \"username/dataset\".")

    username, dataset_name = path_tokens

    dataset = client.get_dataset(dataset_name, username=username)

    remote_url = dataset.get('git_auth_link')

    main(context, repository_path, remote_url)

