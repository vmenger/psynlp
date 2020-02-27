import pandas as pd

import spacy
import glob
import os
import re
import unidecode

from psynlp.spelling.editdisttrie import EditDistTrie
from psynlp.spelling.rankers import NoisyRanker, EmbeddingRanker
from psynlp.utils import get_global_resource, get_local_resource

KNOWN_RANKERS = ['noisy', 'embedding']


class SpellChecker:

    def __init__(self,
                 spacy_model,
                 frequency_threshold=50,
                 use_ranker="noisy",
                 many_texts=False,
                 verbose=False):

        self.verbose = verbose
        self.frequency_threshold = frequency_threshold
        self.many_texts = many_texts

        # tokenizer
        self._init_tokenizer(spacy_model)

        # lexicon
        self._init_lexicon()

        # tries
        self._init_tries()

        # ranker
        self._init_ranker(use_ranker)

    def _init_tokenizer(self):
        if self.verbose:
            print("", "=== Initializing spacy tokenizer ===")

        nlp_model_path = get_global_resource(
            os.path.join('spacy', spacy_model))
        
        nlp = spacy.load(nlp_model_path)
        self.tokenize = lambda x: nlp(x, disable=['tagger', 'parser', 'ner'])

    def _init_lexicon(self):

        if self.verbose:
            print("\n", "=== Initializing lexicon ===")

        self.lexicon = set([])

        # Initialize by reading all files in lexicons/*.txt and adding to the lexicon
        lexicon_path = get_local_resource('lexicons')

        for path in glob.glob(os.path.join(lexicon_path, '*.txt')):

            with open(path, 'r') as file:
                words = file.read().split("\n")

            if self.verbose:
                print("> Adding {} words to lexicon from {}".format(
                    len(words), path))

            self._add_vocab_to_lexicon(words)

        token_frequencies = pd.read_csv(
            get_global_resource('token_frequencies.csv'))

        token_frequencies = token_frequencies[token_frequencies['token'].notnull()]

        self.token_freq_dict = dict(
            zip(token_frequencies['token'], token_frequencies['frequency']))

        # Add frequent tokens to the lexicon
        token_frequencies = token_frequencies[token_frequencies['frequency'] > self.frequency_threshold]
        frequent_tokens = list(token_frequencies['token'])

        if self.verbose:
            print("> Adding {} frequent tokens to lexicon (threshold={})".format(
                len(frequent_tokens), self.frequency_threshold))

        self._add_vocab_to_lexicon(frequent_tokens)

    def _add_vocab_to_lexicon(self, vocabulary_list):
        # Add a list of vocabulary to the lexicon

        # Iterate over words
        for word in vocabulary_list:

            # If not empty
            if (len(word) > 0) and len(self.tokenize(word)) == 1:

                # Add after lowercasing and remapping special characters
                self.lexicon.add(unidecode.unidecode(word.lower()))

        if self.verbose:
            print("> Lexicon size = {}".format(len(self.lexicon)))

    def _init_tries(self):
        # Initialize a single trie (if many_texts == False) or else multiple tries

        if self.verbose:
            print("\n", "=== Initializing EditDistTrie ===")

        # Case where many texsts are to be corrected
        if self.many_texts:

            self.match_tries = {}

            # Min and max length
            min_len = min([len(word) for word in self.lexicon])
            max_len = max([len(word) for word in self.lexicon]) + 1

            # Init trie(i) with words of length in range <i-2, i+2>
            for i in range(min_len, max_len):
                self.tries[i] = EditDistTrie([word for word in self.lexicon if abs(len(word) - i) <= 2])

        # Otherwise only one trie is needed
        else:
            self.match_trie = EditDistTrie(self.lexicon)

    def _init_ranker(self, use_ranker):

        if self.verbose:
            print("\n", "=== Initialize ranker ===")
            print("> Using {} ranker".format(use_ranker))

        if use_ranker not in KNOWN_RANKERS:
            raise ValueError("Unknown ranker specified ({}), choose from: {}".format(
                use_ranker, KNOWN_RANKERS))

        if use_ranker == "noisy":
            self.ranker = NoisyRanker()
        elif use_ranker == "embedding":
            self.ranker = EmbeddingRanker()

    # Public add_vocab method, also re-initializes the tries
    def add_vocab(self, vocabulary_list):

        self._add_vocab(vocabulary_list)
        self._init_tries()

# Determine whether a token is a valid compound token,
# for instance behandelplanbespreking = behandelplan + bespreking
    def _is_compound_token(self, token):

        for i in range(1, len(token)):

            # Split into a left and right part
            left = token[0:i]
            right = token[i:len(token)]

            # Accept if both parts are in the lexicon and at least 3 characters long
            if len(left) >= 3 and len(right) >= 3 and left in self.lexicon and right in self.lexicon:
                return (left, right)

    # Determine whether a token is a valid compound token separated by a 's' or a '-',
    # for instance weekend-verlof = weekend + verlof
    def _is_compound_infix_token(self, token):

        # Iterate over possible splits
        for m in re.finditer("[s-]+", token):

            # Split into left and right part
            left = token[0:m.start()]
            right = token[m.end():len(token)]

            # Accept if both parts are in the lexicon and at least 3 characters long
            if len(left) >= 3 and len(right) >= 3 and left in self.lexicon and right in self.lexicon:
                return(left, right)

    def _contains_numeric(self, token):
        if re.search(r"\d", token):
            return True
        else:
            return False

    def _is_misspelling(self, token):

        if self._contains_numeric(token):
            return False

        if token in self.lexicon:
            return False

        if self._is_compound_token(token) or self._is_compound_infix_token(token):
            return False

        # Other cases are misspellings
        return True

    # Search all matches for a word in the lexicon with edit_distance <= max_cost
    def _search_matches(self, word, max_edit_distance=2):

        # Determine max_cost
        if len(word) <= 3:
            max_edit_distance = 1

        # Find the appropriate trie
        if self.many_texts:
            search_trie = self.match_tries[len(word)]
        else:
            search_trie = self.match_trie

        # Return matches
        return search_trie.search_matches(word, max_edit_distance)

    # Find misspellings in text
    # returns [(misspelling:str, start_idx:int, end_idx:int, context:[str])]
    def find_misspellings(self, text, context_window=10):

        misspelling_tuples = []

        doc = self.tokenize(text)

        for token in doc:

            # If token is a misspelling
            if self._is_misspelling(token.text.lower()):

                # Extract context
                context = [token_sub.text for token_sub in doc[max(
                    token.i - context_window, 0):token.i + context_window]]

                # Append to tuples
                misspelling_tuples.append(
                    (token.text, token.idx, token.idx + len(token), context))

        return misspelling_tuples

    # Select most appropriate correction based on the ranker
    # returns [(misspelling:str, start_idx:int, end_idx:int, best_correction:str)]
    def find_corrections(self, text):

        correction_tuples = []

        for (misspelled_word, start_idx, end_idx, context) in self.find_misspellings(text):

            best_correction = self.ranker.best_candidate(misspelled_word,
                                                         self._search_matches(
                                                             misspelled_word),
                                                         context)

            # Append to tuples
            correction_tuples.append(
                (misspelled_word, start_idx, end_idx, best_correction))

        return correction_tuples

    # Find misspellings, corrections and replace them in the text
    def correct(self, text):

        correction_tuples = self.find_corrections(text)

        # sort from last to first
        # so that indexes keep matching when replacing multiple misspellings
        correction_tuples.sort(key=lambda tup: tup[1], reverse=True)

        for (_, start_idx, end_idx, correction) in correction_tuples:

            if correction is not None:

                text = text[0:start_idx] + correction + text[end_idx:]

        return text
