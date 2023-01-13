# -*- coding: utf-8 -*-

import csv

from zope.component import getUtility
from plone import api
from plone.registry.interfaces import IRegistry
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from genweb.serveistic import _
from genweb.serveistic.config_helper import get_absolute_path, config
from genweb.serveistic.controlpanel import IServeisTICFacetesControlPanelSettings


translates = [
    _(u"category_freq_unknown"),
    _(u"category_freq_horaria"),
    _(u"category_freq_diaria"),
    _(u"category_freq_setmanal"),
    _(u"category_freq_mensual"),
    _(u"category_freq_trimestral"),
    _(u"category_freq_quadrimestral"),
    _(u"category_freq_semestral"),
    _(u"category_freq_anual")
]

# Specify the indexes you want, with ('index_name', 'index_type')
NEW_INDEXES = [
    ('prestador', 'KeywordIndex'),
    ('ubicacio', 'KeywordIndex'),
    ('tipologia', 'KeywordIndex'),
    ('ambit', 'KeywordIndex'),
    ('ca_faceta_1', 'KeywordIndex'),
    ('ca_faceta_2', 'KeywordIndex'),
    ('ca_faceta_3', 'KeywordIndex'),
    ('ca_faceta_4', 'KeywordIndex'),
    ('ca_faceta_5', 'KeywordIndex'),
    ('ca_faceta_6', 'KeywordIndex'),
    ('ca_faceta_7', 'KeywordIndex'),
    ('ca_faceta_8', 'KeywordIndex'),
    ('es_faceta_1', 'KeywordIndex'),
    ('es_faceta_2', 'KeywordIndex'),
    ('es_faceta_3', 'KeywordIndex'),
    ('es_faceta_4', 'KeywordIndex'),
    ('es_faceta_5', 'KeywordIndex'),
    ('es_faceta_6', 'KeywordIndex'),
    ('es_faceta_7', 'KeywordIndex'),
    ('es_faceta_8', 'KeywordIndex'),
    ('en_faceta_1', 'KeywordIndex'),
    ('en_faceta_2', 'KeywordIndex'),
    ('en_faceta_3', 'KeywordIndex'),
    ('en_faceta_4', 'KeywordIndex'),
    ('en_faceta_5', 'KeywordIndex'),
    ('en_faceta_6', 'KeywordIndex'),
    ('en_faceta_7', 'KeywordIndex'),
    ('en_faceta_8', 'KeywordIndex'),
    ('is_general', 'FieldIndex'),
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
        IServeisTICFacetesControlPanelSettings, check=False)

    facets_file_path = get_absolute_path(config.get('facets', 'file_path'))

    if hasattr(settings, 'facetes_table') and settings.facetes_table:
        pass
    else:
        with open(facets_file_path, 'r') as facets_file:
            try:
                settings.facetes_table = [
                    {'faceta': row[0].decode('utf-8'),
                     'valor': row[1].decode('utf-8'),
                     'valor_es': row[2].decode('utf-8'),
                     'valor_en': row[3].decode('utf-8'),
                     }
                    for row in csv.reader(
                        facets_file, delimiter=',', quotechar='"')]
            except:
                pass


def add_container(container, type, title,
                  allowed_types=None, exclude_from_nav=False):
    folder_id = getUtility(IIDNormalizer).normalize(title)
    if folder_id not in container:
        folder = api.content.create(
            type=type,
            id=folder_id,
            title=title,
            container=container)
        api.content.transition(
            obj=folder,
            transition='publish')
        if allowed_types:
            behavior = ISelectableConstrainTypes(folder)
            behavior.setConstrainTypesMode(1)
            behavior.setLocallyAllowedTypes(allowed_types)
            behavior.setImmediatelyAddableTypes(allowed_types)
        folder.exclude_from_nav = exclude_from_nav
    return container[folder_id]


def add_default_folders():
    portal = api.portal.get()
    if 'ca' in portal:
        add_container(
            container=portal['ca'],
            type='Folder',
            title=u"Notificacions",
            allowed_types=('notificaciotic',),
            exclude_from_nav=True)


def setupVarious(context):
    if context.readDataFile('genweb.serveistic.txt') is None:
        return

    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    add_catalog_indexes(catalog)
    add_default_settings()
    add_default_folders()
