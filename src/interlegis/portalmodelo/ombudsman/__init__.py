# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
from Products.CMFCore.permissions import setDefaultRoles


_ = MessageFactory('interlegis.portalmodelo.ombudsman')

setDefaultRoles(
    'interlegis.portalmodelo.ombudsman: View Claim Personal Info',
    ('Manager', 'Owner', 'Contributor', 'Member'))
