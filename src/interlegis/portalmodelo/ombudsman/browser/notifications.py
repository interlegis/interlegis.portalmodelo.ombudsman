# -*- coding: utf-8 -*-
from collective.watcherlist.browser import BaseMail


class ClaimMail(BaseMail):
    """Define email for claim notifications.
    """
    @property
    def subject(self):
        return self.context.title

    @property
    def plain(self):
        title = self.context.title
        uri = self.context.absolute_url()
        return u'{0}\n{1}'.format(title, uri)

    @property
    def html(self):
        title = self.context.title
        uri = self.context.absolute_url()
        return u'<p><a href="{1}">{0}</a></p>'.format(title, uri)
