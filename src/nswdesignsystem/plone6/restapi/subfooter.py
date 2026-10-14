from collective.volto.subfooter.interfaces import ISubfooter
from collective.volto.subfooter.restapi.serializer.subfooter import serialize_data
from plone import api
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import logging


logger = logging.getLogger(__name__)


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class Subfooter:
    """What `@subfooter` returns, as the `subfooter` component of a content response.

    collective.volto.subfooter only provides the `@subfooter` service. Its
    response is a list, so here it goes under `items`.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "subfooter": {
                "@id": f"{api.portal.get().absolute_url()}/@subfooter",
            }
        }
        if not expand:
            return result

        # Don't set an error status here: it would apply to the whole content response
        try:
            record = api.portal.get_registry_record(
                "subfooter_configuration", interface=ISubfooter, default=""
            )
            items = serialize_data(json_data=record) if record else []
        except Exception:
            logger.exception("Could not expand subfooter")
            return result

        result["subfooter"]["items"] = items or []
        return result
