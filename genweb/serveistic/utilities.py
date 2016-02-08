# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.interface import implements

from OFS.SimpleItem import SimpleItem
from genweb.serveistic.controlpanel import IServeisTICControlPanelSettings
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from Acquisition import aq_inner, aq_chain
from genweb.serveistic.content.serveitic import IServeiTIC

import operator
from eea.faceted.vocabularies.utils import compare
from eea.faceted.vocabularies.utils import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName


class IKeywordsCategorizationUtility(Interface):
    """ Utility to manage a registry of the items used in the newsletters
    """

    categories = Attribute(u"keyword categories")


class KeywordsCategorizationUtility(SimpleItem):
    """
    """

    implements(IKeywordsCategorizationUtility)
    categories = None

    def __init__(self):
        """
        """

    def update(self):
        """
        """

    def keywords(self, checked=[]):
        """
        """
        return getFacetes(self, checked)


def serveistic_config():
    """ Funcio que retorna les configuracions del controlpanel """
    registry = queryUtility(IRegistry)
    return registry.forInterface(IServeisTICControlPanelSettings)


def getFacetes(self, checked=[]):
    facetes_added = []
    keywords = []
    header_name = ''
    facetes = serveistic_config().facetes_table
    if facetes:
        facetes_sorted = sorted(facetes, key=lambda x: x['faceta'])

        for tup in facetes_sorted:
            if tup['faceta'] not in facetes_added:
                header_name = tup['faceta']
                keywords.append({'title': tup['faceta'],
                                 'value': tup['faceta'],
                                 'header': True,
                                 'header-obj': ''})
                facetes_added.append(tup['faceta'])

            keywords.append({'title': tup['valor'],
                             'value': tup['valor'],
                             'header': False,
                             'checked': tup['valor'] in checked,
                             'header-obj': header_name})
        return keywords

    else:
        return None


def get_servei(self):
    context = aq_inner(self.context)
    for obj in aq_chain(context):
        if IServeiTIC.providedBy(obj):
            return obj
    return None


# --------------------
# Faceted Vocabularys
# --------------------
class UbicacioVocabulary(object):
    """ Return portal types as vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ See IVocabularyFactory interface
        """

        facetes = serveistic_config().facetes_table
        if facetes:
            facetes_sorted = sorted(facetes, key=lambda x: x['faceta'])
        res = []
        for fac in facetes_sorted:
            if fac['faceta'].encode('utf8') == 'Ubicacio':
                res.append(fac['valor'].encode('utf8'))
        items = [SimpleTerm(value, value, value) for value in res]
        return SimpleVocabulary(items)


class PrestadorVocabulary(object):
    """ Return portal types as vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ See IVocabularyFactory interface
        """

        facetes = serveistic_config().facetes_table
        if facetes:
            facetes_sorted = sorted(facetes, key=lambda x: x['faceta'])
        res = []
        for fac in facetes_sorted:
            if fac['faceta'].encode('utf8') == 'Prestador':
                res.append(fac['valor'].encode('utf8'))
        items = [SimpleTerm(value, value, value) for value in res]
        return SimpleVocabulary(items)


class TipologiaVocabulary(object):
    """ Return portal types as vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ See IVocabularyFactory interface
        """

        facetes = serveistic_config().facetes_table
        if facetes:
            facetes_sorted = sorted(facetes, key=lambda x: x['faceta'])
        res = []
        for fac in facetes_sorted:
            if fac['faceta'].encode('utf8') == 'Tipologia':
                res.append(fac['valor'].encode('utf8'))
        items = [SimpleTerm(value, value, value) for value in res]
        return SimpleVocabulary(items)


class AmbitVocabulary(object):
    """ Return portal types as vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ See IVocabularyFactory interface
        """

        facetes = serveistic_config().facetes_table
        if facetes:
            facetes_sorted = sorted(facetes, key=lambda x: x['faceta'])
        res = []
        for fac in facetes_sorted:
            if fac['faceta'].encode('utf8') == 'Àmbit':
                res.append(fac['valor'].encode('utf8'))
        items = [SimpleTerm(value, value, value) for value in res]
        return SimpleVocabulary(items)