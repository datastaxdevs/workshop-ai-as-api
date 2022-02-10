# NLP Classifier as an API

Readme must be written.

Notes: python3.9/3.10 can get pandas==1.4.0 but python3.7 can get to 1.3.5 max so when trying a venv with py37 (previous: 3.9+) I changed reqfile from `pandas=1.4.0` to `pandas>=1.3.5`.

It seems to work (py3.7)

[And also removed jupyter at that.]

## Curls for the API

```
curl -s localhost:8000/ | python -mjson.tool


curl -XPOST localhost:8000/prediction -d '{"text": "Bla"}' -H 'Content-Type: application/json' | python -mjson.tool
curl -XPOST localhost:8000/prediction -d '{"text": "Bla", "skip_cache": true}' -H 'Content-Type: application/json' | python -mjson.tool


curl -XPOST localhost:8000/predictions -d '{"texts": ["Click HERE for the chance to WIN A FREE ANVIL", "Mmmm, it seems a really top-notch place! The photos made me hungry..."]}' -H 'Content-Type: application/json' | python -mjson.tool
curl -XPOST localhost:8000/predictions -d '{"texts": ["Click HERE for the chance to WIN A FREE ANVIL", "Mmmm, it seems a really top-notch place! The photos made me hungry..."], "echo_input": false}' -H 'Content-Type: application/json' | python -mjson.tool
```

## swagger

http://127.0.0.1:8000/docs