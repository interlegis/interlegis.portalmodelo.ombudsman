# -*- coding: utf-8 -*-
from collective.watcherlist.browser import BaseMail
from plone import api

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
        wftool = api.portal.get_tool('portal_workflow')
        claim = self.context
        wf_state_id = api.content.get_state(claim)
        # initial state define first template
        if wf_state_id == 'pending':
            template = claim.aq_parent.email_template
        # for other states define second template
        else:
            template = claim.aq_parent.email_template_states

        wf_state_title = wftool.getTitleForStateOnType(wf_state_id, 'Claim')
        status = claim.translate(wf_state_title)
        protocol = claim.getId()
        title = claim.title
        url = claim.absolute_url()
        name = claim.name
        email = claim.email
        address = claim.address
        if not address:
            address = u''
        city = claim.city
        if not city:
            city = u''
        state = claim.state
        if not state:
            state = u''
        code = claim.postal_code
        if not code:
            code = u''
        
        template = template.replace('{protocol}', protocol)
        template = template.replace('{title}', title)
        template = template.replace('{url}', url)
        template = template.replace('{name}', name)
        template = template.replace('{email}', email)
        template = template.replace('{address}', address)
        template = template.replace('{city}', city)
        template = template.replace('{state}', state)
        template = template.replace('{postal_code}', code)
        template = template.replace('{status}', status)
        return template
