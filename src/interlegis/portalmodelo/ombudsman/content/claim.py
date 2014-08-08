# -*- coding: utf-8 -*-

from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from five import grok
from plone.dexterity.content import Container


class Claim(Container):
    """A claim to the Ombudsman."""
    grok.implements(IClaim)
