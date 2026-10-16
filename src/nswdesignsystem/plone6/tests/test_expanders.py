"""Tests for the nswSiteSettings and subfooter API expanders."""
from collective.volto.subfooter.interfaces import ISubfooter
from nswdesignsystem.plone6.interfaces import INSWDesignSystemSettings
from nswdesignsystem.plone6.testing import (  # noqa: E501
    NSWDESIGNSYSTEM_PLONE6_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.restapi.interfaces import ISerializeToJson
from zope.component import getMultiAdapter

import json
import unittest


class TestExpanders(unittest.TestCase):
    layer = NSWDESIGNSYSTEM_PLONE6_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        applyProfile(self.portal, "nswdesignsystem.plone6:default")
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.doc = api.content.create(
            container=self.portal, type="Document", id="doc", title="A page"
        )
        api.portal.set_registry_record(
            "breadcrumb_start_depth", 3, interface=INSWDesignSystemSettings
        )
        api.portal.set_registry_record(
            "subfooter_configuration",
            json.dumps(
                [
                    {
                        "rootPath": "/",
                        "items": [
                            {"title": "A page", "linkUrl": [self.doc.UID()]},
                        ],
                    }
                ]
            ),
            interface=ISubfooter,
        )

    def service(self, context, name):
        # plone.rest registers each service as a view named after method, type and name
        return getMultiAdapter(
            (context, self.request), name=f"GET_application_json_{name}"
        ).reply()

    def serialize(self, context, expand=None):
        if expand:
            self.request.form["expand"] = expand
        return getMultiAdapter((context, self.request), ISerializeToJson)()

    def test_not_expanded(self):
        components = self.serialize(self.doc)["@components"]
        self.assertEqual(
            components["nswSiteSettings"],
            {"@id": "http://nohost/plone/doc/@nswSiteSettings"},
        )
        self.assertEqual(
            components["subfooter"], {"@id": "http://nohost/plone/@subfooter"}
        )

    def test_nsw_site_settings_expanded(self):
        settings = self.serialize(self.doc, "nswSiteSettings")["@components"][
            "nswSiteSettings"
        ]
        self.assertEqual(settings["breadcrumb_start_depth"], 3)
        expected = self.service(self.portal, "@nswSiteSettings")
        self.assertEqual({k: v for k, v in settings.items() if k != "@id"}, expected)

    def test_subfooter_expanded(self):
        subfooter = self.serialize(self.doc, "subfooter")["@components"]["subfooter"]
        self.assertEqual(subfooter["@id"], "http://nohost/plone/@subfooter")
        self.assertEqual(subfooter["items"], self.service(self.portal, "@subfooter"))
        link = subfooter["items"][0]["items"][0]["linkUrl"][0]
        self.assertEqual(link["@id"], "http://nohost/plone/doc")
        self.assertEqual(link["UID"], self.doc.UID())

    def test_subfooter_expanded_without_configuration(self):
        api.portal.set_registry_record(
            "subfooter_configuration", "", interface=ISubfooter
        )
        subfooter = self.serialize(self.doc, "subfooter")["@components"]["subfooter"]
        self.assertEqual(subfooter["items"], [])

    def test_expanded_on_site_root(self):
        components = self.serialize(self.portal, "nswSiteSettings,subfooter")[
            "@components"
        ]
        self.assertEqual(components["nswSiteSettings"]["breadcrumb_start_depth"], 3)
        self.assertEqual(len(components["subfooter"]["items"]), 1)
