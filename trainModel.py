""" trainModel.py

        Step 2 in the training: the actual training of the model:
        once initialized, we train it to the prepared data and then
        save the resulting trained model, ready to make predictions.
"""

import pickle
import json
import sys
import numpy as np
#
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Embedding, LSTM, SpatialDropout1D
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.preprocessing.sequence import pad_sequences

# in
trainingDumpFile = 'training/prepared_dataset/spam_training_data.pickle'
# out
trainedModelFile = 'training/trained_model_v1/spam_model.h5'
trainedMetadataFile = 'training/trained_model_v1/spam_metadata.json'
trainedTokenizerFile = 'training/trained_model_v1/spam_tokenizer.json'


if __name__ == '__main__':
    dry = '--dry' in sys.argv[1:]
    print('TRAINING MODEL')

    # load the training data and extract its parts
    print('    Loading training data ... ', end ='')
    data = pickle.load(open(trainingDumpFile, 'rb'))
    X_test = data['X_test']
    X_train = data['X_train']
    y_test = data['y_test']
    y_train = data['y_train']
    labelLegendInverted = data['label_legend_inverted']
    labelLegend = data['label_legend']
    maxSeqLength = data['max_seq_length']
    maxNumWords = data['max_words']
    tokenizer = data['tokenizer']
    print('done')

    # Model preparation
    print('    Initializing model ... ', end ='')
    embedDim = 128
    LstmOut = 196
    #
    model = Sequential()
    model.add(Embedding(maxNumWords, embedDim, input_length=X_train.shape[1]))
    model.add(SpatialDropout1D(0.4))
    model.add(LSTM(LstmOut, dropout=0.3, recurrent_dropout=0.3))
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print('done. Model summary:')
    print(model.summary())

    # Training
    print('    Training (it will take some minutes) ... ', end ='')
    batchSize = 32
    epochs = 3
    model.fit(X_train, y_train,
              validation_data=(X_test, y_test),
              batch_size=batchSize, verbose=1,
              epochs=epochs)
    print('done')

    # Save the result (this involves three separate files)
    # 1. Save the model proper (the model has its own format and its I/O methods)
    print('    Saving model ... ', end ='')
    if not dry:
        model.save(trainedModelFile)
    else:
        print(' **dry-run** ', end='')
    print('done')

    # ... but for later self-contained use in the API then we need:
    #     the model (hdf5 file), saved above
    #     some metadata, that we will export now as JSON for interoperability:
    #         labelLegendInverted
    #         labelLegend
    #         maxSeqLength
    #         maxNumWords
    #     and finally the tokenizer itself

    # 2. save a JSON with the metadata needed to 'run' the model
    print('    Saving metadata ... ', end ='')
    metadataForExport = {
        'label_legend_inverted': labelLegendInverted,
        'label_legend': labelLegend,
        'max_seq_length': maxSeqLength,
        'max_words': maxNumWords,
    }
    if not dry:
        json.dump(metadataForExport, open(trainedMetadataFile, 'w'))
    else:
        print(' **dry-run** ', end='')
    print('done')

    # 3. dump the tokenizer. This is in practice a JSON, but the tokenizer
    #    offers methods to deal with that:
    print('    Saving tokenizer ... ', end ='')
    tokenizerJson = tokenizer.to_json()
    if not dry:
        with open(trainedTokenizerFile, 'w') as f:
            f.write(tokenizerJson)
    else:
        print(' **dry-run** ', end='')
    print('done')
    #
    print('FINISHED')
