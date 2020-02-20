from abc import ABC, abstractmethod

from psynlp.utils import get_global_resource

import spacy


class Tokenizer(ABC):

    @abstractmethod
    def tokenize(self, text):
        pass


class SpacyTokenizer(Tokenizer):

    def __init__(self, spacy_model):

        spacy_model_path = get_global_resource('spacy/{}'.format(spacy_model))

        self.nlp = spacy.load(spacy_model_path)

    def tokenize(self, text):

        doc = self.nlp(text, disable=['ner', 'tagger', 'parser'])

        return [token.text for token in doc]
