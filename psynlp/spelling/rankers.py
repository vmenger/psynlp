from nltk import edit_distance
from doublemetaphone import doublemetaphone

from gensim.models import Word2Vec

import numpy as np
import pandas as pd

from psynlp.utils import get_global_resource

from abc import ABC, abstractmethod


class Ranker(ABC):

    def __init__(self):
        self.optimum_func = None

    def best_candidate(self, misspelled_word, candidates, context):

        scored_candidates = self.score_candidates(
            misspelled_word, candidates, context)

        if len(scored_candidates) == 0:
            return None

        best_tup = self.optimum_func(scored_candidates, key=lambda tup: tup[1])

        return best_tup[0]

    @abstractmethod
    def score_candidates(self, misspelled_word, candidates, context):
        """
        Scores a number of candidates to consider for replacing the misspelling.

        Args:
            misspelled_word (token:str) The misspelled word
            candidates [(candidate:str, edit_distance:int)] A list of possible candidates to consider
            context [token:str] The context of the misspelling, as a list of strings

        Returns:
            A list of tupes [(candidate:str, score:int)]

        """
        pass


class NoisyRanker(Ranker):
    """
    Ranks based on the Noisy model by Lai (2005), using edit distance and phonetic edit distance
    Taken (and adapted) from: https://github.com/clips/clinspell/blob/master/code/ranking_experiments.py
    """

    def __init__(self):

        token_frequencies = pd.read_csv(
            get_global_resource('token_frequencies.csv'))

        self.frequency_dict = dict(
            zip(token_frequencies['token'], token_frequencies['frequency']))

        self.optimum_func = min

    def score_candidates(self, misspelled_word, candidates, context):

        rank_words = []
        rank_scores = []

        # Iterate over candidates, edit distances already computed when generating candidates
        for (candidate, orthographic_edit_distance) in candidates:

            # Compute phonetic edit distance using the double metaphone algorithm
            phonetic_edit_distance = edit_distance(doublemetaphone(misspelled_word)[0],
                                                   doublemetaphone(candidate)[0])

            # Compute spell score
            spell_score = (2 * orthographic_edit_distance +
                           phonetic_edit_distance) ** 2  # P(m|c)

            # Try to find the frequency, or assume frequency of 1 if not known word
            try:
                frequency = self.frequency_dict[candidate]
            except KeyError:
                frequency = 1

            # Compute score
            frequency_score = 1 / (1 + np.log(frequency))  # P(c)
            score = spell_score * frequency_score  # P(c|m) = P(m|c)*P(c)

            # Store word and score
            rank_words.append(candidate)
            rank_scores.append(score)

        # Return as a list of tuples (candidate, score)
        return list(zip(rank_words, rank_scores))


class EmbeddingRanker(Ranker):
    """
    Ranks based on word embeddings
    """

    def __init__(self):
        """ Initialize by loading the word2vec model """

        self.w2v_model = Word2Vec.load(
            get_global_resource('gensim/word2vec.model'))
        self.optimum_func = max

    def score_candidates(self, misspelled_word, candidates, context):

        # Empty lists
        rank_words = []
        rank_scores = []

        # Map words to word2vec id and to distance
        word2idx_context = {}
        word2idx_candidates = {}
        word2dist = {}

        # Iterate over words in the context
        for context_word in context:
            if context_word in self.w2v_model.wv:
                word2idx_context[context_word] = self.w2v_model.wv.vocab[context_word].index

        # Iterate over candidates
        for candidate_word, distance in candidates:
            if candidate_word in self.w2v_model.wv:
                word2idx_candidates[candidate_word] = self.w2v_model.wv.vocab[candidate_word].index
                word2dist[candidate_word] = distance

        # Obtain context vectors
        context_vectors = self.w2v_model.wv.vectors[list(
            word2idx_context.values())]

        # Compute probability values
        composed_vector = np.sum(context_vectors, axis=0) / \
            len(word2idx_context.keys())
        prob_values = np.exp(
            np.dot(composed_vector, self.w2v_model.trainables.syn1neg.T))
        prob_values /= sum(prob_values)

        # For each candidate
        for candidate_word in word2idx_candidates.keys():

            # Normalize by dividing over edit distance
            score = prob_values[word2idx_candidates[candidate_word]
                                ] / word2dist[candidate_word]

            # Append to lists
            rank_words.append(candidate_word)
            rank_scores.append(score)

        # Return as a list of tupes (candidate, score)
        return list(zip(rank_words, rank_scores))
