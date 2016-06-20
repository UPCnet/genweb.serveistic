"""
Web client for the API specified on

https://entornjavapre2.upc.edu/indicadorstic/swagger-ui.html
"""

import requests
from requests.exceptions import ConnectionError
from simplejson.decoder import JSONDecodeError
from datetime import datetime


class Indicator(object):
    def __init__(self, identifier, description, date_modified):
        self.identifier = identifier
        self.description = description
        self.date_modified = date_modified

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Category(object):
    def __init__(self, identifier, description, value, date_modified):
        self.identifier = identifier
        self.description = description
        self.value = value
        self.date_modified = date_modified

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ClientException(Exception):
    pass


class Client(object):
    ENDPOINT_INDICATORS = "indicadors"
    ENDPOINT_CATEGORIES = "categories"
    KEY_INDICATOR_LIST = "indicadors"
    KEY_INDICATOR_IDENTIFIER = "idIndicador"
    KEY_INDICATOR_DESCRIPTION = "descripcioIndicador"
    KEY_INDICATOR_DATE_MODIFIED = "dataModificacioIndicador"
    KEY_CATEGORY_LIST = "categories"
    KEY_CATEGORY_IDENTIFIER = "idCategoria"
    KEY_CATEGORY_DESCRIPTION = "descripcioCategoria"
    KEY_CATEGORY_VALUE = "valor"
    KEY_CATEGORY_DATE_MODIFIED = "dataModificacioCategoria"

    def __init__(self, url_base, header_accept='application/json',
                 header_content_type='application/json'):
        self.url_base = url_base.rstrip('/') if url_base else url_base
        self.header_accept = header_accept
        self.header_content_type = header_content_type

    def _get_headers(self):
        return {
            'Accept': self.header_accept,
            'Content-type': self.header_content_type,
            }

    def _parse_response_result(self, response):
        if 'status' in response and 'message' in response:
            raise ClientException("Error status {0}: {1}".format(
                response['status'], response['message']))

    def _parse_date_modified(self, date_modified_str):
        try:
            date_modified = datetime.strptime(
                date_modified_str[:19], '%Y-%m-%dT%H:%M:%S')
        except (TypeError, ValueError):
            date_modified = None
        return date_modified

    def _parse_response_list_indicators(self, response):
        self._parse_response_result(response)
        if Client.KEY_INDICATOR_LIST not in response:
            raise ClientException(
                "'{0}' is not present in the response".format(
                    Client.KEY_INDICATOR_LIST))
        if not isinstance(response[Client.KEY_INDICATOR_LIST], list):
            raise ClientException("Invalid type of '{0}'".format(
                Client.KEY_INDICATOR_LIST))
        indicators = []
        for indicator_dict in response[Client.KEY_INDICATOR_LIST]:
            if isinstance(indicator_dict, dict):
                indicators.append(Indicator(
                    identifier=indicator_dict.get(
                        Client.KEY_INDICATOR_IDENTIFIER, u''),
                    description=indicator_dict.get(
                        Client.KEY_INDICATOR_DESCRIPTION, u''),
                    date_modified=self._parse_date_modified(
                        indicator_dict.get(
                            Client.KEY_INDICATOR_DATE_MODIFIED, None))))
        return indicators

    def _parse_response_list_categories(self, response):
        self._parse_response_result(response)
        if 'categories' not in response:
            raise ClientException(
                "'{0}' is not present in the response".format(
                    Client.KEY_CATEGORY_LIST))
        if not isinstance(response[Client.KEY_CATEGORY_LIST], list):
            raise ClientException("Invalid type of '{0}'".format(
                Client.KEY_CATEGORY_LIST))
        categories = []
        for category_dict in response[Client.KEY_CATEGORY_LIST]:
            if isinstance(category_dict, dict):
                categories.append(Category(
                    identifier=category_dict.get(
                        Client.KEY_CATEGORY_IDENTIFIER, u''),
                    description=category_dict.get(
                        Client.KEY_CATEGORY_DESCRIPTION, u''),
                    value=category_dict.get(
                        Client.KEY_CATEGORY_VALUE, u''),
                    date_modified=self._parse_date_modified(
                        category_dict.get(
                            Client.KEY_CATEGORY_DATE_MODIFIED, None))))
        return categories

    def list_indicators(self, service_id, count=None):
        """
        Return a list of <Indicator> associated with the specified service.
        """
        try:
            if not service_id or not str(service_id).strip():
                raise ClientException("Parameter 'service_id' cannot be empty")
            response = requests.get(
                '{0}/{1}?idServei={2}'.format(
                    self.url_base, Client.ENDPOINT_INDICATORS, service_id),
                headers=self._get_headers(), verify=False)
            if response.status_code != requests.codes.ok:
                raise ClientException("Status code is not OK ({0})".format(
                    response.status_code))
            if response.text == u'':
                return []
            indicators = self._parse_response_list_indicators(response.json())
            return indicators[:count] if count is not None else indicators
        except ClientException:
            raise
        except JSONDecodeError:
            raise ClientException("The response contains invalid JSON data")
        except ConnectionError:
            raise ClientException("The connection with '{0}' could not be "
                                  "established".format(self.url_base))

    def list_categories(self, service_id, indicator_id, count=None):
        """
        Return a list of <Category> associated with the specified indicator of
        a service.
        """
        try:
            if not service_id or not str(service_id).strip():
                raise ClientException("Parameter 'service_id' cannot be empty")
            if not indicator_id or not str(indicator_id).strip():
                raise ClientException(
                    "Parameter 'indicator_id' cannot be empty")
            response = requests.get(
                '{0}/{1}?idServei={2}&idIndicador={3}'.format(
                    self.url_base, Client.ENDPOINT_CATEGORIES,
                    service_id, indicator_id),
                headers=self._get_headers(), verify=False)
            if response.status_code != requests.codes.ok:
                raise ClientException("Status code is not OK ({0})".format(
                    response.status_code))
            if response.text == u'':
                return []
            categories = self._parse_response_list_categories(response.json())
            return categories[:count] if count is not None else categories
        except ClientException:
            raise
        except JSONDecodeError:
            raise ClientException("The response contains invalid JSON data")
        except ConnectionError:
            raise ClientException("The connection with '{0}' could not be "
                                  "established".format(self.url_base))
