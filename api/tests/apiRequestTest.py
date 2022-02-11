""" apiRequestTest.py

        We put the API to test. This simply shoots the same requests over and
        over and checks the result is as expected. Used to check that running
        more than one of these at once they all pass (i.e. that the predict()
        method in the model has a decent thread safety).
        Note: we do *NOT* hardcode an expected 'score' in the test sentences,
        rather we extract it from the API themselves with a preliminary call,
        because the model training is non-deterministic and my model will
        probably give a 'slightly' different value from yours (but hopefully
        the labels will not change).
        This does not completely remove the need for a tolerance-based
        comparison because the least significant digits may get scrambled
        in the parsing/dumping of the json response.
"""


import requests
import sys


API_BASE_URL = 'http://localhost:8000'
TOLERANCE = 0.0001

sentences = [
    (
        'Congratulations and thank you for submitting the homework',
        'ham',
    ),
    (
        'Nothing works in my browser: it would be useless.',
        'ham',
    ),
    (
        'URGENT! You have WON an awesome prize, call us to redeem your bonus!',
        'spam',
    ),
    (
        'They were just gone for a coffee and came back',
        'ham',
    ),
]


def predictSingle(idx, scores):
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
        return predMatchExpected(sentences[index], scores[sentences[index][0]], rj)


def predictMultiple(idx, num, scores):
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
            predMatchExpected(sentences[index], scores[sentences[index][0]], pred)
            for index, pred in zip(indices, rj)
        ])


def predMatchExpected(expected, score, receivedPred):
    #
    eInput, eResult = expected
    eScore = score
    #
    return all([
        eInput == receivedPred['input'],
        eResult == receivedPred['top']['label'],
        abs(eScore - receivedPred['top']['value']) < TOLERANCE,
    ])


def callForScoreMap():
    url = API_BASE_URL + '/predictions'
    payload = {
        'texts': [
            s[0]
            for s in sentences
        ],
        'echo_input': True,
        'skip_cache': True,
    }
    req = requests.post(url, json=payload)
    #
    rj = req.json()
    return {
        s[0]: pred['top']['value']
        for s, pred in zip(sentences, rj)
    }


if __name__ == '__main__':
    if len(sys.argv) > 1:
        numIterations = int(sys.argv[1])
    else:
        numIterations = 10
    #
    allGood = True
    #
    print('Getting score map... ', end='')
    scoreMap = callForScoreMap()
    print('done.')
    #
    for i in range(numIterations):
        mi = i
        mn = 1 + (i % 5)
        mRes = predictMultiple(mi, mn, scoreMap)
        print('  [%3i] m(%8s) = %s' % (i, '%i, %i' % (mi, mn), mRes))
        sRes = predictSingle(mi, scoreMap)
        print('  [%3i] s(%8s) = %s' % (i, '%i' % mi, sRes))
        if not ( mRes and sRes ):
            print('                        *** FAULTS DETECTED ***')
            allGood = False
    #
    if allGood:
        print('All good')
    else:
        print('***\n*** Some faults occurred. ***\n***')
