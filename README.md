# NLP Classifier as an API

_We now assume all the intro is there, down to ..._

Gitpod is an IDE in the cloud (modeled after VSCode). It comes with a full
"virtual machine" (actually a Kubernetes-managed container), which we will
use as if it were our own computer (e.g. downloading files, executing programs
and scripts, even launching containers from within it).

The button below will: spawn your own Gitpod container + clone this repository
in it + preinstall the required dependencies: **ctrl-click on
it** to make sure you "Open in new tab" (Note: you may have to authenticate
through Github in the process):

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/hemidactylus/NLP-classifier-API)

In a few minutes, a full IDE will be ready in your browser, with a file
explorer on the left, a file editor on the top, and a console (`bash`) below it.

> There are many more other features, probably familiar to those who have
> experience with VSCode. Feel free to play around a bit!


## Part 1: train the model

(sketch of the steps so far)

- check the csv, line 352
- "prepareDataset.py", or "prepareDataset.py -v", check output and code, also diagrams
  (don't worry about `Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory`, it just means no CUDA, no GPU, hence we'll be a tad slower. You may want to do gpu)
  inspect file created
- "trainModel.py", also inspect files created
- "loadTestModel.py"

## Part 2: expose as an API

- cp .env.sample .env and fill it (bundle: currently to a subdir (mmh), id, secret)
- look at minimain code
- `uvicorn api.minimain:miniapp`, a couple of CURLs, quckly
- STOP minimain and look at the complete main api:
    model class
    caching, DB access and object mapper
    typing
    settings
    calls log, caller "id" and streaming
- run the main api
    a couple of CURLs, in sequence to illustrate caching
    keep an eye on CQL Console
    swagger UI to play a bit (e.g. with the streaming + curl!), ```echo `gp url 8000`/docs```
- homeworks


## Notes:

some more notes on X-Forwarded-For ? https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip

Notes: python3.9/3.10 can get pandas==1.4.0 but python3.7 can get to 1.3.5 max so when trying a venv with py37 (previous: 3.9+) I changed reqfile from `pandas=1.4.0` to `pandas>=1.3.5`.

It seems to work (py3.7)

## Curls for the API

```
curl -s localhost:8000/ | python -mjson.tool


curl -XPOST localhost:8000/prediction -d '{"text": "Bla"}' -H 'Content-Type: application/json' | python -mjson.tool
curl -XPOST localhost:8000/prediction -d '{"text": "Bla", "skip_cache": true}' -H 'Content-Type: application/json' | python -mjson.tool


curl -XPOST localhost:8000/predictions -d '{"texts": ["Click HERE for the chance to WIN A FREE ANVIL", "Mmmm, it seems a really top-notch place! The photos made me hungry..."]}' -H 'Content-Type: application/json' | python -mjson.tool
curl -XPOST localhost:8000/predictions -d '{"texts": ["Click HERE for the chance to WIN A FREE ANVIL", "A new sentence!"], "echo_input": false}' -H 'Content-Type: application/json' | python -mjson.tool

# also as GET out of convenience
curl "localhost:8000/prediction?text=rrr&skip_cache=true"

```

## swagger

http://127.0.0.1:8000/docs