import json
import os
import webbrowser
import logging
import click
import coreapi
import py
from coreapi import transports
from coreapi.auth import TokenAuthentication
from functools import lru_cache, wraps

from coreapi import Client
from coreapi import codecs

from raven import Client as RavenClient

from clusterone import client_exceptions
from clusterone.utilities import lazy_property, lazify

raven_client = RavenClient(
    'https://4935170ea1284f9e8c3a0c7552cdb5bd:ac7d8158d3b24bc4aa4ea4d628c616e0@sentry.tensorport.com/5'
)

MATRIX_URL = 'https://clusterone.com/matrix'

# API Endpoint
API_URL = 'https://clusterone.com/api/'

# API description
API_SCHEMA = 'https://clusterone.com/api/schema/'
API_TOKEN = 'https://clusterone.com/api/token/'

#TODO: Get rid of LOCAL_DEV while refactoring this - use something more generic - ex. API target
#Overwriting local dev value insted of variable, because it used across this module
LOCAL_DEV = True if os.environ.get('JUST_LOCAL', 'False').upper() == "TRUE" else False

if LOCAL_DEV:
    API_SCHEMA = 'http://127.0.0.1:8000/api/schema/'
    API_URL = 'http://127.0.0.1:8000/api/'
    MATRIX_URL = 'http://127.0.0.1:8000/'


def get_data_path(dataset_name, local_root, local_repo, path):
    """
    Depending on the environment (clusterone cloud vs local) update path to data.
    Args:
        dataset_name: string, Clusterone dataset repository name, e.g. clusterone/mnist
        local_root: string, specifies the root directory for dataset.
              e.g. /home/username/datasets
        local_repo: string, specifies the repo name inside the root data path.
              e.g. mnist
        path: string, specifies the path inside the repository, (optional)
              e.g. train
    Returns:
        if code is running locally this function returns:
            local_root/local_repo/path
        if code runs on clusterone cloud this function returns:
            /data/dataset_name/path
    """
    #TODO: DO THIS PROPPERLY!!!!!!
    #environment = os.environ['CLUSTERONE_CLOUD']

    environment = os.environ.get('CLUSTERONE_CLOUD') or os.environ.get('TENSORPORT_CLOUD')
    environment = 'clusterone-cloud' if environment else "local"

    #TODO: Hotfixing TEN-819
    # Have no way of manually testing this
    # This should have a propper test case
    # Handling should be abstracted to a function - as it's the same here and in get_logs_path(root)
    # Need to show intent -> this is for platform indenpendence: converting Windows-style paths to UNIX-style paths. Both ways
    # Eg. /like/this/one <-> C:\like\this\one

    local_root = os.path.abspath(local_root)

    path = path.lstrip("/")  # preventing problems with user input

    if environment == 'local':
        return os.path.join(local_root, local_repo, path)
    elif environment == 'clusterone-cloud':
        return os.path.join('/data/', dataset_name, path)
    else:
        print("Environment is not valid. Assuming local.")
        return os.path.join(local_root, local_repo, path)


def get_logs_path(root):
    """
    Depending on the environment (clusterone cloud vs local) update path to logs.
    Args:
        root: string, specifies the directory for logs.
              e.g. /home/username/logs/mnist...
    Returns:
    """

    #TODO: See get_data_path() for more into, hotfixing TEN-819
    root = os.path.abspath(root)

    #TODO: DO THIS PROPPERLY!!!!!!
    #environment = os.environ['CLUSTERONE_CLOUD']

    environment = os.environ.get('CLUSTERONE_CLOUD') or os.environ.get('TENSORPORT_CLOUD')
    environment = 'clusterone-cloud' if environment else "local"

    if environment == 'local':
        return os.path.join(root)
    elif environment == 'clusterone-cloud':
        return os.path.join('/logs/')
    else:
        print("Environment is not valid. Assuming local.")
        return os.path.join(root)

class ClusteroneClient(object):
    """
    Clusterone API Client
    ^^^^^^^^^^^^^^^^^^^^^

    Clusterone Client (tport for short) is a simple Python module that is used to get most up_to_date API schema,
    and execute API calls.

    """
    username = ""
    git_token = ""
    api_schema = {}
    use_in_memory_schema = True


    #TODO: Test this!
    @property
    @lazify
    def framework_slugs(self) -> [str]:
        return [framework['slug'] for framework in self.get_frameworks()]


    #TODO: Test this!
    @property
    @lazify
    def instance_types_slugs(self) -> [str]:
        return [machine['slug'] for machine in self.get_instance_types() if machine['show_for_workers']]


    #TODO: Test this!
    @property
    @lazify
    def ps_type_slugs(self) -> [str]:
        return [machine['slug'] for machine in self.get_instance_types() if machine['show_for_ps']]


    def __init__(self, token="", username="", environment='', use_in_memory_schema=True, schema_json_path=None,
                 api_schema_url=API_SCHEMA, api_url=API_URL):

        self.api_url = api_url
        self.api_schema_url = api_schema_url
        self.environment = environment
        self.use_in_memory_schema = use_in_memory_schema

        self.token = token
        self.username = username

        if not use_in_memory_schema:
            if schema_json_path:
                self.document_path = schema_json_path
            else:
                self.document_path = py.path.local(
                    click.get_app_dir('clusterone')).join('schema.json')

        # Init CoreAPI Client
        self.transport = self.get_transport()
        self.decoders = [codecs.CoreJSONCodec(), codecs.JSONCodec(), codecs.DownloadCodec()]
        self.api_client = Client(
            transports=[self.transport], decoders=self.decoders)

        # Get Schema
        self.api_schema = self.download_schema()

        super(ClusteroneClient, self).__init__()

    def get_transport(self):
        """
        Creates HTTPTransport with auth header information
        :param token:
        :return: HTTPTransport
        """
        if self.token:
            if LOCAL_DEV:
                print('Using Token: %s************' % self.token[:4])
            auth = TokenAuthentication(token=self.token, scheme='JWT')
            return transports.HTTPTransport(headers={'Authorization': '%s %s' % ('JWT', self.token)})
        else:
            return transports.HTTPTransport()

    def get_schema_json(self):
        """
        Reads API SCHEMA from memory or JSON document stored in Clusterone local path
        :return:
        """
        if self.api_schema and self.use_in_memory_schema:
            return self.api_schema

        else:
            if not self.document_path.ensure():
                print('Cannot read from schema JSON, please relogin')
                return None
            store = self.document_path.open('rb')
            content = store.read()
            store.close()
            codec = codecs.CoreJSONCodec()
            return codec.load(content)

    def set_schema(self, document):
        """
        Creates Schema JSON in Clusterone local path
        :param document:
        :return:
        """
        codec = codecs.CoreJSONCodec()
        content = codec.dump(document)
        store = self.document_path.open('wb')
        store.write(content)
        store.close()
        print('Saved schema JSON')

    def download_schema(self):
        """
        Uses Basic Auth to get Schema JSON and save it
        :param document:
        :return:
        """
        if LOCAL_DEV:
            print('Loading Clusterone API Schema: %s' % API_SCHEMA)
        try:
            api_schema = self.api_client.get(API_SCHEMA)

            if self.use_in_memory_schema:
                self.api_schema = api_schema
            else:
                self.set_schema(api_schema)

            return api_schema
        except Exception as e:
            print('Cannot download API Schema: %s' % str(e))
            raise

    def client_action(self, actions_keys, params=None, validate=False):
        """
        Wrapper for Client.action that set decoders, transports and schema document
        :param token:
        :param actions_keys:
        :param schema:
        :param params:
        :param validate:
        :return:
        """
        try:
            data = self.api_client.action(
                self.api_schema, actions_keys, params=params, validate=validate)
            if LOCAL_DEV:
                print("Success: %s" % data)
            return data
        except coreapi.exceptions.LinkLookupError as exc:
            raise client_exceptions.LoginNotSupplied()
        except coreapi.exceptions.ErrorMessage as exc:
            if 'non_field_errors' in exc.error and exc.error['non_field_errors']:
                if (exc.error.title == '400 Bad Request') and exc.error._data['non_field_errors']._data[0] == 'Unable to log in with provided credentials.':
                    print("Try again.")
            else:
                if "400" in exc.error._title:
                    if "Enter a valid \"slug\" consisting of letters, numbers, underscores or hyphens." in exc.error._data["display_name"][0]:
                        raise client_exceptions.InvalidProjectName()
                    elif "Project name is not unique" in exc.error._data["display_name"][0]:
                        raise client_exceptions.DuplicateProjectName()
                    else:
                        print("API Error: %s" % exc.error)
                if "403" in exc.error._title and 'You do not have enough resources to start' in exc.error._data['detail']:
                    raise client_exceptions.InsufficientResources()
                if "500" in exc.error._title:
                    raise client_exceptions.InternalServiceError()

                else:
                    if "404" not in exc.error._title:
                        print("API Error: %s" % exc.error)
                    else:
                        raise exc

            #TODO: Is this propper place for reporoting exceptions
            #raven_client.captureException()
            return

    # -----------------------------
    # Authentication
    def api_login(self, username, password):
        try:
            if LOCAL_DEV:
                print('Loading Initial Clusterone API Schema: %s' %
                      self.api_schema_url)

            response = self.client_action(actions_keys=['token', 'create'], params={
                'username': username,
                'password': password,
            }, validate=True)
            # Reset Token and transport headers
            if not response:
                message = "Couldn't login, please check your username and password"
                return None, message

            self.token = api_token = response.get('token')
            self.transport = self.get_transport()
            self.api_client = Client(
                transports=[self.transport], decoders=self.decoders)
            self.api_schema = self.download_schema()

            # Verify
            profile_response = self.client_action(actions_keys=['profile', 'list'], params={
            }, validate=True)

            self.git_token = git_token = profile_response.get('git_token')
            self.username = username

            user = {'api_token': api_token,
                    'git_token': git_token,
                    'username': username,
                    'first_name': profile_response.get('first_name', username),
                    'last_login': profile_response.get('last_login', 'unknown')}
            return user, "Login successful"
        except Exception as e:
            message = "Authentication was successful, some other error occurred when downloading API Schema: %s" % str(
                e)
            #raven_client.captureException()
            return None, message

    def open_dashboard(self):
        """
        Opens Matrix in a browser
        :return:
        """
        try:
            browser = webbrowser.get("chrome")
            browser.open(MATRIX_URL)
        except:
            print("If you're not using Chrome, we recommend it for best performance.")
            webbrowser.open_new(MATRIX_URL)

    def create_dataset(self, display_name, description='Clusterone Dataset'):
        """
        Creates a dataset thru API
        :return: Dataset Unique Name
        """
        try:
            response = self.client_action(['datasets', 'owned', 'create'], params={
                'display_name': display_name,
                'description': description,
                'parameters': {}
            }, validate=True)

            return response.get('name')

        except client_exceptions.InvalidProjectName as exception:
            raise client_exceptions.InvalidDatasetName()
        except client_exceptions.DuplicateProjectName as exception:
            raise client_exceptions.DuplicateDatasetName()
        except Exception as e:
            print("Couldn't create a dataset thru API, error: %s" % str(e))
            return False

    def create_project(self, display_name, description='Clusterone Project'):
        """
        Creates a project thru API
        :return: Project Unique Name
        """
        try:
            response = self.client_action(['projects', 'owned', 'create'], params={
                'display_name': display_name,
                'description': description,
                'parameters': {}
            }, validate=True)

            return response.get('name')

        #TODO: Somehow redo this -> catching all exceptions bloats sentry and causes further development problems
        #TODO: If this is the final Exception catcher then it shall: log to Sentry then kill the process
        except Exception as exception:
                if isinstance(exception, client_exceptions.InvalidProjectName):
                    raise client_exceptions.InvalidProjectName()
                elif isinstance(exception, client_exceptions.DuplicateProjectName):
                    raise client_exceptions.DuplicateProjectName()
                else:
                    print("Couldn't create a project thru API, error: %s" % str(exception))
                    #raven_client.captureException()
                    return False

    def get_project(self, name, username=None):
        """
        Get Project from Repo
        :return: Project JSON
        """
        try:
            response = self.client_action(['projects', 'details', 'read'], params={
                'name': name,
                'username': username
            }, validate=False)
            return response
        except Exception as e:
            #TODO: This is crap, redo this ASAP
            if isinstance(e, client_exceptions.LoginNotSupplied):
                raise e
            if "404" in e.error._title:
                raise client_exceptions.NonExistantProject()
            else:
                print("Couldn't fetch a project, error: %s" % str(e))
                #raven_client.captureException()
                return False

    def get_projects(self, owner=None, writer=None, reader=None):
        """
        Get List of Owned Projects
        :return: List of Project JSONs
        """
        if owner:
            action = 'owned'
        elif writer:
            action = 'writable'
        elif reader:
            action = 'readable'
        else:
            action = 'readable'

        try:
            response = self.client_action(
                ['projects', action, 'list'], params={}, validate=False)
            return response
        except Exception as e:
            print("Couldn't fetch a project, error: %s" % str(e))
            #raven_client.captureException()
            return False

    def delete_project(self, name, username):
        """
        Deletes a Project
        :return:
        """
        try:
            response = self.client_action(['projects', 'details', 'delete'], params={
                'name': name,
                'username': username
            }, validate=True)
            return response
        except Exception as e:
            print("Couldn't delete a project, error: %s" % str(e))
            #raven_client.captureException()
            return False

    def delete_dataset(self, name, username):
        """
        Deletes a dataset
        :return:
        """
        # TODO: fix this
        try:
            response = self.client_action(['datasets', 'details', 'delete'], params={
                'name': name,
                'username': username
            }, validate=True)
            return response
        except Exception as e:
            print("Couldn't delete a dataset, error: %s" % str(e))
            #raven_client.captureException()
            return False

    def get_dataset(self, name, username):
        """
        Get Datasets from Repo
        :return: Project JSON
        """
        try:
            response = self.client_action(['datasets', 'details', 'read'], params={
                'name': name,
                'username': username
            }, validate=False)
            return response
        except Exception as e:
            if "404" in e.error._title:
                raise client_exceptions.NonExistantDataset()
            else:
                print("Couldn't fetch a dataset, error: %s" % str(e))
                #raven_client.captureException()
                return False

    def get_datasets(self, owner=None, reader=None, writer=None):
        """
        Get List of Owned Datasets
        :return: List of Project JSONs
        """
        # TODO: add various ownership levels
        try:
            if owner is not None:
                response = self.client_action(['datasets', 'owned', 'list'], params={
                }, validate=False)
            else:
                response = self.client_action(['datasets', 'list'], params={
                }, validate=False)
            return response
        except Exception as e:
            print("Couldn't fetch a datasets, error: %s" % str(e))
            #raven_client.captureException()
            return False

    def get_events(self):
        """
        Get List of user related events
        :return: List of Jobs JSONs
        """
        # TODO: add various ownership levels
        try:
            response = self.client_action(
                ['events', 'list'], params={}, validate=False)
            return response
        except Exception as e:
            print("Couldn't fetch a events, error: %s" % str(e))
            #raven_client.captureException()
            return False

    def create_event(self, job_id, event_type, event_level=20, event_content=None):
        """
        Create Event
        :return:
        """
        try:
            response = self.client_action(['events', 'create'], params={
                'job': job_id,
                'event_type': event_type,
                'event_level': event_level,
                'event_content': {}
            }, validate=True)
            return response
        except Exception as e:
            print("Couldn't create event, error: %s" % str(e))
            #raven_client.captureException()
            return False

    @lru_cache(maxsize=1)
    def get_instance_types(self, params=None):
        """
        Get List of Instance Types
        :return: List of AWS Instance Types JSONs
        """
        try:
            response = self.client_action(
                ['instance-types', 'list'], params=params, validate=False)
            return response.get('results')
        except Exception as e:
            #raven_client.captureException()
            print("Couldn't fetch list of instances, error: %s" % str(e))

    def get_frameworks(self, params=None):
        #TODO: What is a list with slug, name, number? A dict? A list of lists?
        """
        Get List of ML frameworks
        :return: List of frameworks with slug, name and number
        """
        try:
            response = self.client_action(
                ['frameworks', 'list'], params=params, validate=False)
            return response.get('results')
        #TODO: WHY LEO, WHY?!!!!!!!
        except Exception as e:
            #raven_client.captureException()
            print("Couldn't fetch list of frameworks, error: %s" % str(e))

    def get_tf_versions(self, params=None):
        """
        DEPRACATED - use get_frameworks instead
        :return: List of frameworks with slug, name and number
        """
        return self.get_frameworks(params)

    def get_jobs(self, params=None):
        """
        Get List of User Running Jobs
        :return: List of Jobs JSONs
        """
        try:
            if params:
                params.update({'limit': 200})
            else:
                params = {'limit': 200}
            response = self.client_action(
                ['jobs', 'list'], params=params, validate=False)
            return response
        except Exception as e:
            print("Couldn't fetch a project, error: %s" % str(e))
            #raven_client.captureException()
            return False

    def get_job(self, params=None):
        """
        Get a single Job
        :return: Job JSONs
        """
        try:
            response = self.client_action(
                ['jobs', 'read'], params=params, validate=False)
            return response
        except Exception as e:
            print("Couldn't fetch a job, error: %s" % str(e))
            #raven_client.captureException()
            return False

    def create_job(self, name, description=None, parameters=None):
        """
        create a Job, require repository ID
        :return:
        """
        project_id = parameters['code']
        datasets_set = parameters['datasets_set']
        git_hash = parameters['code_commit']

        try:
            response = self.client_action(['jobs', 'create'], params={
                'repository': project_id,
                'display_name': name,
                'description': description,
                'parameters': parameters,
                'datasets_set': datasets_set,
                'git_commit_hash': git_hash
            }, validate=True)

            return response
        except Exception as error:
            print("Couldn't create a job, error: %s" % str(error))
            #raven_client.captureException()
            raise

    def delete_job(self, job_id):
        """
        Deletes a Job
        :return:
        """
        response = self.client_action(['jobs', 'delete'], params={
            'job_id': job_id,
        }, validate=True)
        return response

    def start_job(self, job_id):
        """
        Starts a Job
        :return:
        """
        try:
            response = self.client_action(['jobs', 'partial_update'], params={
                'job_id': job_id,
                'status': 'started'
            }, validate=True)
            return response
        except client_exceptions.InsufficientResources as exception:
            raise exception
        except Exception as exception:
            if "404" in exception.error._title:
                raise client_exceptions._NonExistantJob()

            print("Couldn't start a job, error: %s" % str(exception))
            #raven_client.captureException()
            return False

    def stop_job(self, job_id):
        """
        Stops a Job
        :return:
        """
        try:
            response = self.client_action(['jobs', 'partial_update'], params={
                'job_id': job_id,
                'status': 'stopped'
            }, validate=True)
            return response
        except Exception as e:
            print("Couldn't stop a job, error: %s" % str(e))
            #raven_client.captureException()
            return False

    def get_file_list(self, job_id):
        """
        Get list of files/outputs
        :return:
        """
        try:
            response = self.client_action(['jobs', 'files', 'list'], params={
                'job_id': job_id,
            }, validate=True)
            if len(response) > 0:
                file_list = response[0]['contents']
                return file_list
            else:
                return []
        except Exception as e:
            print("Couldn't find a job or files, error: %s" % str(e))
            #raven_client.captureException()
            return False

    def download_file(self, job_id, filename):
        """
        Download file for Job
        :return:
        """
        try:

            download = self.client_action(['jobs', 'file', 'read'], params={
                'job_id': job_id,
                'filename': filename,
            }, validate=False)
            return download
        except Exception as e:
            print("Download file %s error: %s" % (filename, str(e)))
            #raven_client.captureException()
            return False
