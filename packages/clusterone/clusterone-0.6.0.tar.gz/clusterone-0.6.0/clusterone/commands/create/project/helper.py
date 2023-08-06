import time

from clusterone.client_exceptions import RemoteAquisitionFailure


def aquire_remote(project_name, config, client):

    username = config.get('username')
    retry_count, retry_interval = config.retry_count, config.retry_interval

    for _ in range(retry_count):
        time.sleep(retry_interval)

        project = client.get_project(project_name, username)
        git_url = project.get('git_auth_link')

        # API response might be evaluated as None or ""
        if not (git_url is None or git_url == ""):
            return git_url

    raise RemoteAquisitionFailure()

def main(context, name, description):

    client, config = context.client, context.config

    project_name = client.create_project(name, description)
    project_url = aquire_remote(project_name, client=client, config=config)
    return project_url
