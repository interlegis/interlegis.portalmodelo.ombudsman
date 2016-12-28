# -*- coding: utf-8 -*-
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from interlegis.portalmodelo.ombudsman.browser.claims_by_kind import json_claims_by_kind
from interlegis.portalmodelo.ombudsman.browser.claims_by_kind import get_claim_kind
from interlegis.portalmodelo.ombudsman.browser.claims_by_kind import count_claims_by_kind
from interlegis.portalmodelo.ombudsman.browser.claims_by_kind import csv_claims_by_kind
from plone import api

import unittest
import json


def compare_json_dict(expected, value, msg=None):
    if msg is None:
        msg = 'The counts are not equal!'

    for e_kind in expected['items']:
        v_kind_count = [
            v['count'] for v in value['items'] if v.get('label') == e_kind['label']
        ][0]

        if e_kind['count'] != v_kind_count:
            raise unittest.TestCase.failureException('{} - Items {}'.format(msg, e_kind['label']))


class ClaimKindDataTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.office = create_ombudsoffice(self, 'office')

        # Anonymous creates claims
        with api.env.adopt_roles(['Anonymous']):
            api.content.create(self.office, 'Claim', 'claim1')
            api.content.create(self.office, 'Claim', 'claim2')
            api.content.create(self.office, 'Claim', 'claim3')
            api.content.create(self.office, 'Claim', 'claim4')
            api.content.create(self.office, 'Claim', 'claim5')
            api.content.create(self.office, 'Claim', 'claim6')
            api.content.create(self.office, 'Claim', 'claim7')
            api.content.create(self.office, 'Claim', 'claim8')
            api.content.create(self.office, 'Claim', 'claim9')

        with api.env.adopt_roles(['Reviewer']):
            self.office.claim1.kind = "denaoncia"
            self.office.claim2.kind = "daovida"
            self.office.claim3.kind = "elogio"
            self.office.claim4.kind = "elogio"
            self.office.claim5.kind = "pedido-de-acesso-a-informaassapso"
            self.office.claim6.kind = "solicitaassapso"
            self.office.claim7.kind = "sugestapso"
            self.office.claim8.kind = "sugestapso"
            self.office.claim9.kind = "reclamaassapso"

    def test_json_claims_by_kind(self):
        self.addTypeEqualityFunc(dict, compare_json_dict)
        expected = json.loads(
            '['
            '    {"label" : "Denúncia", "count" : 1},'
            '    {"label" : "Dúvida", "count" : 1},'
            '    {"label" : "Elogio", "count" : 2},'
            '    {"label" : "Pedido de acesso à informação", "count" : 1},'
            '    {"label" : "Reclamação", "count" : 1},'
            '    {"label" : "Solicitação", "count" : 1},'
            '    {"label" : "Sugestão", "count" : 2}'
            ']'
        )
        self.assertEqual(expected, json.loads(json_claims_by_kind()))

    def test_csv_claims_by_kind(self):
        expected = (
            'label,count\r\n'
            'Denúncia,1\r\n'
            'Dúvida,1\r\n'
            'Elogio,2\r\n'
            'Pedido de acesso à informação,1\r\n'
            'Reclamação,1\r\n'
            'Solicitação,1\r\n'
            'Sugestão,2\r\n'
        )
        self.assertEqual(expected, csv_claims_by_kind())

    def test_get_claim_kind(self):
        self.assertEqual('Denúncia', get_claim_kind(self.office.claim1))
        self.assertEqual('Dúvida', get_claim_kind(self.office.claim2))
        self.assertEqual('Elogio', get_claim_kind(self.office.claim3))
        self.assertEqual('Elogio', get_claim_kind(self.office.claim4))
        self.assertEqual('Pedido de acesso à informação', get_claim_kind(self.office.claim5))
        self.assertEqual('Solicitação', get_claim_kind(self.office.claim6))
        self.assertEqual('Sugestão', get_claim_kind(self.office.claim7))
        self.assertEqual('Sugestão', get_claim_kind(self.office.claim8))
        self.assertEqual('Reclamação', get_claim_kind(self.office.claim9))

    def test_count_claims_by_kind(self):
        expected = {
            'Sugestão': 2,
            'Elogio': 2,
            'Dúvida': 1,
            'Denúncia': 1,
            'Pedido de acesso à informação': 1,
            'Solicitação': 1,
            'Reclamação': 1
        }
        self.assertEqual(expected, count_claims_by_kind())
