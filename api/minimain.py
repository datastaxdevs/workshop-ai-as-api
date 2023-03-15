"""
    minimain.py
        minimal version of the API
"""

import pathlib
from fastapi import FastAPI

from api.config import getSettings
from api.AIModel import AIModel
from api.schema import SingleTextQuery, MultipleTextQuery


# mockup switch in case one has trouble getting the trained model and
# wants to play with the API nevertheless (see the .env parameters):
settings = getSettings()
if settings.mock_model_class:
    from api.MockSpamAIModel import MockSpamAIModel as AIModel
else:
    from api.AIModel import AIModel


miniapp = FastAPI()


# globally-accessible objects:
spamClassifier = None

@miniapp.on_event("startup")
def onStartup():
    global spamClassifier
    #
    settings = getSettings()
    #
    # location of the model data files
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


@miniapp.get('/')
def basic_info():
    settings = getSettings()
    # prepare to return the non-secret settings...
    info = {
        k: v
        for k, v in settings.dict().items()
        if k not in settings.secret_fields
    }
    # done.
    return info


@miniapp.post('/prediction')
def single_text_prediction(query: SingleTextQuery):
    result = spamClassifier.predict([query.text])[0]
    return result


@miniapp.post('/predictions')
def multiple_text_predictions(query: MultipleTextQuery):
    results = spamClassifier.predict(query.texts)
    return results
