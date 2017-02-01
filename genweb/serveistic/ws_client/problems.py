"""
Web client for the API specified in

https://comunitats.upcnet.es/euniversity/
documents/cataleg-de-serveis/gestor-de-serveis-i-operacions/
administracio-sistema/serveis-web/serveis-rest/
copy_of_descripcio-dels-serveis-web-rest#/
"""

import base64
import datetime

import requests
from requests.exceptions import ConnectionError, ReadTimeout
from simplejson.decoder import JSONDecodeError


class Problem(object):
    def __init__(self, topic, description, url, date_creation, date_fix):
        self.topic = topic
        self.description = description
        self.url = url
        self.date_creation = date_creation
        self.date_fix = date_fix

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ClientException(Exception):
    pass


class Client(object):
    KEY_TOPIC = 'assumpte'
    KEY_DESCRIPTION = 'descripcioProblema'
    KEY_URL = 'urlProblema'
    KEY_DATE_CREATION = 'dataCreacio'
    KEY_DATE_FIX = 'dataLimitResolucioString'

    def __init__(self, endpoint, login_username, login_password,
                 content_type='application/json', timeout=5):
        self.endpoint = endpoint.rstrip('/') if endpoint else endpoint
        self.login_username = login_username
        self.login_password = login_password
        self.content_type = content_type
        self.timeout = timeout

    def _get_headers(self):
        login_username = self.login_username if self.login_username else ""
        login_password = self.login_password if self.login_password else ""
        return {
            'Content-type': self.content_type,
            'login.username': login_username,
            'login.password': login_password,
            'Authorization': "Basic {0}".format(
                base64.b64encode(':'.join([login_username, login_password])))}

    def _parse_response_result(self, response):
        if 'resultat' not in response:
            raise ClientException("'resultat' is not present in the response")
        if response['resultat'] == "ERROR":
            error_code = response['codiError']\
                if 'codiError' in response else 'UNDEFINED'
            error_msg = response['resultatMissatge']\
                if 'resultatMissatge' in response else 'Undefined'
            raise ClientException(
                "Error code {0}: {1}".format(error_code, error_msg))
        elif response['resultat'] == "SUCCESS":
            pass
        else:
            raise ClientException("Invalid value for 'resultat'")

    def _parse_date(self, date):
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return u''

    def _parse_response_list_problems(self, response):
        self._parse_response_result(response)
        if 'llistaProblemes' not in response:
            raise ClientException(
                "'llistaProblemes' is not present in the response")
        if not isinstance(response['llistaProblemes'], list):
            raise ClientException("Invalid type of 'llistaProblemes'")
        problems = []
        for problem_dict in response['llistaProblemes']:
            if isinstance(problem_dict, dict):
                problems.append(Problem(
                    topic=problem_dict.get(Client.KEY_TOPIC, u''),
                    description=problem_dict.get(Client.KEY_DESCRIPTION, u''),
                    url=problem_dict.get(Client.KEY_URL, u''),
                    date_creation=self._parse_date(
                        problem_dict.get(Client.KEY_DATE_CREATION, u'')),
                    date_fix=self._parse_date(
                        problem_dict.get(Client.KEY_DATE_FIX, u''))))
        return problems

    def list_problems(self, product_id, count=None):
        """
        Return a list of <Problem> associated with the specified product.
        """
        try:
            if not product_id or not str(product_id).strip():
                raise ClientException("Parameter 'product_id' cannot be empty")
            response = requests.get(
                '{0}/{1}'.format(self.endpoint, product_id),
                headers=self._get_headers(), verify=False, timeout=self.timeout)
            if response.status_code != requests.codes.ok:
                raise ClientException("Status code is not OK ({0})".format(
                    response.status_code))
            problems = self._parse_response_list_problems(response.json())
            return problems[:count] if count is not None else problems
        except ClientException:
            raise
        except JSONDecodeError:
            raise ClientException("The response contains invalid JSON data")
        except ConnectionError:
            raise ClientException("The connection with '{0}' could not be "
                                  "established".format(self.endpoint))
        except ReadTimeout:
            raise ClientException(
                "There was a timeout while waiting for '{0}'".format(
                    self.endpoint))
