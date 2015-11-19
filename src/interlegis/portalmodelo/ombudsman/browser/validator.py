# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from interlegis.portalmodelo.ombudsman.interfaces import IClaim

from zope.interface import implements, Interface

from zope.schema.interfaces import IField
from zope.component import adapts


from zope.component import getMultiAdapter

from plone.formwidget.recaptcha.validator import WrongCaptchaCode  # noqa

from z3c.form import validator

from z3c.form.interfaces import IValidator


class CaptchaValidator(validator.SimpleFieldValidator):
    implements(IValidator)
    adapts(Interface, Interface, IField, Interface)

    def validate(self, value):
        super(CaptchaValidator, self).validate(value)
        captcha = getMultiAdapter((aq_inner(self.context), self.request),
                                  name='recaptcha')
        if not captcha.verify(input=value):
            raise WrongCaptchaCode
        else:
            return True

# Register Captcha validator for the Captcha field in the ICaptcha Form
validator.WidgetValidatorDiscriminators(CaptchaValidator,
                                        field=IClaim['captcha'])
