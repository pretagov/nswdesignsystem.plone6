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
        super().__init__(context, request)

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
                    field,
                    interface=INSWDesignSystemSettings,
                    default="",
                )
                for field in fields
            }
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
