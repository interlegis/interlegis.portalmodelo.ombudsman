# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.permissions import setDefaultRoles
from plone import api

import logging

PROJECTNAME = 'interlegis.portalmodelo.ombudsman'


def apply_profile(context):
    """Atualiza perfil para versao 1030."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-interlegis.portalmodelo.ombudsman.upgrades.v1030:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 1030')
