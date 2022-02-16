"""
    MockSpamAIModel.py
        a quick-and-dirty mock of the spam-classifier AIModel instance,
        available just to test the API when the actual trained model
        cannot be used for some reason. Definitely not a 'serious' thing.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class MockSpamAIModel:
    modelPath: Path
    tokenizerPath: Optional[Path] = None
    metadataPath: Optional[Path] = None

    model = None
    tokenizer = None
    metadata = None

    def __post_init__(self):
        ...


    def _mockPredict(self, text):
        if len(text) % 2 == 0:
            return {
                'ham': 1.0,
                'spam': 0.0,
            }, {
                'label': 'ham',
                'value': 1.0,
            }
        else:
            return {
                'ham': 0.0,
                'spam': 1.0,
            }, {
                'label': 'spam',
                'value': 1.0,
            }


    def predict(self, texts: List[str], standardTypes=True, echoInput=False):
        """
        Mock-predict on texts with hardcoded results, just to mimic the same
        schema for the returned values.
        """
        results = [
            {
                **{
                    'prediction': pred[0],
                    'top': pred[1],
                },
                **({'input': inputText} if echoInput else {}),
            }
            for pred, inputText in ((self._mockPredict(t), t) for t in texts)
        ]
        return results
