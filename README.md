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

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/hemidactylus/nbws1)

In a few minutes, a full IDE will be ready in your browser, with a file
explorer on the left, a file editor on the top, and a console (`bash`) below it.

> There are many more other features, probably familiar to those who have
> experience with VSCode. Feel free to play around a bit!


## Part 1: train the model




## Part 2: expose as an API




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
curl -XPOST localhost:8000/predictions -d '{"texts": ["Click HERE for the chance to WIN A FREE ANVIL", "Mmmm, it seems a really top-notch place! The photos made me hungry..."], "echo_input": false}' -H 'Content-Type: application/json' | python -mjson.tool
```

## swagger

http://127.0.0.1:8000/docs