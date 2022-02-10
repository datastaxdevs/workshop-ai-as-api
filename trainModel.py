# training.py

import pickle
import json
import numpy as np

from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Embedding, LSTM, SpatialDropout1D
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.preprocessing.sequence import pad_sequences

data = pickle.load(open('training/prepared_dataset/spam_training_data.pickle', 'rb'))

X_test = data['X_test']
X_train = data['X_train']
y_test = data['y_test']
y_train = data['y_train']
label_legend_inverted = data['label_legend_inverted'] # labels_legend_inverted
label_legend = data['label_legend'] # legend
max_seq_length = data['max_seq_length'] # max_sequence
max_words = data['max_words']
tokenizer = data['tokenizer']

# prepare

embed_dim = 128
lstm_out = 196

model = Sequential()
model.add(Embedding(max_words, embed_dim, input_length=X_train.shape[1]))
model.add(SpatialDropout1D(0.4))
model.add(LSTM(lstm_out, dropout=0.3, recurrent_dropout=0.3))
model.add(Dense(2, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])
print(model.summary())

# train

batch_size = 32
epochs = 5
model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=batch_size, verbose=1, epochs=epochs)

# save model

model.save('training/trained_model_v1/spam_model.hdf5')

# as a base test TAKE IT AWAY FROM HERE and move to post_Training!):
def predict(text_str, pMaxSequence=max_seq_length, pTokenizer=tokenizer):
  sequences = pTokenizer.texts_to_sequences([text_str])
  x_input = pad_sequences(sequences, maxlen=pMaxSequence)
  y_output = model.predict(x_input)
  #top_y_index = np.argmax(y_output)
  preds = y_output[0]#[top_y_index]
  labeled_preds = {f"{label_legend_inverted[str(i)]}": x for i, x in enumerate(preds)}
  return labeled_preds

"""
For later use in the API then we need
    the model (hdf5 file)
    something from the pickled, that we will export now as json for interoperability:
        label_legend_inverted
        label_legend
        max_seq_length
        max_words
    and the tokenizer
"""

metadataForExport = {
    'label_legend_inverted': label_legend_inverted,
    'label_legend': label_legend,
    'max_seq_length': max_seq_length,
    'max_words': max_words,
}
json.dump(metadataForExport, open('training/trained_model_v1/spam_metadata.json', 'w'))

tokenizerJson = tokenizer.to_json()
with open('training/trained_model_v1/spam_tokenizer.json', 'w') as f:
    f.write(tokenizerJson)
