from datetime import datetime
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

    def test_no_parameters(self):
        view = api.content.get_view(
            'retrieve_problemes', self.portal, self.layer['request'])
        self.browser.open(view.url())
        self.assertIn(
            "No s&apos;han pogut recuperar els problemes",
            self.browser.contents)

    def test_product_id(self):
        view = api.content.get_view(
            'retrieve_problemes', self.portal, self.layer['request'])
        # problems are empty, count is not present
        with patch('genweb.serveistic.ws_client.problems.Client.list_problems',
                   side_effect=([],)):
            query_string = "?product_id=1234"
            self.browser.open(view.url() + query_string)
            self.assertIn(
                "No s&apos;han trobat problemes",
                self.browser.contents)
            self.assertNotIn(
                "Tots els problemes",
                self.browser.contents)

        # problems are empty, count is present
        with patch('genweb.serveistic.ws_client.problems.Client.list_problems',
                   side_effect=([],)):
            query_string = "?product_id=1234&count=5"
            self.browser.open(view.url() + query_string)
            self.assertIn(
                "No s&apos;han trobat problemes",
                self.browser.contents)
            self.assertNotIn(
                "Tots els problemes",
                self.browser.contents)

        # problems are not empty, count is not present
        problems = [
            Mock(
                date_creation=datetime(2016, 2, 25),
                topic="The topic",
                url="problem-1")]
        with patch('genweb.serveistic.ws_client.problems.Client.list_problems',
                   side_effect=(problems,)):
            query_string = "?product_id=1234"
            self.browser.open(view.url() + query_string)
            self.assertAppearInOrder([
                "25/02/2016",
                "The topic"],
                self.browser.contents)
            self.assertNotIn(
                "No s&apos;han trobat problemes",
                self.browser.contents)
            self.assertNotIn(
                "Tots els problemes",
                self.browser.contents)

        # problems are not empty, count is present
        problems = [
            Mock(
                date_creation=datetime(2016, 2, 25),
                topic="The topic",
                url="problem-1")]
        with patch('genweb.serveistic.ws_client.problems.Client.list_problems',
                   side_effect=(problems,)):
            query_string = "?product_id=1234&count=10"
            self.browser.open(view.url() + query_string)
            self.assertAppearInOrder([
                "25/02/2016",
                "The topic"],
                self.browser.contents)
            self.assertNotIn(
                "No s&apos;han trobat problemes",
                self.browser.contents)
            self.assertIn(
                "Tots els problemes",
                self.browser.contents)

    def test_servei_path(self):
        view = api.content.get_view(
            'retrieve_problemes', self.portal, self.layer['request'])
        # problems are empty, count is not present
        query_string = "?servei_path=/non-existing/path"
        self.browser.open(view.url() + query_string)
        self.assertIn(
            "No s&apos;han trobat problemes",
            self.browser.contents)
        self.assertNotIn(
            "Tots els problemes",
            self.browser.contents)

        # problems are empty, count is present
        query_string = "?servei_path=/non-existing/path&count=5"
        self.browser.open(view.url() + query_string)
        self.assertIn(
            "No s&apos;han trobat problemes",
            self.browser.contents)
        self.assertNotIn(
            "Tots els problemes",
            self.browser.contents)

        # problems are not empty
        servei_1 = fixtures.create_content(self.portal, fixtures.servei_1)
        problema_1 = fixtures.create_content(
            servei_1['problemes'], fixtures.problema_1)
        problema_2 = fixtures.create_content(
            servei_1['problemes'], fixtures.problema_2)
        problema_3 = fixtures.create_content(
            servei_1['problemes'], fixtures.problema_3)
        commit()
        # ... count is not present
        query_string = "?servei_path=" + '/'.join(servei_1.getPhysicalPath())
        self.browser.open(view.url() + query_string)
        self.assertAppearInOrder([
            problema_2.data_creacio.strftime('%d/%m/%Y'),
            'href="' + problema_2.url + '"',
            problema_2.Title(),
            problema_1.data_creacio.strftime('%d/%m/%Y'),
            'href="problemes/' + problema_1.id + '"',
            problema_1.Title(),
            'href="' + problema_3.url + '"',
            problema_3.Title()],
            self.browser.contents)
        self.assertNotIn(
            "No s&apos;han trobat problemes",
            self.browser.contents)
        self.assertNotIn(
            "Tots els problemes",
            self.browser.contents)

        # ... count is present
        query_string = "?servei_path={0}&count=7".format(
            '/'.join(problema_1.getPhysicalPath()))
        self.browser.open(view.url() + query_string)
        self.assertAppearInOrder([
            problema_1.data_creacio.strftime('%d/%m/%Y'),
            problema_1.Title()],
            self.browser.contents)
        self.assertNotIn(
            "No s&apos;han trobat problemes",
            self.browser.contents)
        self.assertIn(
            "Tots els problemes",
            self.browser.contents)

    def test_product_id_and_servei_path(self):
        view = api.content.get_view(
            'retrieve_problemes', self.portal, self.layer['request'])
        # problems are empty, count is not present
        servei_1 = fixtures.create_content(self.portal, fixtures.servei_1)
        problema_1 = fixtures.create_content(
            servei_1['problemes'], fixtures.problema_1)
        commit()

        with patch('genweb.serveistic.ws_client.problems.Client.list_problems',
                   side_effect=([],)):
            query_string = "?product_id=1234&servei_path={0}".format(
                '/'.join(problema_1.getPhysicalPath()))
            self.browser.open(view.url() + query_string)
            self.assertIn(
                "No s&apos;han trobat problemes",
                self.browser.contents)
            self.assertNotIn(
                "Tots els problemes",
                self.browser.contents)
