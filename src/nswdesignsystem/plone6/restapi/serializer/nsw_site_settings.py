from nswdesignsystem.plone6.interfaces import INSWDesignSystemSettings
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import implementer

import json


def serialize_data(json_data, request):
    if not json_data:
        return ""
    try:
        return json_compatible(json.loads(json_data))
    except TypeError as e:
        if isinstance(json_data, dict):
            return json_compatible(json_data)
        request.response.setStatus(400)
        return json_compatible(
            {
                "error": {
                    "type": "SerializationError",
                    "message": str(e),
                }
            }
        )
    except Exception as e:
        request.response.setStatus(400)
        return json_compatible(
            {
                "error": {
                    "type": "SerializationError",
                    "message": str(e),
                }
            }
        )


@implementer(ISerializeToJson)
@adapter(INSWDesignSystemSettings)
class INSWDesignSystemSettingsSerializeToJson(ControlpanelSerializeToJson):
    def __call__(self):
        json_data = super().__call__()
        conf = json_data["data"].get("subfooter_configuration", "")
        if conf:
            json_data["data"]["subfooter_configuration"] = json.dumps(
                serialize_data(json_data=conf, request=self.request)
            )
        return json_data
