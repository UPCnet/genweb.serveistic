# -*- coding: utf-8 -*-

from datetime import datetime

from plone import api


def create_content(container, properties):
    content_dict = {'container': container}
    content_dict.update(properties)
    return api.content.create(**content_dict)

servei_mylist = {
    'type': 'serveitic',
    'id': 'mylist',
    'title': u'myList',
    'description': u'Autoservei de llistes de correu electrònic',
    'responsable': u'Santi Cortés',
    'responsable': u'santi.cortes@gmail.com',
    'product_id': 'mylist',
    'service_id': 'mylist',
    'prestador': ['upcnet'],
    'ubicacio': ['cnord', 'csud'],
    'tipologia': ['web', 'eines-comunicacia3', 'enines-usuari'],
    'ambi': ['gestia3', 'lloc-de-treball-eines-usuari', 'infraestructures'],
}

servei_1 = {
    'type': 'serveitic',
    'id': 'servei-1',
    'title': 'Servei 1'
    }

servei_with_product_id = {
    'type': 'serveitic',
    'id': 'servei-1',
    'title': 'Servei 1',
    'product_id': 'myproduct'
    }

servei_without_product_id = {
    'type': 'serveitic',
    'id': 'servei-1',
    'title': 'Servei 1',
    }

servei_with_service_id = {
    'type': 'serveitic',
    'id': 'servei-1',
    'title': 'Servei 1',
    'service_id': 'myservice'
    }

servei_without_service_id = {
    'type': 'serveitic',
    'id': 'servei-1',
    'title': 'Servei 1',
    }

problema_1 = {
    'type': 'problema',
    'id': 'problema-1',
    'title': 'Problema 1',
    'data_creacio': datetime(2016, 1, 1)
    }

problema_2 = {
    'type': 'problema',
    'id': 'problema-2',
    'title': 'Problema 2',
    'data_creacio': datetime(2016, 1, 2),
    'url': "ueraela"
    }

problema_3 = {
    'type': 'problema',
    'id': 'problema-3',
    'title': 'Problema 3',
    'url': "ueraela3"
    }
