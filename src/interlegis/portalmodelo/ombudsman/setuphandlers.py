# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'interlegis.portalmodelo.ombudsman.upgrades.v1010:default',
            u'interlegis.portalmodelo.ombudsman:uninstall',
            u'Products.BrFieldsAndWidgets:default',
            u'Products.BrFieldsAndWidgets:uninstall',
        ]
