# `spelling` --- The `psynlp` module for detecting and correcting spelling errors in clinical text. 

The `spelling` submodule implements functionality for detecting spelling errors, generating and ranking replacement candidates, and using this as input to correct spelling errors. Correcting text is done using the `SpellChecker` class, while rankers are implemented in the `Ranker` class. 

The general flow for correcting spelling consists of three steps:

1. Find misspelled tokens -- find misspelled tokens based on OpenTaal word lists and a medical lexicon (found in `psynlp/resources/lexicons/*.txt`). Since these words combined do not (nearly) cover all terms used in clinical psychiatric text, we also add all tokens with a frequency >= `frequency_threshold`, as counted in all `decursus` and `rapportage` texts. Some additional logic is implemented, such as looking for compound words (behandelplanbespreking = behandelplan + bespreking) and checking whether there are numeric characters in a token. 

2. Suggest replacements -- based on the same lexicon used above, candidates are suggested based on similarity measured by edit distance (default <= 2). The `EditDistTrie` is used to suggest these candidates.

3. Find the best replacement -- the best candidate out of all suggested replacements is determined by a ranker. Currently, two rankers are implemented: `NoisyRanker`,  based on the noisy channel model (Lai, 2015), and `EmbeddingRanker`,  based on word embeddings and misspelling context. Anecdotally, they work roughly equally well. By default the `NoisyRanker` is used. 

## Usage
```python
from psyspell.spelling import SpellChecker
sp = SpellChecker(spacy_model="model_name")
sp.correct("patient is bekend met een depresieve stoornis")
>>> "patient is bekend met een depressieve stoornis"
```

## API

### SpellChecker::initialization

```python
sc = SpellChecker(frequency_threshold=50,
	          use_ranker='noisy',
      	          many_texts=False,
	          verbose=False
```

| Field | Description | 
| - | - |
`spacy_model` | The name of the spacy model that should be included in the global resource folder
`frequency_threshold` | The threshold for tokens to be included in the lexicon.
`use_ranker` | The ranker to be used. Full list is in the `KNOWN_RANKERS` variable, currently `['noisy', 'embedding']`
`many_texts` | Set to True when processing many texts (>10000-ish). Will take some extra time to initialize but processing will be faster.
`verbose` | Verbosity

### SpellChecker::functions

| Function| Description | Returns 
| - | - | - | 
`sc.add_vocab(vocabulary_list)` | Add more vocabulary to the lexicon of known words. | --
`sc.find_misspellings(text, context_window=10)` | Find misspellings in a text. | `[(misspelling, start_idx, end_idx, [context])]`
`sc.correct_misspellings(text)` | Suggest best for misspellings obtained in `find_misspellings` using the `Ranker` | `[(misspelling, start_idx, end_idx, best_correction)]` 
`sc.correct(text)` | Correct and return text | `text`

### Ranker::initialization
```python
r_noisy = NoisyRanker()
r_embed = EmbeddingRanker()
```

### Ranker::functions

| Function| Description | Returns 
| - | - | - | 
`best_candidate(misspelled_word, candidates, context)` | Determine the best candidate replacement for a misspelling, potentially using its context. | `(best_candidate, score)`
`score_candidates(misspelled_word, candidates, context)` | Determine a score that ranks the candidate replacements | `[(candidate, score)]`



### Ranker::Interface

Use the following interface to define a custom ranker, and then in `spellchecker.py` add it to `KNOWN_RANKERS` and  `_init_ranker()`

```python
class CustomRanker(Ranker):
	def __init__(self):
		pass

	def score_candidates(self, misspelled_word, candidates, context):
		return [(candidate, score)]
```
