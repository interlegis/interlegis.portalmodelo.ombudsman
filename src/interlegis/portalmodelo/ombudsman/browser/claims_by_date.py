# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.api.utils import type_cast
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from interlegis.portalmodelo.ombudsman.interfaces import IOmbudsOffice
from interlegis.portalmodelo.ombudsman.adapters import IResponseContainer
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getUtility
from zope.schema import getFieldsInOrder

from collections import Counter
from io import BytesIO
from claims_util import import_from_dicts
import rows


def json_claims_by_date():
    counter = count_claims_by_date()
    result = import_from_dicts(counter)
    result.order_by('label')
    return rows.export_to_json(result)


def csv_claims_by_date():
    counter = count_claims_by_date()
    result = import_from_dicts(counter)
    result.order_by('label')
    return rows.export_to_csv(result)


def count_claims_by_date():
    catalog = api.portal.get_tool('portal_catalog')
    claims = catalog(object_provides=IClaim.__identifier__)
    return Counter([get_claim_creation_date(claim.getObject()) for claim in claims])


def get_claim_creation_date(claim):
    return claim.creation_date.Date()


class CSVKindData(grok.View):
    """Generates a CSV with information about Ombuds Offices and claims.
    """
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('ombudsman-date-csv')

    def update(self):
        self.catalog = api.portal.get_tool('portal_catalog')

    def render(self):
        return csv_claims_by_date()


class JSONKindData(grok.View):
    """Generates a JSON with information about Ombuds Offices and claims.
    """
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('ombudsman-date-json')

    def update(self):
        self.catalog = api.portal.get_tool('portal_catalog')

    def render(self):
        return json_claims_by_date()
