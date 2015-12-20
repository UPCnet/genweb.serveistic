# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName


# Specify the indexes you want, with ('index_name', 'index_type')
NEW_INDEXES = [('tipus', 'FieldIndex')
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

def setupVarious(context):
    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    add_catalog_indexes(catalog)
