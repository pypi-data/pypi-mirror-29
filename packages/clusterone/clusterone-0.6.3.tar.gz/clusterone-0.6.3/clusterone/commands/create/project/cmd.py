import click

from clusterone import authenticate

from clusterone.messages import project_creation_in_progress_message
from .helper import main


@click.command()
@click.argument('name')
@click.option('--description', default='')
@click.pass_obj
@authenticate()
def command(context, name, description):
    """
    Create a new clusterone project and outputs it's git remote url
    """

    click.echo(project_creation_in_progress_message)

    remote_url = main(context, name, description)

    click.echo(remote_url)

    return remote_url

