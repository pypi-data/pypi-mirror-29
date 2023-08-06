from subprocess import call
import pytest

@pytest.mark.skip(reason="Cannot be run without cleanup, and the delete command isin't functional yet")
def test_comands_can_be_composed_together():

    #TODO: Make it run in the approperiate directory regardless of invocation path
    #TODO: Update the readme with caution info about the sponge package

    bashCommand = "python3 clusterone/clusterone_cli.py create project a26 | sponge | tail -n 1 | python3 clusterone/clusterone_cli.py ln project"
    exit_code = call(bashCommand, shell=True)

    print("Be sure to have install `sponge` package")
    assert exit_code is 0

