# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from plone import api
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collections import Counter
from claims_util import import_from_dicts
import rows


def json_claims_by_state():
    counter = count_claims_by_state()
    result = import_from_dicts(counter)
    result.order_by('label')
    return rows.export_to_json(result)


def csv_claims_by_state():
    counter = count_claims_by_state()
    result = import_from_dicts(counter)
    result.order_by('label')
    return rows.export_to_csv(result)


def count_claims_by_state():
    catalog = api.portal.get_tool('portal_catalog')
    claims = catalog(object_provides=IClaim.__identifier__)
    return Counter([get_claim_state(claim.getObject()) for claim in claims])


def get_claim_state(claim):
    # TODO: Use I18N.
    traduz_estados = {
        'pending': 'Pendente',
        'accepted': 'Aceita',
        'moving': 'Tramitando',
        'rejected': 'Rejeitada',
        'resolved': 'Resolvida'
    }

    return traduz_estados[api.content.get_state(obj=claim)]


class CSVStateData(grok.View):
    """Generates a CSV with information about Ombuds Offices and claims.
    """
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('ombudsman-state-csv')

    def update(self):
        self.catalog = api.portal.get_tool('portal_catalog')

    def render(self):
        return csv_claims_by_state()


class JSONStateData(grok.View):
    """Generates a JSON with information about Ombuds Offices and claims.
    """
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('ombudsman-state-json')

    def update(self):
        self.catalog = api.portal.get_tool('portal_catalog')

    def render(self):
        return json_claims_by_state()


