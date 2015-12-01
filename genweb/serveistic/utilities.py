# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.interface import implements

from OFS.SimpleItem import SimpleItem
from BTrees.OOBTree import OOBTree

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from genweb.serveistic.controlpanel import IServeisTICControlPanelSettings
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry


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
        facetes_added = []
        keywords = []
        facetes = self.serveistic_config().facetes_table
        facetes_sorted = sorted(facetes, key=lambda x: x['faceta'])
        for tup in facetes_sorted:
            if tup['faceta'] not in facetes_added:
                keywords.append({'title': tup['faceta'],
                                 'value': tup['faceta'],
                                 'header':  True})
                facetes_added.append(tup['faceta'])

            keywords.append({'title': tup['valor'],
                             'value': tup['valor'],
                             'header': False,
                             'checked': tup['valor'] in checked})
        return keywords

    def serveistic_config(self):
        """ Funcio que retorna les configuracions del controlpanel """
        registry = queryUtility(IRegistry)
        return registry.forInterface(IServeisTICControlPanelSettings)
