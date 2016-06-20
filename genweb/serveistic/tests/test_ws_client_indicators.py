# -*- coding: utf-8 -*-

"""Unit tests for the Web Service client."""

import json
import unittest
from mock import patch, MagicMock
import datetime

from requests.exceptions import ConnectionError

from genweb.serveistic.ws_client.indicators import (
    Client, ClientException, Indicator, Category)


class TestWSClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            url_base='http://url_base')

    def test_parse_date_modified(self):
        date_modified_str = '2016-06-13T17:39:44.545+02:00'
        date_modified_gold = datetime.datetime(2016, 6, 13, 17, 39, 44)
        self.assertEqual(
            date_modified_gold,
            self.client._parse_date_modified(date_modified_str))

    def test_parse_date_modified_is_empty(self):
        date_modified_str = ''
        date_modified_gold = None
        self.assertEqual(
            date_modified_gold,
            self.client._parse_date_modified(date_modified_str))

    def test_parse_date_modified_is_none(self):
        date_modified_str = None
        date_modified_gold = None
        self.assertEqual(
            date_modified_gold,
            self.client._parse_date_modified(date_modified_str))

    def test_parse_date_modified_has_wrong_type(self):
        date_modified_str = 20160613
        date_modified_gold = None
        self.assertEqual(
            date_modified_gold,
            self.client._parse_date_modified(date_modified_str))

        date_modified_str = [20160613]
        date_modified_gold = None
        self.assertEqual(
            date_modified_gold,
            self.client._parse_date_modified(date_modified_str))

    def test_parse_date_modified_has_wrong_format(self):
        # Time not provided
        date_modified_str = '2016-06-13'
        date_modified_gold = None
        self.assertEqual(
            date_modified_gold,
            self.client._parse_date_modified(date_modified_str))

        # Seconds not provided
        date_modified_str = '2016-06-13T17:39'
        date_modified_gold = None
        self.assertEqual(
            date_modified_gold,
            self.client._parse_date_modified(date_modified_str))

        # Month is not zero-padded
        date_modified_str = '2016-6-13T17:39:44.545+02:00'
        date_modified_gold = None
        self.assertEqual(
            date_modified_gold,
            self.client._parse_date_modified(date_modified_str))

        # Date separator is not dash
        date_modified_str = '2016/06/13T17:39:44.545+02:00'
        date_modified_gold = None
        self.assertEqual(
            date_modified_gold,
            self.client._parse_date_modified(date_modified_str))

    def test_parse_response_result_with_defined_exception(self):
        response = json.loads('''
            {
                "status": "ERROR",
                "message": "This is the message"
            }''')
        try:
            self.client._parse_response_result(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "Error status ERROR: This is the message",
                cexception.message)

    def test_parse_response_list_indicators_empty(self):
        response = json.loads('''
            {
            }''')
        try:
            self.client._parse_response_list_indicators(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "'indicadors' is not present in the response",
                cexception.message)

    def test_parse_response_list_categories_empty(self):
        response = json.loads('''
            {
            }''')
        try:
            self.client._parse_response_list_categories(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "'categories' is not present in the response",
                cexception.message)

    def test_parse_response_list_indicators_invalid_type(self):
        response = json.loads('''
{
   "idServei": "7887",
   "indicadors":
   {
      "dataModificacioIndicador": "2016-04-13T15:35:00.123",
      "descripcioIndicador": "centenars de centenars",
      "idIndicador": "Nombre d'usuaris"
   }
}''')
        try:
            self.client._parse_response_list_indicators(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "Invalid type of 'indicadors'",
                cexception.message)

        response = json.loads('''
{
   "idServei": "7887",
   "indicadors": 123
}''')
        try:
            self.client._parse_response_list_indicators(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "Invalid type of 'indicadors'",
                cexception.message)

    def test_parse_response_list_categories_invalid_type(self):
        response = json.loads('''
{
   "idServei": "7887",
   "idIndicador": "indicador_1",
   "categories":
   {
      "dataModificacioCategoria": "2015-12-03T19:15:50.231",
      "descripcioCategoria": "categoria important",
      "idCategoria": "Nombre d'usuaris",
      "valor": "578"
   }
}''')
        try:
            self.client._parse_response_list_categories(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "Invalid type of 'categories'",
                cexception.message)

        response = json.loads('''
{
   "idServei": "7887",
   "idIndicador": "indicador-1",
   "categories": 123
}''')
        try:
            self.client._parse_response_list_categories(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "Invalid type of 'categories'",
                cexception.message)

    def test_parse_response_list_indicators_not_empty(self):
        response = json.loads('''
{
   "idServei": "7887",
   "indicadors":
   [
       {
          "dataModificacioIndicador": "2016-04-13T15:35:00.123",
          "descripcioIndicador": "centenars de centenars",
          "idIndicador": "Nombre d'usuaris"
       },
       {
          "dataModificacioIndicador": "wrong format",
          "descripcioIndicador": "centenars de centenars 2",
          "idIndicador": "Nombre d'usuaris 2"
       },
       {}
   ]
}
''')
        results = self.client._parse_response_list_indicators(response)
        self.assertEqual(len(results), 3)
        self.assertEqual(
            results[0],
            Indicator(
                date_modified=datetime.datetime(2016, 4, 13, 15, 35, 0),
                description=u"centenars de centenars",
                identifier=u"Nombre d'usuaris"))

        self.assertEqual(
            results[1],
            Indicator(
                date_modified=None,
                description=u"centenars de centenars 2",
                identifier=u"Nombre d'usuaris 2"))

        self.assertEqual(
            results[2],
            Indicator(
                date_modified=None,
                description=u'',
                identifier=u''))

    def test_parse_response_list_categories_not_empty(self):
        response = json.loads('''
{
   "idServei": "7887",
   "idIndicador": "indicador-1",
   "categories":
   [
       {
          "dataModificacioCategoria": "2015-12-03T19:15:50.231",
          "descripcioCategoria": "categoria important",
          "idCategoria": "categoria-1",
          "valor": "578"
       },
       {
          "dataModificacioCategoria": "wrong date",
          "descripcioCategoria": "categoria important 2",
          "idCategoria": "categoria-2",
          "valor": "678"
       },
       {}
   ]
}
''')
        results = self.client._parse_response_list_categories(response)
        self.assertEqual(len(results), 3)
        self.assertEqual(
            results[0],
            Category(
                date_modified=datetime.datetime(2015, 12, 3, 19, 15, 50),
                description=u"categoria important",
                identifier=u"categoria-1",
                value=u"578"))

        self.assertEqual(
            results[1],
            Category(
                date_modified=None,
                description=u'categoria important 2',
                identifier=u'categoria-2',
                value=u'678'))

        self.assertEqual(
            results[2],
            Category(
                date_modified=None,
                description=u'',
                identifier=u'',
                value=u''))

    def test_list_indicators(self):
        # Parameter service_id empty
        try:
            self.client.list_indicators("  \n   \t  ")
            self.fail("ClientException should have been raised")
        except ClientException as exception:
            self.assertEqual("Parameter 'service_id' cannot be empty",
                             exception.message)
        try:
            self.client.list_indicators(None)
            self.fail("ClientException should have been raised")
        except ClientException as exception:
            self.assertEqual("Parameter 'service_id' cannot be empty",
                             exception.message)

        # Connection error
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=ConnectionError):
            try:
                self.client.list_indicators(1)
                self.fail("ClientException should have been raised")
            except ClientException as exception:
                self.assertEqual("The connection with '{0}' could not be "
                                 "established".format(self.client.url_base),
                                 exception.message)
        # Response status is not OK
        response_mock = MagicMock(status_code=500)
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock,)):
            try:
                self.client.list_indicators(1)
                self.fail("ClientException should have been raised")
            except ClientException as exception:
                self.assertEqual("Status code is not OK (500)",
                                 exception.message)

        # Response status is OK
        response_mock = MagicMock(status_code=200)
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock,)), patch(
                'genweb.serveistic.ws_client.indicators.Client._parse_response_list_indicators',
                side_effect=([],)):
            self.assertEqual([], self.client.list_indicators(1))

        # Response text is empty
        response_mock = MagicMock(status_code=200, text=u'')
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock,)):
            self.assertEqual([], self.client.list_indicators(1))

        response_mock = MagicMock(status_code=200, text='')
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock,)):
            self.assertEqual([], self.client.list_indicators(1))

    def test_list_indicators_with_count_parameter(self):
        response_mock = MagicMock(status_code=200)
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock for _ in range(5))), patch(
                'genweb.serveistic.ws_client.indicators.Client._parse_response_list_indicators',
                side_effect=([1, 2, 3, 4, 5, 6, 7, 8] for _ in range(5))):

            self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8],
                             self.client.list_indicators(1))
            self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8],
                             self.client.list_indicators(1, None))
            self.assertEqual([],
                             self.client.list_indicators(1, 0))
            self.assertEqual([1, 2, 3, 4, 5],
                             self.client.list_indicators(1, 5))
            self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8],
                             self.client.list_indicators(1, 10))

    def test_list_categories(self):
        # Parameter service_id empty
        try:
            self.client.list_categories("  \n   \t  ", "indicator-1")
            self.fail("ClientException should have been raised")
        except ClientException as exception:
            self.assertEqual("Parameter 'service_id' cannot be empty",
                             exception.message)
        try:
            self.client.list_categories(None, "indicator-1")
            self.fail("ClientException should have been raised")
        except ClientException as exception:
            self.assertEqual("Parameter 'service_id' cannot be empty",
                             exception.message)

        # Parameter indicator_id empty
        try:
            self.client.list_categories("service-1", "  \n   \t  ")
            self.fail("ClientException should have been raised")
        except ClientException as exception:
            self.assertEqual("Parameter 'indicator_id' cannot be empty",
                             exception.message)
        try:
            self.client.list_categories("service-1", None)
            self.fail("ClientException should have been raised")
        except ClientException as exception:
            self.assertEqual("Parameter 'indicator_id' cannot be empty",
                             exception.message)

        # Connection error
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=ConnectionError):
            try:
                self.client.list_categories(1, 1)
                self.fail("ClientException should have been raised")
            except ClientException as exception:
                self.assertEqual("The connection with '{0}' could not be "
                                 "established".format(self.client.url_base),
                                 exception.message)
        # Response status is not OK
        response_mock = MagicMock(status_code=500)
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock,)):
            try:
                self.client.list_categories(1, 1)
                self.fail("ClientException should have been raised")
            except ClientException as exception:
                self.assertEqual("Status code is not OK (500)",
                                 exception.message)

        # Response status is OK
        response_mock = MagicMock(status_code=200)
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock,)), patch(
                'genweb.serveistic.ws_client.indicators.Client._parse_response_list_categories',
                side_effect=([],)):
            self.assertEqual([], self.client.list_categories(1, 1))

        # Response text is empty
        response_mock = MagicMock(status_code=200, text=u'')
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock,)):
            self.assertEqual([], self.client.list_categories(1, 1))

        response_mock = MagicMock(status_code=200, text='')
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock,)):
            self.assertEqual([], self.client.list_categories(1, 1))

    def test_list_categories_with_count_parameter(self):
        response_mock = MagicMock(status_code=200)
        with patch('genweb.serveistic.ws_client.indicators.requests.get',
                   side_effect=(response_mock for _ in range(5))), patch(
                'genweb.serveistic.ws_client.indicators.Client._parse_response_list_categories',
                side_effect=([1, 2, 3, 4, 5, 6, 7, 8] for _ in range(5))):

            self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8],
                             self.client.list_categories(1, 1))
            self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8],
                             self.client.list_categories(1, 1, count=None))
            self.assertEqual([],
                             self.client.list_categories(1, 1, count=0))
            self.assertEqual([1, 2, 3, 4, 5],
                             self.client.list_categories(1, 1, count=5))
            self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8],
                             self.client.list_categories(1, 1, count=10))
