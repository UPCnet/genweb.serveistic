"""
Web client for the API specified in

https://comunitats.upcnet.es/euniversity/
documents/cataleg-de-serveis/gestor-de-serveis-i-operacions/
administracio-sistema/serveis-web/serveis-rest/
copy_of_descripcio-dels-serveis-web-rest#/
"""

import datetime

import requests
from requests.exceptions import ConnectionError
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

    def __init__(self, endpoint, login_username, login_password, domini,
                 content_type='application/json'):
        self.endpoint = endpoint
        self.login_username = login_username
        self.login_password = login_password
        self.domini = domini
        self.content_type = content_type

    def _get_headers(self):
        return {
            'Content-type': self.content_type,
            'login.username': self.login_username,
            'login.password': self.login_password,
            'domini': self.domini}

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
                    date_creation=datetime.datetime.strptime(
                        problem_dict.get(Client.KEY_DATE_CREATION),
                        '%Y-%m-%d %H:%M:%S.%f')
                    if Client.KEY_DATE_CREATION in problem_dict else u'',
                    date_fix=u''))
        return problems

    def list_problems(self, product_id):
        """
        Return a list of <Problem> associated with the specified product.
        """
        try:
            response = requests.get(
                '{0}/{1}'.format(self.endpoint, product_id),
                headers=self._get_headers())
            if response.status_code != requests.codes.ok:
                raise ClientException("Status code is not OK")
            return self._parse_response_list_problems(response.json())
        except ClientException:
            raise
        except JSONDecodeError:
            raise ClientException("The response contains invalid JSON data")
        except ConnectionError:
            raise ClientException("The connection could not be established")
