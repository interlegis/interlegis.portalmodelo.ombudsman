# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.app.content.interfaces import INameFromTitle
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class INameFromDate(Interface):
    """An object that supports gettings it name from its creation date."""


# XXX: refactor, seems to me this is not the best way to implement
#      a namechooser; we should be independent from INameFromTitle
#      also, it should be safer to use microseconds instead time
class NameFromDate(object):
    """Automatically generates name for content based on its creation date.
    """
    implements(INameFromTitle)
    adapts(INameFromDate)

    def __new__(cls, context):
        title = DateTime().strftime('%Y%m%d%H%M%S')
        instance = super(NameFromDate, cls).__new__(cls)
        instance.title = title
        return instance

    def __init__(self, context):
        pass
