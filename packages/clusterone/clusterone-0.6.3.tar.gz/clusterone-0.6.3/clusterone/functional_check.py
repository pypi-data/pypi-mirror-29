"""
This is a functional test for the basic CLI commands
Is is named "check" insted of "test" to avoid being collected by pytest

This is not env agnostic - it has hardcoded my home directory, etc. Will refactor when plugging into CI

CAUTION: it is to be called from CLI folder
"""

#TODO: Change prints to logger
#TODO: Add visual progress indicators on waiting

import subprocess
import random
import string
from subprocess import run, PIPE
from time import sleep
import requests
import json

from clusterone import ClusteroneClient

INVOCATION_PREFIX = "python3 clusterone/clusterone_cli.py"

def just(command):
    just_command = "{} {}".format(INVOCATION_PREFIX, command)
    return just_command

def call(command, asserted=True):
    command_list = command.split()
    result = run(command_list, stdout=PIPE)

    if asserted:
        exit_code = result.returncode
        assert exit_code == 0

    return result.stdout

def get_outputs(token):
    """
    This one should be move to the CLI
    """

    job_data = str(call(just("get jobs")), 'utf-8')
    job_data_parsed = job_data.split()

    job_id = job_data_parsed[job_data_parsed.index("None/clusterone-test-bob") + 2]

    url = "https://clusterone.com/api/jobs/{}/files/".format(job_id)
    header = {"Authorization": "JWT {}".format(token)}
    response = requests.request("GET", url, headers=header)
    output_files = json.loads(response.text)[0]['contents']

    return output_files

def main():

    salt = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    username = "cluster-one-test-{}".format(salt)
    print("Generated username: {}".format(username))
    password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
    print("Generated pass: {}".format(password))

    exit_code = 0
    client = ClusteroneClient(username=username)

    try:
        call("rm -f /home/allgreed/.config/clusterone/config.json")

        response = client.client_action(['register', 'create'], params={
            'username': username,
            'email': '{}@example.com'.format(salt),
            'password': password,
        }, validate=True)
        print("Registration complete")

        login_output = call(just("login --username {} --password {}").format(username, password)).decode("utf-8")
        assert "Welcome" in login_output
        print("Login completed")

        token = json.loads((call("cat /home/allgreed/.config/clusterone/config.json")).decode("utf-8"))['token']
        print("Token aquired: {}...".format(token[0:10]))

        job_state = str(call(just("get jobs")), 'utf-8')
        assert "clusterone-test-bob" not in job_state
        print("Jobs clean")

        call("git clone -q https://github.com/clusterone/mnist")
        call(just("create project clusterone-test-mnist"))
        call(just("ln project -p clusterone-test-mnist -r ./mnist"))

        subprocess.call("cd mnist; git push -q clusterone", shell=True)
        print("Local and remote project clone completed")
        sleep(60)

        call(just("create job distributed --name clusterone-test-bob --project clusterone-test-mnist --module mnist"))
        sleep(5)
        job_state = str(call(just("get jobs")), 'utf-8')
        assert "clusterone-test-bob" in job_state
        print("Job successfully created")

        call(just("start job -p clusterone-test-mnist/clusterone-test-bob"))
        job_status = str(call(just("get job clusterone-test-mnist/clusterone-test-bob")), 'utf-8')
        assert "started" in job_status
        print("Job successfully started")

        current_outputs = get_outputs(token)
        assert current_outputs == []
        print("Outputs clean")

        sleep(60 * 10)

        current_outputs = get_outputs(token)
        assert len(current_outputs) > 0
        print("SUCCESS!")

    except AssertionError as exception:
        print("FAILED!")
        exit_code = 1

    print("Cleaning...")
    call(just("stop -p clusterone-test-mnist/clusterone-test-bob"), asserted=False)
    subprocess.call("echo 'y' | {} rm job clusterone-test-mnist/clusterone-test-bob ; sleep 1".format(INVOCATION_PREFIX), shell=True)
    subprocess.call("echo 'y' | {} rm project clusterone-test-mnist ; sleep 1".format(INVOCATION_PREFIX), shell=True)
    url = "https://clusterone.com/api/users/{}".format(username)
    header = {"Authorization": "JWT {}".format(token)}
    response = requests.request("DELETE", url, headers=header)
    call("rm -rf mnist", asserted=False)
    print("Cleaning done, exiting")
    exit(exit_code)

if __name__ == "__main__":
    main()
