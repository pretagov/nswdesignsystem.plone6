from nswdesignsystem.plone6.interfaces import INSWDesignSystemSettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


# Gives 'nswdesignsystem.plone6.interfaces'. Doing it this way in case we move it later
SCHEMA_PREFIX = INSWDesignSystemSettings.__identifier__
CONTROL_PANEL_TITLE = "NSW Design System Settings"


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
