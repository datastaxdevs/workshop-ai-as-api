"""
    main.py
        main module of the API
"""

import pathlib
import datetime
from fastapi import FastAPI

from api.AIModel import AIModel
from api.config import getSettings
from api.schema import (SingleTextQuery, MultipleTextQuery)


app = FastAPI()

# globally-accessible objects:
startTime = None
spamClassifier = None

@app.on_event("startup")
def onStartup():
    global startTime
    global spamClassifier
    #
    startTime = datetime.datetime.now()
    settings = getSettings()
    #
    # location of the model data files
    BASE_DIR = pathlib.Path(__file__).resolve().parent
    MODEL_DIR = BASE_DIR.parent / settings.model_directory
    SPAM_HD_PATH = MODEL_DIR / 'spam_model.hdf5'
    SPAM_TOKENIZER_PATH = MODEL_DIR / 'spam_tokenizer.json'
    SPAM_METADATA_PATH = MODEL_DIR / 'spam_metadata.json'
    # actual loading of the classifier model
    spamClassifier = AIModel(
        modelPath=SPAM_HD_PATH,
        tokenizerPath=SPAM_TOKENIZER_PATH,
        metadataPath=SPAM_METADATA_PATH,
    )


@app.get('/')
def routeMain():
    settings = getSettings()
    # prepare to return all settings...
    info = {k: v for k, v in settings.dict().items()}
    # plus more fields:
    info['started_at'] = startTime.strftime('%Y-%m-%dT%H:%M:%S')
    # done.
    return info


@app.post('/prediction')
def routePrediction(query: SingleTextQuery):
    result = spamClassifier.predict([query.text])[0]
    return result


@app.post('/predictions')
def routePredictions(query: MultipleTextQuery):
    results = spamClassifier.predict(query.texts, echoInput=query.echo_input)
    return results
