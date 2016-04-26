# -*- coding: utf-8 -*-

"""Unit tests for the Indicadors data access."""

import unittest
from mock import Mock
import math

from genweb.serveistic.data_access.indicadors import IndicadorsDataReporter


class TestDataAccessIndicadors(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.client.list_indicators = Mock(
            side_effect=self.mock_list_indicators)
        self.client.list_categories = Mock(
            side_effect=self.mock_list_categories)

    def mock_list_indicators(self, serviceid, count):
        return [
            Mock(
                identifier="indicator-{0}".format(i),
                description="indicator-{0} desc".format(i),
                date_modified="indicator-{0} date".format(i))
            for i in range(count)
            ]

    def mock_list_categories(self, *args, **kwargs):
        return [
            Mock(
                identifier="category-{0}".format(i),
                description="description-{0}".format(i),
                date_modified="data_modified-{0}".format(i),
                value="value-{0}")
            for i in range(3)
        ]

    def test_list_by_service_id(self):
        reporter = IndicadorsDataReporter(self.client)

        # No count_category_max specified
        count = 10
        indicadors = reporter.list_by_service_id(
            'mock-id', count=count)
        self.assertEqual(len(indicadors), 10)

        # count_category_max is more restrictive than count
        count = 10
        for count_category_max in (1, 3, 4):
            count_indicadors = min(count, math.ceil(count_category_max / 3.0))
            indicadors = reporter.list_by_service_id(
                'mock-id', count=count, count_category_max=count_category_max)
            self.assertEqual(len(indicadors), count_indicadors)
            count_categories = sum(
                [len(indicador['categories']) for indicador in indicadors])
            self.assertEqual(count_categories, count_category_max)

        # count is more restrictive than count_category_max
        count = 1
        count_category_max = 4
        indicadors = reporter.list_by_service_id(
            'mock-id', count=count, count_category_max=count_category_max)
        self.assertEqual(len(indicadors), 1)
        count_categories = sum(
            [len(indicador['categories']) for indicador in indicadors])
        self.assertEqual(count_categories, 3)
