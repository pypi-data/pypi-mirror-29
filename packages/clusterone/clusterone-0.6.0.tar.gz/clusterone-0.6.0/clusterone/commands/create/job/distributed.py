try:
    from math import inf
except ImportError as exception:
    inf = float('inf')

import click
from click import IntRange, Choice
from click.exceptions import BadParameter

from clusterone import authenticate

from .base_cmd import base_options, base, WORKER_INSTANCE_TYPE, PARAMETER_SERVER_INSTANCE_TYPE


PS_REPLICAS_WARINING_THRESHOLD = 5
WORKER_REPLICAS_WARINING_THRESHOLD = 10

POSITIVE_INTEGER = IntRange(1, inf)

@click.command()
@click.pass_obj
@authenticate()
@base_options
@click.option(
    '--worker-type',
    type=WORKER_INSTANCE_TYPE,
    default="t2.small",
    help="Type of the worker instances.")
@click.option(
    '--ps-type',
    type=PARAMETER_SERVER_INSTANCE_TYPE,
    default="t2.small",
    help="Type of the parameter server instances.")
@click.option(
    '--worker-replicas',
    type=POSITIVE_INTEGER,
    default=2,
    help="Number of worker instances.",
    )
@click.option(
    '--ps-replicas',
    type=POSITIVE_INTEGER,
    default=1,
    help="Number of parameter server instances.",
    )
def command(context, **kwargs):
    """
    Creates a distributed job.
    See also: create job single.
    """

    client = context.client
    job_configuration = base(context, kwargs)

    job_configuration['parameters']['mode'] = "distributed"

    ps_replicas, worker_replicas = kwargs['ps_replicas'], kwargs['worker_replicas']

    if ps_replicas > PS_REPLICAS_WARINING_THRESHOLD:
        click.echo("Caution: You are creating a job with more than {} parameter servers.".format(PS_REPLICAS_WARINING_THRESHOLD))
    if worker_replicas > WORKER_REPLICAS_WARINING_THRESHOLD:
        click.echo("Caution: You are creating a job with more than {} workers.".format(WORKER_REPLICAS_WARINING_THRESHOLD))

    #TODO: Redo this in better way, when refactoring
    # Right now it lists "pytorch" as a valid options
    # Shall do a custom framework with custom help and move the logic there
    if job_configuration['parameters']['framework'] == 'pytorch-1.0.0':
        raise BadParameter("PyTorch is only supported for single jobs. For PyTorch please use `create job single [...]` instead.", param_hint="--framework")

    #TODO: This is shitty as shit, refactor at first opportunity!!!!!!
    job_configuration['parameters']['workers'] =  {'slug': kwargs['worker_type'], 'replicas': worker_replicas}
    job_configuration['parameters']['parameter_servers'] =  {'slug': kwargs['ps_type'], 'replicas': ps_replicas}

    client.create_job(
        job_configuration['meta']['name'],
        description=job_configuration['meta']['description'],
        parameters=job_configuration['parameters'],
        )
