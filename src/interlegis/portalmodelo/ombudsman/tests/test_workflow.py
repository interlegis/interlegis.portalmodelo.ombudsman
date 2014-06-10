# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from plone import api

import unittest


class ClaimWorkflowTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.office = create_ombudsoffice(self, 'office')

        # Anonymous creates two claims
        with api.env.adopt_roles(['Anonymous']):
            api.content.create(self.office, 'Claim', 'claim1')
            api.content.create(self.office, 'Claim', 'claim2')

    def test_claim_lifecycle_reviewer(self):
        # Shortcuts
        get_state = api.content.get_state
        transition = api.content.transition

        with api.env.adopt_roles(['Reviewer']):
            # Reviewer rejects the claim1
            transition(self.office.claim1, 'reject')
            self.assertEqual(get_state(self.office.claim1), 'rejected')

            # Reviewer cycles claim2
            transition(self.office.claim2, 'accept')
            self.assertEqual(get_state(self.office.claim2), 'accepted')
            transition(self.office.claim2, 'move')
            self.assertEqual(get_state(self.office.claim2), 'moving')
            transition(self.office.claim2, 'move')
            self.assertEqual(get_state(self.office.claim2), 'moving')
            transition(self.office.claim2, 'resolve')
            self.assertEqual(get_state(self.office.claim2), 'resolved')

    def test_claim_lifecycle_site_administrator(self):
        # Shortcuts
        get_state = api.content.get_state
        transition = api.content.transition

        with api.env.adopt_roles(['Site Administrator']):
            # Site Administrator rejects the claim1
            transition(self.office.claim1, 'reject')
            self.assertEqual(get_state(self.office.claim1), 'rejected')

            # Site Administrator cycles claim2
            transition(self.office.claim2, 'accept')
            self.assertEqual(get_state(self.office.claim2), 'accepted')
            transition(self.office.claim2, 'move')
            self.assertEqual(get_state(self.office.claim2), 'moving')
            transition(self.office.claim2, 'move')
            self.assertEqual(get_state(self.office.claim2), 'moving')
            transition(self.office.claim2, 'resolve')
            self.assertEqual(get_state(self.office.claim2), 'resolved')

    def test_claim_lifecycle_manager(self):
        # Shortcuts
        get_state = api.content.get_state
        transition = api.content.transition

        with api.env.adopt_roles(['Manager']):
            # Manager rejects the claim1
            transition(self.office.claim1, 'reject')
            self.assertEqual(get_state(self.office.claim1), 'rejected')

            # Manager cycles claim2
            transition(self.office.claim2, 'accept')
            self.assertEqual(get_state(self.office.claim2), 'accepted')
            transition(self.office.claim2, 'move')
            self.assertEqual(get_state(self.office.claim2), 'moving')
            transition(self.office.claim2, 'move')
            self.assertEqual(get_state(self.office.claim2), 'moving')
            transition(self.office.claim2, 'resolve')
            self.assertEqual(get_state(self.office.claim2), 'resolved')
