from gettext import gettext as _

class ClusteroneException(Exception):
    def __init__(self):
        super(ClusteroneException, self).__init__()
        self.exit_code = 1

class InvalidProjectName(ClusteroneException):
    def __str__(self):
        return "Your project name is invalid, please be sure to only use letters, digits, hiphens and underscores"

class InvalidDatasetName(ClusteroneException):
    def __str__(self):
        return "Your dataset name is invalid, please be sure to only use letters, digits, hiphens and underscores"

class DuplicateProjectName(ClusteroneException):
    def __str__(self):
        return "Duplicate project name. Project names must be unique"

class DuplicateDatasetName(ClusteroneException):
    def __str__(self):
        return "Duplicate dataset name. Dataset names must be unique"

class LocalRepositoryFailure(ClusteroneException):
    def __str__(self):
        return "Couldn't find a git repository. Please run this command in a valid repository or provide a valid repo-path."

class RemoteAquisitionFailure(ClusteroneException):
    def __str__(self):
        return "Failed to get git remote. Please contact Clusterone for support."

class LinkAlreadyPresent(ClusteroneException):
    def __str__(self):
        return "Cannot link. This repository already has a clusterone remote."

class NonExistantProject(ClusteroneException):
    def __str__(self):
        return "Cannot resolve name to a project. Are you sure that such a project exists? If so consider checking project owner and your permissions."

class NonExistantDataset(ClusteroneException):
    def __str__(self):
        return "Cannot resolve name to a dataset. Are you sure that such a dataset exists? If so consider checking dataset owner and your permissions."

class JobNameConflict(ClusteroneException):
    def __init__(self, possible_ids):

        super(JobNameConflict, self).__init__()
        self.ids = possible_ids

    def __str__(self):
        return "{}{}{}".format(
            "Job name resolves to multiple ids:\n",
            "".join(["{}\n".format(id) for id in self.ids]),
            "Cannot proceed. Please rerun this command with one of the id's above.")

class _NonExistantJob(ClusteroneException):
    def __str__(self):
        return "There is no job with such id. Are you sure that such a job exists?"

class NonExistantJob(ClusteroneException):
    def __str__(self):
        return "Cannot resolve name to a job. Are you sure that such a job exists?"

class NoProjectCommits(ClusteroneException):
    def __str__(self):
        return "This project has no commits, cannot proceed."

class FailedCommitReference(ClusteroneException):
    def __str__(self):
        return "Cannot find commit of that hash. Are you sure that such a commit exists?"

#TODO: Is this the most approperiate? See usage in tp_client
class LoginNotSupplied(ClusteroneException):
    def __str__(self):
        return "Action not authorized. Please log in or check your token."

class InternalServiceError(ClusteroneException):
    def __str__(self):
        return "Something went terribly wrong on our side, please contact us for immidiete support."

class RunningJobRemoveAttempt(ClusteroneException):
    def __str__(self):
        return "This job is currently running."

class BussyProjectRemoveAttempt(ClusteroneException):
    def __str__(self):
        return "This project has currently running jobs."

class InsufficientResources(ClusteroneException):
    def __str__(self):
        return "Your exceeding you plan limit or do not have enough credits to proceed."

class BussyDatasetRemoveAttempt(ClusteroneException):
    def __str__(self):
        return "This dataset is currently in use by a running job. Removing it may cause the job to fail."
