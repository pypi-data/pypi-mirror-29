from click.exceptions import BadParameter
from clusterone.client_exceptions import JobNameConflict, NonExistantJob

def path_to_project(project_path, context=None):
    """
    Coverts project_path [format. username/project] to ClusterOne project_id
    """

    client, config = context.client, context.config

    project_tokens = project_path.split('/')
    if len(project_tokens) == 1:
        project_tokens = [config.get("username")] + project_tokens

    if not len(project_tokens) == 2:
        raise BadParameter(param_hint="project path", message="Please provide a valid project path. The format is \"username/project\".")

    username, project_name = project_tokens
    project = client.get_project(project_name, username)
    return project

def path_to_job_id(job_path, context=None):
    """
    Coverts job_path [format. username/project/job] to ClusterOne job id
    """

    client, config = context.client, context.config

    path_tokens = job_path.split('/')

    if len(path_tokens) == 2:
        path_tokens = [config.get("username")] + path_tokens
    elif not len(path_tokens) == 3:
        raise BadParameter(param_hint="job-path", message="Please provide a valid job-path. The format is \"username/project/job-name\".")

    owner, project_name, job_name = path_tokens

    job_start_candidates = client.get_jobs({
        "repository": client.get_project(project_name, owner)['id'],
        "display_name": job_name
        })

    if len(job_start_candidates) is 0:
        raise NonExistantJob()

    if len(job_start_candidates) is not 1:
        candidate_ids = list(map(lambda job: job['job_id'], job_start_candidates))
        raise JobNameConflict(candidate_ids)

    job_id = job_start_candidates[0]['job_id']

    return job_id

def path_to_dataset(dataset_path, context=None):
    """
    Coverts dataset_path [format. username/dataset] to ClusterOne dataset_id
    """

    client, config = context.client, context.config

    dataset_tokens = dataset_path.split('/')
    if len(dataset_tokens) == 1:
        dataset_tokens = [config.get("username")] + dataset_tokens

    if not len(dataset_tokens) == 2:
        raise BadParameter(param_hint="dataset path", message="Please provide a valid dataset path. The format is \"username/dataset\".")

    username, dataset_name = dataset_tokens
    dataset = client.get_dataset(dataset_name, username)
    return dataset
