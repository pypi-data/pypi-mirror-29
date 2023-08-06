import click
from click import Choice
from click.exceptions import BadParameter

from clusterone import client
from clusterone.utilities import LazyChoice
from .base_cmd import job_base_options, base


@job_base_options
@click.option(
    '--instance-type',
    type=LazyChoice(client.instance_types_slugs),
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
    job_configuration['parameters']['workers'] = \
    {
        'slug': kwargs['instance_type'],
        'replicas': 1
    }

    client.create_job(
        job_configuration['meta']['name'],
        description=job_configuration['meta']['description'],
        parameters=job_configuration['parameters'],
        )
