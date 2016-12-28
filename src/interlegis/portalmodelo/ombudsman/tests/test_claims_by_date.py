# /*/ coding: utf/8 /*/
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from interlegis.portalmodelo.ombudsman.browser.claims_by_date import json_claims_by_date
from interlegis.portalmodelo.ombudsman.browser.claims_by_date import get_claim_creation_date
from interlegis.portalmodelo.ombudsman.browser.claims_by_date import count_claims_by_date
from interlegis.portalmodelo.ombudsman.browser.claims_by_date import csv_claims_by_date
from plone import api

import unittest
import json
import datetime
from DateTime import DateTime


def compare_json_dict(expected, value, msg=None):
    if msg is None:
        msg = 'The counts are not equal!'

    for e_date in expected['items']:
        v_date_count = [
            v['count'] for v in value['items'] if v.get('label') == e_date['label']
        ][0]

        if e_date['count'] != v_date_count:
            raise unittest.TestCase.failureException('{} / Items {}'.format(msg, e_date['label']))


class ClaimDateDataTestCase(unittest.TestCase):

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
            self.office.claim1.creation_date = DateTime('2015/01/09 14:01:00 GMT+2')
            self.office.claim2.creation_date = DateTime('2016/02/08 13:03:00 GMT+2')
            self.office.claim3.creation_date = DateTime('2015/03/07 12:06:00 GMT+2')
            self.office.claim4.creation_date = DateTime('2016/04/06 11:09:00 GMT+2')
            self.office.claim5.creation_date = DateTime('2016/05/05 10:12:00 GMT+2')
            self.office.claim6.creation_date = DateTime('2015/06/04 19:15:00 GMT+2')
            self.office.claim7.creation_date = DateTime('2016/07/03 18:18:00 GMT+2')
            self.office.claim8.creation_date = DateTime('2016/08/02 17:21:00 GMT+2')
            self.office.claim9.creation_date = DateTime('2015/09/01 16:24:00 GMT+2')

    def test_json_claims_by_date(self):
        self.addTypeEqualityFunc(dict, compare_json_dict)
        expected = json.loads(
            '['
            '    {"label" : "2015/01/09", "count" : 1},'
            '    {"label" : "2015/03/07", "count" : 1},'
            '    {"label" : "2015/06/04", "count" : 1},'
            '    {"label" : "2015/09/01", "count" : 1},'
            '    {"label" : "2016/02/08", "count" : 1},'
            '    {"label" : "2016/04/06", "count" : 1},'
            '    {"label" : "2016/05/05", "count" : 1},'
            '    {"label" : "2016/07/03", "count" : 1},'
            '    {"label" : "2016/08/02", "count" : 1}'
            ']'
        )
        self.assertEqual(expected, json.loads(json_claims_by_date()))

    def test_csv_claims_by_date(self):
        expected = (
            'label,count\r\n'
            '2015/01/09,1\r\n'
            '2015/03/07,1\r\n'
            '2015/06/04,1\r\n'
            '2015/09/01,1\r\n'
            '2016/02/08,1\r\n'
            '2016/04/06,1\r\n'
            '2016/05/05,1\r\n'
            '2016/07/03,1\r\n'
            '2016/08/02,1\r\n'
        )
        self.assertEqual(expected, csv_claims_by_date())

    def test_get_claim_creation_date(self):
        self.assertEqual('2015/01/09', get_claim_creation_date(self.office.claim1))
        self.assertEqual('2016/02/08', get_claim_creation_date(self.office.claim2))
        self.assertEqual('2015/03/07', get_claim_creation_date(self.office.claim3))
        self.assertEqual('2016/04/06', get_claim_creation_date(self.office.claim4))
        self.assertEqual('2016/05/05', get_claim_creation_date(self.office.claim5))
        self.assertEqual('2015/06/04', get_claim_creation_date(self.office.claim6))
        self.assertEqual('2016/07/03', get_claim_creation_date(self.office.claim7))
        self.assertEqual('2016/08/02', get_claim_creation_date(self.office.claim8))
        self.assertEqual('2015/09/01', get_claim_creation_date(self.office.claim9))

    def test_count_claims_by_date(self):
        expected = {
            '2016/04/06': 1,
            '2015/09/01': 1,
            '2015/03/07': 1,
            '2015/06/04': 1,
            '2016/07/03': 1,
            '2016/02/08': 1,
            '2016/05/05': 1,
            '2015/01/09': 1,
            '2016/08/02': 1
        }
        
        self.assertEqual(expected, count_claims_by_date())
