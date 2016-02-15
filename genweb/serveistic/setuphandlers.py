# -*- coding: utf-8 -*-

import csv

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from genweb.serveistic.config_helper import get_absolute_path, config
from genweb.serveistic.controlpanel import IServeisTICControlPanelSettings


# Specify the indexes you want, with ('index_name', 'index_type')
NEW_INDEXES = [
    ('prestador', 'KeywordIndex'),
    ('ubicacio', 'KeywordIndex'),
    ('tipologia', 'KeywordIndex'),
    ('ambit', 'KeywordIndex')
    ]


# Afegit creació d'indexos programàticament i controladament per:
# http://maurits.vanrees.org/weblog/archive/2009/12/catalog
def add_catalog_indexes(catalog):
    indexables = []
    indexes = catalog.indexes()
    for name, meta_type in NEW_INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
    if len(indexables) > 0:
        catalog.manage_reindexIndex(ids=indexables)


def add_default_settings():
    settings = getUtility(IRegistry).forInterface(
        IServeisTICControlPanelSettings, check=False)

    facets_file_path = get_absolute_path(config.get('facets', 'file_path'))

    with open(facets_file_path, 'r') as facets_file:
        settings.facetes_table = [
            {'faceta': row[0].decode('utf-8'), 'valor': row[1].decode('utf-8')}
            for row in csv.reader(facets_file, delimiter=',', quotechar='"')]


def setupVarious(context):
    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    add_catalog_indexes(catalog)
    add_default_settings()
