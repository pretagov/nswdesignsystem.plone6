from plone.schema import ASCIILine
from plone.supermodel.model import Fieldset
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.autoform import directives
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface

from nswdesignsystem.plone6.constants import (
    COLOUR_PALETTE,
    SCHEMA_PREFIX,
    CONTROL_PANEL_TITLE,
)


class INSWDesignSystemSettings(Interface):
    nsw_brand_dark = ASCIILine(
        title="NSW Brand dark",
        description="Set the primary colour",
        required=False,
    )
    directives.widget(
        "nsw_brand_dark",
        frontendOptions={
            "widget": "color_picker",
            "widgetProps": {"colors": COLOUR_PALETTE},
        },
    )


INSWDesignSystemSettings.setTaggedValue(
    FIELDSETS_KEY,
    [
        Fieldset(
            "independent_fieldset",
            fields=["nsw_brand_dark"],
            label="Independent branding",
            description="Settings in here require an independent branding exemption.",
        )
    ],
)


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
