# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from interlegis.portalmodelo.ombudsman.interfaces import IOmbudsOffice
from plone import api
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collections import Counter
from claims_util import import_from_dicts
import rows
import json


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


class CountStateData(grok.View):
    """Generates a count state data of claims with information about Ombuds Offices and claims.
       It's used to populate chart
    """
    grok.context(IOmbudsOffice)
    grok.require('zope2.View')
    grok.name('ombudsman-state-count')

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        count = count_claims_by_state()
        pendente = int(count['Pendente'])
        aceita = int(count['Aceita'])
        tramitando = int(count['Tramitando'])
        rejeitada = int(count['Rejeitada'])
        resolvida = int(count['Resolvida'])

        j = {}
        j['count'] = pendente
        j['label'] = "Pendente"
        k = {}
        k['count'] = aceita
        k['label'] = "Aceita"
        l = {}
        l['count'] = tramitando
        l['label'] = "Tramitando"
        m = {}
        m['count'] = rejeitada
        m['label'] = "Rejeitada"
        n = {}
        n['count'] = resolvida
        n['label'] = "Resolvida"
        solicitacao = [j, k, l, m, n]
        return json.dumps(solicitacao, sort_keys=True, indent=2)

