class Rule:
    '''
    Simple class representing a rule.
    '''

    def __init__(self, level, position):
        '''
        Create a new rule.

        Arguments:
            level (Enum member) - The level, e.g. NegationContext.NEGATED
            position (str) - The position, i.e. preceding, following, pseudo, termination
        '''
        self.level = level
        self.position = position


class MatchedRule:
    '''
    Simple class representing a matched rule.
    '''

    def __init__(self, token_start, token_end, level, position, text):
        '''
        Create a new matched rule.

        Arguments:
            token_start (int) - The first token index in the sentence
            token_end (int) - The last token index in the sentence
            level (Enum member) - The level, e.g. NegationContext.NEGATED
            position (str) - The position, i.e. preceding, following, pseudo, termination
            text (str) - The text that was matched
        '''

        self.token_start = token_start,
        self.token_end = token_end,
        self.level = level
        self.position = position
        self.text = text

        # Context class (e.g. NegationContext, HistoricalContext, etc)
        self.context_class = type(level).__name__

    def __str__(self):
        '''
        Simple string method. 
        '''
        return "token_span = ({}, {}), level={}, position={}, text={}".format(self.token_start,
                                                                              self.token_end,
                                                                              self.level,
                                                                              self.position,
                                                                              self.text
                                                                              )

    def __repr__(self):
        '''
        Simple repr method. 
        '''
        return "({})".format(str(self))