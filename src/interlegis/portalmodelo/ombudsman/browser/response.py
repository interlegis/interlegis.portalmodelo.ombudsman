# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.ombudsman import _
from interlegis.portalmodelo.ombudsman.adapters import IResponseContainer
from interlegis.portalmodelo.ombudsman.adapters import Response
from interlegis.portalmodelo.ombudsman.interfaces import IBrowserLayer
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from plone import api
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class AddResponseView(grok.View):
    """Add a response to the claim.
    """
    grok.context(IClaim)
    grok.layer(IBrowserLayer)
    grok.name('add-response')
    grok.require('interlegis.portalmodelo.ombudsman.AddResponse')

    def render(self):
        transition = self.request.form.get('transition', None)
        text = self.request.form.get('text', None)
        if transition is None or not text:
            msg = _(u'There were some errors. Required input is missing.')
            api.portal.show_message(message=msg, request=self.request, type='error')
        else:
            review_state = api.content.get_state(self.context)
            # we use the current state as a marker to indicate
            # no review state change
            if transition != review_state:
                # we need to make the transition first
                api.content.transition(self.context, transition)
                review_state = api.content.get_state(self.context)
            responses = IResponseContainer(self.context)
            responses.add(Response(review_state, text))

            # notify the claim has a new response
            notify(ObjectModifiedEvent(self.context))
            msg = _(u'Item created.')
            api.portal.show_message(message=msg, request=self.request)

        self.request.response.redirect(self.context.absolute_url())
