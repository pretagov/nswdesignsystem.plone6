"""Module where all interfaces, events and exceptions live."""

from nswdesignsystem.plone6.constants import COLOUR_PALETTE
from plone.autoform import directives
from plone.base.interfaces.controlpanel import ISocialMediaSchema
from plone.schema import ASCIILine
from plone.schema import Bool
from plone.schema import Int
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import getFields


class INswdesignsystemPlone6Layer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class INSWDesignSystemSettings(ISocialMediaSchema):
    # DEFAULT FIELDSET
    breadcrumb_start_depth = Int(
        title="Breadcrumb start depth",
        description="What depth in the site to start showing the breadcrumb",
        min=1,
        max=5,
        default=2,
    )
    acknowledgement_of_country = ASCIILine(
        title="Acknowledgement of country",
        required=False,
    )

    # SOCIAL FIELDSET
    directives.omitted("share_social_data")
    directives.omitted("facebook_app_id")
    linkedin_url = ASCIILine(
        title="LinkedIn URL",
        required=False,
    )
    youtube_url = ASCIILine(
        title="YouTube URL",
        required=False,
    )

    # INDEPENDENT FIELDSET
    show_site_title_text = Bool(
        title="Show site title name in header",
        description="Whether to show the name of the site next to the site logo",
        default=True,
        required=False,
    )
    show_acknowledgement_of_country = Bool(
        title="Show acknowledgement of country",
        description="Whether to show the AOC in the lower footer if providing a custom implementation",
        default=True,
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
    nsw_brand_light = ASCIILine(
        title="NSW Brand light colour",
        description="Set the secondary colour",
        required=False,
    )
    directives.widget(
        "nsw_brand_light",
        frontendOptions={
            "widget": "color_picker",
            "widgetProps": {"colors": COLOUR_PALETTE},
        },
    )
    nsw_brand_accent = ASCIILine(
        title="NSW Brand accent colour",
        description="Set the accent colour",
        required=False,
    )
    directives.widget(
        "nsw_brand_accent",
        frontendOptions={
            "widget": "color_picker",
            "widgetProps": {"colors": COLOUR_PALETTE},
        },
    )
    nsw_brand_supplementary = ASCIILine(
        title="NSW Brand supplementary colour",
        description="Set the supplementary colour",
        required=False,
    )
    directives.widget(
        "nsw_brand_supplementary",
        frontendOptions={
            "widget": "color_picker",
            "widgetProps": {"colors": COLOUR_PALETTE},
        },
    )
    nsw_independent_upper_footer_colour = ASCIILine(
        title="Upper footer background colour",
        required=False,
    )
    directives.widget(
        "nsw_independent_upper_footer_colour",
        frontendOptions={
            "widget": "color_picker",
            "widgetProps": {"colors": COLOUR_PALETTE},
        },
    )
    nsw_independent_aoc_colour = ASCIILine(
        title="Custom AOC background colour",
        required=False,
    )
    directives.widget(
        "nsw_independent_aoc_colour",
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
    FIELDSETS_KEY,
    [
        Fieldset(
            "social_fieldset",
            fields=social_fields,
            label="Social links",
        ),
        Fieldset(
            "independent_fieldset",
            fields=[
                "show_site_title_text",
                "show_acknowledgement_of_country",
                "nsw_brand_dark",
                "nsw_brand_light",
                "nsw_brand_accent",
                "nsw_brand_supplementary",
                "nsw_independent_upper_footer_colour",
                "nsw_independent_aoc_colour",
            ],
            label="Independent branding",
            description="Settings in here require an independent branding exemption.",
        ),
    ],
)
