import click
from click import confirm

from clusterone import authenticate
from clusterone.utilities import serialize_job
from clusterone.client_exceptions import RunningJobRemoveAttempt

@click.command()
@click.pass_obj
@click.argument(
    'job-path-or-id',
    )
@authenticate()
def command(context, job_path_or_id):
    """
    Removes a job, confirmation required
    """

    client = context.client
    job = serialize_job(job_path_or_id, context=context)

    if job['status'] in ['started', 'running']:
        raise RunningJobRemoveAttempt()

    confirm("Removing a job is irreversible and job outputs will be deleted. Are you sure?", abort=True)

    client.delete_job(job['job_id'])
