# -*- coding: utf-8 -*-

from interlegis.portalmodelo.ombudsman.config import PROJECTNAME
from interlegis.portalmodelo.ombudsman.interfaces import IBrowserLayer
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers

import unittest


DEPENDENCIES = [
    'collective.z3cform.datagridfield',
    'plone.app.dexterity',
    # 'BrFieldsAndWidgets',  # XXX: even as product is installed, we got False
]

ADD_PERMISSIONS = (
    dict(
        title='interlegis.portalmodelo.ombudsman: Add Claim',
        expected=['Anonymous'],
    ),
    dict(
        title='interlegis.portalmodelo.ombudsman: Add Ombuds Office',
        expected=['Contributor', 'Manager', 'Owner', 'Site Administrator'],
    ),
    dict(
        title='interlegis.portalmodelo.ombudsman: Add Response',
        expected=['Contributor', 'Manager', 'Owner', 'Site Administrator'],
    ),
)


class InstallTestCase(unittest.TestCase):
    """Ensure package is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.setup = self.portal['portal_setup']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_dependencies_installed(self):
        for i in DEPENDENCIES:
            self.assertTrue(
                self.qi.isProductInstalled(i), '{0} not installed'.format(i))

    def test_add_permissions(self):
        for permission in ADD_PERMISSIONS:
            roles = self.portal.rolesOfPermission(permission['title'])
            roles = [r['name'] for r in roles if r['selected']]
            self.assertListEqual(roles, permission['expected'])

    def test_browserlayer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())


class UninstallTestCase(unittest.TestCase):
    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_uninstalled(self):
        self.assertNotIn(IBrowserLayer, registered_layers())
