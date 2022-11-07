from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)

from plone.restapi.controlpanels import RegistryConfigletPanel

from zope.component import adapter
from zope.interface import Interface

from nswdesignsystem.plone6.constants import (
    SCHEMA_PREFIX,
    CONTROL_PANEL_TITLE,
)
from nswdesignsystem.plone6.interfaces import INSWDesignSystemSettings


class NSWDesignSystemRegistryEditForm(RegistryEditForm):
    label = CONTROL_PANEL_TITLE
    schema = INSWDesignSystemSettings
    schema_prefix = SCHEMA_PREFIX


class NSWDesignSystemControlPanelFormWrapper(ControlPanelFormWrapper):
    form = NSWDesignSystemRegistryEditForm


@adapter(Interface, Interface)
class NSWDesignSystemRegistryConfigletPanel(RegistryConfigletPanel):
    """Volto control panel"""

    title = CONTROL_PANEL_TITLE
    schema = INSWDesignSystemSettings
    schema_prefix = SCHEMA_PREFIX
    configlet_id = "nswdesignsystem"
    configlet_category_id = "Products"
    group = "Products"
