# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.api.utils import type_cast
from interlegis.portalmodelo.ombudsman.interfaces import IClaim
from interlegis.portalmodelo.ombudsman.interfaces import IOmbudsOffice
from interlegis.portalmodelo.ombudsman.adapters import IResponseContainer
from plone import api
# from plone.autoform.interfaces import READ_PERMISSIONS_KEY
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getUtility
from zope.schema import getFieldsInOrder

import json


def permission_map_for_anonymous():
    if api.user.is_anonymous():
        return [
            'email', 'genre', 'age', 'address', 'postal_code',
            'name', 'city', 'state']
    return []


class JSONView(grok.View):
    """Generates a JSON with information about Ombuds Offices and claims.
    """
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('ombudsman-json')

    def update(self):
        self.catalog = api.portal.get_tool('portal_catalog')

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        j = {}
        j['ombudsoffices'] = self.get_ombudsoffices()
        j['claims'] = self.get_claims()
        return json.dumps(j, sort_keys=True, indent=4)

    def serialize(self, results):
        """Serialize fields of a list of Dexterity-based content type objects.

        :param results: [required] list of objects to be serialized
        :type results: list of catalog brains
        :returns: list of serialized objects
        :rtype: list of dictionaries
        """
        s = []
        for i in results:
            obj = i.getObject()
            # initialize a dictionary with the object uri
            fields = dict(uri=obj.absolute_url())  # XXX: should we use UUID?
            # find out object schema to list its fields
            schema = getUtility(IDexterityFTI, name=obj.portal_type).lookupSchema()
            # XXX: probably there's a better way to accomplish this
            # but I do not know how to access the roles and permissions
            # of an anonymous user
            # read_permission_mapping = schema.queryTaggedValue(READ_PERMISSIONS_KEY)
            # if read_permission_mapping is None:
            # read_permission_mapping = {}
            read_permission_mapping = []
            if obj.portal_type == 'Claim':
                read_permission_mapping = permission_map_for_anonymous()

                # Date fields that are not being presented.
                fields['modification_date'] = obj.modification_date.ISO8601()
                fields['creation_date'] = obj.creation_date.ISO8601()
                # Set the review state for a Claim.
                review_state = api.content.get_state(obj=obj)
                fields['review_state'] = review_state
                # Set a list of responses.
                fields['responses'] = self.set_claim_response(obj)

            # TODO: Should we include attached fields information to the
            # JSON API?

            # continue with the rest of the fields
            for name, field in getFieldsInOrder(schema):
                if name in read_permission_mapping:
                    continue  # private information; do not display it
                # 'name' could be a @property and not a real field
                if not hasattr(obj, name):
                    continue
                value = getattr(obj, name)
                fields[name] = type_cast(value)
            s.append(fields)
        return s

    def get_ombudsoffices(self):
        """Return list of Ombuds Office objects on site as a list of
        dictionaries.
        """
        results = self.catalog(object_provides=IOmbudsOffice.__identifier__)
        return self.serialize(results)

    def get_claims(self):
        """Return list of Claim objects on site as a list of dictionaries.
        """
        results = self.catalog(object_provides=IClaim.__identifier__)
        return self.serialize(results)

    def set_claim_response(self, claim):
        """Return a list of Claim response objects as dictionaries.
        """
        results = []
        container = IResponseContainer(claim)
        for id, response in enumerate(container):
            if response is None:
                continue  # response has been removed
            results.append(dict(id=id + 1,
                                creator=type_cast(response.creator),
                                date=type_cast(response.date),
                                review_state=type_cast(response.review_state),
                                text=type_cast(response.text)))
        return results
