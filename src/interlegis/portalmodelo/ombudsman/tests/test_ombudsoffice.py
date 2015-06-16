# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman.interfaces import IOmbudsOffice
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer

import unittest


class OmbudsOfficeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.office = api.content.create(self.portal, 'OmbudsOffice', 'office')

    def test_adding(self):
        self.assertTrue(IOmbudsOffice.providedBy(self.office))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='OmbudsOffice')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='OmbudsOffice')
        schema = fti.lookupSchema()
        self.assertEqual(IOmbudsOffice, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='OmbudsOffice')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IOmbudsOffice.providedBy(new_object))

    def test_exclude_from_navigation_behavior(self):
        self.assertTrue(IExcludeFromNavigation.providedBy(self.office))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.office))
        self.assertTrue(IAttributeUUID.providedBy(self.office))

    def test_constraints(self):
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError) as cm:
            api.content.create(self.office, 'Document', 'document')
        self.assertEqual(
            cm.exception.message,
            "Cannot add a 'Document' object to the container."
        )

    def test_get_emails_for_areas(self):
        self.office.areas = [
            dict(responsible='John Doe', email='foo@bar.com', area='Area 1 Title'),
            dict(responsible='Mary Doe', email='baz@qux.com', area='Area 2 Title'),
        ]
        expected = {'area-1-title': 'foo@bar.com', 'area-2-title': 'baz@qux.com'}
        self.assertDictEqual(self.office.get_emails_for_areas(), expected)

