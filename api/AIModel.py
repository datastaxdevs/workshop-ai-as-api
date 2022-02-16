"""
    AIModel.py
        a class to wrap the a text classifier: the model and its usage.
"""

import json
from operator import itemgetter
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences


@dataclass
class AIModel:
    modelPath: Path
    tokenizerPath: Optional[Path] = None
    metadataPath: Optional[Path] = None

    model = None
    tokenizer = None
    metadata = None

    def __post_init__(self):
        if self.modelPath.exists():
            self.model = load_model(self.modelPath) 
        else:
            raise ValueError('Could not load model data')
        #
        if self.tokenizerPath and self.tokenizerPath.exists():
            tokenizerText = self.tokenizerPath.read_text()
            self.tokenizer = tokenizer_from_json(tokenizerText)
        else:
            raise ValueError('Could not load tokenizer data')
        #
        if self.metadataPath and self.metadataPath.exists():
            self.metadata = json.loads(self.metadataPath.read_text())
        else:
            raise ValueError('Could not load metadata')


    def getPaddedSequencesFromTexts(self, texts: List[str]):
        """
        Convert a list of texts into the corresponding list
        of (zero-left-padded) integer lists using the tokenizer.
        """
        sequences = self.tokenizer.texts_to_sequences(texts)
        maxSeqLength = self.metadata['max_seq_length']
        padded = pad_sequences(sequences, maxlen=maxSeqLength)
        return padded


    def getLabelName(self, labelIndex):
        """
        Convert a numeric index to the corresponding label text
        for a prediction result.
        """
        return self.metadata['label_legend_inverted'][str(labelIndex)]


    def getTopPrediction(self, predictionDict):
        """
        Utility method to extract the top prediction, i.e. that with
        the highest accuracy ("the category the input belongs to").
        """
        if len(predictionDict) == 0:
            return None
        else:
            topK, topV = sorted(
                predictionDict.items(),
                key=itemgetter(1),
                reverse=True,
            )[0]
            return {
                'label': topK,
                'value': topV,
            }


    def _convertFloat(self, standardTypes, fVal):
        """ Utility method to get rid of numpy numeric types."""
        return float(fVal) if standardTypes else fVal


    def predict(self, texts: List[str], standardTypes=True, echoInput=False):
        """
        Classify a list of texts. The output has the format of a list
            [
                {
                    "prediction": {
                        label1: confidence1,
                        ...
                    }
                  [ "input": input_text, ]
                    "top": {"label": top_label, "value": top_value}
                }
            ]
        If standardTypes = True (default), care is taken to convert all numbers
        to ordinary Python types. This is because with numpy numbers one would
        get an error trying to serialize the output as JSON:
              "TypeError: Object of type float32 is not JSON serializable"
        if echoInput = True (default is False), the input text is also
        passed back.
        """
        xInput = self.getPaddedSequencesFromTexts(texts)
        predictions = self.model.predict(xInput)
        labeledPredictions = [
            {
                self.getLabelName(predIndex): self._convertFloat(standardTypes,
                                                                 predValue)
                for predIndex, predValue in enumerate(list(prediction))
            }
            for prediction in predictions
        ]
        results = [
            {
                **{
                    'prediction': labeledPrediction,
                    'top': self.getTopPrediction(labeledPrediction),
                },
                **({'input': inputText} if echoInput else {}),
            }
            for labeledPrediction, inputText in zip(labeledPredictions, texts)
        ]
        return results
