# -*- coding: utf-8 -*-

"""Unit tests for the Indicadors data access."""

import unittest
from mock import Mock, patch
import math
import datetime

from genweb.serveistic.data_access.indicadors import (
    IndicadorsDataReporter, IndicadorsDataReporterException)


class TestDataAccessIndicadors(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.client.list_indicators = Mock(
            side_effect=self.mock_list_indicators)
        self.client.list_categories = Mock(
            side_effect=self.mock_list_categories)

    def mock_list_indicators(self, service_id, count=None):
        if service_id == 'invalid-service':
            return []
        if service_id == '3x2-service':
            return [
                Mock(
                    identifier="indicator-{0}".format(i + 1),
                    description="indicator-{0} desc".format(i + 1),
                    date_modified=datetime.datetime(2016, 1, 15, 13, 35, 10))
                for i in range(3)]
        else:
            return [
                Mock(
                    identifier="indicator-{0}".format(i + 1),
                    description="indicator-{0} desc".format(i + 1),
                    date_modified=datetime.datetime(2016, 1, 15, 13, 35, 10))
                for i in range(count)]

    def mock_list_categories(self, service_id, indicator_id, count=None):
        if service_id == 'invalid-service':
            return []
        elif service_id == '3x2-service':
            return [
                Mock(
                    identifier="category-{0}".format(i + 1),
                    description="description-{0}".format(i + 1),
                    date_modified=datetime.datetime(2016, 1, 15, 13, 35, 10),
                    value="value-{0}")
                for i in range(2)]
        else:
            return [
                Mock(
                    identifier="category-{0}".format(i),
                    description="description-{0}".format(i),
                    date_modified=datetime.datetime(2016, 1, 15, 13, 35, 10),
                    value="value-{0}")
                for i in range(3)]

    # Test list_by_service_id (lbsi)
    def test_lbsi_count_category_should_not_limit_if_not_specified(self):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=lambda msgid: ''))
        count_indicator = 10
        indicadors = reporter.list_by_service_id(
            'mock-id', count_indicator=count_indicator)
        self.assertEqual(len(indicadors), 10)

    def test_lbsi_count_category_should_limit_if_specified(self):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=lambda msgid: ''))
        count_indicator = 10
        for count_category in (1, 3, 4):
            indicators = reporter.list_by_service_id(
                'mock-id',
                count_indicator=count_indicator, count_category=count_category)
            total_indicators = len(indicators)
            total_categories = sum(
                [len(indicator['categories']) for indicator in indicators])
            self.assertEqual(math.ceil(count_category / 3.0), total_indicators)
            self.assertEqual(count_category, total_categories)

    def test_lbsi_count_category_should_not_limit_if_count_indicator_is_more_restrictive(self):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=lambda msgid: ''))
        count_indicator = 1
        count_category = 4
        indicators = reporter.list_by_service_id(
            'mock-id',
            count_indicator=count_indicator, count_category=count_category)
        total_categories = sum(
            [len(indicator['categories']) for indicator in indicators])
        self.assertEqual(count_indicator, len(indicators))
        self.assertLess(total_categories, count_category)

    # Test list_by_service_id_and_indicators_order (lbso)
    def test_lbso_should_delegate_when_order_is_none(self):
        reporter = IndicadorsDataReporter(self.client)
        with patch(
                'genweb.serveistic.data_access.indicadors.'
                'IndicadorsDataReporter.list_by_service_id') as list_by_service_id:
            reporter.list_by_service_id_and_indicators_order(
                'mock-id', indicators_order=None, count_indicator=10)
            self.assertTrue(list_by_service_id.called)

    def test_lbso_should_delegate_when_order_is_empty(self):
        reporter = IndicadorsDataReporter(self.client)
        with patch(
                'genweb.serveistic.data_access.indicadors.'
                'IndicadorsDataReporter.list_by_service_id') as list_by_service_id:
            reporter.list_by_service_id_and_indicators_order(
                'mock-id', indicators_order='', count_indicator=10)
            self.assertTrue(list_by_service_id.called)

    def test_lbso_should_return_empty_list_when_count_indicator_is_0(self):
        reporter = IndicadorsDataReporter(self.client)
        self.assertEqual(
            [], reporter.list_by_service_id_and_indicators_order(
                'mock-id',
                indicators_order="1.1, 1.2, 2.1, 3.1",
                count_indicator=0))

    def test_lbso_should_return_empty_list_when_count_category_is_0(self):
        reporter = IndicadorsDataReporter(self.client)
        self.assertEqual(
            [], reporter.list_by_service_id_and_indicators_order(
                'mock-id',
                indicators_order="1.1, 1.2, 2.1, 3.1",
                count_indicator=3,
                count_category=0))

    def test_lbso_should_raise_when_order_is_not_valid(self):
        reporter = IndicadorsDataReporter(self.client)
        with self.assertRaises(IndicadorsDataReporterException) as context:
            reporter.list_by_service_id_and_indicators_order(
                'mock-id',
                indicators_order="1-1, 1-2, 2-1, 3-1", count_indicator=10)
        self.assertEqual(
            'Indicators order is not valid', context.exception.message)

    def test_lbso_should_return_empty_list_when_service_id_is_not_valid(self):
        reporter = IndicadorsDataReporter(self.client)
        self.assertEqual(
            [], reporter.list_by_service_id_and_indicators_order(
                'invalid-service',
                indicators_order="1.1, 1.2, 2.1, 3.1",
                count_indicator=3,
                count_category=0))

    def test_lbso_should_only_return_valid_index_indicators_in_the_right_order(self):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=lambda msgid: ''))
        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="0.1, 0.2, 3.0, 3.1, 3.2, 3.3, 4.1, 4.2, 2.0")
        self.assertEqual(2, len(indicators))
        self.assertEqual('indicator-3', indicators[0]['identifier'])
        self.assertEqual('indicator-2', indicators[1]['identifier'])

    def test_lbso_should_only_return_valid_index_categories_in_the_right_order(self):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=lambda msgid: ''))
        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="0.1, 0.2, 3.0, 3.2, 3.1, 3.3, 4.1, 4.2, 2.0")
        self.assertEqual(2, len(indicators[0]['categories']))
        self.assertEqual(
            'category-2', indicators[0]['categories'][0]['identifier'])
        self.assertEqual(
            'category-1', indicators[0]['categories'][1]['identifier'])
        self.assertEqual(0, len(indicators[1]['categories']))

    def test_lbso_should_limit_indicators_if_count_specified(self):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=lambda msgid: ''))
        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="3.2, 2.1, 1.2",
            count_indicator=1)
        self.assertEqual(1, len(indicators))
        self.assertEqual('indicator-3', indicators[0]['identifier'])

        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="3.2, 2.1, 1.2",
            count_indicator=2)
        self.assertEqual(2, len(indicators))
        self.assertEqual('indicator-3', indicators[0]['identifier'])
        self.assertEqual('indicator-2', indicators[1]['identifier'])

        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="3.2, 2.1, 1.2",
            count_indicator=3)
        self.assertEqual(3, len(indicators))
        self.assertEqual('indicator-3', indicators[0]['identifier'])
        self.assertEqual('indicator-2', indicators[1]['identifier'])
        self.assertEqual('indicator-1', indicators[2]['identifier'])

        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="3.2, 2.1, 1.2",
            count_indicator=4)
        self.assertEqual(3, len(indicators))
        self.assertEqual('indicator-3', indicators[0]['identifier'])
        self.assertEqual('indicator-2', indicators[1]['identifier'])
        self.assertEqual('indicator-1', indicators[2]['identifier'])

    def test_lbso_should_limit_categories_if_count_specified(self):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=lambda msgid: ''))
        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="3.2, 2.1, 1.2",
            count_category=1)
        total_categories = sum(
            [len(indicator['categories']) for indicator in indicators])
        self.assertEqual(1, total_categories)

        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="3.2, 2.1, 1.2",
            count_category=2)
        total_categories = sum(
            [len(indicator['categories']) for indicator in indicators])
        self.assertEqual(2, total_categories)

        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="3.2, 2.1, 1.2",
            count_category=3)
        total_categories = sum(
            [len(indicator['categories']) for indicator in indicators])
        self.assertEqual(3, total_categories)

        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="3.2, 2.1, 1.2",
            count_category=4)
        total_categories = sum(
            [len(indicator['categories']) for indicator in indicators])
        self.assertEqual(3, total_categories)

    def test_lbso_count_category_should_not_limit_if_count_indicator_is_more_restrictive(self):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=lambda msgid: ''))
        indicators = reporter.list_by_service_id_and_indicators_order(
            '3x2-service',
            indicators_order="3.2, 2.1, 1.2",
            count_indicator=2,
            count_category=3)
        self.assertEqual(2, len(indicators))
        total_categories = sum(
            [len(indicator['categories']) for indicator in indicators])
        self.assertEqual(2, total_categories)

    @patch('genweb.serveistic.data_access.indicadors._')
    def test_translate_frequency_should_translate_unk_if_freq_not_in_values(self, mock_):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=Mock()))
        reporter._translate_frequency('Invalid frequency')
        mock_.assert_called_with('category_freq_unknown')

    @patch('genweb.serveistic.data_access.indicadors._')
    def test_translate_frequency_should_translate_unk_if_freq_is_none(self, mock_):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=Mock()))
        reporter._translate_frequency(None)
        mock_.assert_called_with('category_freq_unknown')

    @patch('genweb.serveistic.data_access.indicadors._')
    def test_translate_frequency_should_translate_unk_if_freq_not_str(self, mock_):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=Mock()))
        reporter._translate_frequency(123)
        mock_.assert_called_with('category_freq_unknown')

    @patch('genweb.serveistic.data_access.indicadors._')
    def test_translate_frequency_should_translate_lowercased_freq_if_freq_in_values(self, mock_):
        reporter = IndicadorsDataReporter(
            self.client, context=Mock(translate=Mock()))
        reporter._translate_frequency(u'Horaria')
        mock_.assert_called_with('category_freq_horaria')
