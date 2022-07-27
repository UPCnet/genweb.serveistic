# -*- coding: utf-8 -*-
from Products.Five import BrowserView

from plone import api

import transaction


class MigracioFacetes(BrowserView):

    def __call__(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        serveistic = catalog(portal_type='serveitic')
        for serveitic in serveistic:
            servei = serveitic.getObject()
            servei.ca_faceta_1 = servei.tipologia
            servei.es_faceta_1 = servei.tipologia
            servei.en_faceta_1 = servei.tipologia

            servei.ca_faceta_2 = servei.ambit
            servei.es_faceta_2 = servei.ambit
            servei.en_faceta_2 = servei.ambit

            servei.ca_faceta_3 = servei.ubicacio
            servei.es_faceta_3 = servei.ubicacio
            servei.en_faceta_3 = servei.ubicacio

            servei.ca_faceta_4 = servei.prestador
            servei.es_faceta_4 = servei.prestador
            servei.en_faceta_4 = servei.prestador

            servei.reindexObject()

        transaction.commit()
        return "OK"
