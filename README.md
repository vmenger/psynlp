# `psynlp` --- NLP functionality for psychiatric text

> :exclamation: Most of the functionality in this project has now been made available the library [clinlp: production ready NLP pipelines for Dutch Clinical Text](https://github.com/umcu/clinlp). Although the code here might still benefit some projects, the project itself is no longer maintained (and thus archived).

This package bundles some functionality for applying NLP (preprocessing) techniques to clinical text in psychiatry. Specifically, it contains the following `submodules`: 

* [`preprocessing`](docs/submodule_readmes/README_preprocessing.md) -- Preprocessing text
* [`spelling`](docs/submodule_readmes/README_spelling.md) -- Spelling correction
* [`entity`](docs/submodule_readmes/README_entity.md) -- Entity matching
* [`context`](docs/submodule_readmes/README_context.md) -- Detecting properties of entities (e.g. negation, plausibility) based on context

These submodules are further documented in their respective readmes, which you will find by following the links above. 

## Installation

Since some paths need to be initialized, installation is most easily done by downloading the source, modifying paths in (`psynlp/utils.py` -- see Requirements below), and running:

```sh
pip install -r requirements.txt
python setup.py install 
```

#### Dependencies

The `psynlp` package has the following dependencies (automatically installed when using the commands above):
* `doublemetaphone`
* `gensim`
* `nltk`
* `pandas`
* `spacy` 

## Requirements

Some functionality requires specific models, which are not included in the repository because of their privacy-sensitive nature. Their paths should be specified in `psynlp/utils.py`. 

* A `spacy` model can be obtained [here](https://spacy.io/models) (e.g. `python -m spacy download nl_core_news_sm` for standard Dutch model)
* A `gensim` trained Word2Vec model, used for the `EmbeddingRanker` in the `spelling` module.
* Token frequencies in the specific corpus required for the `NoisyRanker`, in a `csv` file (`;`-separated with a `token` and a `frequency` column).

## Usage

`psynlp` follows an object-oriented paradigm, much like the `sklearn` libary for machine learning. To use the spelling correction from the `spelling` submodule for instance, the following code can be used:

```python
from psynlp.spelling import SpellChecker
c = SpellChecker(spacy_model="your_spacy_model_name")
c.correct("Dit is een tekst met daarin een splefout")
>>> "Dit is een tekst met daarin een spelfout"
```

Usage is futher documented in detail in the respective submodule READMEs. 

## Examples

Basic usage and API of each submodule is documented in the submodule README. Additionally, some use cases are documented in the following notebooks (also referenced in the relevant submodule READMEs):

* [`preprocessing.ipynb`](docs/notebooks/preprocessing.ipynb) -- Example code for preprocessing
* [`spelling.ipynb`](docs/notebooks/spelling.ipynb) -- Example code for spelling correction
* [`entity.ipynb`](docs/notebooks/entity.ipynb) -- Example code for entity recognition
* [`context.ipynb`](docs/notebooks/context.ipynb) -- Example code for context matching
* [`example_pipeline.ipynb`](docs/notebooks/example_pipeline.ipynb) -- Example code for extracting variables from text, using all of the four submodules

## Contributors
Vincent Menger -- Conceptualization, developing code

Nick Ermers -- Improving context detection
