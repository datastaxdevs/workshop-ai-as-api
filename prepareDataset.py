# pre_training.py

import pickle
import json
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

dataSetFile = 'training/dataset/spam-dataset.csv'


# if __name__ == '__main__':

df = pd.read_csv(dataSetFile)
#
labels = df['label'].tolist()
texts = df['text'].tolist()
#
label_legend = {"ham": 0, "spam": 1}
label_legend_inverted = {f"{v}": k for k,v in label_legend.items()}
#
labels_as_int = [label_legend[x] for x in labels]

MAX_NUM_WORDS = 280
tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

# what did we do? see this
#   inverse_word_index = {v: k for k, v in tokenizer.word_index.items()}
#   [[inverse_word_index[i] for i in sequences[101]]]
#   texts[101]

MAX_SEQ_LENGTH = 300
X = pad_sequences(sequences, maxlen=MAX_SEQ_LENGTH)

# what did we do? see this
#   [len(s) for s in sequences[:20]]
#   len(sequences)
#   X.shape
#   type(X)
#   X

labels_as_int_array = np.asarray(labels_as_int)

y = to_categorical(labels_as_int_array)

# see:
#   y.shape
#   labels_as_int_array.shape
# Also see:
#   to_categorical([0,1,2,0,0,1])
# Also see:
#   y[:3]
#   labels[:3]
#   label_legend

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
# shapes: (5043, 300) (2485, 300) (5043, 2) (2485, 2)

training_data = {
    "X_train": X_train, 
    "X_test": X_test,
    "y_train": y_train,
    "y_test": y_test,
    "max_words": MAX_NUM_WORDS,
    "max_seq_length": MAX_SEQ_LENGTH,
    "label_legend": label_legend,
    "label_legend_inverted": label_legend_inverted, 
    "tokenizer": tokenizer,
}
with open('training/prepared_dataset/spam_training_data.pickle', 'wb') as f:
    pickle.dump(training_data, f)
