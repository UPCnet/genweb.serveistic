# -*- coding: utf-8 -*-

"""Unit tests for the Indicadors data access."""

import unittest
from mock import Mock, patch
import datetime

from genweb.serveistic.data_access.indicadors import (
    IndicadorsMatrixDataReporter)


class TestDataAccessIndicadorsMatrix(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.client.list_indicators = Mock(
            side_effect=self.mock_list_indicators)
        self.client.list_categories = Mock(
            side_effect=self.mock_list_categories)

    def mock_list_indicators(self, service_id, count=None):
        """
        Return following indicators:
        service-1:
          - indicator-1
          - indicator-2
          - indicator-3
        """
        if service_id == 'service-1':
            return [
                Mock(
                    identifier="indicator-{0}".format(i),
                    description="indicator-{0} desc".format(i),
                    date_modified=datetime.datetime(2016, 1, 15, 13, 35, 10))
                for i in range(1, 4)]
        else:
            return []

    def mock_list_categories(self, service_id, indicator_id, count=None):
        """
        Return following categories:
        service-1:
          - indicator-1:
            - category-1.1
            - category-1.2
            - category-1.3
          - indicator-2:
            - category-2.1
          - indicator-3
        """
        if indicator_id == 'indicator-1':
            return [
                Mock(
                    identifier="category-1.{0}".format(i),
                    description="description-1.{0}".format(i),
                    date_modified=datetime.datetime(2016, 1, 15, 13, 35, 10),
                    value="value-1.{0}")
                for i in range(1, 4)]
        elif indicator_id == 'indicator-2':
            return [
                Mock(
                    identifier="category-2.{0}".format(i),
                    description="description-2.{0}".format(i),
                    date_modified=datetime.datetime(2016, 1, 15, 13, 35, 10),
                    value="value-2.{0}")
                for i in range(1, 2)]
        else:
            return []

    def test_getitem_should_raise_typeerror_if_item_is_none(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'noservice')
        with self.assertRaises(TypeError) as context:
            reporter[None]
        self.assertEqual(
            "item must be either an integer or a 2-integer tuple",
            context.exception.message)

    def test_getitem_should_raise_typeerror_if_item_is_str(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'noservice')
        with self.assertRaises(TypeError) as context:
            reporter['1']
        self.assertEqual(
            "item must be either an integer or a 2-integer tuple",
            context.exception.message)

    def test_getitem_should_raise_typeerror_if_item_is_3_element_tuple(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'noservice')
        with self.assertRaises(TypeError) as context:
            reporter[1, 2, 3]
        self.assertEqual(
            "item must be either an integer or a 2-integer tuple",
            context.exception.message)

    def test_getitem_should_not_raise_typeerror_if_item_is_int(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'noservice')
        with patch(
                "genweb.serveistic.data_access.indicadors."
                "IndicadorsMatrixDataReporter._getitem_from_int") as getitem_from_int:
            reporter[1]

    def test_getitem_should_raise_typeerror_if_item_is_2_non_int_element_tuple(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'noservice')
        with self.assertRaises(TypeError) as context:
            reporter[1, '2']
        self.assertEqual(
            "item must be either an integer or a 2-integer tuple",
            context.exception.message)
        with self.assertRaises(TypeError) as context:
            reporter[1.1, 2]
        self.assertEqual(
            "item must be either an integer or a 2-integer tuple",
            context.exception.message)

    def test_getitem_should_not_raise_typeerror_if_item_is_2_element_tuple(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'noservice')
        with patch(
                "genweb.serveistic.data_access.indicadors."
                "IndicadorsMatrixDataReporter._getitem_from_tuple") as getitem_from_tuple:
            reporter[1, 2]

    def test_getitem_should_call_from_int_when_item_is_int(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'noservice')
        with patch(
                "genweb.serveistic.data_access.indicadors."
                "IndicadorsMatrixDataReporter._getitem_from_int") as getitem_from_int:
            with patch(
                    "genweb.serveistic.data_access.indicadors."
                    "IndicadorsMatrixDataReporter._getitem_from_tuple") as getitem_from_tuple:
                reporter[1]
            self.assertEqual(1, getitem_from_int.call_count)
            self.assertEqual(0, getitem_from_tuple.call_count)

    def test_getitem_should_call_from_tuple_when_item_is_tuple(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'noservice')
        with patch(
                "genweb.serveistic.data_access.indicadors."
                "IndicadorsMatrixDataReporter._getitem_from_int") as getitem_from_int:
            with patch(
                    "genweb.serveistic.data_access.indicadors."
                    "IndicadorsMatrixDataReporter._getitem_from_tuple") as getitem_from_tuple:
                reporter[1, 2]
            self.assertEqual(1, getitem_from_tuple.call_count)
            self.assertEqual(0, getitem_from_int.call_count)

    def test_getitem_from_int_should_cache_indicators_after_first_time(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'service-1')
        reporter._getitem_from_int(2)
        with patch(
                "genweb.serveistic.data_access.indicadors."
                "IndicadorsMatrixDataReporter._retrieve_indicators") as retrieve_indicators:
            reporter._getitem_from_int(2)
            self.assertEqual(0, retrieve_indicators.call_count)

    def test_getitem_from_int_should_raise_indexerror_if_index_is_lt1(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'service-1')
        with self.assertRaises(IndexError):
            reporter._getitem_from_int(0)

    def test_getitem_from_int_should_raise_indexerror_if_index_is_gtsize(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'service-1')
        with self.assertRaises(IndexError):
            reporter._getitem_from_int(4)

    def test_getitem_from_int_should_return_right_indicator(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'service-1')
        self.assertEquals(
            'indicator-2', reporter._getitem_from_int(2).identifier)

    def test_getitem_from_tuple_should_cache_categories_after_first_time(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'service-1')
        reporter._getitem_from_tuple((1, 1))
        with patch(
                "genweb.serveistic.data_access.indicadors."
                "IndicadorsMatrixDataReporter._retrieve_categories") as retrieve_categories:
            reporter._getitem_from_tuple((1, 1))
            self.assertEqual(0, retrieve_categories.call_count)

    def test_getitem_from_tuple_should_raise_indexerror_if_index_is_lt1(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'service-1')
        with self.assertRaises(IndexError):
            reporter._getitem_from_tuple((1, 0))

    def test_getitem_from_tuple_should_raise_indexerror_if_index_is_gtsize(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'service-1')
        with self.assertRaises(IndexError):
            reporter._getitem_from_tuple((1, 4))

    def test_getitem_from_tuple_should_return_right_category(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'service-1')
        self.assertEquals(
            'category-1.2', reporter._getitem_from_tuple((1, 2)).identifier)

    def test_getitem_should_raise_indexerror_when_service_does_not_exist(self):
        reporter = IndicadorsMatrixDataReporter(self.client, 'noservice')
        with self.assertRaises(IndexError):
            reporter[1]
        with self.assertRaises(IndexError):
            reporter[1, 1]

