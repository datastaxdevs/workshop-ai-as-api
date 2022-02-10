""" db.py """

import os
import pathlib
from dotenv import load_dotenv

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection


load_dotenv()

ASTRA_DB_KEYSPACE = os.environ['ASTRA_DB_KEYSPACE']
ASTRA_DB_CLIENT_SECRET = os.environ['ASTRA_DB_CLIENT_SECRET']
ASTRA_DB_CLIENT_ID = os.environ['ASTRA_DB_CLIENT_ID']
ASTRA_DB_BUNDLE_PATH = os.environ['ASTRA_DB_BUNDLE_PATH']
DB_MODULE_DIR = pathlib.Path(__file__).resolve().parent
CLUSTER_BUNDLE = str(DB_MODULE_DIR.parent.parent / ASTRA_DB_BUNDLE_PATH)


def getCluster():
    cloud_config= {
        'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    return Cluster(cloud=cloud_config, auth_provider=auth_provider)
    

def initSession():
    cluster = getCluster()
    session = cluster.connect()
    # once you do this, the session will return rows in dict format!
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
