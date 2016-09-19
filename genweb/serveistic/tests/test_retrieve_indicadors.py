from mock import patch

from plone.testing.z2 import Browser
from plone import api
from transaction import commit

from genweb.serveistic.testing import FunctionalTestCase
from genweb.serveistic.tests.fixtures import (
    fixtures as fixtures,
    retrieve_indicadors as fixtures_retrieve)


class TestRetrieveIndicadors(FunctionalTestCase):
    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.portal)
        self.browser.handleErrors = False
        # Full error log can be found in self.portal.error_log.getLogEntries()

    def assertAppearsBefore(self, subtxt_1, subtxt_2, txt):
        self.assertIn(subtxt_1, txt)
        self.assertIn(subtxt_2, txt)
        self.assertTrue(
            txt.find(subtxt_1) < txt.find(subtxt_2),
            "{0} does not appear before {1}".format(subtxt_1, subtxt_2))

    def assertAppearInOrder(self, subtxts, txt):
        def assertAppearsBefore(subtxt_1, subtxt_2):
            self.assertAppearsBefore(subtxt_1, subtxt_2, txt)
            return subtxt_2
        reduce(assertAppearsBefore, subtxts)

    def test_allindicators_text_should_appear_when_count_specified_and_indicadors_not_empty(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.list_by_service_id_and_indicators_order',
                   side_effect=(fixtures_retrieve.indicadors,)):
            query_string = "?count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertIn(
                "Tots els indicadors",
                self.browser.contents)

    def test_allindicators_text_should_not_appear_when_indicadors_empty(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.list_by_service_id_and_indicators_order',
                   side_effect=([],)):
            query_string = "?count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertNotIn(
                "Tots els indicadors",
                self.browser.contents)

    def test_allindicators_text_should_not_appear_when_indicadors_is_none(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.list_by_service_id_and_indicators_order',
                   side_effect=(None,)):
            query_string = "?count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertNotIn(
                "Tots els indicadors",
                self.browser.contents)

    def test_allindicators_text_should_not_appear_when_count_not_specified(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.list_by_service_id_and_indicators_order',
                   side_effect=(fixtures_retrieve.indicadors,)):
            self.browser.open(view.url())
            self.assertNotIn(
                "Tots els indicadors",
                self.browser.contents)

    def test_allindicators_text_should_not_appear_when_no_service_id(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_without_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])
        self.browser.open(view.url())

        self.assertNotIn(
            "Tots els indicadors",
            self.browser.contents)

    def test_noindicators_text_should_not_appear_when_indicadors_not_empty(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.'
                   'list_by_service_id_and_indicators_order',
                   side_effect=(fixtures_retrieve.indicadors,)):
            query_string = "?count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertNotIn(
                "No hi ha cap indicador enregistrat relacionat amb "
                "aquest servei",
                self.browser.contents)

    def test_noindicators_text_should_appear_when_indicadors_empty(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.'
                   'list_by_service_id_and_indicators_order',
                   side_effect=([],)):
            query_string = "?count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertIn(
                "No hi ha cap indicador enregistrat relacionat amb "
                "aquest servei",
                self.browser.contents)

    def test_noindicators_text_should_appear_when_indicadors_none(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.'
                   'list_by_service_id_and_indicators_order',
                   side_effect=(None,)):
            query_string = "?count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertIn(
                "No hi ha cap indicador enregistrat relacionat amb "
                "aquest servei",
                self.browser.contents)

    def test_noindicators_text_should_appear_when_no_service_id(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_without_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])
        self.browser.open(view.url())

        self.assertIn(
            "No hi ha cap indicador enregistrat relacionat amb aquest servei",
            self.browser.contents)

    def test_indicators_data_should_appear_when_indicadors_not_empty(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.'
                   'list_by_service_id_and_indicators_order',
                   side_effect=(fixtures_retrieve.indicadors,)):
            query_string = "?count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertAppearInOrder([
                "Indicador 1",
                "v1.1", "Categoria 1.1", "2/2/2015",
                "v1.2", "Categoria 1.2", "3/2/2015",
                "Indicador 2",
                "v2.1", "Categoria 2.1", "5/2/2015",
                "v2.2", "Categoria 2.2", "6/2/2015",
                "v2.3", "Categoria 2.3", "7/2/2015"
                ],
                self.browser.contents)

    def test_indicators_number_should_be_limited_by_parameter_count(self):
        pass

    def test_categories_number_should_be_limited_by_parameter_count_category(self):
        pass

    def test_indicators_order_should_be_applied_when_order_defined_and_apply_order_specified(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id_and_indicators_order)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.'
                   'list_by_service_id',
                   side_effect=(fixtures_retrieve.indicadors,)) as list_by_service_id:
            with patch('genweb.serveistic.data_access.indicadors.'
                       'IndicadorsMatrixDataReporter', autospec=True):
                query_string = "?apply_order=yes&count_indicator=5"
                self.browser.open(view.url() + query_string)
                self.assertFalse(list_by_service_id.called)

    def test_indicators_order_should_not_be_applied_when_apply_order_not_specified(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id_and_indicators_order)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.'
                   'list_by_service_id',
                   side_effect=(fixtures_retrieve.indicadors,)) as list_by_service_id:
            query_string = "?count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertTrue(list_by_service_id.called)

    def test_indicators_order_should_not_be_applied_when_apply_order_set_as_no(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id_and_indicators_order)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.'
                   'list_by_service_id',
                   side_effect=(fixtures_retrieve.indicadors,)) as list_by_service_id:
            query_string = "?apply_order=no&count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertTrue(list_by_service_id.called)

    def test_indicators_order_should_not_be_applied_when_order_not_defined(self):
        servei = fixtures.create_content(
            self.portal, fixtures.servei_with_service_id)
        commit()

        view = api.content.get_view(
            'retrieve_indicadors', servei, self.layer['request'])

        with patch('genweb.serveistic.data_access.indicadors.'
                   'IndicadorsDataReporter.'
                   'list_by_service_id',
                   side_effect=(fixtures_retrieve.indicadors,)) as list_by_service_id:
            query_string = "?apply_order=yes&count_indicator=5"
            self.browser.open(view.url() + query_string)
            self.assertTrue(list_by_service_id.called)
