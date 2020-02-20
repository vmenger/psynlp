import unidecode
import re

from abc import ABC, abstractmethod


class Normalizer(ABC):

    def _replace_special_characters(self, text):
        return unidecode.unidecode(text)

    def _remove_double_whitespaces(self, text):
        return re.sub(" +", " ", text)

    def _remove_double_newlines(self, text):
        return re.sub("\n+", "\n", text)

    @abstractmethod
    def normalize(self, text):
        pass


class BasicNormalizer(Normalizer):

    def _replace_ranges(self, text):
        return re.sub(" - ", "-", text)

    def normalize(self, text):

        text = self._replace_ranges(text)

        text = self._replace_special_characters(text)

        text = self._remove_double_whitespaces(text)

        text = self._remove_double_newlines(text)

        return text
