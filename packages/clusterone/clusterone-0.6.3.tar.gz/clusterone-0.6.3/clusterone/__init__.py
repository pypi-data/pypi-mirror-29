from clusterone import client_exceptions, messages

from .clusterone_client import ClusteroneClient

#TODO: Solve this better at higher level
# to satisfy clusterone projetcs' dependecy
from .clusterone_client import get_logs_path, get_data_path

ClusteroneException = client_exceptions.ClusteroneException
from .auth import authenticate

from clusterone.instances import CLIENT_INSTANCE as client

