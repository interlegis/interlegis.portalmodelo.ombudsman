# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.ombudsman import _
from interlegis.portalmodelo.ombudsman.interfaces import IBrowserLayer
from interlegis.portalmodelo.ombudsman.interfaces import IOmbudsOffice
from plone import api
from plone.memoize import view
from Products.CMFPlone import PloneMessageFactory as PMF

grok.templatedir('templates')


class View(grok.View):
    """Default view for OmbudsOffice content type.
    """
    grok.context(IOmbudsOffice)
    grok.layer(IBrowserLayer)
    grok.require('zope2.View')
    grok.template('ombudsoffice_view')

    def update(self):
        self.wftool = api.portal.get_tool('portal_workflow')

    def is_anonymous(self):
        return api.user.is_anonymous()

    def _claims(self):
        """Return a list of claims inside the current Ombuds Office.

        :returns: a list of claims sorted by modified reverse
        :rtype: list of dictionaries
        """
        results = self.context.listFolderContents({'portal_type': 'Claim'})
        claims = []
        for i in results:
            review_state = api.content.get_state(i)
            klass = 'state-' + review_state
            state = review_state
            review_state = self.wftool.getTitleForStateOnType(review_state, 'Claim')
            claims.append(dict(
                title=i.title,
                description=i.description,
                url=i.absolute_url(),
                klass=klass,
                state=state,
                review_state=PMF(review_state),
                created=i.created(),
                modified=i.modified(),
            ))
        return sorted(claims, key=lambda m: m['modified'], reverse=True)

    @view.memoize
    def claims(self):
        """Return a list of claims inside the current Ombuds Office (cached).
        """
        # TODO: we need to use batching here
        return self._claims()

    def get_claims_by_state(self):
        """Return a dictionary with a list of claims by state inside the
        current Ombuds Office.
        """
        # workflow is first element of the chain
        workflow_id = self.wftool.getChainFor('Claim')[0]
        states = [i for i in self.wftool[workflow_id].states]
        results = {}
        for s in states:
            results[s] = [i for i in self.claims() if i['state'] == s]
        return results


class SearchView(grok.View):
    """Search for a claim with the id specified and redirect to it, if found.
    """
    grok.context(IOmbudsOffice)
    grok.layer(IBrowserLayer)
    grok.name('search-claim')
    grok.require('zope2.View')

    def render(self):
        claim = self.request.form.get('claim', None)
        if not claim:
            msg = _(u'No claim id specified.')
            api.portal.show_message(message=msg, request=self.request, type='error')
        else:
            results = self.context.listFolderContents({'portal_type': 'Claim'})
            results = dict((i.id, i) for i in results)
            if claim in results:
                self.request.response.redirect(results[claim].absolute_url())
                return
            else:
                msg = _(u'Claim id not found.')
                api.portal.show_message(message=msg, request=self.request, type='error')
        self.request.response.redirect(self.context.absolute_url())
