# -*- coding: utf-8 -*-

from interlegis.portalmodelo.ombudsman.interfaces import IOmbudsOffice
from five import grok
from plone.dexterity.content import Container
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer


class OmbudsOffice(Container):
    """Container to store claims to the Ombudsman.
    """
    grok.implements(IOmbudsOffice)

    def get_emails_for_areas(self):
        """Return a dictionary with areas as keys and emails as values.
        """
        return dict((queryUtility(IIDNormalizer).normalize(i['area']),
                     i['email']) for i in self.areas)
