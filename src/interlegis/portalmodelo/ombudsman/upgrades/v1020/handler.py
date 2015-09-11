# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.permissions import setDefaultRoles
from plone import api

import logging

PROFILE_ID = 'interlegis.portalmodelo.ombudsman:default'

def grant_view_to_contributors(context, logger=None):
    """Method to grant claim view personal info permission to contributors.

    When called from the import_various method, 'context' is
    the plone site and 'logger' is the portal_setup logger.

    But this method will be used as upgrade step, in which case 'context'
    will be portal_setup and 'logger' will be None.

    Adapted from: http://docs.plone.org/develop/addons/components/genericsetup.html?highlight=upgrade%20steps#id1
    """

    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(PROJECTNAME)

    site = api.portal.getSite()
    site.manage_permission(
        'interlegis.portalmodelo.ombudsman: View Claim Personal Info',
        roles = ['Manager', 'Owner', 'Contributor', 'Member'],
        acquire=1)

    logger.info("View Claim Personal Info granted to Manager, Owner and Contributor.")
