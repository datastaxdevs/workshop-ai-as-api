""" paginationTest.py """

import datetime
from cassandra.cqlengine.functions import Token

from api.database.db import initSession
from api.database.models import (SpamCacheItem, SpamCallItem)


INPUT = 'WIN'

if __name__ == '__main__':

    initSession()

    # sanity check
    cacheItem = SpamCacheItem.filter(
        model_version='v1',
        input=INPUT,
    ).first()
    print('%s => %s\n' % (INPUT, cacheItem.result))

    # pagination is handled by the object mappers, we just browse results
    query = SpamCallItem.objects().filter(
        caller_id='test',
        called_hour=datetime.datetime(2022, 2, 10, 11),
    )
    for i, item in enumerate(query):
        print(i, item.input)
