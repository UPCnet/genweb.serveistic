from mock import Mock, patch

from plone.testing.z2 import Browser
from plone import api
from transaction import commit

from genweb.serveistic.testing import FunctionalTestCase
from genweb.serveistic.tests.fixtures import fixtures


class TestRetrieveProblemes(FunctionalTestCase):
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

    def test_retrieve_from_path(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_without_product_id)
        fixtures.create_content(
            servei['problemes'], fixtures.problema_1)
        fixtures.create_content(
            servei['problemes'], fixtures.problema_2)
        commit()

        view = api.content.get_view(
            'retrieve_problemes', servei, self.layer['request'])

        # problems not empty, count is present
        query_string = "?count=5"
        self.browser.open(view.url() + query_string)
        self.assertAppearInOrder([
            "02/01/2016",
            "Problema 2",
            "01/01/2016",
            "Problema 1",
            ],
            self.browser.contents)
        self.assertIn(
            "Tots els problemes",
            self.browser.contents)
        self.assertNotIn(
            "No hi ha cap problema enregistrat relacionat amb aquest servei",
            self.browser.contents)

        # problems not empty, count not present
        self.browser.open(view.url())
        self.assertAppearInOrder([
            "02/01/2016",
            "Problema 2",
            "01/01/2016",
            "Problema 1",
            ],
            self.browser.contents)
        self.assertNotIn(
            "Tots els problemes",
            self.browser.contents)
        self.assertNotIn(
            "No hi ha cap problema enregistrat relacionat amb aquest servei",
            self.browser.contents)

        # problems is empty
        servei['problemes'].manage_delObjects(servei['problemes'].keys())
        commit()

        self.browser.open(view.url())
        self.assertNotIn("02/01/2016", self.browser.contents)
        self.assertNotIn("Problema 2", self.browser.contents)
        self.assertNotIn("01/01/2016", self.browser.contents)
        self.assertNotIn("Problema 1", self.browser.contents)
        self.assertIn(
            "No hi ha cap problema enregistrat relacionat amb aquest servei",
            self.browser.contents)
        self.assertNotIn(
            "Tots els problemes",
            self.browser.contents)

    def test_retrieve_from_ws(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_product_id)
        fixtures.create_content(
            servei['problemes'], fixtures.problema_1)
        fixtures.create_content(
            servei['problemes'], fixtures.problema_2)
        commit()

        view = api.content.get_view(
            'retrieve_problemes', servei, self.layer['request'])

        # problems not empty, count is present
        problems = [
            Mock(
                date_creation="25/02/2016",
                topic="The topic 1",
                url="problem-1"),
            Mock(
                date_creation="26/02/2016",
                topic="The topic 2",
                url="problem-2"),
            ]
        with patch('genweb.serveistic.data_access.problemes.ProblemesDataReporter.list_by_product_id',
                   side_effect=(problems,)):
            query_string = "?count=5"
            self.browser.open(view.url() + query_string)
            self.assertAppearInOrder([
                "25/02/2016",
                "The topic",
                "26/02/2016",
                "The topic 2",
                ],
                self.browser.contents)
            self.assertIn(
                "Tots els problemes",
                self.browser.contents)
            self.assertNotIn(
                "No hi ha cap problema enregistrat relacionat amb aquest "
                "servei",
                self.browser.contents)

        # problems not empty, count not present
        problems = [
            Mock(
                date_creation="25/02/2016",
                topic="The topic 1",
                url="problem-1"),
            Mock(
                date_creation="26/02/2016",
                topic="The topic 2",
                url="problem-2"),
            ]
        with patch('genweb.serveistic.data_access.problemes.ProblemesDataReporter.list_by_product_id',
                   side_effect=(problems,)):
            self.browser.open(view.url())
            self.assertAppearInOrder([
                "25/02/2016",
                "The topic",
                "26/02/2016",
                "The topic 2",
                ],
                self.browser.contents)
            self.assertNotIn(
                "Tots els problemes",
                self.browser.contents)
            self.assertNotIn(
                "No hi ha cap problema enregistrat relacionat amb aquest "
                "servei",
                self.browser.contents)

        # problems is empty
        with patch('genweb.serveistic.data_access.problemes.ProblemesDataReporter.list_by_product_id',
                   side_effect=([],)):
            self.browser.open(view.url())
            self.assertIn(
                "No hi ha cap problema enregistrat relacionat amb aquest "
                "servei",
                self.browser.contents)
            self.assertNotIn(
                "Tots els problemes",
                self.browser.contents)

        # problems is None
        with patch('genweb.serveistic.data_access.problemes.ProblemesDataReporter.list_by_product_id',
                   side_effect=(None,)):
            self.browser.open(view.url())
            self.assertIn(
                "No hi ha cap problema enregistrat relacionat amb aquest "
                "servei",
                self.browser.contents)
            self.assertNotIn(
                "Tots els problemes",
                self.browser.contents)
