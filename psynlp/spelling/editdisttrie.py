""" 
This module contains functionality for the EditDistTrie class. 
Taken (and slightly adapted) from: http://stevehanov.ca/blog/?id=114
"""


class EditDistTrie:
    """ An EditDistTrie a fast way to lookup all matches with edit_dist <= max_cost in a lexicon """

    def __init__(self, lexicon):
        """ Initalize using the lexicon """

        self._trie = _TrieNode()

        for word in lexicon:
            self._trie.insert(word)

    def search_matches(self, word, max_cost=2):
        """
        The search function returns a list of all words that are less than the given
        maximum distance from the target word
        """

        # build first row
        current_row = range(len(word) + 1)

        results = []

        # recursively search each branch of the trie
        for letter in self._trie.children:
            self._searchRecursive(self._trie.children[letter],
                                  letter,
                                  word,
                                  current_row,
                                  results,
                                  max_cost)

        return results

    def _searchRecursive(self, node, letter, word, previous_row, results, max_cost):
        """ 
        This recursive helper is used by the search function above. It assumes that
        the previous_row has been filled in already.
        """

        columns = len(word) + 1
        current_row = [previous_row[0] + 1]

        # Build one row for the letter, with a column for each letter in the target
        # word, plus one for the empty string at column 0
        for column in range(1, columns):

            insert_cost = current_row[column - 1] + 1
            delete_cost = previous_row[column] + 1

            if word[column - 1] != letter:
                replace_cost = previous_row[column - 1] + 1
            else:
                replace_cost = previous_row[column - 1]

            current_row.append(min(insert_cost, delete_cost, replace_cost))

        # if the last entry in the row indicates the optimal cost is less than the
        # maximum cost, and there is a word in this trie node, then add it.
        if current_row[-1] <= max_cost and node.word is not None:
            results.append((node.word, current_row[-1]))

        # if any entries in the row are less than the maximum cost, then
        # recursively search each branch of the trie
        if min(current_row) <= max_cost:
            for letter in node.children:
                self._searchRecursive(node.children[letter],
                                      letter,
                                      word,
                                      current_row,
                                      results,
                                      max_cost)


class _TrieNode:
    """
    The Trie data structure keeps a set of words, organized with one node for
    each letter. Each node has a branch for each letter that may follow it in the
    set of words.
    """

    def __init__(self):
        """ Init """

        self.word = None
        self.children = {}

    def insert(self, word):
        """ Insert word """

        for letter in word:
            if letter not in self.children:
                self.children[letter] = _TrieNode()

            self = self.children[letter]

        self.word = word