# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from genweb.serveistic.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of genweb.serveistic into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if genweb.serveistic is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('genweb.serveistic'))

    def test_uninstall(self):
        """Test if genweb.serveistic is cleanly uninstalled."""
        self.installer.uninstallProducts(['genweb.serveistic'])
        self.assertFalse(self.installer.isProductInstalled('genweb.serveistic'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IGenwebServeisticLayer is registered."""
        from genweb.serveistic.interfaces import IGenwebServeisticLayer
        from plone.browserlayer import utils
        self.failUnless(IGenwebServeisticLayer in utils.registered_layers())
