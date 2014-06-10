# -*- coding: utf-8 -*-
"""Adapt a Claim with a container of responses.

This is based on code from Products.Poi; for more information see:
https://github.com/collective/Products.Poi/blob/master/Products/Poi/adapters.py
"""
from datetime import datetime
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from persistent import Persistent
from persistent.list import PersistentList
from plone import api
from Products.CMFPlone import PloneMessageFactory as PMF
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.container.contained import ObjectAddedEvent
from zope.container.contained import ObjectRemovedEvent
from zope.event import notify
from zope.interface import Attribute
from zope.interface import implements
from zope.interface import Interface


class IResponseContainer(Interface):
    pass


class IResponse(Interface):

    creator = Attribute('Id of user responding the claim.')
    date = Attribute('Date and time when this response was made.')
    review_state = Attribute('State when this response was made.')
    text = Attribute('Text of the response.')


class ResponseContainer(Persistent):

    implements(IResponseContainer)
    adapts(IClaim)
    ANNO_KEY = 'claim.responses'

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)
        self.__mapping = annotations.get(self.ANNO_KEY, None)
        if self.__mapping is None:
            self.__mapping = PersistentList()
            annotations[self.ANNO_KEY] = self.__mapping

    def __contains__(self, key):
        return key in self.__mapping

    def __getitem__(self, i):
        i = int(i)
        return self.__mapping.__getitem__(i)

    def __delitem__(self, item):
        self.__mapping.__delitem__(item)

    def __len__(self):
        return self.__mapping.__len__()

    def __setitem__(self, i, y):
        self.__mapping.__setitem__(i, y)

    def append(self, item):
        self.__mapping.append(item)

    def remove(self, id):
        id = int(id)
        self[id] = None

    def add(self, item):
        self.append(item)
        id = str(len(self))
        event = ObjectAddedEvent(item, newParent=self.context, newName=id)
        notify(event)

    def delete(self, id):
        event = ObjectRemovedEvent(self[id], oldParent=self.context, oldName=id)
        self.remove(id)
        notify(event)


class Response(Persistent):

    implements(IResponse)

    def get_review_state_title(self, review_state):
        wftool = api.portal.get_tool('portal_workflow')
        title = wftool.getTitleForStateOnType(review_state, 'Claim')
        return PMF(title)

    def __init__(self, review_state, text):
        self.__parent__ = self.__name__ = None
        self.creator = api.user.get_current().id
        self.date = datetime.now()
        self.review_state = self.get_review_state_title(review_state)
        self.text = text
