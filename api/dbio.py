"""
    dbio.py
        utilities for database I/O
"""

import json
import datetime
from cassandra.util import datetime_from_uuid1

from api.database.models import (SpamCacheItem, SpamCallItem)


DB_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


def formatCallerLogJSON(caller_id, called_hour):
    """
    Takes care of making the caller log into a stream of strings
    forming, overall, a valid JSON. Tricky are the commas.
    """
    isFirst = True
    yield '['
    for index, item in enumerate(readCallerLog(caller_id, called_hour)):
        yield '%s%s' % (
            '' if isFirst else ',',
            json.dumps({
                'index': index,
                'input': item.input,
                'called_at': datetime_from_uuid1(item.called_at).strftime(DB_DATE_FORMAT),
            }),
        )
        isFirst = False
    yield ']'


# utility function to get the whole hour, used as column in the call-log table
def getThisHour(): return datetime.datetime(*datetime.datetime.now().timetuple()[:4])


def storeCallsToLog(inputs, caller_id):
    """
    Store a call-log entry to the database.
    """
    called_hour = getThisHour()
    for input in inputs:
        SpamCallItem.create(
            caller_id=caller_id,
            called_hour=called_hour,
            input=input,
        )


def readCallerLog(caller_id, called_hour):
    """
    Query the database to get all caller-log entries
    for a given caller and hour chunk, and return them as a generator.

    Pagination is handled automatically by the Cassandra drivers.
    """
    query = SpamCallItem.objects().filter(
        caller_id=caller_id,
        called_hour=called_hour,
    )
    for item in query:
        yield item


def cachePrediction(input, resultMap):
    """
    Store a cached-text entry to the database.
    """
    cacheItem = SpamCacheItem.create(
        input=input,
        result=resultMap['top']['label'],
        confidence=resultMap['top']['value'],
        prediction_map=resultMap['prediction'],
    )


def readCachedPrediction(modelVersion, input, echoInput=False):
    """
    Try to retrieve a cached-text entry from the database.
    Return None if nothing is found.

    Note that this explicitly needs the model version
    to run the correct select (through the object mapper)
    to the database.
    """
    cacheItems = SpamCacheItem.filter(
        model_version=modelVersion,
        input=input,
    )
    cacheItem = cacheItems.first()
    if cacheItem:
        return {
            **{
                'prediction': cacheItem.prediction_map,
                'top': {
                    'label': cacheItem.result,
                    'value': cacheItem.confidence,
                },
            },
            **({'input': cacheItem.input} if echoInput else {}),
        }
    else:
        return None
