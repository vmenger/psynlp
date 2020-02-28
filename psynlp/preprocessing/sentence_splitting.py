import glob
import re

import nltk

from psynlp.utils import get_local_resource

from abc import ABC, abstractmethod


class SentenceSplitter(ABC):

    def __init__(self, verbose=False, normalizer=None):

        self.verbose = verbose

        # Abbreviations
        self.abbreviations = []
        self._load_abbreviations()

        # # NLTK sentence tokenizer
        nltk_pickle_filepath = get_local_resource('nltk/dutch.pickle')

        self.sentence_tokenizer = nltk.data.load(
            "file:{}".format(nltk_pickle_filepath))

        self._init_normalizer(normalizer)

    def _init_normalizer(self, normalizer):
        if normalizer is None:

            from psynlp.preprocessing import BasicNormalizer
            self.normalizer = BasicNormalizer()

        else:

            self.normalizer = normalizer

    def _load_abbreviations(self):

        self._read_abbreviations()

        self._deduplicate_abbreviations()

        self._sort_abbreviations()

        if self.verbose:
            print("Using {} abbreviations".format(len(self.abbreviations)))

    def _read_abbreviations(self):

        abbreviation_filepaths = get_local_resource(
            'abbreviation_lists/*.txt')

        for abbrev_filepath in glob.glob(abbreviation_filepaths):

            with open(abbrev_filepath) as abbrev_file:

                for abbreviation in abbrev_file.readlines():

                    # remove \n at end of line
                    self.abbreviations.append(abbreviation[:-1])

    def _deduplicate_abbreviations(self):

        # Remove duplicates
        self.abbreviations = list(set(self.abbreviations))

    def _sort_abbreviations(self):

        # Sort based on length so that e.g. 'medepat.' is mateched before 'pat.'
        self.abbreviations.sort(key=len, reverse=True)

    # Gebruikt om de punten (.) in afkortingen te verwijderen zonder daarbij op hoofdletter te matchen
    def _replace_ignorecase(self, find, replace, text):

        re_pattern = re.compile(find, re.IGNORECASE)
        text = re_pattern.sub(replace, text)

        return (text)

    def _remove_periods_from_abbreviations(self, text):

        for abbreviation in self.abbreviations:
            text = self._replace_ignorecase("(?<!\w){}".format(
                re.escape(abbreviation)), abbreviation.replace(".", ""), text)

        return (text)

    def _replace_period_in_numeric_context(self, text):

        # Wanneer er cijfers gevolgd worden door een punt (bijvoorbeeld 1. in een tussenkopje), en er daarna geen cijfer
        # volgt (dus niet 2.5 mg), verwijderen we de punt. Dit helpt bij het splitsen op zinnen.
        text = re.sub("(\d+)\.([a-zA-Z])", "\\1 \\2", text)
        text = re.sub("(\d+)\.(?!\d)", "\\1", text)

        return(text)

    def _replace_tabs_with_whitespaces(self, text):
        return re.sub("\t", " ", text)

    def _trim_whitespaces(self, text):

        text = re.sub("^\s", "", text)  # start of text
        text = re.sub("\s$", "", text)  # end of text

        return (text)

    def _detect_enumerations(self, text, threshold=2):

        # Patroon voor het vinden van " - "-style opsommingen
        count_regexp = sum(1 for m in re.finditer(r"\s-\s[^0-9]", text))

        if count_regexp >= threshold:
            text = re.sub("\s-\s", "\n\n - ", text)

        return (text)

    def _melt_text_columns(self, dataframe, hash_var, text_columns):

        dataframe = dataframe.melt(id_vars=[hash_var], value_vars=text_columns) \
                             .rename(columns={'variable': 'stelling', 'value': 'text'}) \
                             .dropna(subset=['text']) \
                             .reset_index(drop=True)

        return dataframe

    def _explode_sentences(self, hash_var, dataframe):

        dataframe = dataframe.explode('text_sentences') \
                             .rename(columns={'text_sentences': 'text'})

        dataframe['sentence_counter'] = dataframe.groupby(
            [hash_var, "stelling"]).cumcount() + 1

        return dataframe

    @abstractmethod
    def _process_text(self, text, normalize=True):
        pass

    @abstractmethod
    def _process_sentence(self, sentence):
        pass

    @abstractmethod
    def split(self, text):
        pass

    def process_dataframe(self, dataframe, hash_var, text_columns):

        # Drop duplicates
        dataframe = dataframe.drop_duplicates(hash_var)

        dataframe = self._melt_text_columns(dataframe, hash_var, text_columns)

        dataframe['text_sentences'] = dataframe['text'].apply(
            lambda x: self.split(x))

        dataframe = dataframe.drop(['text'], 1)

        dataframe = self._explode_sentences(hash_var, dataframe)

        return(dataframe)


class BasicSentenceSplitter(SentenceSplitter):

    def _process_text(self, text, normalize=True):

        if normalize:
            text = self.normalizer.normalize(text)

        text = self._replace_period_in_numeric_context(text)

        text = self._remove_periods_from_abbreviations(text)

        text = self._replace_tabs_with_whitespaces(text)

        text = self._detect_enumerations(text)

        return (text)

    def _process_sentence(self, sentence):

        sentence = self._trim_whitespaces(sentence)

        return (sentence)

    def split(self, text):

        text = self._process_text(text)

        sentences_output = []

        # Splits eerst op witregels
        for newline in text.split("\n"):

            # Daarbinnen gebruiken we de sentence tokenizer van nltk
            for sentence in self.sentence_tokenizer.tokenize(newline):

                sentence = self._process_sentence(sentence)
                sentences_output.append(sentence)

        return (sentences_output)
