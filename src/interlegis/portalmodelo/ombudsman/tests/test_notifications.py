# -*- coding: utf-8 -*-
from collective.watcherlist.interfaces import IWatcherList
from interlegis.portalmodelo.ombudsman.testing import INTEGRATION_TESTING
from plone import api
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class NotificationsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        area = dict(responsible='John Doe', email='foo@bar.com', area='area1')
        with api.env.adopt_roles(['Manager']):
            self.office = api.content.create(
                self.portal, 'OmbudsOffice', 'office', areas=[area])

    def test_add_claim(self):
        claim = api.content.create(
            self.office, 'Claim', title='My claim', area='area1', email='baz@qux.com')

        watchers = IWatcherList(claim)
        self.assertEqual(len(watchers.watchers), 2)
        self.assertIn('foo@bar.com', watchers.watchers)
        self.assertIn('baz@qux.com', watchers.watchers)

    def test_modify_claim(self):
        claim = api.content.create(
            self.office, 'Claim', title='My claim', area='area1', email='baz@qux.com')

        claim.email = 'baz@qux.org'
        notify(ObjectModifiedEvent(claim))

        watchers = IWatcherList(claim)
        self.assertEqual(len(watchers.watchers), 2)
        self.assertIn('foo@bar.com', watchers.watchers)
        self.assertNotIn('baz@qux.com', watchers.watchers)
        self.assertIn('baz@qux.org', watchers.watchers)
