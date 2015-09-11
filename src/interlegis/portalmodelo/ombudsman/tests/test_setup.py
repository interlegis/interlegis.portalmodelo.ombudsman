# -*- coding: utf-8 -*-

from interlegis.portalmodelo.ombudsman.config import PROJECTNAME
from interlegis.portalmodelo.ombudsman.interfaces import IBrowserLayer
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers
from Products.GenericSetup.upgrade import listUpgradeSteps

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

VIEW_PERMISSIONS = (
    dict(
        title='interlegis.portalmodelo.ombudsman: View Claim Personal Info',
        expected=[
            'Contributor',
            'Manager',
            'Member',
            'Owner',
            'Site Administrator'],
    ),
)

class BaseTestCase(unittest.TestCase):
    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    profile = 'interlegis.portalmodelo.ombudsman:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.wt = self.portal['portal_workflow']
        self.st = self.portal['portal_setup']


class InstallTestCase(BaseTestCase):
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

    def permissions_helper(self, permissions):
        for permission in permissions:
            roles = self.portal.rolesOfPermission(permission['title'])
            roles = [r['name'] for r in roles if r['selected']]
            self.assertListEqual(roles, permission['expected'])

    def test_add_permissions(self):
        self.permissions_helper(ADD_PERMISSIONS)

    def test_view_permissions(self):
        self.permissions_helper(VIEW_PERMISSIONS)

    def test_browserlayer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

class TestUpgrade(BaseTestCase):
    """Ensure product upgrades work."""

    def test_to1020_available(self):
        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '1000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] in (('1010',), ('1020',)))
                and (step[0]['source'] in (('1000',), ('1010',)))]
        self.assertEqual(len(step), 2)

class UninstallTestCase(unittest.TestCase):
    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_uninstalled(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_uninstalled(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertNotIn(IBrowserLayer, registered_layers())
