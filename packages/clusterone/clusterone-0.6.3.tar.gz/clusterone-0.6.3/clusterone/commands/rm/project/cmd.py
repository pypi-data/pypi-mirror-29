import click
from click import confirm

from clusterone import authenticate
from clusterone.client_exceptions import BussyProjectRemoveAttempt
from clusterone.utilities import path_to_project

@click.command()
@click.pass_obj
@click.argument(
    'project-path-or-id',
    )
@authenticate()
def command(context, project_path_or_id):
    """
    Removes a project, confirmation required
    """

    client = context.client

    project = path_to_project(project_path_or_id, context=context)

    project_jobs = client.get_jobs({
        "repository": project['id'],
    })
    project_has_running_jobs = any(
        map(lambda job: job['status'] in ['started', 'running'], project_jobs)
    )

    if project_has_running_jobs:
        raise BussyProjectRemoveAttempt()

    confirm("Removing a project will remove all associated jobs and outputs. Are you sure?", abort=True)

    client.delete_project(project['name'], project['username'])
