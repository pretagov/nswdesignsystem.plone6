from nswdesignsystem.plone6.interfaces import INSWDesignSystemSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema import getFieldsInOrder

import logging


logger = logging.getLogger(__name__)


def _refresh_registry():
    logger.info("Refreshing registry")
    registry = getUtility(IRegistry)
    registry.registerInterface(INSWDesignSystemSettings)


def upgrade_1000_to_1001(context):
    logger.info("Upgrading nswdesignsystem.plone6 addon to 1001")

    _refresh_registry()

    registry = getUtility(IRegistry)
    interface = INSWDesignSystemSettings

    for field, _ in getFieldsInOrder(interface):
        new_id = f"{interface.__identifier__}.{field}"
        old_id = f"nswdesignsystem.{field}"
        try:
            old_record = registry.records[old_id]
        except KeyError:
            continue

        logger.info(
            "Deleting key %s with value %s and inserting into record %s",
            old_id,
            old_record.value,
            new_id,
        )

        if old_record:
            registry[new_id] = old_record.value
        try:
            del registry.records[old_id]
        except KeyError:
            continue
    logger.info("Upgraded nswdesignsystem.plone6 addon to 1001")
