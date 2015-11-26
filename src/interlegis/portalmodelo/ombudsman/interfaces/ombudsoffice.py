# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
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

    form.widget('email_template', WysiwygFieldWidget)
    email_template = schema.Text(
        title=_(u'Template for fist email after claim created.'),
        description=_(u'Use vars {title}, {protocol}, {url}, {name}, {email}, \
{address}, {city}, {state}, {postalcode}, {status} to customize your template.'),
        required=False,
    )

    form.widget('email_template_states', WysiwygFieldWidget)
    email_template_states = schema.Text(
        title=_(u'Template for further email after alter state of claim.'),
        description=_(u'Use vars {title}, {protocol}, {url}, {name}, {email}, \
{address}, {city}, {state}, {postalcode}, {status} to customize your template.'),
        required=False,
    )


    display_claims = schema.Bool(
        title=_(u'Display claims for anonymous?'),
        description=_(u''),
        required=False,
        default=True,
    )

