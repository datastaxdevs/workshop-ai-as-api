""" models.py """

import os
import uuid
from dotenv import load_dotenv
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


load_dotenv()

ASTRA_DB_KEYSPACE = os.environ['ASTRA_DB_KEYSPACE']
MODEL_VERSION = os.environ['MODEL_VERSION']


class SpamCacheItem(Model):
    __table_name__ = 'spam_cache_items'
    __keyspace__ = ASTRA_DB_KEYSPACE
    __connection__ = 'my-astra-session'
    model_version = columns.Text(primary_key=True, partition_key=True, default=MODEL_VERSION)
    input = columns.Text(primary_key=True, partition_key=True)
    stored_at = columns.TimeUUID(default=uuid.uuid1)
    result = columns.Text()
    confidence = columns.Float()
    prediction_map = columns.Map(columns.Text, columns.Float)


class SpamCallItem(Model):
    __table_name__ = 'spam_calls_per_caller'
    __keyspace__ = ASTRA_DB_KEYSPACE
    __connection__ = 'my-astra-session'
    caller_id = columns.Text(primary_key=True, partition_key=True)
    called_hour = columns.DateTime(primary_key=True, partition_key=True)
    called_at = columns.TimeUUID(primary_key=True, default=uuid.uuid1, clustering_order='ASC')
    input = columns.Text()
