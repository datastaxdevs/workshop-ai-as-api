""" db.py """

import os
# import pathlib
from dotenv import load_dotenv

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection


load_dotenv()

ASTRA_DB_KEYSPACE = os.environ['ASTRA_DB_KEYSPACE']
ASTRA_DB_SECURE_BUNDLE_PATH = os.environ['ASTRA_DB_SECURE_BUNDLE_PATH']
ASTRA_DB_APPLICATION_TOKEN = os.environ['ASTRA_DB_APPLICATION_TOKEN']


# ASTRA_DB_CLIENT_SECRET = os.environ['ASTRA_DB_CLIENT_SECRET']
# ASTRA_DB_CLIENT_ID = os.environ['ASTRA_DB_CLIENT_ID']
# ASTRA_DB_BUNDLE_PATH = os.environ['ASTRA_DB_BUNDLE_PATH']
# DB_MODULE_DIR = pathlib.Path(__file__).resolve().parent
# CLUSTER_BUNDLE = str(DB_MODULE_DIR.parent.parent / ASTRA_DB_BUNDLE_PATH)


def getCluster():
    """
    Create a Cluster instance to connect to Astra DB.
    Uses the secure-connect-bundle and the connection secrets.
    """
    cloud_config= {
        'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
    }
    auth_provider = PlainTextAuthProvider('token', ASTRA_DB_APPLICATION_TOKEN)
    return Cluster(cloud=cloud_config, auth_provider=auth_provider)
    

def initSession():
    """
    Create the DB session and return it to the caller.
    Most important, the session is also set as default and made available
    to the object mapper through global settings. I.e., no need to actually
    do anything with the return value of this function.
    """
    cluster = getCluster()
    session = cluster.connect()
    # Remember: once you do this, the session will return rows in dict format
    # for any query (i.e. not only those within the object mapper).
    connection.register_connection('my-astra-session', session=session)
    connection.set_default_connection('my-astra-session')
    return connection


if __name__ == '__main__':
    initSession()
    row = connection.execute('SELECT release_version FROM system.local').one()
    if row:
        print(row['release_version'])
    else:
        print('An error occurred.')
