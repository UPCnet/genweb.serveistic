# -*- coding: utf-8 -*-

from datetime import datetime

from zope.component import getUtility
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer


def create_content(container, properties):
    content_dict = {'container': container}
    content_dict.update(properties)
    return api.content.create(**content_dict)


def normalize_facet_values(obj):
    normalizer = getUtility(IIDNormalizer)
    for facet in ('prestador', 'ubicacio', 'tipologia', 'ambit'):
        if facet in obj:
            obj[facet] = [
                normalizer.normalize(facet_value.encode('utf-8'))
                for facet_value in obj[facet]]
    return obj

servei_mylist = {
    'type': 'serveitic',
    'id': 'mylist',
    'title': u'myList',
    'description': u'Autoservei de llistes de correu electrònic',
    'responsable': u'Santi Cortés',
    'responsableMail': u'santi.cortes@gmail.com',
    'product_id': 'mylist',
    'service_id': 'mylist',
    'prestador': ['upcnet'],
    'ubicacio': ['cnord', 'csud'],
    'tipologia': ['web', 'eines-comunicacia3', 'enines-usuari'],
    'ambit': ['gestia3', 'lloc-de-treball-eines-usuari', 'infraestructures'],
}

servei_wrcx = dict(
    type='serveitic',
    id='servei_wrcx',
    title=u"Servei WRCX",
    description=u"Servei Web de Recerca Ubicat als Campus",
    responsable=u"José García",
    responsableMail=u"jose.garcia@upc.edu",
    product_id="servei_wrcx",
    service_id="servei_wrcx",
    tipologia=[u"Web", u"Gestor continguts"],
    ambit=[u"Recerca"],
    ubicacio=[u"CNord", u"CSud"],
    prestador=[],
    )

servei_wgcu = dict(
    type='serveitic',
    id='servei_wgcu',
    title=u"Servei WGCU",
    description=u"Servei Web de Gestió als Campus per UPCnet",
    responsable=u"José García",
    responsableMail=u"jose.garcia@upc.edu",
    product_id="servei_wgcu",
    service_id="servei_wgcu",
    tipologia=[u"Web", u"Eines comunicació"],
    ambit=[u"Gestió"],
    ubicacio=[u"CNord", u"Manresa"],
    prestador=[u"UPCnet"],
    )

servei_wgct = dict(
    type='serveitic',
    id='servei_wgct',
    title=u"Servei WGCT",
    description=u"Servei Web de Gestió per Terrassa",
    responsable=u"José García",
    responsableMail=u"jose.garcia@upc.edu",
    product_id="servei_wgct",
    service_id="servei_wgct",
    tipologia=[u"Web", u"Ofimàtica"],
    ambit=[u"Gestió"],
    ubicacio=[u"CNord"],
    prestador=[u"Terrassa"],
    )

servei_exlm = dict(
    type='serveitic',
    id='servei_exlm',
    title=u"Servei EXLM",
    description=u"Servei ERP al CBLlobregat per Movistar",
    responsable=u"José García",
    responsableMail=u"jose.garcia@upc.edu",
    product_id="servei_exlm",
    service_id="servei_exlm",
    tipologia=[u"ERP", u"Ofimàtica"],
    ambit=[],
    ubicacio=[u"CBLlobregat"],
    prestador=[u"Movistar"],
    )

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
