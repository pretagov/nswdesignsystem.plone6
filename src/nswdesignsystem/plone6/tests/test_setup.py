"""Setup tests for this package."""
from nswdesignsystem.plone6.testing import (  # noqa: E501
    NSWDESIGNSYSTEM_PLONE6_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


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

        # TODO: Find out why the setup in `testing.py` isn't working for this profile install
        applyProfile(self.portal, "nswdesignsystem.plone6:default")

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
        from nswdesignsystem.plone6.interfaces import INswdesignsystemPlone6Layer
        from plone.browserlayer import utils

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
        from nswdesignsystem.plone6.interfaces import INswdesignsystemPlone6Layer
        from plone.browserlayer import utils

        self.assertNotIn(INswdesignsystemPlone6Layer, utils.registered_layers())
