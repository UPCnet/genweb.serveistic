from mock import Mock, patch

from plone.testing.z2 import Browser
from plone import api
from transaction import commit

from genweb.serveistic.testing import FunctionalTestCase
from genweb.serveistic.tests.fixtures import fixtures


class TestRetrieveIndicadors(FunctionalTestCase):
    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.portal)

    def assertAppearsBefore(self, subtxt_1, subtxt_2, txt):
        self.assertIn(subtxt_1, txt)
        self.assertIn(subtxt_2, txt)
        self.assertTrue(txt.find(subtxt_1) < txt.find(subtxt_2))

    def assertAppearInOrder(self, subtxts, txt):
        def assertAppearsBefore(subtxt_1, subtxt_2):
            self.assertAppearsBefore(subtxt_1, subtxt_2, txt)
            return subtxt_2
        reduce(assertAppearsBefore, subtxts)

    def test_retrieve_from_ws(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        # indicadors not empty, count is present
        indicadors = [
            Mock(
                identifier="id-1",
                description="Indicador 1",
                categories=[
                    Mock(description="Categoria 1.1", value="v1.1"),
                    Mock(description="Categoria 1.2", value="v1.2"),
                    ]
                ),
            Mock(
                identifier="id-2",
                description="Indicador 2",
                categories=[
                    Mock(description="Categoria 2.1", value="v2.1"),
                    Mock(description="Categoria 2.2", value="v2.2"),
                    Mock(description="Categoria 2.3", value="v2.3"),
                    ]
                ),
            ]
        with patch('genweb.serveistic.data_access.indicadors.IndicadorsDataReporter.list_by_service_id',
                   side_effect=(indicadors,)):
            query_string = "?count=5"
            self.browser.open(view.url() + query_string)
            self.assertAppearInOrder([
                "Indicador 1",
                "Categoria 1.1", "v1.1",
                "Categoria 1.2", "v1.2",
                "Indicador 2",
                "Categoria 2.1", "v2.1",
                "Categoria 2.2", "v2.2",
                "Categoria 2.3", "v2.3"
                ],
                self.browser.contents)
            self.assertIn(
                "Tots els indicadors",
                self.browser.contents)
            self.assertNotIn(
                "No hi ha cap indicador enregistrat relacionat amb "
                "aquest servei",
                self.browser.contents)

        # indicadors not empty, count not present
        indicadors = [
            Mock(
                identifier="id-1",
                description="Indicador 1",
                categories=[
                    Mock(description="Categoria 1.1", value="v1.1"),
                    Mock(description="Categoria 1.2", value="v1.2"),
                    ]
                ),
            Mock(
                identifier="id-2",
                description="Indicador 2",
                categories=[
                    Mock(description="Categoria 2.1", value="v2.1"),
                    Mock(description="Categoria 2.2", value="v2.2"),
                    Mock(description="Categoria 2.3", value="v2.3"),
                    ]
                ),
            ]
        with patch('genweb.serveistic.data_access.indicadors.IndicadorsDataReporter.list_by_service_id',
                   side_effect=(indicadors,)):
            self.browser.open(view.url())
            self.assertAppearInOrder([
                "Indicador 1",
                "Categoria 1.1", "v1.1",
                "Categoria 1.2", "v1.2",
                "Indicador 2",
                "Categoria 2.1", "v2.1",
                "Categoria 2.2", "v2.2",
                "Categoria 2.3", "v2.3"
                ],
                self.browser.contents)
            self.assertNotIn(
                "Tots els indicadors",
                self.browser.contents)
            self.assertNotIn(
                "No hi ha cap indicador enregistrat relacionat amb "
                "aquest servei",
                self.browser.contents)

        # indicators is empty
        with patch('genweb.serveistic.data_access.indicadors.IndicadorsDataReporter.list_by_service_id',
                   side_effect=([],)):
            self.browser.open(view.url())
            self.assertIn(
                "No hi ha cap indicador enregistrat relacionat amb "
                "aquest servei",
                self.browser.contents)
            self.assertNotIn(
                "Tots els indicadors",
                self.browser.contents)

        # indicadors is None
        with patch('genweb.serveistic.data_access.indicadors.IndicadorsDataReporter.list_by_service_id',
                   side_effect=(None,)):
            self.browser.open(view.url())
            self.assertIn(
                "No hi ha cap indicador enregistrat relacionat amb "
                "aquest servei",
                self.browser.contents)
            self.assertNotIn(
                "Tots els indicadors",
                self.browser.contents)

    def test_retrieve_from_ws_when_servei_has_no_service_id(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_without_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])
        self.browser.open(view.url())

        self.assertIn(
            "No hi ha cap indicador enregistrat relacionat amb "
            "aquest servei",
            self.browser.contents)
        self.assertNotIn(
            "Tots els indicadors",
            self.browser.contents)
