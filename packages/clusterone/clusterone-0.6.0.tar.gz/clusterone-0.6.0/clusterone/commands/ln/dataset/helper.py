import git

from clusterone.client_exceptions import LocalRepositoryFailure, LinkAlreadyPresent

def main(context, repository_path, remote_url):

    try:
        git_repository = git.Repo(repository_path)
    except git.InvalidGitRepositoryError:
        raise LocalRepositoryFailure()

    try:
        git_repository.create_remote('clusterone', remote_url)
    #TODO: This exception may be too broad
    except git.exc.GitCommandError:
        raise LinkAlreadyPresent()

