""" prepareDataset.py
    
        Step 1 in the training: we convert the (human-readable) CSV
        with training data into number matrices with the appropriate
        shape, ready for the actual training of the classifier.
"""

import sys
import pickle
import json
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split


# in
datasetInputFile = 'training/dataset/spam-dataset.csv'
# out
trainingDumpFile = 'training/prepared_dataset/spam_training_data.pickle'


if __name__ == '__main__':
    # just for additional output, not relevant for the process itself
    verbose = '-v' in sys.argv[1:]
    def _reindent(t, n): return '\n'.join('%s%s' % (' ' * n if ix > 0 else '', l) for ix, l in enumerate(t.split('\n')))

    print('PREPARE DATASET')

    # Reading the input file and preparing legend info
    print('    Reading ... ', end ='')
    df = pd.read_csv(datasetInputFile)
    labels = df['label'].tolist()
    texts = df['text'].tolist()
    #
    labelLegend = {'ham': 0, 'spam': 1}
    labelLegendInverted = {'%i' % v: k for k,v in labelLegend.items()}
    labelsAsInt = [labelLegend[x] for x in labels]
    print('done')
    if verbose:
        print('        texts[350]           = "%s ..."' % texts[350][:45])
        print('        labelLegend          = %s' % str(labelLegend))
        print('        labelLegendInverted  = %s' % str(labelLegendInverted))
        print('        labels               = %s  +...' % str(labels[:5]))
        print('        labelsAsInt          = %s  +...' % str(labelsAsInt[:5]))

    # Tokenization of texts
    print('    Tokenizing ... ', end ='')
    MAX_NUM_WORDS = 280
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    print('done')
    if verbose:
        print('        tokenizer.word_index             = %s +...' % str(dict(list(tokenizer.word_index.items())[:5])))
        inverseWordIndex = {v: k for k, v in tokenizer.word_index.items()}
        print('        inverseWordIndex                 = %s +...' % str(dict(list(inverseWordIndex.items())[:5])))
        print('        sequences[350]                   = %s' % str(sequences[350]))
        print('        [')
        print('            inverseWordIndex[i]')
        print('            for i in sequences[350]')
        print('        ]                                = %s' % (
            [inverseWordIndex[i] for i in sequences[350]]
        ))
        print('        texts[350]                       = "%s"' % texts[350])

    # Padding of sequences
    print('    Padding ... ', end ='')
    MAX_SEQ_LENGTH = 300
    X = pad_sequences(sequences, maxlen=MAX_SEQ_LENGTH)
    print('done')
    if verbose:
        print('        [len(s) for s in sequences]      = %s + ...' % str([len(s) for s in sequences[:6]]))
        print('        len(sequences)                   = %s' % str(len(sequences)))
        print('        X.shape                          = %s' % str(X.shape))
        print('        type(X)                          = %s' % str(type(X)))
        print('        X[350]                           = ... + %s' % str(X[350][285:]))

    # Switch to categorical form for labels
    print('    Casting as categorical ... ', end ='')
    labelsAsIntArray = np.asarray(labelsAsInt)
    y = to_categorical(labelsAsIntArray)
    print('done')
    if verbose:
        print('        labelsAsIntArray.shape           = %s' % str(labelsAsIntArray.shape))
        print('        y.shape                          = %s' % str(y.shape))
        print('        y[:5]                            = %s' % _reindent(str(y[:5]),43))
        print('        labels[:5]                       = %s' % str(labels[:5]))
        print('        labelLegend                      = %s' % str(labelLegend))

    print('    Splitting dataset ... ', end ='')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    print('done')
    if verbose:
        print('        X_train.shape = %s' % str(X_train.shape))
        print('        X_test.shape  = %s' % str(X_test.shape))
        print('        y_train.shape = %s' % str(y_train.shape))
        print('        y_test.shape  = %s' % str(y_test.shape))
        # Respectively: (5043, 300) (2485, 300) (5043, 2) (2485, 2)

    print('    Saving ... ', end ='')
    trainingData = {
        'X_train': X_train, 
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'max_words': MAX_NUM_WORDS,
        'max_seq_length': MAX_SEQ_LENGTH,
        'label_legend': labelLegend,
        'label_legend_inverted': labelLegendInverted, 
        'tokenizer': tokenizer,
    }
    with open(trainingDumpFile, 'wb') as f:
        pickle.dump(trainingData, f)
    print('done')
    if verbose:
        print('        Saved keys = %s' % '/'.join(sorted(trainingData.keys())))
    #
    print('FINISHED')
