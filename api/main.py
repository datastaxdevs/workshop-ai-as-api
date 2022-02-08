"""
    main.py
        main module of the API
"""

import pathlib
from fastapi import FastAPI

from api.AIModel import AIModel


app = FastAPI()

# location of the model data files
BASE_DIR = pathlib.Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / 'training' / 'trained_model'
SPAM_HD_PATH = MODEL_DIR / 'spam_model.hdf5'
SPAM_TOKENIZER_PATH = MODEL_DIR / 'spam_tokenizer.json'
SPAM_METADATA_PATH = MODEL_DIR / 'spam_metadata.json'


# spamClassifier = AIModel(
#     modelPath=SPAM_HD_PATH,
#     tokenizerPath=SPAM_TOKENIZER_PATH,
#     metadataPath=SPAM_METADATA_PATH,
# )
# print(str(spamClassifier))


@app.get('/')
def main_index():
    return {'a': 123, 'b': [1,2,{'x': 0.1}, True]}


