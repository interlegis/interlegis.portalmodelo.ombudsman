# -*- coding: utf-8 -*-

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from plone import api


def create_ombudsoffice(self, id):
    area = dict(responsible='John Doe', email='foo@bar.com', area='area1')
    with api.env.adopt_roles(['Manager']):
        return api.content.create(
            self.portal, 'OmbudsOffice', id, areas=[area])


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import interlegis.portalmodelo.ombudsman
        self.loadZCML(package=interlegis.portalmodelo.ombudsman)

    def setUpPloneSite(self, portal):
        self.applyProfile(
            portal, 'interlegis.portalmodelo.ombudsman:default')

FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='interlegis.portalmodelo.ombudsman:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='interlegis.portalmodelo.ombudsman:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='interlegis.portalmodelo.ombudsman:Robot',
)
