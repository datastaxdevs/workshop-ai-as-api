"""
    main.py
        main module of the API
"""

import pathlib
import datetime
import logging
from typing import List
from fastapi import FastAPI, Request, Depends
from fastapi.responses import StreamingResponse
from cassandra.cqlengine.management import sync_table

from api.config import getSettings
from api.schema import (SingleTextQuery, MultipleTextQuery)
from api.schema import (APIInfo, PredictionResult, CallerLogEntry)

from api.dbio import (formatCallerLogJSON, storeCallsToLog, cachePrediction,
                      readCachedPrediction, getThisHour)
from api.database.db import initSession
from api.database.models import (SpamCacheItem, SpamCallItem)


# mockup switch in case one has trouble getting the trained model and
# wants to play with the API nevertheless (see the .env parameters):
settings = getSettings()
if settings.mock_model_class:
    from api.MockSpamAIModel import MockSpamAIModel as AIModel
else:
    from api.AIModel import AIModel


apiDescription="""
Spam Classifier API

A sample API exposing a Keras text classifier model.
"""
tags_metadata = [
    {
        'name': 'classification',
        'description': 'Requests for text classifications.',
    },
    {
        'name': 'info',
        'description': 'Retrieving various types of information from the API.',
    },
]
app = FastAPI(
    title="Spam Classifier API",
    description=apiDescription,
    version="0.1",
    openapi_tags=tags_metadata,
)


# globally-accessible objects:
startTime = None
spamClassifier = None
DBSession = None


@app.on_event("startup")
def onStartup():
    """
    load/prepare/initialize all global variables for usage by the running API.
    """
    logging.basicConfig(level=logging.INFO)
    logging.info('     API Startup begins')
    global startTime
    global spamClassifier
    #
    startTime = datetime.datetime.now()
    settings = getSettings()
    #
    # location of the model data files
    logging.info('     Loading classifier model')
    API_BASE_DIR = pathlib.Path(__file__).resolve().parent
    MODEL_DIR = API_BASE_DIR.parent / settings.model_directory
    SPAM_HD_PATH = MODEL_DIR / 'spam_model.h5'
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
    logging.info('     DB initialization')
    DBSession = initSession()
    sync_table(SpamCacheItem)
    sync_table(SpamCallItem)
    logging.info('     API Startup completed.')


@app.get('/', response_model=APIInfo, tags=['info'])
def basic_info(request: Request):
    """
    Show some basic API configuration parameters,
    along with the identity of the caller as seen by the server.
    """
    settings = getSettings()
    # prepare to return the non-secret settings...
    info = {
        k: v
        for k, v in settings.dict().items()
        if k not in settings.secret_fields
    }
    # plus some more fields:
    info['started_at'] = startTime.strftime('%Y-%m-%d %H:%M:%S.%f')
    # if behind a reverse proxy, we must use X-Forwarded-For ...
    info['caller_id'] = request.client[0]
    # done.
    return APIInfo(**info)


@app.post('/prediction', response_model=PredictionResult, tags=['classification'])
def single_text_prediction(query: SingleTextQuery, request: Request):
    """
    Get the classification result for a single text.

    Uses cache when available, unless instructed not to do so.
    """
    settings = getSettings()
    cached = None if query.skip_cache else readCachedPrediction(settings.model_version, query.text, echoInput=query.echo_input)
    storeCallsToLog([query.text], request.client[0])
    if not cached:
        result = spamClassifier.predict([query.text], echoInput=query.echo_input)[0]
        cachePrediction(query.text, result)
        result['from_cache'] = False
        return PredictionResult(**result)
    else:
        cached['from_cache'] = True
        return PredictionResult(**cached)


@app.get('/prediction', response_model=PredictionResult, tags=['classification'])
def single_text_prediction_get(request: Request, query: SingleTextQuery = Depends()):
    """
    Get the classification result for a single text (through a GET request).

    Uses cache when available, unless instructed not to do so.
    """

    # We "recycle" the very same function attached to the POST endpoint
    # (this GET endpoint is there to exemplify a GET route with parameters, that's all.
    # Well, it also makes it for a more browser-friendly way of testing the API, I guess).
    return single_text_prediction(query, request)


@app.post('/predictions', response_model=List[PredictionResult], tags=['classification'])
def multiple_text_predictions(query: MultipleTextQuery, request: Request):
    """
    Get the classification result for a list of texts.

    Uses cache when available, unless instructed not to do so.

    _Internal notes:_

    care is taken to separate cached and noncached inputs, process
    only the noncached ones, and merge the full output back for returning.
    """

    """ NOTE: Ignoring reading from cache, this would simply be:
        results = spamClassifier.predict(query.texts, echoInput=query.echo_input)
        storeCallsToLog(query.texts, request.client[0])
        #
        for t, r in zip(query.texts, results):
            cachePrediction(t, r)
        #
        return results
    In the following we get a bit sophisticated and retrieve
    what we can from cache (doing the rest and re-merging at the end)
    (the assumption here is that predicting is much more expensive)
    """
    # what is in the cache?
    settings = getSettings()
    cachedResults = [
        None if query.skip_cache else readCachedPrediction(settings.model_version, text, echoInput=query.echo_input)
        for text in query.texts
    ]
    # what must be done?
    notCachedItems = [
        (i, t)
        for i, t in enumerate(query.texts)
        if cachedResults[i] is None
    ]
    if notCachedItems != []:
        indicesToDo, textsToDo = zip(*notCachedItems)
        resultsDone = spamClassifier.predict(textsToDo, echoInput=query.echo_input)
    else:
        indicesToDo, textsToDo = [], []
        resultsDone = []
    #
    # log everything and cache new items
    storeCallsToLog(query.texts, request.client[0])
    for t, r in zip(textsToDo, resultsDone):
        cachePrediction(t, r)
    #
    # merge the two and return
    results = [
        {**cr, **{'from_cache': True}} if cr is not None else cr
        for cr in cachedResults
    ]
    if indicesToDo != []:
        for i, newResult in zip(indicesToDo, resultsDone):
            results[i] = newResult
            results[i]['from_cache'] = False
    return [
        PredictionResult(**r)
        for r in results
    ]


@app.get('/recent_log', response_model=List[CallerLogEntry], tags=['info'])
def get_recent_calls_log(request: Request):
    """
    Get a list of all classification requests issued by the caller in the
    current hour.

    _Internal notes:_

    The response of this endpoint may potentially be a long list and we
    don't want to have it all in memory at once, so we stream the response
    as it is progressively fetched from the database.

    Note: we do not actually use pydantic conversion in creating
    the response since it is streamed, but still we want to annotate
    this endpoint (e.g. for the docs) with 'response_model' above.

    Note on how to pass a media type: see example at
    https://fastapi.tiangolo.com/advanced/custom-response/#using-streamingresponse-with-file-like-objects
    """
    caller_id = request.client[0]
    called_hour = getThisHour()
    #
    return StreamingResponse(
        formatCallerLogJSON(caller_id, called_hour),
        media_type='application/json',
    )
