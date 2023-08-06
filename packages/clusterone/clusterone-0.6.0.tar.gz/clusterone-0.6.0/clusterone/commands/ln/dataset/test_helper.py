import pytest
import git

from clusterone.client_exceptions import LocalRepositoryFailure, LinkAlreadyPresent
from . import helper
from .helper import main


def test_git_repo_check(mocker):
    helper.git.Repo = mocker.Mock()

    main(None, "/some/path/to/repo", "git link")

    helper.git.Repo.assert_called_with("/some/path/to/repo")

def test_git_repo_rethrow(mocker):
    helper.git.Repo = mocker.Mock()
    helper.git.Repo.side_effect = git.InvalidGitRepositoryError()

    with pytest.raises(LocalRepositoryFailure):
        main(None, "/some/path/to/repo", "git link")

def test_link(mocker):
    helper.git.Repo = mocker.Mock()
    instance_mock = mocker.Mock()
    helper.git.Repo.return_value = instance_mock

    main(None, "/some/path/to/repo", "git link")

    instance_mock.create_remote.assert_called_with("clusterone", "git link")

def test_link_failure(mocker):
    helper.git.Repo = mocker.Mock()
    instance_mock = mocker.Mock()
    instance_mock.create_remote.side_effect = git.exc.GitCommandError("command", "status")
    helper.git.Repo.return_value = instance_mock

    with pytest.raises(LinkAlreadyPresent):
        main(None, "/some/path/to/repo", "git link")

