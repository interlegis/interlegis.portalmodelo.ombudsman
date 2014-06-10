# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from five import grok
from interlegis.portalmodelo.ombudsman.adapters import IResponseContainer
from interlegis.portalmodelo.ombudsman.interfaces import IBrowserLayer
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from plone import api
from plone.dexterity.utils import addContentToContainer
from plone.directives import dexterity
from plone.memoize import view
from Products.CMFPlone import PloneMessageFactory as PMF

grok.templatedir('templates')


class View(dexterity.DisplayForm):
    """Default view for Claim content type.
    """
    grok.context(IClaim)
    grok.layer(IBrowserLayer)
    grok.require('zope2.View')
    grok.template('claim_view')

    @property
    def can_add_response(self):
        mt = api.portal.get_tool('portal_membership')
        return mt.checkPermission(
            'interlegis.portalmodelo.ombudsman.AddResponse', self.context)

    def is_anonymous(self):
        return api.user.is_anonymous()

    def transitions(self):
        """Return a list of available transitions for the claim.
        """
        wftool = api.portal.get_tool('portal_workflow')
        available_transitions = wftool.getTransitionsFor(self.context)
        current_state = api.content.get_state(self.context)
        current_title = wftool.getTitleForStateOnType(current_state, 'Claim')

        # as first, we add the current state as a no-change condition
        transitions = [dict(id=current_state, title=PMF(current_title))]

        # now we add the all available transitions
        for i in available_transitions:
            transitions.append(
                dict(id=i['id'], title=PMF(i['name'])))

        return transitions

    def _responses(self):
        """Return a list of responses for the current Claim.
        """
        responses = []
        container = IResponseContainer(self.context)
        for id, response in enumerate(container):
            if response is None:
                continue  # response has been removed
            responses.append(dict(
                id=id + 1,
                creator=response.creator,
                date=response.date,
                review_state=response.review_state,
                text=response.text,
            ))
        return responses

    @view.memoize
    def responses(self):
        return self._responses()

    def has_responses(self):
        return len(self.responses()) > 0


class AddView(dexterity.AddForm):
    grok.name('Claim')
    grok.require('interlegis.portalmodelo.ombudsman.AddClaim')

    def update(self):
        # XXX: currently, any user can add a claim
        #      do we need to check if the user is anonymous?
        super(AddView, self).update()

    def add(self, object):
        """Add the object to the container skipping constraints and
        redirect to the container.
        """
        container = aq_inner(self.context)
        obj = addContentToContainer(container, object, checkConstraints=False)
        self.immediate_view = '{0}/{1}'.format(container.absolute_url(), obj.id)
