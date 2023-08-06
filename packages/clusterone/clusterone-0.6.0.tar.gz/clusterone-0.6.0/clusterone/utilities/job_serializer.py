from uuid import UUID

from clusterone.utilities import path_to_job_id

def main(job_path_or_id, context=None):

    client = context.client

    job_path, job_id = None, None

    try:
        UUID(job_path_or_id)
        job_id = job_path_or_id
    except ValueError:
        job_path = job_path_or_id

    if job_path:
        job_id = path_to_job_id(job_path, context=context)

    job = client.get_job({"job_id": job_id})

    return job
