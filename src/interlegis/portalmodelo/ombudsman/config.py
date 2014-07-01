# -*- coding: utf-8 -*-
from zope.schema.vocabulary import SimpleVocabulary

PROJECTNAME = 'interlegis.portalmodelo.ombudsman'

# this empty vocabulary is used when we call the AreasVocabulary
# outside the context of an Ombuds Office
EMPTY = SimpleVocabulary.fromItems([])
