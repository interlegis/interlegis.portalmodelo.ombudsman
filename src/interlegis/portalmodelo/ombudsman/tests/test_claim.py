# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from interlegis.portalmodelo.ombudsman.testing import create_ombudsoffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        office = create_ombudsoffice(self, 'office')
        self.claim = api.content.create(office, 'Claim', 'claim')

    def test_adding(self):
        self.assertTrue(IClaim.providedBy(self.claim))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Claim')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Claim')
        schema = fti.lookupSchema()
        self.assertEqual(IClaim, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Claim')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IClaim.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.claim))
        self.assertTrue(IAttributeUUID.providedBy(self.claim))

    def test_constraints(self):
        with self.assertRaises(InvalidParameterError) as cm:
            api.content.create(self.portal, 'Claim', 'claim')
        self.assertIn(
            "Cannot add a 'Claim' object to the container.",
            cm.exception.message
        )

    def test_claim_is_excluded_from_navigation(self):
        self.navtree = self.portal['portal_properties'].navtree_properties
        metaTypesNotToList = self.navtree.metaTypesNotToList
        self.assertIn('Claim', metaTypesNotToList)
