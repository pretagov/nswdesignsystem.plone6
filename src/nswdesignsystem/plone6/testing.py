# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    PLONE_FIXTURE,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing import z2
from plone.testing.zope import WSGI_SERVER_FIXTURE

import nswdesignsystem.plone6


class NswdesignsystemPlone6Layer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=nswdesignsystem.plone6)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "nswdesignsystem.plone6:default")


NSWDESIGNSYSTEM_PLONE6_FIXTURE = NswdesignsystemPlone6Layer()


NSWDESIGNSYSTEM_PLONE6_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NSWDESIGNSYSTEM_PLONE6_FIXTURE,),
    name="NswdesignsystemPlone6Layer:IntegrationTesting",
)


NSWDESIGNSYSTEM_PLONE6_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(NSWDESIGNSYSTEM_PLONE6_FIXTURE,),
    name="NswdesignsystemPlone6Layer:FunctionalTesting",
)


NSWDESIGNSYSTEM_PLONE6_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        NSWDESIGNSYSTEM_PLONE6_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="NswdesignsystemPlone6Layer:AcceptanceTesting",
)
