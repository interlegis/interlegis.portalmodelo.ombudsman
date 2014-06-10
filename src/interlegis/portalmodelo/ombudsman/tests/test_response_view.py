# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman.interfaces import IBrowserLayer
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import FUNCTIONAL_TESTING
from plone import api
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import directlyProvides

import unittest


class ResponseViewTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IBrowserLayer)
        office = create_ombudsoffice(self, 'office')
        self.claim = api.content.create(office, 'Claim', 'claim')

    def test_add_response_no_parameters(self):
        # invoke the view and check the status message
        self.claim.unrestrictedTraverse('add-response')()
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'There were some errors. Required input is missing.'
        self.assertEqual(msg[0].message, expected)

    def test_add_response(self):
        self.request.form['transition'] = 'move'
        self.request.form['text'] = 'Your claim is being processed.'
        # invoke the view and check the status message
        self.claim.unrestrictedTraverse('add-response')()
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Item created.'
        self.assertEqual(msg[0].message, expected)
