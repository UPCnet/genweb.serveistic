# -*- coding: utf-8 -*-

import unittest

from zope.interface import Invalid

from genweb.serveistic.content.serveitic import (
    validate_service_indicators_order,
    parse_service_indicators_order)


class TestIndicatorsOrder(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_should_accept_one_value(self):
        validate_service_indicators_order("1.11")

    def test_validate_should_accept_one_value_ending_comma(self):
        validate_service_indicators_order("1.11,")

    def test_validate_should_accept_multiple_values(self):
        validate_service_indicators_order("1.1,2.3")

    def test_validate_should_accept_multiple_values_ending_comma(self):
        validate_service_indicators_order("1.1,2.3,")

    def test_validate_should_not_accept_space_after_ending_comma(self):
        with self.assertRaises(Invalid):
            validate_service_indicators_order("1.1,2.3, ")

    def test_validate_should_accept_multiple_digit_numbers(self):
        validate_service_indicators_order("1.11,22.2,33.44")

    def test_validate_should_raise_if_no_dots(self):
        with self.assertRaises(Invalid):
            validate_service_indicators_order("1,2,3")

    def test_validate_should_raise_if_no_commas(self):
        with self.assertRaises(Invalid):
            validate_service_indicators_order("1.1 2.3")

    def test_validate_should_accept_1_space_after_commas(self):
        validate_service_indicators_order("1.1,2.3, 3.1")

    def test_validate_should_raise_if_gt1_space_after_commas(self):
        with self.assertRaises(Invalid):
            validate_service_indicators_order("1.1,2.3,  3.1")

    def test_parse_should_return_list(self):
        result = parse_service_indicators_order("1.1, 2.1, 3.1")
        self.assertEqual(list, type(result))

    def test_parse_should_return_empty_list_when_order_empty(self):
        result = parse_service_indicators_order("")
        self.assertEqual([], result)

    def test_parse_should_return_list_of_n_elements_when_n_indicator_items(self):
        result = parse_service_indicators_order("1.1, 2.1, 3.1")
        self.assertEqual(3, len(result))

    def test_parse_should_return_list_of_2_element_tuples(self):
        result = parse_service_indicators_order("1.1, 2.1, 3.1")
        for element in result:
            self.assertEqual(tuple, type(element))
            self.assertEqual(2, len(element))

    def test_parse_2_element_tuples_should_contain_int_and_list(self):
        result = parse_service_indicators_order("1.1, 2.1, 3.1")
        for element in result:
            self.assertEqual(int, type(element[0]))
            self.assertEqual(list, type(element[1]))

    def test_parse_2_element_tuples_int_should_be_numbers_before_dots(self):
        result = parse_service_indicators_order("1.1, 2.1, 3.1")
        self.assertEqual(1, result[0][0])
        self.assertEqual(2, result[1][0])
        self.assertEqual(3, result[2][0])

    def test_parse_should_group_indicator_indexes_when_appear_consecutively(self):
        result = parse_service_indicators_order("1.1, 2.1, 2.2, 3.1, 1.2")
        self.assertEqual(1, result[0][0])
        self.assertEqual(2, result[1][0])
        self.assertEqual(3, result[2][0])
        self.assertEqual(1, result[3][0])

    def test_parse_should_group_category_indexes_by_indicator_index(self):
        result = parse_service_indicators_order("1.1, 1.1, 3.1, 2.1, 2.2, 1.2")
        self.assertListEqual([1, 1], result[0][1])
        self.assertListEqual([1], result[1][1])
        self.assertListEqual([1, 2], result[2][1])
        self.assertListEqual([2], result[3][1])

