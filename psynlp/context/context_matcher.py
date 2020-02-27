import numpy as np

from itertools import chain

import spacy

from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

from psynlp.context.rule import Rule
from psynlp.context.rule import MatchedRule

import re

from psynlp.utils import get_global_resource

KNOWN_CONTEXTS = ['experiencer', 'negation', 'plausibility', 'temporality']

POSITION_TO_IND = {'preceding': 0,
                   'following': 1,
                   'pseudo': 2,
                   'termination': 3
                   }


class ContextMatcher:
    '''
    Detexts context of entities in text.
    '''

    def __init__(self, spacy_model, add_preconfig_triggers=True):

        # Nlp (tokenizer)
        spacy_model_path = get_global_resource(
            'spacy/{}'.format(spacy_model))
        self._nlp = spacy.load(spacy_model_path)

        # Init phrase matcher for matching phrases
        self.phrase_matcher = PhraseMatcher(self._nlp.vocab, attr="LOWER")

        # Init pattern matcher for matching spacy patterns
        self.pattern_matcher = Matcher(self._nlp.vocab, validate=True)

        # Init empty dict of regexp patterns for matching regexps
        self.trigger_regexps = {}

        # Dictionary from rule_keys to to rule. Will keep track of the rule that was triggered,
        # since the spacy matcher can only identify a rule using a string. Later on we can
        # the process the matches appropriately.
        self._rule_key_to_rule = {}
        self._num_rules = 0

        # List of context_classes (e.g. NegationContext, HistoricalContext)
        self._context_classes = []

        # Initially, there are no matches
        self._matched_rules = None

        # Length of the sentence
        self._sentence_length = None

        # Add preconfig triggers
        if add_preconfig_triggers:
            self._add_preconfig_triggers()

    def get_context_classes(self):
        return self._context_classes

    def _add_preconfig_triggers(self):
        '''
        Add all preconfigured contexts. Needs to be updated manually for new contexts
        '''

        for c in KNOWN_CONTEXTS:
            self._add_preconfig_context(c)

    def _add_rule_(self, rule):
        '''
        Add a new rule, by creating a key and adding it to rule_key_to_rule

        Arguments:
        rule (Rule) - The new rule.

        '''

        # Determine rule_key
        self._num_rules += 1
        rule_key = "rule_{}".format(self._num_rules)

        # Add to dictionary
        self._rule_key_to_rule[rule_key] = rule

        # Return the key
        return rule_key

    def _add_preconfig_context(self, context_string):

        if context_string not in KNOWN_CONTEXTS:
            raise NameError(
                "Preconfigured context {} does not exist".format(context_string))

        else:

            if context_string == "experiencer":
                from psynlp.context.triggers import ExperiencerContext, experiencer_triggers
                self.add_custom_context(
                    ExperiencerContext, experiencer_triggers)

            elif context_string == "negation":
                from psynlp.context.triggers import NegationContext, negation_triggers
                self.add_custom_context(NegationContext, negation_triggers)

            elif context_string == "plausibility":
                from psynlp.context.triggers import PlausibilityContext, plausibility_triggers
                self.add_custom_context(
                    PlausibilityContext, plausibility_triggers)

            elif context_string == "temporality":
                from psynlp.context.triggers import TemporalityContext, temporality_triggers
                self.add_custom_context(
                    TemporalityContext, temporality_triggers)

    def add_custom_context(self, context_class, triggers):

        # Add to context classes
        self._context_classes.append(context_class)

        # Iterate over the triggers
        for trigger_key, trigger_list in triggers.items():

            # Unpack key
            # rule_level, e.g. NegationContext.NEGATED
            # rule_type, e.g. phrase, pattern, regexp
            # rule_position, e.g. preceding, following, psuedo, termination
            (rule_level, rule_type, rule_position) = trigger_key

            # If there are triggers in the list
            if len(trigger_list) > 0:

                # Create a new rule and, determine a key
                new_rule = Rule(level=rule_level,
                                position=rule_position)

                rule_key = self._add_rule_(new_rule)

                # Phrases (in the phrase matcher)
                if rule_type == "phrase":

                    nlp_phrases = list(self._nlp.tokenizer.pipe(trigger_list))
                    self.phrase_matcher.add(rule_key, [*nlp_phrases])

                # Patterns (in the pattern matcher)
                elif rule_type == "pattern":

                    self.pattern_matcher.add(rule_key, trigger_list)

                # Regepxs (in a list)
                elif rule_type == "regexp":

                    for regexp in trigger_list:
                        self.trigger_regexps[rule_key] = regexp

                else:
                    raise NameError(
                        "Rule type {} does not exist".format(rule_type))

    def _match_spacy_triggers(self, doc, matcher):

        matches = matcher(doc)

        # Process phrase and pattern matches
        for match_id, token_start, token_end in matches:

            # Find the match type and tokens
            rule_key = self._nlp.vocab.strings[match_id]
            rule = self._rule_key_to_rule[rule_key]
            match_tokens = doc[token_start:token_end]

            # Create a MatchedRule object that will be further processed later
            matched_rule = MatchedRule(token_start=token_start,
                                       token_end=token_end,
                                       level=rule.level,
                                       position=rule.position,
                                       text=match_tokens)

            self._matched_rules.append(matched_rule)

    def _match_regexp_triggers(self, text, doc):

        # Process regexps
        for rule_key in self.trigger_regexps:

            # Obtain rule
            rule = self._rule_key_to_rule[rule_key]

            # Iterate over matches
            for match in re.finditer(self.trigger_regexps[rule_key], text):

                # Determine span
                char_start, char_end = match.span()
                span = doc.char_span(char_start, char_end)  # todo beter fixen

                # If the span is not empty
                if span is not None:

                    # Create a MatchedRule object that will be further processed later
                    matched_rule = MatchedRule(token_start=span.start,
                                               token_end=span.end,
                                               level=rule.level,
                                               position=rule.position,
                                               text=span
                                               )

                    self._matched_rules.append(matched_rule)

    def _match_triggers(self, text):

        # Initialize
        self._matched_rules = []

        # Spacy tokenize document and find matches using the spacy matchers
        doc = self._nlp(text, disable=['parser', 'ner'])
        self._sentence_length = len(doc)

        self._match_spacy_triggers(doc, self.phrase_matcher)
        self._match_spacy_triggers(doc, self.pattern_matcher)

        self._match_regexp_triggers(text, doc)

    def _split_matches_per_context(self):

        # Matched rules per context class
        context_class_to_matched_rules = {}

        # Iterate over the context classes (e.g. NegationContext,
        # HistoricalContext) to divide the rules in each class
        for context_class in self._context_classes:

            # Empty list of matched rules per context class
            context_class_to_matched_rules[context_class.__name__] = []

        # Iterate over the context classes (e.g. NegationContext,
        # TemporalityContext) to divide the rules in each class
        for matched_rule in self._matched_rules:
            context_class_to_matched_rules[matched_rule.context_class].append(
                matched_rule)

        return (context_class_to_matched_rules)

    def _get_initialized_token_mask(self, level_dim, matched_rules):

        # Create a numpy array with token_mask, with three dimensions:
        # axis=0   Level (level 0 = nonexisting, level 1 = default (RECENT/AFFIRMED) and will not be used)
        # axis=1   Position
        # axis=2   Sentence length
        token_mask = np.zeros((level_dim,
                               len(POSITION_TO_IND.keys()),
                               self._sentence_length)
                              )

        # Iterate over the matched rules
        for matched_rule in matched_rules:

            # Set token_mask to 1 where rules are matched
            token_mask[matched_rule.level.value,
                       POSITION_TO_IND[matched_rule.position],
                       matched_rule.token_start[0]:matched_rule.token_end[0]] = 1

        return token_mask

    def _forward_fill_token_mask(self, token_mask, level_dim):

        # Forward fill preceding triggers
        # Iterate over levels
        for j in range(2, level_dim):

            # Fill value
            pre_shift = 0

            # Iterate over tokens
            for i in range(self._sentence_length):

                # If matches a preceding trigger and no pseudo trigger, set fill value to 1
                if (token_mask[j, POSITION_TO_IND['preceding'], i] == 1) and (token_mask[j, POSITION_TO_IND['pseudo'], i] == 0):
                    pre_shift = 1

                # If matches a termination trigger, set fill value to 0
                if (token_mask[j, POSITION_TO_IND['termination'], i] == 1):
                    pre_shift = 0

                # Change to fill value
                token_mask[j, POSITION_TO_IND['preceding'], i] = pre_shift

        return (token_mask)

    def _backward_fill_token_mask(self, token_mask, level_dim):

        # Iterate over levels
        for j in range(2, level_dim):

            # Fill value
            post_shift = 0

            # Iterate over tokens in reversed order
            for i in reversed(range(self._sentence_length)):

                # If matches a following trigger and no pseudo trigger, set fill value to 1
                if (token_mask[j, POSITION_TO_IND['following'], i] == 1) and (token_mask[j, POSITION_TO_IND['pseudo'], i] == 0):
                    post_shift = 1

                # If matches a termination trigger, set fill value to 0
                if (token_mask[j, POSITION_TO_IND['termination'], i] == 1):
                    post_shift = 0

                # Change to fill value
                token_mask[j, POSITION_TO_IND['following'], i] = post_shift

        return (token_mask)

    def _process_token_mask(self, token_mask, level_dim):

        # Take the maximum of the 'preceding' and 'following masks'
        token_mask = np.max(token_mask[:, :2, :], axis=1)

        # Multiply with range to obtain index
        token_mask = token_mask * np.arange(level_dim).reshape(-1, 1)

        # Take maximum over levels
        token_mask = np.max(token_mask, axis=0)

        # Make sure default is used when nothing matches
        token_mask[token_mask == 0] = 1

        return (token_mask)

    def _get_token_mask_per_class(self, context_class, context_class_to_matched_rules):

        # Fetch rules
        matched_rules = context_class_to_matched_rules[context_class.__name__]

        # If there are no rules, revert to default label
        if len(matched_rules) == 0:
            token_mask = np.ones(self._sentence_length).reshape(-1, 1)

        # Otherwise compute token_mask
        else:

            # Level dimensionality is determined by the value of the largest level
            level_dim = max(
                [matched_rule.level.value for matched_rule in matched_rules]) + 1

            token_mask = self._get_initialized_token_mask(level_dim,
                                                          matched_rules)

            token_mask = self._forward_fill_token_mask(token_mask,
                                                       level_dim)

            token_mask = self._backward_fill_token_mask(token_mask,
                                                        level_dim)

            token_mask = self._process_token_mask(token_mask,
                                                  level_dim)

        return token_mask

    def _process_matches(self, entities):

        if self._matched_rules is None:
            raise NameError("Matcher not yet called.")

        context_class_to_matched_rules = self._split_matches_per_context()

        # Iterate over context classes (e.g. NegationContext)
        for context_class in self._context_classes:

            token_mask = self._get_token_mask_per_class(
                context_class, context_class_to_matched_rules)

            # For each entity, add appropriate label
            for entity in entities:

                # Take the lowest match
                enum_value = np.min(
                    token_mask[entity.token_start:entity.token_end])
                enum_label = context_class(enum_value).name
                entity.add_context(enum_label)

    def match_context(self, text, entities):

        if len(entities) > 0:

            self._match_triggers(text)

            self._process_matches(entities)
