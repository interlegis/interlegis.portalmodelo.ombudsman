# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from five import grok
from interlegis.portalmodelo.ombudsman.adapters import IResponseContainer
from interlegis.portalmodelo.ombudsman.browser import validator
from interlegis.portalmodelo.ombudsman.interfaces import IBrowserLayer
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from plone import api
from plone.dexterity.utils import addContentToContainer
from plone.directives import dexterity
from plone.directives import form
from plone.memoize import view
from plone.registry.interfaces import IRegistry
from Products.CMFPlone import PloneMessageFactory as PMF
from z3c.form import field
from zope.component import queryUtility

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
        return api.user.has_permission(
            'interlegis.portalmodelo.ombudsman: Add Response')

    @property
    def can_view_personal_info(self):
        return api.user.has_permission(
            'interlegis.portalmodelo.ombudsman: View Claim Personal Info')

    def is_anonymous(self):
        return api.user.is_anonymous()

    def transitions(self):
        """Return a list of available transitions for the claim.
        """
        wftool = api.portal.get_tool('portal_workflow')
        available_transitions = wftool.getTransitionsFor(self.context)
        current_state = api.content.get_state(self.context)

        # as first, we add the current state as a no-change condition
        transitions = [dict(id=current_state, title=PMF('No change'))]

        # now we add the all available transitions
        for i in available_transitions:
            transitions.append(
                dict(id=i['id'], title=PMF(i['name'])))

        return transitions

    def _responses(self):
        """Return a list of responses for the current Claim.
        """
        transforms = api.portal.get_tool('portal_transforms')
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
                text=transforms.convertTo(
                    'text/html',
                    response.text,
                    context=self.context,
                    mimetype='text/x-web-intelligent'
                ).getData()
            ))
        return responses

    @view.memoize
    def responses(self):
        return self._responses()

    def has_responses(self):
        return len(self.responses()) > 0

    def _files(self):
        """Return a list of files for the current Claim ordered by creation date
        """
        path = '/'.join(self.context.getPhysicalPath())
        ct = api.portal.get_tool('portal_catalog')
        results = ct.searchResults(
            portal_type='File',
            path=path,
            sort_on='created',
        )
        files = []
        for id, brain in enumerate(results):
            files.append(dict(
                id=id + 1,
                title=brain.Title,
                creator=brain.Creator,
                description=brain.Description,
                url='{0}/at_download/file'.format(brain.getURL()),
                date=brain.created,
            ))
        return files

    @view.memoize
    def files(self):
        return self._files()

    def has_files(self):
        return len(self.files()) > 0


class AddView(dexterity.AddForm):
    grok.name('Claim')
    grok.require('interlegis.portalmodelo.ombudsman.AddClaim')

    def show_recaptcha_widget(self):
        anon = api.user.is_anonymous()
        q_i = api.portal.get_tool(name='portal_quickinstaller')
        recaptcha_installed = q_i.isProductInstalled(
            'plone.formwidget.recaptcha')
        recaptcha_configured = False

        if recaptcha_installed:
            from plone.formwidget.recaptcha.interfaces import IReCaptchaSettings
            registry = queryUtility(IRegistry)
            settings = registry.forInterface(IReCaptchaSettings)
            recaptcha_configured = (len(settings.public_key) > 0)
        return (recaptcha_installed and recaptcha_configured)

    def update(self):
        if self.show_recaptcha_widget():
            self.fields = field.Fields(IClaim).select('captcha')
            from plone.formwidget.recaptcha import ReCaptchaFieldWidget
            self.fields['captcha'].widgetFactory = ReCaptchaFieldWidget
            self.fields.widgetFactory = form.mode(captcha='display')
        # XXX: currently, any user can add a claim
        #      do we need to check if the user is anonymous?
        super(AddView, self).update()

    def add(self, object):
        """Add the object to the container skipping constraints and
        redirect to the container.
        """
        container = aq_inner(self.context)

        data, errors = self.extractData()
        if errors:
            return

        # Validate Captcha
        anon = api.user.is_anonymous()
        good_to_go = False
        if 'captcha' not in data:
            data['captcha'] = u""
        captcha = validator.CaptchaValidator(self.context,
                                             self.request,
                                             None,
                                             IClaim['captcha'],
                                             None)
        if captcha.validate(data['captcha']):
            good_to_go = True

        else:
            good_to_go = True

        if good_to_go:
            obj = addContentToContainer(
                container, object, checkConstraints=False)
            self.immediate_view = '{0}/{1}'.format(
                container.absolute_url(), obj.id)


