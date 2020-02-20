# `preprocessing` --- The `psynlp` module for doing some basic preprocessing on clinical text. 

The `preprocessing` submodule implements some basic functionality for preprocessing clinical text. It currently implements the following things: 

* Normalizing
* Sentence splitting
* Tokenizing

The abstract classes  `Normalizer`, `SentenceSplitter` and `Tokenizer` define the interface (see table below), with ready-to-use implementations provided in the implementation classes. It is always possible to use/define your own custom normalizer, sentence splitter or tokenizer, by creating a new class with your own custom logic. The current implementations (`BasicNormalizer`,  `BasicSentenceSplitter`, `SpacyTokenizer`) are used in other projects, so beware that changing them might lead to unexpected behaviour in other projects (e.g. nlp resource training, decursus/rapportage pipelines). 

| Abstract Class | Functions | Implementations
|--|--|--|
| `Normalizer` | `normalize` | `BasicNormalizer`
| `SentenceSplitter` | `process_text` `split`, `process_sentence` | `BasicSentenceSplitter`
| `Tokenizer` | `tokenize` | `SpacyTokenizer`

A complete API can be found at the bottom of this readme. 

## Normalizing

The BasicNormalizer implements some basic normalization steps, such as removing special characters, and removing double whitespaces/newlines. 

#### Usage

```python
from psynlp.preprocessing import BasicNormalizer

bn = BasicNormalizer()
bn.normalize("Patiënt  werd vannacht opgenomen.")
>> "Patient werd vannacht opgenomen."
```

## Sentence splitting

Splitting text into sentences early is a step that becomes very useful in later stages, as processing text sentence-by-sentence strikes a nice balance between processing texts and processing words. When using the `context` submodule, only sentences are accepted as input. 

A ready-for-use implementation can be found in `BasicSentenceSplitter`. This implementation makes use of the `nltk` sentence tokenizer, which based on some experimentation works well (and relatively fast). The `nltk`  sentence tokenizer is used in combination with some custom rules and scripts, such as always splitting on `\n`, and not splitting on the period in `2.5 milligram`. 

#### Usage

```python
from psynlp.preprocessing import BasicSentenceSplitter

bss = BasicSentenceSplitter()
bss.split("Dit is zin één. Dit is zin twee.")
>> ['Dit is zin één.', 'Dit is zin twee.']
```

## Tokenizing

For tokenizing, the SpacyTokenizer is implemented, which is based on the out-of-the-box Dutch tokenizer that Spacy provides, with some additional logic for correctly tokenizing DEDUCE-tags and some other symbols such as `/` and `-`. NB: the spacy model is created in the `nlpresourcetraining` pipeline, and automatically loaded from the shared drive when creating the `SpacyTokenizer`.

#### Usage

```python
from psynlp.preprocessing import SpacyTokenizer
st = SpacyTokenizer(spacy_model="spacy_model_name")
st.tokenize("Deze tekst gaat over <PERSOON-1>.")
>>> ['Deze', 'tekst', 'gaat', 'over', '<PERSOON-1>', '.']
```

## API

### Normalizer::initialization
```python
bn = BasicNormalizer()
```

### Normalizer::functions
| Function| Description | Returns 
| - | - | - | 
`bn.normalize(text)` | Normalize text | `text`

### Normalizer::interface

```python
class CustomNormalizer(Normalizer):
	def normalize(self, text):
		return text
```

### SentenceSplitter::initialization

```python
bss = BasicSentenceSplitter(verbose=False, 
			    normalizer=None)
```
| Field | Description | 
| - | - |
`verbose` | Verbosity 
`normalizer` | An instance of the `Normalizer` class, such as a `BasicNormalizer` or `None` if texts should not be normalized

### SentenceSplitter::functions

| Function| Description | Returns 
| - | - | - | 
`bss.split(text)` | Split a text into sentences. | `[sentence]`
`bss.process_dataframe(dataframe, hash_var, text_columns)` | Processes a `dataframe` by splitting the texts in `text_columns` into separate rows, requires a unique `hash_var` | exploded dataframe



### SentenceSplitter::interface 

```python
class CustomSentenceSplitter(SentenceSplitter):
	def _process_text(self, text): # before splitting
		return text
		
	def split(self, text): # defines how to split
		return text
			
	def _process_sentence(self, sentence): # post process sentence after splitting
		return sentence
```

### Tokenizer::initialization

```python
st = SpacyTokenizer(spacy_model)
```
| Field | Description | 
| - | - |
`spacy_model` | The spacy model to use from global resources

### Tokenizer::functions

| Function| Description | Returns 
| - | - | - | 
`st.tokenize(text)` | Tokenize the text | `[tokens]`

### Tokenizer::interface

```python
class CustomTokenizer(Tokenizer):
	def tokenize(self, text):
		return(text)
``` 		

