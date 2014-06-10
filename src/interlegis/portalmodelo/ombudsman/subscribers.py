# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from collective.watcherlist.interfaces import IWatcherList
from five import grok
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


@grok.subscribe(IClaim, IObjectAddedEvent)
@grok.subscribe(IClaim, IObjectModifiedEvent)
def added_response(claim, event):
    """Send message to people involved in the claim when it is created or
    modified.
    """
    ombudsoffice = aq_parent(claim)
    watchers = IWatcherList(claim)
    # clear the list of watchers to deal with any change
    watchers.watchers = []

    # add the email for the responsible area, if exists
    emails = ombudsoffice.get_emails_for_areas()
    email = emails.get(claim.area)
    if email:
        watchers.watchers.append(email)

    # add the email of the owner of the claim
    watchers.watchers.append(claim.email)

    watchers.send('claim-mail')
