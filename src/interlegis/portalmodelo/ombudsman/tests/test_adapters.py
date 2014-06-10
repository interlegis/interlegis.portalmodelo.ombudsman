# -*- coding: utf-8 -*-
from datetime import datetime
from interlegis.portalmodelo.ombudsman.adapters import IResponseContainer
from interlegis.portalmodelo.ombudsman.adapters import Response
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from plone import api

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        office = create_ombudsoffice(self, 'office')
        self.claim = api.content.create(office, 'Claim', 'claim')

    def test_adding(self):
        adapter = IResponseContainer(self.claim)
        review_state = api.content.get_state(self.claim)
        adapter.add(Response(review_state, u'First response.'))

        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.claim, 'accept')
            review_state = api.content.get_state(self.claim)
            adapter.add(Response(review_state, u'Second response.'))
            api.content.transition(self.claim, 'resolve')
            review_state = api.content.get_state(self.claim)
            adapter.add(Response(review_state, u'Third response.'))

        self.assertEqual(len(adapter), 3)

        # check the first response
        self.assertEqual(adapter[0].creator, 'test_user_1_')
        self.assertEqual(adapter[0].review_state, 'Pending')
        self.assertTrue(isinstance(adapter[0].date, datetime))
        self.assertEqual(adapter[0].text, u'First response.')

        # same creator, we only adopted a rol to make the transition
        self.assertEqual(adapter[1].creator, 'test_user_1_')
        self.assertEqual(adapter[2].creator, 'test_user_1_')

        # dates are sequential
        self.assertTrue(adapter[0].date < adapter[1].date)
        self.assertTrue(adapter[1].date < adapter[2].date)

        # review states and text are ok
        self.assertEqual(adapter[1].review_state, 'Accepted')
        self.assertEqual(adapter[2].review_state, 'Resolved')
        self.assertEqual(adapter[1].text, u'Second response.')
        self.assertEqual(adapter[2].text, u'Third response.')
