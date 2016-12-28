# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from interlegis.portalmodelo.ombudsman.browser.claims_by_state import json_claims_by_state
from interlegis.portalmodelo.ombudsman.browser.claims_by_state import get_claim_state
from interlegis.portalmodelo.ombudsman.browser.claims_by_state import count_claims_by_state
from interlegis.portalmodelo.ombudsman.browser.claims_by_state import csv_claims_by_state
from plone import api

import unittest
import json


def compare_json_dict(expected, value, msg=None):
    if msg is None:
        msg = 'The counts are not equal!'

    for e_state in expected['items']:
        v_state_count = [
            v['count'] for v in value['items'] if v.get('label') == e_state['label']
        ][0]

        if e_state['count'] != v_state_count:
            raise unittest.TestCase.failureException('{} - Items {}'.format(msg, e_state['label']))


class ClaimJsonDataTestCase(unittest.TestCase):

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

        # Shortcuts
        transition = api.content.transition

        with api.env.adopt_roles(['Reviewer']):
            # Reviewer rejects the claim1
            transition(self.office.claim1, 'reject')

            # Reviewer cycles claim2
            transition(self.office.claim2, 'accept')
            transition(self.office.claim2, 'move')
            transition(self.office.claim2, 'move')
            transition(self.office.claim2, 'resolve')

            # Reviewer accepts claim3
            transition(self.office.claim3, 'accept')

            # Reviewer move claim4
            transition(self.office.claim4, 'accept')
            transition(self.office.claim4, 'move')
            transition(self.office.claim4, 'move')

    def test_json_claims_by_state(self):
        self.addTypeEqualityFunc(dict, compare_json_dict)
        expected = json.loads(
            '['
            '    {"label" : "Aceita", "count" : 1},'
            '    {"label" : "Pendente", "count" : 1},'
            '    {"label" : "Rejeitada", "count" : 1},'
            '    {"label" : "Resolvida", "count" : 1},'
            '    {"label" : "Tramitando", "count" : 1}'
            ']'
        )
        self.assertEqual(expected, json.loads(json_claims_by_state()))

    def test_csv_claims_by_state(self):
        expected = (
            'label,count\r\n'
            'Aceita,1\r\n'
            'Pendente,1\r\n'
            'Rejeitada,1\r\n'
            'Resolvida,1\r\n'
            'Tramitando,1\r\n'
        )
        self.assertEqual(expected, csv_claims_by_state())


    def test_get_claim_state(self):
        self.assertEqual('Rejeitada', get_claim_state(self.office.claim1))
        self.assertEqual('Resolvida', get_claim_state(self.office.claim2))
        self.assertEqual('Aceita', get_claim_state(self.office.claim3))
        self.assertEqual('Tramitando', get_claim_state(self.office.claim4))
        self.assertEqual('Pendente', get_claim_state(self.office.claim5))

    def test_count_claims_by_state(self):
        expected = {
            'Rejeitada': 1,
            'Resolvida': 1,
            'Aceita': 1,
            'Tramitando': 1,
            'Pendente': 1,
        }
        self.assertEqual(expected, count_claims_by_state())
