# -*- coding: utf-8 -*-
from nswdesignsystem.plone6.interfaces import INSWDesignSystemSettings
from nswdesignsystem.plone6.restapi.serializer.nsw_site_settings import serialize_data
from plone import api
from plone.autoform.interfaces import OMITTED_KEY
from plone.restapi.services import Service
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.schema import getFields


@implementer(IPublishTraverse)
class NSWSiteSettingsGet(Service):
    def __init__(self, context, request):
        super(NSWSiteSettingsGet, self).__init__(context, request)

    def reply(self):
        omitted_fields = INSWDesignSystemSettings.getTaggedValue(OMITTED_KEY)
        # Using the fieldset key to ensure that the removed fields from ISocialMediaSchema aren't included
        fields = [
            field
            for field in getFields(INSWDesignSystemSettings)
            if field not in omitted_fields
        ]
        records = {}

        try:
            records = {
                field: api.portal.get_registry_record(
                    # TODO: Why do I need to manually add the prefix here and why does using the `interface` argument fail?
                    f"nswdesignsystem.{field}",
                    default="",
                )
                for field in fields
            }
        except KeyError as e:
            # TODO: Better logging & response of missing key
            return {}
        except Exception as e:
            # TODO: Do I need a 400 error?
            self.request.response.setStatus(400)
            return {
                "error": dict(
                    type=e.__class__.__name__,
                    message=translate(str(e), context=self.request),
                )
            }

        site_depth = (
            len([val for val in self.context.absolute_url_path().split("/") if val]) + 1
        )

        records["site_depth"] = site_depth

        if not records:
            return {}

        return serialize_data(json_data=records)
