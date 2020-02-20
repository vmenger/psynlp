class Entity:
    '''
    A simple and straightforward class for representing entities in text. 
    '''

    def __init__(self, token_start, token_end, rule, text):
        '''
        Initialize new entity. 

        Arguments:
            token_start (int) - The index of the first token in the sentence
            token_end (int) - The index of the last token in the sentence
            rule (str) - The rule that was matched to find this entity (e.g. depressie)
            text (str) - The value of this entity (e.g. somber, depressief)
        '''

        # Register variables
        self.token_start = token_start
        self.token_end = token_end
        self.rule = rule
        self.text = text

        # Context is not (yet) detected, so initially empty
        self.context = None

    def add_context(self, context_element):
        '''
        Add a context element for this entity.

        Arguments:
            context_element (str): The label of the context element (e.g. RECENT, NEGATED, HYPOTHETICAL, etc)
        '''

        # Create empty set
        if self.context is None:
            self.context = []

        # Add the context element
        self.context.append(context_element)

    def __str__(self):
        ''' String method '''

        if self.context is not None:

            return "token_span=({}, {}), rule={}, text={}, context={}".format(self.token_start,
                                                                              self.token_end,
                                                                              self.rule,
                                                                              self.text,
                                                                              self.context
                                                                              )
        else:
            return "token_span=({}, {}), rule={}, text={}".format(self.token_start,
                                                                  self.token_end,
                                                                  self.rule,
                                                                  self.text,
                                                                  )

    def __repr__(self):
        ''' Repr method '''
        return "({})".format(str(self))
