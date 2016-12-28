# -*- coding: utf-8 -*-
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from plone.app.testing import applyProfile
from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.app.dexterity.behaviors.metadata import Categorization
from plone.dexterity.schema import SchemaInvalidatedEvent
from zope.event import notify
from zope.component import getUtility
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from interlegis.portalmodelo.ombudsman.browser.claims_by_tag import json_claims_by_tag
from interlegis.portalmodelo.ombudsman.browser.claims_by_tag import get_claim_tag
from interlegis.portalmodelo.ombudsman.browser.claims_by_tag import count_claims_by_tag
from interlegis.portalmodelo.ombudsman.browser.claims_by_tag import csv_claims_by_tag
from plone import api

import unittest
import json


def compare_json_dict(expected, value, msg=None):
    if msg is None:
        msg = 'The counts are not equal!'

    for e_tag in expected['items']:
        v_tag_count = [
            v['count'] for v in value['items'] if v.get('label') == e_tag['label']
        ][0]

        if e_tag['count'] != v_tag_count:
            raise unittest.TestCase.failureException('{} - Items {}'.format(msg, e_tag['label']))


class ClaimKindDataTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.office = create_ombudsoffice(self, 'office')

        fti = queryUtility(IDexterityFTI, name='Claim')
        behaviors = list(fti.behaviors)
        behaviors.append(ICategorization.__identifier__)
        fti.behaviors = tuple(behaviors)
        # invalidate schema cache
        notify(SchemaInvalidatedEvent('Claim'))
        self.fti = fti

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
            self.office.claim1.setSubject([u'subject1'])
            self.office.claim2.setSubject([u'subject2'])
            self.office.claim3.setSubject([u'subject3'])
            self.office.claim4.setSubject([u'subject4'])
            self.office.claim5.setSubject([u'subject5'])
            self.office.claim6.setSubject([u'subject6'])
            self.office.claim7.setSubject([u'subject7'])
            self.office.claim8.setSubject([u'subject8'])
            self.office.claim9.setSubject([u'subject9'])

    def test_json_claims_by_tag(self):
        self.addTypeEqualityFunc(dict, compare_json_dict)
        expected = json.loads(
            '['
            '    {"label" : "subject1", "count" : 1},'
            '    {"label" : "subject2", "count" : 1},'
            '    {"label" : "subject3", "count" : 1},'
            '    {"label" : "subject4", "count" : 1},'
            '    {"label" : "subject5", "count" : 1},'
            '    {"label" : "subject6", "count" : 1},'
            '    {"label" : "subject7", "count" : 1},'
            '    {"label" : "subject8", "count" : 1},'
            '    {"label" : "subject9", "count" : 1}'
            ']'
        )
        self.assertEqual(expected, json.loads(json_claims_by_tag()))

    def test_csv_claims_by_tag(self):
        expected = (
            'label,count\r\n'
            'subject1,1\r\n'
            'subject2,1\r\n'
            'subject3,1\r\n'
            'subject4,1\r\n'
            'subject5,1\r\n'
            'subject6,1\r\n'
            'subject7,1\r\n'
            'subject8,1\r\n'
            'subject9,1\r\n'
        )
        self.assertEqual(expected, csv_claims_by_tag())

    def test_get_claim_tag(self):
        self.assertEqual('subject1', get_claim_tag(self.office.claim1))
        self.assertEqual('subject2', get_claim_tag(self.office.claim2))
        self.assertEqual('subject3', get_claim_tag(self.office.claim3))
        self.assertEqual('subject4', get_claim_tag(self.office.claim4))
        self.assertEqual('subject5', get_claim_tag(self.office.claim5))
        self.assertEqual('subject6', get_claim_tag(self.office.claim6))
        self.assertEqual('subject7', get_claim_tag(self.office.claim7))
        self.assertEqual('subject8', get_claim_tag(self.office.claim8))
        self.assertEqual('subject9', get_claim_tag(self.office.claim9))

    def test_count_claims_by_tag(self):
        expected = {
            'subject1': 1,
            'subject2': 1,
            'subject3': 1,
            'subject4': 1,
            'subject5': 1,
            'subject6': 1,
            'subject7': 1,
            'subject8': 1,
            'subject9': 1
        }
        self.assertEqual(expected, count_claims_by_tag())
