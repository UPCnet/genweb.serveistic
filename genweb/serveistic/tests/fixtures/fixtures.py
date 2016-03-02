from datetime import datetime

from plone import api


def create_content(container, properties):
    content_dict = {'container': container}
    content_dict.update(properties)
    return api.content.create(**content_dict)

servei_1 = {
    'type': 'serveitic',
    'id': 'servei-1',
    'title': 'Servei 1'
    }

problema_1 = {
    'type': 'problema',
    'id': 'problema-1',
    'title': 'Problema 1',
    'data_creacio': datetime(2016, 1, 1)
    }
