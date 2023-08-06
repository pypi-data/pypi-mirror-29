#!/usr/bin/env python3

import six
import json
import os
import sys
import click
import git
import logging
import click_log
import functools
import time

from clusterone import ClusteroneClient
from clusterone import authenticate
from clusterone.config import Config
from clusterone.clusterone_client import MATRIX_URL

from clusterone.version import VERSION
from clusterone.utils import random_name_generator, normalize, normalize_string, select_valid_index, render_table, tokenize_repo, question, info, option, repo_name_validator, \
    job_name_validator, select_repo, describe, select_job, \
    select_valid_integer, get_current_version
from clusterone.tf_runner import run_tf

from gettext import gettext as _

# TODO: Handle KeyBoardInterrup at high level here

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME_DIR = os.getcwd()
logger = logging.getLogger(__name__)

# Bunch of global messages
global_config = Config()
global_config.__init__()
global_config.load()
if global_config.get('username') is None:
    owner_help_message = 'Specify owner by usernames'
else:
    owner_help_message = 'Specify owner by username, default: %s' % global_config.get(
        'username')

pass_config = click.make_pass_decorator(Config, ensure=True)


class Context(object):
    def __init__(self, client, config, cwd):
        self.client = client
        self.config = config
        self.cwd = cwd


from clusterone import ClusteroneException
from clusterone.utilities import log_error


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
@click.pass_context
def cli(context):
    """
    Welcome to Clusterone Command Line Interface.
    """
    config = Config()
    config.load()
    client = ClusteroneClient(token=config.get('token'), username=config.get('username'))
    context.obj = Context(client, config, HOME_DIR)


def main():
    try:
        cli()
    except ClusteroneException as exception:
        log_error(exception)
        sys.exit(exception.exit_code)
        # except Exceptions as exception:
        # # here Sentry logger is a good idea
        #     pass


# ---------------------------------------

@cli.group()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
def get(context):
    """
    < project(s) | dataset(s) | job(s) | events >
    """
    pass


@cli.group()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
def create(context):
    """
    < project | dataset | job >
    """
    pass


@cli.group()
@click.pass_obj
def rm(context):
    """
    < project | dataset | job >
    """
    pass


@create.group()
@click.pass_obj
def job(context):
    """
    < single | distributed >
    """

    pass


@cli.group()
@click.pass_context
def init(context):
    """
    < project | dataset >
    """
    pass


@cli.group()
@click.pass_context
def ln(config):
    """
    < project | dataset >
    """
    pass


@cli.group()
@click.pass_context
def start(config):
    """
    < job >
    """
    pass


# TODO: Redo the above to be dynamic -> eg. job command goes through it's modules and lists single | distributed dynamically

# ------------------------

# TODO: Redo this to dynamic import
from clusterone import commands

get.add_command(commands.get.job.command, 'job')
create.add_command(commands.create.project.command, 'project')

job.add_command(commands.create.job.single.command, 'single')
job.add_command(commands.create.job.distributed.command, 'distributed')

rm.add_command(commands.rm.job.command, 'job')
rm.add_command(commands.rm.project.command, 'project')
rm.add_command(commands.rm.dataset.command, 'dataset')

get.add_command(commands.get.project.command, 'project')

init.add_command(commands.init.project.command, 'project')

ln.add_command(commands.ln.project.command, 'project')
ln.add_command(commands.ln.dataset.command, 'dataset')

start.add_command(commands.start.job.command, 'job')
create.add_command(commands.create.dataset.command, 'dataset')

# ---

cli.add_command(commands.stop.job.command, 'stop')


# ------------------------

@cli.command()
@click.option('--username', '-u', prompt=True)
@click.option('--password', '-p', prompt=True, hide_input=True)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
def login(config, username, password):
    """
    Log into Clusterone
    """

    # Version Check
    if not get_current_version():
        click.echo(info("There is an updated version in PYPI - please run pip install clusterone --upgrade"))
        return

    client = ClusteroneClient()
    user, message = client.api_login(username, password)
    if user is not None:
        # Save Token and Username in Config File
        config['token'] = client.token
        config['git_token'] = client.git_token
        config['username'] = username
        if user['first_name'] != '':
            config['first_name'] = user['first_name']
        else:
            config['first_name'] = username

        config.save()
        click.echo(info("Welcome %s! \nYour last login was on %s" %
                        (config['first_name'], user['last_login'])))

        return client.token
    else:
        click.echo(info("Login Failed! %s" % message))
        return


@cli.command()
@click.pass_obj
@authenticate()
def logout(context):
    """
    Log out from Clusterone
    """

    config = context.config

    if click.confirm("%s, Are you sure you want to log out?" %
                         (config.get('first_name'))):
        config.delete()


@cli.command()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
def matrix(config):
    """
    Open Matrix in your browser
    """
    client = ClusteroneClient(
        token=config.get('token'), username=config.get('username'))
    click.echo(info("Entering Matrix: %s") % MATRIX_URL)
    client.open_dashboard()


@click.command()
@click.option(
    '--owner', default=global_config.get('username'), help=owner_help_message)
# @click_log.simple_verbosity_option()
# @click_log.init(__name__)
@click.pass_obj
@authenticate()
def get_jobs(context, owner):
    """
    List jobs
    """
    config = context.config

    # TODO: filter by owner name is not working
    client = ClusteroneClient(
        token=config.get('token'), username=config.get('username'))
    running_jobs = client.get_jobs(params={'owner': owner})
    if running_jobs:
        data = []
        data.append(['#', 'Name', 'Id', 'Project', 'Status', 'Launched at'])

        i = 0
        valid_jobs = []
        for job in running_jobs:
            try:
                data.append([
                    i,
                    '%s/%s' % (job.get('owner'), job.get('display_name')),
                    job['job_id'],
                    '%s/%s:%s' %
                    (job.get('repository_owner'), job.get('repository_name'),
                     job.get('git_commit_hash')[:8]),
                    job.get('status'),
                    '' if job.get('launched_at') is None else job.get(
                        'launched_at')[:-5]
                ])
                i += 1
                valid_jobs.append(job)
            except Exception as exception:
                pass
        table = render_table(data, 36)
        click.echo(table.table)
        return running_jobs
    else:
        click.echo(info("You don't seem to have any jobs yet. Try just create job to make one."))
        return


get.add_command(get_jobs, 'jobs')


@cli.command()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
@authenticate()
def pulse(context):
    """
    Get status of jobs
    """

    config = context.config

    # TODO: show resources for each job
    client = ClusteroneClient(
        token=config.get('token'), username=config.get('username'))
    running_jobs = client.get_jobs()  # TODO Check running job parameter
    if running_jobs:
        click.echo(info('Jobs:'))
        data = []
        data.append(['#', 'Job', 'Project', 'Status', 'Launched at'])

        i = 0
        valid_jobs = []
        for job in running_jobs:
            try:
                data.append([
                    i,
                    '%s/%s' % (job.get('owner'), job.get('display_name')),
                    '%s/%s:%s' %
                    (job.get('repository_owner'), job.get('repository_name'),
                     job.get('git_commit_hash')[:8]),
                    job.get('status'),
                    '' if job.get('launched_at') is None else job.get(
                        'launched_at')[:-5]
                ])
                i += 1
                valid_jobs.append(job)
            except:
                pass
        table = render_table(data, 36)
        click.echo(table.table)
        return running_jobs
    else:
        click.echo(info("You don't seem to have any jobs yet. Try 'tport create job' to make one."))
        return


@cli.command()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
@authenticate()
def watch(context):
    """
    Shortcut for tport get events --watch
    """

    config = context.config

    client = ClusteroneClient(
        token=config.get('token'), username=config.get('username'))
    while True:
        events = client.get_events()
        if events:
            data = [['Time', 'Job', 'Status', 'Event']]

            for e in events:
                try:
                    data.append([
                        e.get('created_at')[:19],
                        e.get('job_name'),
                        e.get('event_level_display'),
                        e.get('event_type_display')
                    ])
                except:
                    pass
            table = render_table(data, 54)
            os.system("printf '\033c'")
            click.echo(table.table)
            time.sleep(1)
        else:
            click.echo("Failed to query recent events. Perhaps you have not started a job yet. Try 'tport run'.")
            return None


@click.command()
@authenticate()
@click.pass_obj
@click.option('--owner')
def get_projects(context, owner=None):
    """
    List projects
    """

    config = context.config

    # TODO: fix owner
    client = ClusteroneClient(
        token=config.get('token'), username=config.get('username'))

    projects = client.get_projects()

    if projects:
        click.echo(info("All projects:"))
        data = []
        data.append(
            ['#', 'Project', 'Created at', 'Description'])

        i = 0
        for project in projects:
            try:
                data.append([
                    i,
                    "%s/%s" % (project.get('owner')
                               ['username'], project.get('name')),
                    project.get('created_at')[:19],
                    project.get('description')
                ])
                i += 1
            except:
                pass
        table = render_table(data, 36)
        click.echo(table.table)
        return projects
    else:
        click.echo(info(
            "No projects found. Use 'tport create project' to start a new one."))
        return None


get.add_command(get_projects, 'projects')


@click.command()
@click.option('--name', prompt=True)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
@authenticate()
def get_dataset(context, name):
    """
    Get information about a dataset
    """

    client, config = context.client, context.config

    dataset = client.get_dataset(name, config.get('username'))

    click.echo("Dataset: %s | ID: %s" % (dataset.get('name'),
                                            dataset.get('id')))
    return dataset


get.add_command(get_dataset, 'dataset')


@click.command()
@click.option('--owner')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
@authenticate()
def get_datasets(context, owner=None):
    """
    List datasets
    """
    client, config = context.client, context.config

    datasets = client.get_datasets(owner)

    if datasets:
        click.echo(info("All datasets:"))
        data = []
        data.append(
            ['#', 'Dataset', 'Modified at', 'Description'])

        i = 0
        for project in datasets:
            try:
                data.append([
                    i,
                    "%s/%s" % (project.get('owner')
                               ['username'], project.get('name')),
                    project.get('modified_at')[:19],
                    project.get('description')
                ])
                i += 1
            except:
                pass
        table = render_table(data, 36)
        click.echo(table.table)
        return datasets
    else:
        click.echo("It doesn't look like you have any datasets yet. You can make a new one with 'tport create dataset'.")
        return None


get.add_command(get_datasets, 'datasets')


@click.command()
@click.option('--watch', is_flag=True, default=False, help='Watch events every 1 second.')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
@authenticate()
def get_events(context, watch):
    """
    See latest events
    """
    config = context.config

    client = ClusteroneClient(
        token=config.get('token'), username=config.get('username'))
    flag = True
    while flag:
        flag = watch
        events = client.get_events()
        if events:
            data = [['Time', 'Job', 'Status', 'Event']]

            i = 0
            for e in events:
                try:
                    data.append([
                        e.get('created_at')[:19],
                        e.get('job_name'),
                        e.get('event_level_display'),
                        e.get('event_type_display')
                    ])
                    i += 1
                except:
                    pass
            table = render_table(data, 54)
            if flag:
                os.system("printf '\033c'")
            click.echo(table.table)
            if flag:
                time.sleep(1)
        else:
            click.echo("Failed to query recent events. Perhaps you have not started a job yet. Try 'tport run'.")
            return None


get.add_command(get_events, 'events')


# TODO: Manage this -> this code is from former run job command

# @click.option('--local', is_flag=True, default=False, help='Run the job locally. Works both with distributed or single-node.')

# local=None,

#    if local:
#        run_local_tf(package_path, module, training_mode, worker_replicas,
#                     ps_replicas, requirements, current_env, framework_version)

def run_local_tf(package_path, module, training_mode, worker_replicas,
                 ps_replicas, requirements=None, current_env=False, tf_version=None):
    # Select training mode
    training_modes = ['single-node', 'distributed']
    if (training_mode is None) or (not training_mode in training_modes):
        if not training_mode:
            mode = click.echo(question('Select a training mode from'))
        else:
            mode = click.echo(
                question('%s is not a valid training mode. Select from' %
                         training_mode))
        for i, mode in enumerate(training_modes):
            click.echo('%s | %s' % (i, mode))
        mode_id = select_valid_index(0,
                                     len(training_modes) - 1,
                                     question("Select training mode from"))
        training_mode = training_modes[mode_id]

    if training_mode == 'distributed':
        # Specify number of workers
        if worker_replicas == None:
            worker_replicas = click.prompt(
                text=question('Select number of workers'), default=1)
        else:
            worker_replicas = int(worker_replicas)
        # Specify number of parameter servers
        if ps_replicas == None:
            ps_replicas = click.prompt(
                text=question('Select number of parameter servers'), default=1)
        else:
            ps_replicas = int(ps_replicas)

    # Specify module
    if module is None:
        module = click.prompt(
            text=question('Specify the python module to run'),
            default='main')

    # Strip .py from module, many users leave it there!
    module = module.strip('.py')

    if not current_env:
        if requirements is None:
            choice = select_valid_index(0, 2,
                                        question(
                                            "Requirements file not specified. You can \n    0- Specify a requirements file\n    1- Run without installing any requirements\n    2- Use your current environment (not recommended).\n -> Which one do you want?"))
            if choice == 0:
                current_env = False
                requirements = click.prompt(
                    text=question('Specify the requirements file'),
                    default='requirements.txt')
                requirements = os.path.join(os.getcwd(), requirements)
            elif choice == 1:
                current_env = False
                requirements = None
            elif choice == 2:
                current_env = True

    if tf_version is None:
        tf_version = '1.0.0'

    print("Running %s locally" % training_mode)
    assert (training_mode in ['single-node', 'distributed'])
    run_tf(
        cwd=os.getcwd(),
        package_path=package_path,
        module=module,
        mode=training_mode,
        worker_replicas=worker_replicas,
        ps_replicas=ps_replicas,
        requirements=requirements,
        current_env=current_env,
        tf_version=tf_version)


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option('--job-id')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
@authenticate()
def download_files(context, path, job_id=None):
    """
    downloads all outputs and saves at specified path
    """
    config, client = context.config, context.client
    try:
        client = ClusteroneClient(
            token=config.get('token'), username=config.get('username'))
        # We get list of user jobs and allow user to select them
        if not job_id:
            jobs = client.get_jobs()
            if jobs:
                job_id, job_name = select_job(jobs, 'Select the job you want to download files from')
            else:
                click.echo(
                    info(
                        "You do not seem to have any jobs. Use 'tport run' to run a job."
                    ))
                return
        else:
            job = client.get_job(params={'job_id': job_id})
            if job:
                job_id = job.get('job_id')
                job_name = job.get('display_name')
            else:
                click.echo(info("%s is not a valid job id." % job_id))
                return
        # Download file list
        job_file_list = client.get_file_list(job_id)
        counter = 0
        for file in job_file_list:
            counter += 1
            # Display the files
            click.echo(
                option('%s | %s | %s kb' % (counter, file['name'], file['size'] / 1024)))
            try:
                if file['size'] > 0:
                    # Save file in specified path
                    file_content = client.download_file(job_id, file['name'])
                    file_path = os.path.join(path, file['name'])
                    f = open(file_path, "w")
                    f.write(file_content)
                    f.close()

            except Exception as e:
                click.echo("Failed to download files: %s" % str(e))
                logger.error("Failed to download file: %s" % str(e), exc_info=True)
                continue

    except Exception as e:
        logger.error("Failed to download files", exc_info=True)
        return


if __name__ == '__main__':
    main()
