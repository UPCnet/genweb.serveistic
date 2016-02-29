# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE


import unittest2 as unittest


class GenwebServeisticLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import genweb.upc
        import genweb.serveistic
        self.loadZCML(package=genweb.upc)
        self.loadZCML(package=genweb.serveistic)
        z2.installProduct(app, 'Products.DateRecurringIndex')
        z2.installProduct(app, 'plone.app.contenttypes')
        z2.installProduct(app, 'genweb.controlpanel')
        z2.installProduct(app, 'genweb.theme')
        z2.installProduct(app, 'genweb.portlets')
        z2.installProduct(app, 'genweb.banners')
        z2.installProduct(app, 'genweb.serveistic')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'genweb.controlpanel:default')
        applyProfile(portal, 'genweb.theme:default')
        applyProfile(portal, 'genweb.portlets:default')
        applyProfile(portal, 'genweb.banners:default')
        applyProfile(portal, 'genweb.serveistic:default')

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # Commit so that the test browser sees these objects
        portal.portal_catalog.clearFindAndRebuild()
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')
        z2.uninstallProduct(app, 'plone.app.contenttypes')
        z2.uninstallProduct(app, 'genweb.controlpanel')
        z2.uninstallProduct(app, 'genweb.theme')
        z2.uninstallProduct(app, 'genweb.portlets')
        z2.uninstallProduct(app, 'genweb.banners')
        z2.uninstallProduct(app, 'genweb.serveistic')


FIXTURE = GenwebServeisticLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="GenwebServeisticLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="GenwebServeisticLayer:Functional")
ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="GenwebServeisticLayer:Robot")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
