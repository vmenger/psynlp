from enum import Enum

class TemporalityContext(Enum):
    CURRENT = 1
    HISTORICAL = 2
    CONTINUOUS = 3

temporality_triggers = {}

months = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'november', 'december']

temporality_triggers[TemporalityContext.HISTORICAL, 'phrase', 'preceding'] = [ 
    'al bekende', # Kan ook recent zijn? 
    'als baby',
    'als kind',
    'als puber', 
    'als tiener',
    'bij eerste presentatie',
    'destijds',
    'eerdere',
    # 'eerste', # Twijfelgeval, bv "Destijds eerste psychose doorgemaakt", vs "Dit is zijn eerste psychose"
    'gedocumenteerd',
    'gedocumenteerde',
    'geschiedenis van',
    'geschiedenis',
    'herinnering',
    'herinneringen',
    'in de kindertijd',
    'in de vg',
    'in de voorgeschiedenis',
    'in het verleden',
    'in voorgeschiedenis',
    'jaar', #?
    'jaren', #?
    'maand', #?
    'maanden', #?
    'niet actueel',
    'op jong volwassen leeftijd',
    'op jonge leeftijd',
    'subacute',
    'subacuut',
    'toen',
    'verleden van',
    'vg',
    'voorgeschiedenis',
    'vroeger', 
    'werd',
#     'lijkt',
#     'reeds bekende', # Kan ook recent zijn?
#     'sinds', # dubieus
]

temporality_triggers[TemporalityContext.HISTORICAL, 'phrase', 'following'] = [
    'als baby',
    'als kind',
    'als puber', 
    'als tiener',
    'geweest',
    'heeft gehad',
    'heeft meegemaakt',
    'heeft plaatsgehad',
    'heeft plaatsgevonden',
    'in de geschiedenis',
    'in de kindertijd',
    'in de psychiatrische voorgeschiedenis',
    'in de vg',
    'in de vg',
    'in de voorgeschiedenis',
    'in de voorgeschiedenis',
    'in het verleden',
    'in jeugd',
    'in remissie',
    'in voorgeschiedenis',
    'in voorgeschiedenis',
    'is gebeurd',
    'is geweest',
    'meegemaakt',
    'nu in remissie',
    'op jong volwassen leeftijd',
    'op jonge leeftijd',
    'opgelost',

]

temporality_triggers[TemporalityContext.HISTORICAL, 'phrase', 'pseudo'] = [
    'blanco psychiatrische vg',
    'blanco psychiatrische voorgeschiedenis',
    'blanco vg', 
    'blanco voorgeschiedenis',
    'lijkt meer', 
    'lijkt minder',
    'lijkt niet meer',
    'lijkt niet minder',
    'vg blanco',
    'voorgeschiedenis blanco', #etc
]

temporality_triggers[TemporalityContext.HISTORICAL, 'phrase', 'termination'] = [
    'actueel',
    'afgenomen', 
    'afname',
    'nu',
    'primair',
    'toegenomen',
    'toename',
    ',',
]

temporality_triggers[TemporalityContext.CONTINUOUS, 'phrase', 'preceding'] = [
    # afname 
    # continuous
    # toename
    'aanhouden van',
    'aanhoudende', 
    'afgenomen', 
    'afname',
    'al',
    'bekend met',
    'blijft',
    'blijvende', 
    'langer bestaande', 
    'meer',
    'minder', 
    'nog', 
    'oplopen van',
    'oplopende', 
    'persisterend',
    'reeds',
    'sedert', 
    'sinds',
    'sindsdien',
    'toegenomen', 
    'toename', 
    'toenemende', 
    'vanaf',
    'verbeterde', 
    'verbetering',
    'verergering',
    'vermindering', 
    'verminderen',
    'verslechterde',
    'verslechtering',
    'voortdurende', 

]

temporality_triggers[TemporalityContext.CONTINUOUS, 'phrase', 'following'] = [
    # afname 
    # continuous
    # toename
    'afgenomen',
    'afneemt', 
    'afnemen',
    'afnemende',
    'blijft',
    'blijven', 
    'doorgaan', 
    'langer bestaand',
    'loopt op', 
    'neemt af', 
    'neemt toe',
    'onveranderd', 
    'onverminderd',
    'oploopt',
    'oplopen',
    'opspelen', 
    'persisteert',
    'recidiverend', #? 
    'toeneemt',
    'toenemen',
    'verbeterd',
    'verergeren', 
    'verhoogd',
    'verminderd', 
    'verslechterd',
    'voortbestaan',
    'voortduren', 
    'zijn toegenomen',
]

temporality_triggers[TemporalityContext.CONTINUOUS, 'phrase', 'pseudo'] = [
    'nog niet',
    'nog geen',
]

temporality_triggers[TemporalityContext.CONTINUOUS, 'phrase', 'termination'] = [
    ',',
]


### Patterns ###

temporality_triggers[TemporalityContext.HISTORICAL, 'pattern', 'preceding'] = [

    # in <jaartal>
    [{'LOWER' : {'IN' : ['in', 'rond']}}, 
     {'TEXT': {'REGEX': r'^(19|20)\d{2}$'}}
    ],

    # <jaartal>:
    [{'TEXT' : {'REGEX' : r'^(19|20)\d{2}$'}},
     {'TEXT' : ':'}
    ],

    # jaar/maand(en) geleden
    [{'LOWER' : {'IN' : ['jaar', 'jaren', 'maand', 'maanden']}},
     {'LOWER' : 'geleden'}
    ],

    # sinds zijn/haar xxe
    [{'LOWER' : 'sinds'},
     {'LOWER' : {'IN' : ['zijn', 'haar']}},
     {'TEXT' : {'REGEX' : r'^\d{,2}e$'}}
    ],

    # jaartal
    [
     {'TEXT' : {'REGEX': r'^(19|20)\d{2}$'}}
    ],

    # in <maand>
    [
     {'LOWER' : 'in'},
     {'LOWER' : {'IN' : months}}
    ],


    # # ovt
    # [
    #  {'TAG': {'REGEX': r'ovt'}}
    # ],

    # # voltooid deelwoord
    # [
    #  {'TAG': {'REGEX': r'verldw'}}
    # ]


]

temporality_triggers[TemporalityContext.HISTORICAL, 'pattern', 'following'] = [

    # in <jaartal>
    [{'LOWER' : {'IN' : ['in', 'rond']}}, 
     {'TEXT': {'REGEX': r'^(19|20)\d{2}$'}}
    ],

    # jaar/maand(en) geleden
    [{'LOWER' : {'IN' : ['jaar', 'jaren', 'maand', 'maanden']}},
     {'LOWER' : 'geleden'}
    ],

    # sinds zijn/haar xxe
    [{'LOWER' : 'sinds'},
     {'LOWER' : {'IN' : ['zijn', 'haar']}},
     {'TEXT' : {'REGEX' : r'^\d{,2}e$'}}
    ],

    # in <maand>
    [
     {'LOWER' : 'in'},
     {'LOWER' : {'IN' : months}}
    ],

    # in <maand>
    [
     {'LOWER' : 'in'},
     {'LOWER' : {'IN' : months}}
    ],


]

temporality_triggers[TemporalityContext.HISTORICAL, 'pattern', 'pseudo'] = [

]

temporality_triggers[TemporalityContext.HISTORICAL, 'pattern', 'termination'] = [

]

temporality_triggers[TemporalityContext.CONTINUOUS, 'pattern', 'preceding'] = [

    # De afgelopen/laatste tijd/weken/maanden/jaren
    [
     {'LOWER' : {'IN' : ['laatste', 'afgelopen', 'voorgaande']}},
     {'LOWER' : {'IN' : ['tijd', 'weken', 'maanden', 'jaren']}}
    ],

    # sinds/vanaf <maand>
    [
     {'LOWER' : {'IN' : ['sinds', 'vanaf']}},
     {'LOWER' : {'IN' : months}}
    ],

]

temporality_triggers[TemporalityContext.CONTINUOUS, 'pattern', 'following'] = [

    # sinds/vanaf <maand>
    [
     {'LOWER' : {'IN' : ['sinds', 'vanaf']}},
     {'LOWER' : {'IN' : months}}
    ],

]





### Regexps
temporality_triggers[TemporalityContext.HISTORICAL, 'regexp', 'preceding'] = [
    r'op [\d\-/]+ jarige leeftijd',
]

temporality_triggers[TemporalityContext.HISTORICAL, 'regexp', 'following'] = [
    r'op [\d\-/]+ jarige leeftijd',
]

temporality_triggers[TemporalityContext.HISTORICAL, 'regexp', 'pseudo'] = [
    r'\d dd',
]

temporality_triggers[TemporalityContext.HISTORICAL, 'regexp', 'termination'] = [

]