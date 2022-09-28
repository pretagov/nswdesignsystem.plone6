# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles

from nswdesignsystem.plone6.testing import (  # noqa: E501
    NSWDESIGNSYSTEM_PLONE6_INTEGRATION_TESTING,
)

try:
    from plone.base.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that nswdesignsystem.plone6 is properly installed."""

    layer = NSWDESIGNSYSTEM_PLONE6_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if nswdesignsystem.plone6 is installed."""
        self.assertTrue(self.installer.is_product_installed("nswdesignsystem.plone6"))

    def test_dependencies_installed(self):
        """Test if nswdesignsystem.plone6 is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.volto.formsupport")
        )
        self.assertTrue(
            self.installer.is_product_installed("collective.volto.subfooter")
        )

    def test_browserlayer(self):
        """Test that INswdesignsystemPlone6Layer is registered."""
        from plone.browserlayer import utils

        from nswdesignsystem.plone6.interfaces import INswdesignsystemPlone6Layer

        self.assertIn(INswdesignsystemPlone6Layer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = NSWDESIGNSYSTEM_PLONE6_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("nswdesignsystem.plone6")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if nswdesignsystem.plone6 is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("nswdesignsystem.plone6"))

    def test_browserlayer_removed(self):
        """Test that INswdesignsystemPlone6Layer is removed."""
        from plone.browserlayer import utils

        from nswdesignsystem.plone6.interfaces import INswdesignsystemPlone6Layer

        self.assertNotIn(INswdesignsystemPlone6Layer, utils.registered_layers())
