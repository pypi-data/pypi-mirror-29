import click

from clusterone import authenticate


@click.command()
@click.pass_context
@authenticate()
@click.argument('name')
@click.option('--description', '-d', default='')
@click.option('--repo-path', '-r')
def command(context, name, description, repo_path):
    """
    Create a new project and link current repo to clusterone remote
    """

    # This is required to break circular import and make this Python2.7 compliant
    from clusterone import commands

    cwd = context.obj.cwd

    remote_url = context.invoke(commands.create.project.command, name=name, description=description)

    # since context cannot be referenced in the deault paramters
    repository_path = repo_path if repo_path is not None else cwd

    commands.ln.project.helper.main(context.obj, repository_path, remote_url)

    return
