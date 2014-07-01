# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from plone import api
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_claim_types_vocabulary(self):
        office1 = create_ombudsoffice(self, 'office1')
        office2 = create_ombudsoffice(self, 'office2')
        claim1 = api.content.create(office1, 'Claim', 'claim1')
        claim2 = api.content.create(office2, 'Claim', 'claim2')

        office1.claim_types = [
            dict(claim_type=u'Solicitação de informação'),
            dict(claim_type=u'Type 2'),
            dict(claim_type=u'Type 3'),
        ]
        office2.claim_types = [
            dict(claim_type=u'Type 3'),
            dict(claim_type=u'Type 4'),
            dict(claim_type=u'Type 5'),
            dict(claim_type=u'Type 6'),
        ]

        name = 'interlegis.portalmodelo.ombudsman.ClaimTypes'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util)

        # when adding a claim we are in the context of an Ombuds Office
        claim_types = util(office1)
        self.assertEqual(len(claim_types), 3)
        self.assertIn('solicitacao-de-informacao', claim_types)

        # when viewing a claim we are in its context
        claim_types = util(claim1)
        self.assertEqual(len(claim_types), 3)
        self.assertIn('solicitacao-de-informacao', claim_types)

        claim_types = util(claim2)
        self.assertEqual(len(claim_types), 4)
        self.assertNotIn('solicitacao-de-informacao', claim_types)

        # outside the context of an Ombuds Office we have no items
        claim_types = util(self.portal)
        self.assertEqual(len(claim_types), 0)

    def test_areas_vocabulary(self):
        office1 = create_ombudsoffice(self, 'office1')
        office2 = create_ombudsoffice(self, 'office2')
        claim1 = api.content.create(office1, 'Claim', 'claim1')
        claim2 = api.content.create(office2, 'Claim', 'claim2')

        office1.areas = [
            dict(area=u'Comunicação Social'),
            dict(area=u'Area 2'),
            dict(area=u'Area 3'),
        ]
        office2.areas = [
            dict(area=u'Area 3'),
            dict(area=u'Area 4'),
            dict(area=u'Area 5'),
            dict(area=u'Area 6'),
        ]

        name = 'interlegis.portalmodelo.ombudsman.Areas'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util)

        # when adding a claim we are in the context of an Ombuds Office
        areas = util(office1)
        self.assertEqual(len(areas), 3)
        self.assertIn('comunicacao-social', areas)

        # when viewing a claim we are in its context
        areas = util(claim1)
        self.assertEqual(len(areas), 3)
        self.assertIn('comunicacao-social', areas)

        areas = util(claim2)
        self.assertEqual(len(areas), 4)
        self.assertNotIn('comunicacao-social', areas)

        # outside the context of an Ombuds Office we have no items
        areas = util(self.portal)
        self.assertEqual(len(areas), 0)
