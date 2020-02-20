import spacy
from spacy.matcher import PhraseMatcher

from psynlp.entity import Entity

from psynlp.utils import get_global_resource

from abc import ABC, abstractmethod


class EntityMatcher(ABC):

    @abstractmethod
    def extract_entities(self, text):
        pass


class BasicEntityMatcher(EntityMatcher):
    '''
    A straightforward entity matcher, that outputs a list of entites that is found in a text.
    '''

    def __init__(self, entity_sets, spacy_model, case_sensitive=False):
        '''
        Initialize by adding the entities and the spacy model.

        Arguments
            entity_sets (dict) - A dictionary of entity sets, with entity_sets[rule_name] = [phrase_1, ..., phrase_n]
            nlp (spacy model) - A spacy model
            case_sensitive (boolean) - Whether the entity matcher should be case sensitive
        '''

        # Nlp (tokenizer)
        spacy_model_path = get_global_resource(
            'spacy/{}'.format(spacy_model))
        self.nlp = spacy.load(spacy_model_path)

        # Determine spacy attribute
        if case_sensitive:
            spacy_attr == "ORTH"
        else:
            spacy_attr = "LOWER"

        # Entity matcher
        self.ent_matcher = PhraseMatcher(self.nlp.vocab, attr=spacy_attr)

        for entity_key in entity_sets.keys():
            self.ent_matcher.add(
                entity_key, [*list(self.nlp.tokenizer.pipe(entity_sets[entity_key]))])

    def extract_entities(self, text):
        '''
        Extract the entities in the text, based on the entity_sets.

        Arguments:
            text (str) - The text in which entities should be matched.
        '''

        # Empty list of entities
        entities = []

        # Tokenize and run matcher
        doc = self.nlp(text)
        matches = self.ent_matcher(doc)

        # For each match found by the PhraseMatcher
        for match_id, token_start, token_end in matches:

            # Create a new entity
            entity = Entity(token_start=token_start,
                            token_end=token_end,
                            rule=self.nlp.vocab.strings[match_id],
                            text=doc[token_start:token_end],
                            )

            # Add to list of entities
            entities.append(entity)

        # Return
        return entities
