# -*- coding: utf-8 -*-
from interlegis.portalmodelo.ombudsman import _
from plone.directives import form
from plone.supermodel import model
from zope import schema


class IClaim(model.Schema):
    """A claim to the Ombudsman."""

    kind = schema.Choice(
        title=_(u'Tipos de solicitação'),
        description=_(
            u'help_kind',
            default=u'Selecione o tipo de solicitação.',
        ),
        required=True,
        vocabulary=u'interlegis.portalmodelo.ombudsman.ClaimTypes'
    )

    area = schema.Choice(
        title=_(u'Area'),
        description=_(
            u'help_area',
            default=u'Selecione a área para a qual a solicitação será enviada.',
        ),
        required=True,
        vocabulary=u'interlegis.portalmodelo.ombudsman.Areas'
    )

    title = schema.TextLine(
        title=_(u'Topic'),
        description=_(u''),
        required=True,
    )

    form.widget('description', rows=20)
    description = schema.Text(
        title=_(u'Details'),
        description=_(
            u'help_description',
            default=u'Por favor, informe detalhes adicionais.',
        ),
        required=True,
    )

    form.read_permission(email='interlegis.portalmodelo.ombudsman.ViewClaimPersonalInfo')
    name = schema.TextLine(
        title=_(u'Name'),
        description=_(u'help_name', default=u''),
        required=True,
    )

    form.read_permission(email='interlegis.portalmodelo.ombudsman.ViewClaimPersonalInfo')
    email = schema.ASCIILine(
        title=_(u'Email'),
        description=_(
            u'help_email',
            default=u'Informe o email para onde serão enviadas informações sobre a solicitação.',
        ),
        required=True,
    )

    form.read_permission(email='interlegis.portalmodelo.ombudsman.ViewClaimPersonalInfo')
    address = schema.TextLine(
        title=_(u'Address'),
        description=_(u'help_address', default=u'Informe seu endereço.'),
        required=False,
    )

    form.read_permission(email='interlegis.portalmodelo.ombudsman.ViewClaimPersonalInfo')
    postal_code = schema.TextLine(
        title=_(u'Postal code'),
        description=_(u'help_postal_code', default=u''),
        required=False,
    )

    city = schema.TextLine(
        title=_(u'City'),
        description=_(u'help_city', default=u'Informe sua cidade.'),
        required=False,
    )

    state = schema.Choice(
        title=_(u'State'),
        description=_(u'help_state', default=u'Informe seu estado.'),
        required=False,
        vocabulary=u'brasil.estados',
    )
