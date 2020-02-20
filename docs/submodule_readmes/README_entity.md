
# `entity` --- The `psynlp` module for matching entities in text

The `entity` submodule contains some very basic funcationality for extracting entities from text. 

A matcher is implemented in `BasicEntityMatcher`, which simply finds literal phrases using the Spacy matcher. Note that the context element of an `Entity` is not used by default. 

## Usage

```python
from psynlp.entity import BasicEntityMatcher

entity_phrases = {}
entity_phrases['symptoms'] = ['boos', 'somber', 'slaapt slecht'] # also accepts phrases
entity_phrases['diagnoses'] = ['depressie', 'psychose']

bem = BasicEntityMatcher(entity_phrases, spacy_model="spacy_model_name")
bem.extract_entities("Deze patient is somber, heeft wellicht een depressie.")
>>> [(token_span=(3, 4), rule=symptoms, text=somber), (token_span=(8, 9), rule=diagnoses, text=depressie)]
```

## API

#### BasicEntityMatcher::initialization
```python
bem = BasicEntityMatcher(entity_phrases,
			 spacy_model,
			 case_sensitive=False)
```
| Field | Description | 
| - | - |
`entity_phrases` | A dictionary of rule=>phrases pair, such as for instance under the Usage paragraph in this readme. 
`spacy_model` | The spacy model to load (by default `2_include_embeddings`  is used). 
`case_sensitive`  | Whether to match phrases case sensitive

#### BasicEntityMatcher::functions

| Function| Description | Returns 
| - | - | - | 
`extract_entities(text)` | Extract entities from a text | A set of `Entity` objects

#### EntityMatcher::interface

```python
class CustomEntityMatcher(EntityMatcher):
	def extract_entities(self, text):
		return entities
```

#### Entity::initialization
```python
e  = Entity(token_start,
		  token_end,
		  rule,
		  text)
```

| Field | Description | 
| - | - |
`token_start` | The index of the first token that is matched		
`token_end` | The index of the last token that is matched
`rule` | The rule of the dicationary that was matched
`text` | The exact text that was matched
