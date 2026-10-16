from nswdesignsystem.plone6.interfaces import INSWDesignSystemSettings
from nswdesignsystem.plone6.restapi.serializer.nsw_site_settings import serialize_data
from plone import api
from plone.autoform.interfaces import OMITTED_KEY
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces import IPublishTraverse
from zope.schema import getFields

import logging


logger = logging.getLogger(__name__)


def get_records():
    omitted_fields = INSWDesignSystemSettings.getTaggedValue(OMITTED_KEY)
    # Using the fieldset key to ensure that the removed fields from ISocialMediaSchema aren't included
    fields = [
        field
        for field in getFields(INSWDesignSystemSettings)
        if field not in omitted_fields
    ]
    return {
        field: api.portal.get_registry_record(
            field,
            interface=INSWDesignSystemSettings,
            default="",
        )
        for field in fields
    }


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class NSWSiteSettings:
    """The site settings as the `nswSiteSettings` component of a content response."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "nswSiteSettings": {
                "@id": f"{self.context.absolute_url()}/@nswSiteSettings",
            }
        }
        if not expand:
            return result

        # Don't set an error status here: it would apply to the whole content response
        try:
            records = get_records()
        except Exception:
            logger.exception("Could not expand nswSiteSettings")
            return result

        result["nswSiteSettings"].update(json_compatible(records))
        return result


@implementer(IPublishTraverse)
class NSWSiteSettingsGet(Service):
    def __init__(self, context, request):
        super().__init__(context, request)

    def reply(self):
        records = {}

        try:
            records = get_records()
        except KeyError:
            # TODO: Better logging & response of missing key
            return {}
        except Exception as error:
            # TODO: Do I need a 400 error?
            self.request.response.setStatus(400)
            return {
                "error": dict(
                    type=error.__class__.__name__,
                    message=translate(str(error), context=self.request),
                )
            }

        if not records:
            return {}

        return serialize_data(json_data=records, request=self.request)
