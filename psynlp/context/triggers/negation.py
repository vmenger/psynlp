from enum import Enum

class NegationContext(Enum):
    AFFIRMED = 1
    NEGATED = 2

negation_triggers = {}

### Phrases
negation_triggers[NegationContext.NEGATED, 'phrase', 'preceding'] = [
    'afwezigheid van',
    'deed geen',
    'deed niet',
    'geen aanwijzing voor',
    'geen aanwijzingen voor',
    'geen abnormale',
    'geen bewijs voor',
    'geen klachten van',
    'geen klachten van',
    'geen oorzaak van ',
    'geen reden tot',
    'geen reden voor',
    'geen sprake van',
    'geen suggestie van',
    'geen teken van',
    'geen tekenen van',
    'geen',
    'is geen',
    'is niet',
    'konden geen',
    'konden niet',
    'kunnen geen',
    'kunnen niet', 
    'nam af',
    'negatief voor',
    'niet waarschijnlijk',
    'niet',
    'nooit last gehad van',
    'nooit',
    'ontkend',
    'ontkennend',
    'ontkent',
    'ontwikkelde geen',
    'ontwikkelde nooit',
    'ontwikkelt geen',
    'onwaarschijnlijk',
    'patient is niet',
    'patient was niet',
    'sluit uit',
    'subklinisch',
    'subklinische',
    'toonde geen',
    'toonde geen',
    'uitgesloten',
    'versus',
    'vrij van',
    'waren geen', 
    'waren niet', 
    'was geen',
    'was niet',
    'zijn geen', 
    'zijn niet',
    'zonder indicatie van ',
    'zonder teken van',
    'zonder tekenen van',
    'zonder',
]

negation_triggers[NegationContext.NEGATED, 'phrase', 'following'] = [
    # 'in remissie', eigenlijk is dit temporeel
    'afwezig',
    'is uitgesloten',
    'is verdwenen',
    'is weg',
    'kan worden uitgesloten',
    'laag ingeschat',
    'nam af',
    'niet aan de orde',
    'niet aanwezig',
    'niet besproken',
    'niet gezien',
    'niet meer',
    'niet waarschijnlijk',  
    'onwaarschijnlijk',
    'opgelost',
    'preventieplan',
    'speelt niet',
    'waren niet',
    'was niet',
    'werd uitgesloten',
    'werden ontkend',
    'werden uitgesloten',
    'worden ontkend',
    'zijn afwezig',
    'zijn ontkend',
    'zijn uitgesloten',
    'zijn verdwenen',
    'zijn weg',
]

negation_triggers[NegationContext.NEGATED, 'phrase', 'pseudo'] = [
    'geen afname',
    'geen oorzaak van',
    'geen toename',
    'geen verandering',
    'geen verbetering',
    'geen verdere',
    'geen zekere verandering',
    'gram negatief',
    'herkent zich niet',
    'is misschien niet',
    'is mogelijk niet',
    'kan niet',
    'misschien niet', 
    'mogelijk niet',
    'niet alleen',
    'niet besproken',
    'niet duidelijk',
    'niet gevraagd',
    'niet mogelijk om ',
    'niet noodzakelijkerwijs',
    'niet perse',
    'niet uit te sluiten',
    'niet uitgesloten',
    'niet uitgevraagd',
    'niet uitgevraagd',
    'niet zeker of',
    'wel of niet',
    'zonder moeite',
    'zonder moelijkheid',
    'zonder verdere',
    'niet goed',
]

negation_triggers[NegationContext.NEGATED, 'phrase', 'termination'] = [
    'aangezien er',
    'afgezien van',
    'alhoewel',
    'andere mogelijkheden tot',
    'andere redenen tot',
    'andere redenen voor',
    'behalve', 
    'behoudens',
    'bron van',
    'bron voor',
    'bronnen van',
    'bronnen voor',
    'buiten',
    'daarentegen',
    'dat',
    'desalniettemin',
    'die', 
    'doch',
    'etiologie van',
    'etiologie voor',
    'hetgeen',
    'hoewel',
    'losstaand van',
    'maar',
    'naast',
    'niettemin', 
    'nochtans',
    'nog',
    'ofschoon',
    'ondergeschikt',
    'reden tot',
    'reden van',
    'reden voor',
    'redenen tot',
    'redenen voor',
    'renenen van',
    'soms',
    'toch',
    'trigger voor',
    'uitgezonderd',
    'voelt zich',
    'wel',
    'welke',
    ',',
]

### Patterns
negation_triggers[NegationContext.NEGATED, 'pattern', 'preceding'] = [

]

negation_triggers[NegationContext.NEGATED, 'pattern', 'following'] = [

]

negation_triggers[NegationContext.NEGATED, 'pattern', 'pseudo'] = [

    # niet <verb>
    [
     {"LOWER" : 'niet'},
     {"POS" : 'VERB'}
    ],



]

negation_triggers[NegationContext.NEGATED, 'pattern', 'termination'] = [

    [{'LOWER' : 'als', 'OP' : "?"},
     {'LOWER' : {'IN' : ['de', 'een']}, 'OP' : '?'},
     {'LOWER' : {'IN' : ['bron', 'bronnen', 'reden', 'redenen', 'oorzaak', 'oorzaken', 'oorsprong', 'etiologie']}},
     {'LOWER' : {'IN' : ['van', 'voor', 'tot']}}
    ],

]

### Regexps
negation_triggers[NegationContext.NEGATED, 'regexp', 'preceding'] = [

]

negation_triggers[NegationContext.NEGATED, 'regexp', 'following'] = [

]

negation_triggers[NegationContext.NEGATED, 'regexp', 'pseudo'] = [

]

negation_triggers[NegationContext.NEGATED, 'regexp', 'preceding'] = [

]
