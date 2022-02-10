"""
    main.py
        main module of the API
"""

import pathlib
import datetime
from fastapi import FastAPI, Request
from cassandra.cqlengine.management import sync_table

from api.AIModel import AIModel
from api.config import getSettings
from api.schema import (SingleTextQuery, MultipleTextQuery)

from api.database.db import initSession
from api.database.models import (SMSCacheItem, SMSCallItem)

app = FastAPI()

# globally-accessible objects:
startTime = None
spamClassifier = None
DBSession = None


@app.on_event("startup")
def onStartup():
    global startTime
    global spamClassifier
    #
    startTime = datetime.datetime.now()
    settings = getSettings()
    #
    # location of the model data files
    API_BASE_DIR = pathlib.Path(__file__).resolve().parent
    MODEL_DIR = API_BASE_DIR.parent / settings.model_directory
    SPAM_HD_PATH = MODEL_DIR / 'spam_model.hdf5'
    SPAM_TOKENIZER_PATH = MODEL_DIR / 'spam_tokenizer.json'
    SPAM_METADATA_PATH = MODEL_DIR / 'spam_metadata.json'
    # actual loading of the classifier model
    spamClassifier = AIModel(
        modelPath=SPAM_HD_PATH,
        tokenizerPath=SPAM_TOKENIZER_PATH,
        metadataPath=SPAM_METADATA_PATH,
    )
    #
    # Database
    DBSession = initSession()
    sync_table(SMSCacheItem)
    sync_table(SMSCallItem)


@app.get('/')
def routeMain(request: Request):
    settings = getSettings()
    # prepare to return the non-secret settings...
    info = {
        k: v
        for k, v in settings.dict().items()
        if k not in settings.secret_fields
    }
    # plus some more fields:
    info['started_at'] = startTime.strftime('%Y-%m-%dT%H:%M:%S')
    # if behind a reverse proxy, we must use X-Forwarded-For ...
    info['caller_id'] = request.client[0]
    # done.
    return info


@app.post('/prediction')
def routePrediction(query: SingleTextQuery, request: Request):
    cached = None if query.skip_cache else readCachedPrediction(query.text)
    storeCallsToLog([query.text], request.client[0])
    if not cached:
        result = spamClassifier.predict([query.text])[0]
        cachePrediction(query.text, result)
        result['from_cache'] = False
        return result
    else:
        cached['from_cache'] = True
        return cached

@app.post('/predictions')
def routePredictions(query: MultipleTextQuery, request: Request):
    results = spamClassifier.predict(query.texts, echoInput=query.echo_input)
    storeCallsToLog(query.texts, request.client[0])
    #
    for t, r in zip(query.texts, results):
        cachePrediction(t, r)
    #
    return results


def cachePrediction(input, resultMap):
    cacheItem = SMSCacheItem.create(
        input=input,
        result=resultMap['top']['label'],
        confidence=resultMap['top']['value'],
        prediction_map=resultMap['prediction'],
    )


def readCachedPrediction(input):
    settings = getSettings()
    cacheItems = SMSCacheItem.filter(
        model_version=settings.model_version,
        input=input,
    )
    cacheItem = cacheItems.first()
    if cacheItem:
        return {
            'prediction': cacheItem.prediction_map,
            'top': {
                'label': cacheItem.result,
                'value': cacheItem.confidence,
            },
            'input': cacheItem.input,
        }
    else:
        return None


def storeCallsToLog(inputs, caller_id):
    called_hour = getThisHour()
    for input in inputs:
        SMSCallItem.create(
            caller_id=caller_id,
            called_hour=called_hour,
            input=input,
        )


def getThisHour(): return datetime.datetime(*datetime.datetime.now().timetuple()[:4])
