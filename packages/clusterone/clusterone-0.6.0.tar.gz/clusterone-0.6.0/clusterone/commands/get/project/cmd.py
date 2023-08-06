import click

from clusterone import authenticate
from clusterone.utilities import path_to_project, make_table


HEADER = ['Name', 'Created', 'Owner', 'Size [Mb]', 'Modified']

def extract_data_from_project(project):
    return [
        project['name'],
        project['created_at'],
        project['owner']['username'],
        project['size'],
        project['modified_at'],
    ]

@click.command()
@click.pass_obj
@authenticate()
@click.argument(
    'project_path',
    )
def command(context, project_path):
    """
    Get information about a project
    """

    project = path_to_project(project_path, context=context)
    project_data = extract_data_from_project(project)
    click.echo(make_table([project_data], header=HEADER))

    return project
