from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.autoform import directives
from plone.autoform.interfaces import OMITTED_KEY
from plone.base.interfaces.controlpanel import ISocialMediaSchema
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.schema import ASCIILine, Bool, Int
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset
from zope.component import adapter
from zope.interface import Interface
from zope.schema import getFields

from nswdesignsystem.plone6.constants import (
    COLOUR_PALETTE,
    SCHEMA_PREFIX,
    CONTROL_PANEL_TITLE,
)


class INSWDesignSystemSettings(ISocialMediaSchema):
    breadcrumb_start_depth = Int(
        title="Breadcrumb start depth",
        description="What depth in the site to start showing the breadcrumb",
        min=1,
        max=5,
        default=2,
    )
    show_site_title_text = Bool(
        title="Show site title name in header",
        description="Whether to show the name of the site next to the site logo",
        default=True,
    )
    linkedin_url = ASCIILine(
        title="LinkedIn URL",
        required=False,
    )
    youtube_url = ASCIILine(
        title="YouTube URL",
        required=False,
    )
    nsw_brand_dark = ASCIILine(
        title="NSW Brand dark colour",
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


excluded_social_fields = ["share_social_data", "facebook_app_id"]
social_fields = [
    *[
        field
        for field in getFields(ISocialMediaSchema).keys()
        if field not in excluded_social_fields
    ],
    "linkedin_url",
    "youtube_url",
]

INSWDesignSystemSettings.setTaggedValue(
    OMITTED_KEY,
    [(Interface, field, "true") for field in excluded_social_fields],
)

INSWDesignSystemSettings.setTaggedValue(
    FIELDSETS_KEY,
    [
        Fieldset(
            "social_fieldset",
            fields=social_fields,
            label="Social links",
        ),
        Fieldset(
            "independent_fieldset",
            fields=["show_site_title_text", "nsw_brand_dark"],
            label="Independent branding",
            description="Settings in here require an independent branding exemption.",
        ),
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
