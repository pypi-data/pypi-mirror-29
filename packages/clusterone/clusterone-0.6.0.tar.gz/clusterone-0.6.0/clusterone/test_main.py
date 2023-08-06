from subprocess import call

import pytest

from clusterone.utils import get_current_version


def test_tport_throws_but_pytest_does_not():
    #TODO: Make it run in the approperiate directory regardless of invocation path
    bashCommand = "python3 clusterone/clusterone_cli.py"
    exit_code = call(bashCommand, shell=True)

    print("Please visit README-> Development -> Additional naming conventions and note about folder structure -> Caution. This may be a potential solution to your problem. Keep on Clusteronein'!")
    assert exit_code is 0

def test_clusterone_projects_dependency_met():
    """
    Clusterone project depend on 2 functions from the client.
    Thoose function should be properly exposed until further notice
    """

    try:
        from clusterone import get_data_path, get_logs_path
    except ImportError as exception:
        pytest.fail("Clusterone should propperly expose thoose 2 functions")

def test_local_dev():
    """
    Prevents pushing to production with LOCAL_DEV enabled
    This happened in the past
    """

    from clusterone.clusterone_client import LOCAL_DEV
    print("Please visit Readme -> Development -> Caution -> Developing with LOCAL_DEV for more details")
    assert not LOCAL_DEV


def test_version():
    """
    Makes sure that the version set in repo is >= the latest pypi version
    """

    #TODO: Rename this to something more approperaite and move this to utilities
    assert get_current_version()

