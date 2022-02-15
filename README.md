<!--- STARTEXCLUDE --->
# NLP text classification as an API

[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/hemidactylus/NLP-classifier-API)
[![License Apache2](https://img.shields.io/hexpm/l/plug.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Discord](https://img.shields.io/discord/685554030159593522)](https://discord.com/widget?id=685554030159593522&theme=dark)

Time: *50 minutes*. Difficulty: *Intermediate*. [Start Building!](#lets-start)

Learn to build your own NLP text classifier and expose it as an API: an
interactive workshop featuring
* AI-based text analysis with Tensorflow/Keras
* Astra DB, a Database-as-a-Service built on Apache Cassandra™
* FastAPI, the high-performance Python framework for creating APIs
* lots of useful Python libraries and packages (`pydantic`, `dotenv`, `sklearn`, `uvicorn`, ...)

<!--- ENDEXCLUDE --->

![Workshop cover](images/nlp-classifier-api-cover.png)



## During this hands-on workshop, you will:
* prepare the labeled dataset for model training;
* train the model to classify any input text;
* export the trained model and test it interactively;
* create your free NoSQL database for data storage;
* set up and start an API exposing the classifier as a reusable class;
* learn how to speed up the API with DB-based caching;
* inspect how a streaming response is handled in the API.



## Frequently asked questions

- *Can I run the workshop on my computer?*

> You don't have to, **you can do everything in the cloud from the comfort of your browser**! But there is nothing preventing you from running the workshop on your own machine.
> If you do so, you will need
> * `git` installed on your local system;
> * [Python v3.6+ installed on your local system](https://www.python.org/downloads/).
>
> In this readme, we try to provide instructions for local development as well - but keep in mind that
> the main focus is development on Gitpod, hence **we can't guarantee live support** about local development
> in order to keep on track with the schedule. However, we will do our best to give you the info you need to succeed.

- *What other prerequisites are there?*
> * You will need a GitHub account;
> * You will also need an Astra account: don't worry, we'll work through that in the following.

- *Do I need to pay for anything for this workshop?*
> * **No.** All tools and services we provide here are FREE.

- *Will I get a certificate if I attend this workshop?*

> Attending the session is not enough. You need to complete the homeworks detailed below and you will get a nice participation certificate a.k.a. badge.

<details><summary>Show me the **credits** for this workshop</summary>

### Credits

The core of this workshop is an adaptation from the excellent content ["AI as an API,"](https://www.youtube.com/watch?v=56qQNcHJxyQ)
created by [CodingEntrepreneurs](https://www.youtube.com/channel/UCWEHue8kksIaktO8KTTN_zg).
You are very much encouraged to watch it, as it touches on more topics
and includes steps that unavoidably had to be taken out when converting to
this shorter format.

However, the opposite is also true: the code you'll see here is almost completely
rewritten from scratch, generally using different tools or techniques;
the API has a different structure and offers different
endpoints, which better fit the particular pedagogical intent we had in mind
and highlight some best practices for using databases such as Cassandra for storage.

So, all in all, you'd be better off by watching both contents!

</details>



## Materials for the Session

It doesn't matter if you join our workshop live or you prefer to work at your own pace,
we have you covered. In this repository, you'll find everything you need for this workshop:

- [Workshop Video](#)
- [Slide deck](#)
- [Discord chat](https://dtsx.io/discord)
- [Questions and Answers](https://community.datastax.com/)



## Homework

<img src="images/nlp-as-api-badge.png?raw=true" width="200" align="right" />

Don't forget to complete your assignment and get your **verified skill badge**:

1. do all practice steps described below until you can query your API running in Gitpod.
2. Now roll up your sleeves and modify the code as follows: TBD
3. Take a SCREENSHOT of requests/responses with the modified API. _Note: you will have to restart the API to see all changes!_
4. Submit your homework [here](#).

That's it, you are done! Expect an email in a few days!




# Let's start

## Table of contents

1. [Create your Astra DB instance](#create-and-setup-astra-db)
2. [Load the project into Gitpod](#load-the-project-into-gitpod)
3. [Train the model](#train-the-model)
4. [Expose as API](#expose-as-api)
5. [Use the API](#use-the-api)
6. [Homework instructions](#homework-instructions)



## Create and setup Astra DB

You will now create a database with a keyspace in it (a _keyspace_ can contain _tables_).
Our API needs a couple of tables for persistent storage: they will be created programmatically on startup
if they don't exist, so there's no need to worry too much about them.

Besides creating the database, you need to retrieve a couple of codes and assets
for the API to be able to connect to it in a secure and authenticated way.

_**`ASTRA DB`** is the simplest way to run Cassandra with zero operations at all - just push the button and get your cluster. No credit card required, $25.00 USD credit every month, roughly 20M read/write operations and 80GB storage monthly - sufficient to run small production workloads._

Start by Ctrl-clicking on this button (to open in a new tab)
and then follow the instructions below:

<a href="https://astra.datastax.com"><img src="images/create_astra_db_button.png?raw=true" /></a>

- create an Astra DB instance [as explained here](https://github.com/datastaxdevs/awesome-astra/wiki/Create-an-AstraDB-Instance), with database name = `workshops` and keyspace = `spamclassifier`;
- generate and download a Secure Connect Bundle [as explained here](https://github.com/datastaxdevs/awesome-astra/wiki/Download-the-secure-connect-bundle);
- generate and retrieve a DB Token [as explained here](https://github.com/datastaxdevs/awesome-astra/wiki/Create-an-Astra-Token#c---procedure). **Important**: use the role "DB Administrator" for the token. You will later need the "Client ID" and "Client Secret" for this token.

Moreover, keep the Astra DB dashboard open: it will be useful later.
In particular you may find it convenient to have the CQL Console within reach
(click on your database on the left sidebar, then locate the "CQL Console" tab
in the main panel).



## Load the project into Gitpod

Gitpod is an IDE in the cloud (modeled after VSCode). It comes with a full
"virtual machine" (actually a Kubernetes-managed container), which we will
use as if it were our own computer (e.g. downloading files, executing programs
and scripts, training the model and eventually starting the API from it).

The button below will:

- spawn your own Gitpod container;
- clone this repository in it and open it in the IDE;
- preinstall the required dependencies.

**ctrl-click on the Gitpod button** to make sure you "Open in new tab"
(Note: you may have to authenticate
through Github in the process):

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/hemidactylus/NLP-classifier-API)

In a few minutes, a full IDE will be ready in your browser, with a file
explorer on the left, a file editor on the top
(with this very README open for convenience), and a console (`bash`) below it.

> _Note_: you will probably see "errors" related to mismatching versions
> between the `tensorflow` package and others (notably `numpy`). You should
> be able to ignore them and just go ahead.

> There are many more other features, probably familiar to those who have
> experience with VSCode. Feel free to play around a bit!

> If you want to work on your laptop, make sure you install all Python
> dependencies listed in `requirements.txt` (doing so in a Python virtual
> environment is _strongly suggested_) and add the main repo root
> to the `PYTHONPATH`.

<details><summary>Show me a map of the Gitpod starting layout</summary>

<img src="images/gitpod_view.png?raw=true" />

1. File explorer
2. Editor
3. Panel for console(s)
4. Console switcher
</details>



## Train the model

The goal of this phase is to have our text classifier model ready
to be used: that means, not only will we train it on a labeled dataset,
but also we will take care of exporting it in a format suitable
for later loading by the API.


### Inspect the starting dataset

Open the file `training/dataset/spam-dataset.csv` and have a look
at the lines there. (_Tip_: you can open a file in Gitpod by locating
it with the "File Explorer" on your left, but if you like using the keyboard
you may simply issue the command `gp open training/dataset/spam-dataset.csv`
from the `bash` Console at the bottom.)

This is a CSV file with three columns (separated by commas):

- whether the line is spam or "ham" (i.e. the opposite of spam),
- a short piece of text (a "message"),
- the tag identifying the source of this datapoint.

The third column betrays the mixed origin of the data: in order to
create a labeled dataset of around 7.5K messages marked as spam/ham,
two different (publicly available) sets have been merged
(namely [this one](https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection)
and [this one](https://archive.ics.uci.edu/ml/datasets/YouTube+Spam+Collection)).

Luckily for you, the (not always fun) task of cleaning, validating and normalizing the
heterogeneous (and usually imperfect) data has been already done for you -- something
that is seldom true, alas, in a real-world task.

Look at line 352 of this file for an example we will inspect time and again:
is that message spam or ham? (_Tip_: hit Ctrl-G in the Gitpod editor to
jump to a specific line number.)

<details><summary>Show me that line in Gitpod's editor</summary>
    <img src="images/gitpod_gotoline.png?raw=true" />
</details>


### Prepare the dataset for training

We want to "teach" a machine to distinguish between spam and ham: unfortunately,
machines prefer to speak numbers rather than words.
We then need to transform the human-readable CSV file above into a format
that, albeit less readable by us, is more suited to the subsequent task
of training the classifier. 
We will express (a cleaned-out version of) the text into a sequence
of numbers, each representing a token (one word) forming the message text.

More precisely:

- first we will initialize a "tokenizer", asking it to build a dictionary (i.e. a token/number mapping) best suited for the texts at hand;
- then, we will use the tokenizer to reduce all messages into (variable-length) sequences of numbers;
- these sequences will be "padded", i.e. we will make sure they end up all having the same length: in this way, the whole dataset will be represented by a rectangular matrix of integer numbers, possibly with leading zeroes;
- the "spam/ham" column of the input dataset is recast as "categorical": that is, it is made into two columns, one for "spamminess" and one for "hamminess", both admitting the values zero or one: this turns out to be a formulation much friendlier to machine-learning tasks in general;
- finally we will split the labeled dataset into a "training" and a "testing" disjoint parts. This is a very important concept: the effectiveness of a model should always be validated on data points **not used during training**.

All these steps can be largely automated by using data-science Python packages
such as `pandas`, `numpy`, `tensorflow/keras`.
Indeed this is all accomplished by launching the following script
(which you should open and dissect line by line to learn more):

```
python prepareDataset.py -v
```

(the `-v` stands for "verbose": you will see some sample values and
various objects being printed as the script progresses, which will
shed more light on what kind of transformations exactly are taking place).

> _Note_: don't worry if you see a message such as `Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory`. It just means that this environment lacks the CUDA libraries, hence most Tensorflow tasks will be considerably slower than on a GPU. If you work on your laptop, you may want to switch to using a GPU for the training task, if you have the option to do so.

The dataset preparation starts with the CSV file you saw earlier
and ends up exporting the new data format in the `training/prepared_dataset`
directory. Two observations are in order:

- the "big matrix of numbers" encoding the messages and the one containing their spam/ham status are useless without the tokenizer: after all, to process a new message you would need to know how to make it into a sequence of numbers, right?
- the `pickle` protocol used in writing the reformulated data is strictly Python-specific and should not be treated as a long-term (or interoperable!) format. Please see next step (below) for a sensible way to store model, tokenizer and metadata on disk.

Try to have a look at the `pickle` file created by the `prepareDataset.py` script. Well,
it's a binary file indeed, and there is not much to be seen there. Let's move along.


### Train the model

It is time to train the model, i.e. fit a neural network to the task of
associating _a spam/ham label to a text message_.
Well, actually the task is now more like "associating a 0/1 number to a sequence
of integer numbers (padded to fixed length with leading zeroes)".

The code for creating and training the model is very short (a handful of lines of code,
excluding loading from disk and writing to it), but running it will take several minutes:
launch the script

```
python trainModel.py
```

and wait for it to finish (it will take probably twelve minutes or so on Gitpod).

The training script works as follows:

1. all variables created and stored in the previous steps are loaded back to memory;
2. a specific architecture of a neural network is created, still a "blank slate" in terms of what it "knows". Its structure is that of a LSTM ([long-short-term-memory](https://en.wikipedia.org/wiki/Long_short-term_memory)), a [specific kind](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM) of recurrent neural network with some clever modifications aimed at enhancing its ability to "remember" things between non-adjacent locations in a sequence, such as two displaced positions in a string of text;
3. the network (our classifier) is trained: that means it will progressively adapt its internal (many thousands of) parameters in order to best reproduce the input training set. Each individual neuron in the network is a relatively simple component - the "intelligence" coming from their sheer quantity and the particular choice of parameters determining which neurons affect which other and by how much;
4. Once the training process has finished, the script carefully saves everything (model, tokenizer and associated metadata) in a format that can be later loaded by the API in a stand-alone way.

Perhaps by now the training process is completed and everything has been
saved in the `training/trained_model_v1` directory (_Note_: we keep a version
number in the model to be able to seamlessly switch to a newer classifier, or even
hypothetically to expose several of them at once in a single API).

Take a look in the output directory: there should be

- a (small) JSON file with some metadata describing some features of the model;
- a (larger) JSON file containing the full definition of the tokenizer. This has been created, and will be loaded, using helper functions provided with the tokenizer itself for our convenience;
- a (rather large) binary file containing "the model". That means, among other things, the shape and topology of the neural network and all "weights", i.e. the parameters dictating which neurons will affect which others, and by how much. Saving and loading this file, which is in the HDF5 format, is best left to routines kindly offered by Keras.


### Test the trained model

Before moving on to the API section, let us just make sure that the saved
trained model is self-contained: that is, let's check that by loading
the contents of `training/trained_model_v1` and nothing else we are able
to perform meaningful estimates of the spam/ham status for a new arbitrary
piece of text.

The script `loadTestModel.py` does exactly that: it loads the saved model
and uses that to "predict" the ham/spam labels for new texts. Try it with

```
python loadTestModel.py
```

or even, if you feel creative, something like
```
python loadTestModel.py This is my example sentence and let us see if this is ham
```

Note that the output is given in terms of "probabilities", or "confidence":
we can interpret a result like `{'ham': 0.92, 'spam': 0.08}` as
_the input is ham with 92% confidence_. Indeed, generally speaking,
ML-based classifiers are very sophisticated machines for statistical inference.

If you look at the (very simple) code of this function, you will see how the
model, once loaded, is used to make predictions (it all boils down to the model's
`predict` method, but first the input text must be recast as sequence of numbers,
and likewise the results must be made readable by humans again).

_Note_: the model lends itself very well to processing several input texts
in parallel (which generally is a big advantage in terms of performance; it is
something we will exploit in the API as well). **Can you see where this is apparent
in this test code?**

<details><summary>Tell me the answer</summary>

**Answer:** The function `predictSpamStatus` always receives a single text as input,
but this text is made into a one-element list before encoding as numbers
(`pTokenizer.texts_to_sequences([text])`). Much in the same way,
once the model has emitted its prediction, the code gets the first (and only)
element of a list of results (`yOutput[0]`).

Just by looking at these manipulations one can guess that multiple texts
can be processed in parallel with negligible changes to the code, which indeed
turns out to be the case.

</details>



## Expose as API

Now your model is trained and saved to disk, ready to be used.
It is time to expose it with FastAPI in the form of easy-to-use
HTTP requests.

We will first look at a minimal version of the API, just to get a first
taste of how FastAPI works, and then turn to a full-fledged version,
with more endpoints and a database-backed caching layer.


### Configure dot-env and DB connect bundle

Remember the "Secure Connect Bundle" you downloaded earlier from the Astra DB UI?
It's time to upload it to Gitpod.

> If you work locally, skip the upload and just be aware of the path to it for what comes next in the `.env` file.

Locate the file on your computer using the "finder/explorer".
Drag and drop the bundle into the Gitpod explorer window: _make sure you drop it on the
file explorer window in Gitpod._

<details><summary>Show me how to drag-and-drop the bundle to Gitpod</summary>
    <img src="images/drag-and-drop-bundle.png?raw=true" />
</details>

As a check, you may want to verify the file is available in the right location with:

    ls -lh secure-connect-*.zip

The output should tell you the exact file name (you can also make sure the
file size is around 12KB while you are at it).

Now we must prepare a **dot-env file** containing the configuration
required by the API (directory names, paths and, most important, the parameters
to access the Astra DB persistence layer).

Make a copy of the example environment file and open it in the editor with

```
cp .env.sample .env
gp open .env
```

Most of the settings in this file are already filled for you (they will be
picked up by the API as you start it).

_Important:_ Make sure you paste your App ID and App Secret obtained earlier with the
Astra DB Token in the `ASTRA_DB_CLIENT_SECRET` and `ASTRA_DB_CLIENT_ID` variables
(keep the quotes and don't leave spaces around the equal sign).

As for the `ASTRA_DB_KEYSPACE` and `ASTRA_DB_BUNDLE_PATH` settings, you probably
don't need to worry (they must match the keyspace you created earlier in the
database and the location and file name of the Secure Connect Bundle you just
uploaded to Gitpod, respectively.)


### Baby steps: a minimal API

`uvicorn api.minimain:app --reload`

- look at minimain code

- a couple of CURLs, quckly

### Start the full API

- STOP minimain and look at the complete main api:
    model class
    caching, DB access and object mapper
    typing
    settings
    calls log, caller "id" and streaming


## Use the API

API Docs (`http://127.0.0.1:8000/docs`) and API testing

Also check on Astra DB

- run the main api
    a couple of CURLs, in sequence to illustrate caching
    keep an eye on CQL Console
    swagger UI to play a bit (e.g. with the streaming + curl!), ```echo `gp url 8000`/docs```


## Notes:

some more notes on X-Forwarded-For ? https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip


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
