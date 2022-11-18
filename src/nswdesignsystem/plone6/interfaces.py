# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.autoform import directives
from plone.base.interfaces.controlpanel import ISocialMediaSchema
from plone.schema import ASCIILine, Bool, Int
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import getFields

from nswdesignsystem.plone6.constants import (
    COLOUR_PALETTE,
)


class INswdesignsystemPlone6Layer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class INSWDesignSystemSettings(ISocialMediaSchema):
    directives.omitted("share_social_data")
    directives.omitted("facebook_app_id")
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
                "nsw_brand_dark",
                "nsw_brand_light",
                "nsw_brand_accent",
                "nsw_brand_supplementary",
            ],
            label="Independent branding",
            description="Settings in here require an independent branding exemption.",
        ),
    ],
)
