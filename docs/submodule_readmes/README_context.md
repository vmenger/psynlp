
# `context` --- The `psynlp` module for determining entity modifiers based on context

The `context` submodule can detect whether entities are (for instance) negated, historical, experienced by someone else, or hypothetical, based on the context of a sentence. 

## Triggers

There are four types of triggers:
1. Preceding triggers -- modify entities that *follow* the trigger
2. Following triggers -- modify entities that *precede* the trigger
3. Pseudo triggers -- triggers that look like a trigger, but should not be regarded as such (e.g. 'geen toename'). 
4. Termination triggers -- triggers that end the scope of preceding and following triggers.

There are three ways to match triggers:
1. Phrase -- A literal phrase, that can span multiple tokens (e.g. 'niet waarschijnlijk')
2. Pattern -- [A spacy pattern](https://spacy.io/usage/rule-based-matching)
3. Regexp -- A regexp, but beware this does not match based on tokens but on full text, e.g. matching for `somber` does not only match the literal token `somber`, but also the `somber` in ver`somber`d or `somber`der.

There are four types of preconfigured triggers:
1. Experiencer [`PATIENT`, `OTHER`] -- Whether the entity applies to the patient or another person (such as a family member). 
2. Negation [`AFFIRMED`, `NEGATED`] -- Whether the entity is affirmed or negated
3. Plausibility [`PLAUSIBLE`, `HYPOTHETICAL`] -- Whether the entity is plausible or hypothetical
4. Temporality [`RECENT`, `HISTORICAL`, `CONTINUOUS`] -- Whether an entity is recent (defined as present in the last two weeks but not before), historical (defined as present before two weeks ago, but not now) or continuous (defined as present before two weaks ago, and present currently). 

Triggers should be defined in a dictionary as such (it is not necessary to add empty trigger lists for irrelevant combinations): 
```python
negation_triggers = {}

negation_triggers[NegationContext.NEGATED, 'phrase', 'following'] = ['trigger_1', 'trigger_2', ... 'trigger_n']
```

The preconfigured sets of triggers triggers can be viewed in in `psynlp.context.triggers`. They are added by default to the `ContextMatcher`, but can be disabled using the `add_preconfig_triggers` flag. 

To define a custom context type, define an Enum class with at least two levels and triggers for each of them (see the classes in `psynlp.context.triggers`  for examples). 

## Usage

It's important to know that the `ContextMatcher` takes a *sentence*  as input -- using a full text as input will carry the scope of a single trigger throughout the entire text. 

``` python

from psynlp.entity import BasicEntityMatcher
from psynlp.context import ContextMatcher

entity_phrases = {}
entity_phrases['symptomen'] = ['boos', 'somber']
entity_phrases['diagnoses'] = ['depressie', 'psychose']

sentence = "Deze patient is niet somber, maar heeft wellicht wel een depressie."

bem = BasicEntityMatcher(entity_phrases)
entities = bem.extract_entities(sentence)

cm = ContextMatcher()
cm.match_context(sentence, entities)

print(entities)
[(token_span=(4, 5), rule=symptomen, text=somber, context=['PATIENT', 'NEGATED', 'PLAUSIBLE', 'CURRENT']), 
 (token_span=(11, 12), rule=diagnoses, text=depressie, context=['PATIENT', 'AFFIRMED', 'PLAUSIBLE', 'CURRENT'])]
```

## API

#### ContextMatcher::initialization

```python
cm = ContextMatcher(spacy_model,
		    add_preconfig_triggers=True)
```

| Field | Description | 
| - | - |
`spacy_model` | A spacy model that can be found in the global resources folder
`add_preconfig_triggers` | Whether to add the preconfigured `Negation`, `Experiencer`, etc triggers. 

#### ContextMatcher::functions

| Function| Description | Returns 
| - | - | - | 
`cm.get_context_classes()` | Find out what context classes are included | A list of context classes
`cm.add_custom_context(context_class, triggers)` | Add a custom context class, by adding a custom `Enum` class and a dictionary of `triggers` | `None`
`cm.match_context(text, entities)` | Match the context of the entities, and modify the `Entity` objects based on the context | `None`, but modifies the list of Entities. 

