import click
from click import Choice
from click.exceptions import BadParameter

from clusterone import authenticate

from .base_cmd import base_options, base, WORKER_INSTANCE_TYPE


@click.command()
@click.pass_obj
@authenticate()
@base_options
#TODO: Unifiy this with distributed at code level
@click.option(
    '--instance-type',
    type=WORKER_INSTANCE_TYPE,
    default="t2.small",
    help="Type of single instance to run.")
def command(context, **kwargs):
    """
    Creates a single-node job.
    See also: create job distributed.
    """

    client = context.client
    job_configuration = base(context, kwargs)

    job_configuration['parameters']['mode'] = "single"

    #TODO: This is crap, move this to base
    job_configuration['parameters']['workers'] = {'slug': kwargs['instance_type'], 'replicas': 1}

    if job_configuration['parameters']['framework'] == "pytorch"  and not job_configuration['parameters']['tf_version'] == "":
        raise BadParameter("This pytorch version is not supported, try \"latest\" instead.", param_hint="--framework-version")

    client.create_job(
        job_configuration['meta']['name'],
        description=job_configuration['meta']['description'],
        parameters=job_configuration['parameters'],
        )
