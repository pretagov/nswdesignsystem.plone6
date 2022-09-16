# -*- coding: utf-8 -*-
from plone.api.content import create as createContent
from plone.api.content import get as getContent
from plone.api.content import delete as deleteContent
from plone.api.portal import get as getPortal
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "nswdesignsystem.plone6:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["nswdesignsystem.plone6.upgrades"]


def create_global_search_page(context):
    portal = getPortal()
    search_page = getContent(path="/about")

    if not search_page:
        search_page = createContent(
            id="search", type="Document", title="Search", container=portal
        )
    search_page.blocks = {
        "cc6cf326-69b5-42da-b768-0eb89b0a152f": {"@type": "title"},
        "e633675a-8067-49cb-97c5-b74ac7314f53": {
            "@type": "search",
            "showSearchInput": True,
            "facetsTitle": "Filter results",
            "listingBodyTemplate": "default",
            "showSortOn": True,
            "sortOnLabel": "Sort by",
            "sortOnOptions": ["created", "sortable_title"],
            "variation": "facetsLeftSide",
            "query": {
                "query": [
                    {
                        "i": "path",
                        "o": "plone.app.querystring.operation.string.absolutePath",
                        "v": "/",
                    },
                    {
                        "i": "portal_type",
                        "o": "plone.app.querystring.operation.selection.none",
                        "v": ["Image", "File"],
                    },
                ],
                "sort_order": "ascending",
            },
        },
    }
    search_page.blocks_layout = {
        "items": [
            "cc6cf326-69b5-42da-b768-0eb89b0a152f",
            "e633675a-8067-49cb-97c5-b74ac7314f53",
        ]
    }
    search_page.exclude_from_nav = True


def post_install(context):
    """Post install script"""
    create_global_search_page(context)
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    portal = getPortal()
    deleteContent(portal["search"])
    # Do something at the end of the uninstallation of this package.
