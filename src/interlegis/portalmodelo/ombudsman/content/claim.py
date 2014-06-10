# -*- coding: utf-8 -*-

from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from five import grok
from plone.dexterity.content import Item


class Claim(Item):
    """A claim to the Ombudsman."""
    grok.implements(IClaim)
