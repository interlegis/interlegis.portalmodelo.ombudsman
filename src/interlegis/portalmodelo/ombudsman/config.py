# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman import _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

PROJECTNAME = 'interlegis.portalmodelo.ombudsman'

# vocabularies
GENRES = SimpleVocabulary([
    SimpleTerm(value='f', title=_(u'Feminino')),
    SimpleTerm(value='m', title=_(u'Masculino')),
])

AGES = SimpleVocabulary([
    SimpleTerm(value='15', title=_(u'Menos que 15')),
    SimpleTerm(value='20', title=_(u'Entre 16 e 20')),
    SimpleTerm(value='30', title=_(u'Entre 21 e 30')),
    SimpleTerm(value='40', title=_(u'Entre 31 e 40')),
    SimpleTerm(value='50', title=_(u'Entre 41 e 50')),
    SimpleTerm(value='60', title=_(u'Entre 51 e 60')),
    SimpleTerm(value='70', title=_(u'Entre 61 e 70')),
    SimpleTerm(value='71', title=_(u'Acima de 71')),
])

# this empty vocabulary is used when we call the AreasVocabulary
# outside the context of an Ombuds Office
EMPTY = SimpleVocabulary.fromItems([])
