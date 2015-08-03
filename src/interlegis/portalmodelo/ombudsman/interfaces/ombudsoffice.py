# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from interlegis.portalmodelo.ombudsman import _
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema


class IClaimTypeItem(model.Schema):
    """Define a claim type record."""

    claim_type = schema.TextLine(
        title=_(u'Claim Type'),
        required=True,
    )


class IAreaItem(model.Schema):
    """Define an area record."""

    area = schema.TextLine(
        title=_(u'Area'),
        required=True,
    )

    responsible = schema.TextLine(
        title=_(u'Responsible'),
        required=True,
    )

    email = schema.TextLine(
        title=_(u'Email'),
        required=True,
    )


class IOmbudsOffice(model.Schema):
    """Folder to store claims to the Ombudsman."""

    title = schema.TextLine(
        title=_(u'Ombuds Office'),
        description=_(u''),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        description=_(u''),
        required=False,
    )

    form.widget(claim_types=DataGridFieldFactory)
    claim_types = schema.List(
        title=_(u'Claim Types'),
        description=_(u'Enter claim types.'),
        required=True,
        value_type=DictRow(title=u'claim_types_row', schema=IClaimTypeItem),
    )

    form.widget(areas=DataGridFieldFactory)
    areas = schema.List(
        title=_(u'Areas'),
        description=_(u'Enter areas, name and email of responsible persons.'),
        required=True,
        value_type=DictRow(title=u'areas_row', schema=IAreaItem),
    )

    managers = schema.List(
        title=_(u'Managers'),
        description=_(u'Enter areas, name and email of responsible persons.'),
        required=False,
        value_type=schema.Choice(vocabulary=u'plone.app.vocabularies.Users'),
    )
