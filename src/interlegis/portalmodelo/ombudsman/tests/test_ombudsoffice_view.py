# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman.interfaces import IBrowserLayer
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from plone import api
from zope.interface import directlyProvides

import unittest


class BaseOmbudsOfficeViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IBrowserLayer)
        self.office = create_ombudsoffice(self, 'office')


class ViewTestCase(BaseOmbudsOfficeViewTestCase):

    def test_claims(self):
        view = api.content.get_view('view', self.office, self.request)
        view.update()
        self.assertEqual(len(view._claims()), 0)

        api.content.create(self.office, 'Claim', 'claim1')
        api.content.create(self.office, 'Claim', 'claim2')
        api.content.create(self.office, 'Claim', 'claim3')
        self.assertEqual(len(view._claims()), 3)

    def test_get_claims_by_state(self):
        api.content.create(self.office, 'Claim', 'claim1')
        api.content.create(self.office, 'Claim', 'claim2')
        api.content.create(self.office, 'Claim', 'claim3')

        # current workflow has 5 states: pending, rejected, accepted, moving and resolved
        with api.env.adopt_roles(['Manager']):
            # Claim 2 will be moving
            api.content.transition(self.office.claim2, 'accept')
            api.content.transition(self.office.claim2, 'move')
            # Claim 3 will be resolved
            api.content.transition(self.office.claim3, 'accept')
            api.content.transition(self.office.claim3, 'move')
            api.content.transition(self.office.claim3, 'resolve')

        view = api.content.get_view('view', self.office, self.request)
        view.update()
        claims_by_state = view.get_claims_by_state()
        self.assertEqual(len(claims_by_state), 5)
        self.assertEqual(len(claims_by_state['pending']), 1)
        self.assertEqual(len(claims_by_state['moving']), 1)
        self.assertEqual(len(claims_by_state['resolved']), 1)
