# post_training_read_test.py
#   we check that one can just read from ../trained and start predicting

import json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras import models

tokenizer = tokenizer_from_json(open('training/trained_model_v1/spam_tokenizer.json').read())
metadata = json.load(open('training/trained_model_v1/spam_metadata.json'))
#   relevant keys:
#       label_legend_inverted
#       max_seq_length

model = models.load_model('training/trained_model_v1/spam_model.hdf5')
# model.summary()

def _predictSpamminess(text, spamModel, pMaxSequence, pLabelLegendInverted, pTokenizer):
  sequences = pTokenizer.texts_to_sequences([text])
  x_input = pad_sequences(sequences, maxlen=pMaxSequence)
  y_output = spamModel.predict(x_input)
  preds = y_output[0]
  labeled_preds = {f"{pLabelLegendInverted[str(i)]}": x for i, x in enumerate(preds)}
  return labeled_preds

sampleTexts = [
    'This is a nice touch, adding a sense of belonging and coziness. Thank you so much.',
    'Click here to WIN A FREE IPHONE and this and that.',
]

print('\n' * 4)
for st in sampleTexts:
    preds = _predictSpamminess(st, model, metadata['max_seq_length'], metadata['label_legend_inverted'], tokenizer)
    print(st, preds)
    print('*' * 20)
