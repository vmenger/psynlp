from enum import Enum

class PlausibilityContext(Enum):
    PLAUSIBLE = 1
    HYPOTHETICAL = 2

plausibility_triggers = {}

### Phrases
plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'phrase', 'preceding'] = [ 
    'als er',
    'als',
    'ambivalent',
    'beoordelen van',
    'cave',
    'dd', 
    'diagnostiek',
    'differentiaal diagnostisch',  
    'eventueel',
    'eventuele',
    'evt',
    'hypothese',
    'hypothesen',
    'hypotheses',
    'indien er',
    'indien',
    'kan indiceren',
    'kan worden',
    'kan zijn',
    'kan',
    'kans op',
    'mgl',
    'mogelijk gerelateerd aan',
    'mogelijk',
    'mogelijke',
    'neiging tot',
    'niet duidelijk',
    'observeren van',
    'onduidelijk',
    'rekening houden met',
    'risico op',
    'twijfel',
    'uitsluiten',
    'verdenking',
    'vermoedde',
    'vermoedden',
    'vermoeden van',
    'vermoeden',
    'vermoedt', 
    'voorlopige diagnose',
    'wanneer',
    'wel of niet',
    'wordt gedacht aan',
    'zorgen voor',
    'zou',
    'dan',

]

plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'phrase', 'following'] = [ 
   '?',
   'ambivalent',
   'kan worden',
   'kan zijn',
   'niet besproken',
   'niet duidelijk',
   'niet uitgevraagd', 
   'onduidelijk',
   'vermoedde',
   'vermoedden',
   'zou worden',
   'zou zijn',
]

plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'phrase', 'pseudo'] = [ 
    'als baby',
    'als kind',
    'als puber', 
    'als tiener',
    'geduid als',
    'niet mogelijk',
]

plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'phrase', 'termination'] = [ 
    'aanwezig',
    'ter preventie',
    'zeer waarschijnlijk',
    'zeker',
    'zonder twijfel',
    ',',
]

### Patterns
plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'pattern', 'preceding'] = [ 

]

plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'pattern', 'following'] = [ 

]

plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'pattern', 'pseudo'] = [ 

]

plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'pattern', 'termination'] = [ 

]

### Regexps
plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'regexp', 'preceding'] = [ 

]

plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'regexp', 'following'] = [ 

]

plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'regexp', 'pseudo'] = [ 

]

plausibility_triggers[PlausibilityContext.HYPOTHETICAL, 'regexp', 'termination'] = [ 

]
