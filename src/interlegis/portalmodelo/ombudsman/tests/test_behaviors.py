# -*- coding: utf-8 -*-
from datetime import datetime
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser

import transaction
import unittest


class NameFromDateTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['app'])
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.browser.handleErrors = False
        self.office = create_ombudsoffice(self, 'office')
        self.office.claim_types = [{'claim_type': '1'}]

        transaction.commit()

    def test_name_behavior(self):
        browser = self.browser
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        browser.open('http://nohost/plone/office/++add++Claim')
        browser.getControl('Topic').value = 'A Claim'
        browser.getControl('Name').value = 'Machado de Assis'
        browser.getControl('Email').value = 'machado@assis.org'
        browser.getControl('Address').value = 'ABL 12'
        browser.getControl('Postal code').value = '80982-912'
        browser.getControl('City').value = 'Cosme Velho'
        browser.getControl('State').value = ['RJ', ]
        browser.getControl('Details').value = 'Foo bar '

        browser.getControl('Save').click()
        now = datetime.now()
        self.assertIn('/office/' + now.strftime('%Y%m%d'), browser.url)
