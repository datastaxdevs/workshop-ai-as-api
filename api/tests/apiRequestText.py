import requests
import sys


API_BASE_URL = 'http://localhost:8000'
TOLERANCE = 0.0001

sentences = [
    ('Congratulations and thank you for submitting the homework', 'ham', 0.814928),
    ('Nothing works in my browser: it would be useless.', 'ham', 0.990825),
    ('They were just gone for a coffee and came back', 'ham', 0.755243),
]


def predictSingle(idx):
    url = API_BASE_URL + '/prediction'
    index = idx % len(sentences)
    payload = {
        'text': sentences[index][0],
        'echo_input': True,
        'skip_cache': True,
    }
    req = requests.post(url, json=payload)
    #
    if req.status_code != 200:
        return False
    else:
        rj = req.json()
        return predMatchExpected(sentences[index], rj)


def predictMultiple(idx, num):
    url = API_BASE_URL + '/predictions'
    indices = [
        (idx + j) % len(sentences)
        for j in range(num)
    ]
    payload = {
        'texts': [
            sentences[i][0]
            for i in indices
        ],
        'echo_input': True,
        'skip_cache': True,
    }
    req = requests.post(url, json=payload)
    #
    if req.status_code != 200:
        return False
    else:
        rj = req.json()
        return all([
            predMatchExpected(sentences[index], pred)
            for index, pred in zip(indices, rj)
        ])


def predMatchExpected(expectedTriple, receivedPred):
    #
    eInput, eResult, eConfidence = expectedTriple
    #
    return all([
        eInput == receivedPred['input'],
        eResult == receivedPred['top']['label'],
        abs(eConfidence - receivedPred['top']['value']) < TOLERANCE,
    ])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        numIterations = int(sys.argv[1])
    else:
        numIterations = 10
    #
    allGood = True
    for i in range(numIterations):
        mi = i
        mn = 1 + (i % 5)
        mRes = predictMultiple(mi, mn)
        print('[%3i] m(%i,%i) = %s' % (i, mi, mn, mRes))
        sRes = predictSingle(mi)
        print('[%3i] s(%i) = %s' % (i, mi, sRes))
        if not ( mRes and sRes ):
            print('                        *** FAULTS DETECTED ***')
            allGood = False
    #
    if allGood:
        print('All good')
    else:
        print('***\n*** Some faults occurred. ***\n***')
