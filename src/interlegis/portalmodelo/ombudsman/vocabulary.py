# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from interlegis.portalmodelo.ombudsman.config import EMPTY
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from interlegis.portalmodelo.ombudsman.interfaces import IOmbudsOffice
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import queryUtility
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def ClaimTypesVocabulary(context):
    """Return the available types of claims inside an Ombuds Office. This
    vocabulary is context sensitive and must be called from a Claim.
    """
    context = aq_inner(context)
    if IOmbudsOffice.providedBy(context):
        # we should be adding a claim
        parent = context
    elif IClaim.providedBy(context):
        # we are viewing a Claim
        parent = aq_parent(context)
        assert IOmbudsOffice.providedBy(parent)
    else:
        return EMPTY

    items = []
    for i in parent.claim_types:
        title = i['claim_type']
        value = queryUtility(IIDNormalizer).normalize(title)
        items.append(SimpleTerm(value=value, title=title))
    return SimpleVocabulary(items)


def AreasVocabulary(context):
    """Return the available areas inside an Ombuds Office. This vocabulary is
    context sensitive and must be called from a Claim.
    """
    context = aq_inner(context)
    if IOmbudsOffice.providedBy(context):
        # we should be adding a claim
        parent = context
    elif IClaim.providedBy(context):
        # we are viewing a Claim
        parent = aq_parent(context)
        assert IOmbudsOffice.providedBy(parent)
    else:
        return EMPTY

    items = []
    for i in parent.areas:
        title = i['area']
        value = queryUtility(IIDNormalizer).normalize(title)
        items.append(SimpleTerm(value=value, title=title))
    return SimpleVocabulary(items)
