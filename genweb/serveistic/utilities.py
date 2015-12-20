# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.interface import implements

from OFS.SimpleItem import SimpleItem
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
    facetes_sorted = sorted(facetes, key=lambda x: x['faceta'])
    try:
        for tup in facetes_sorted:
            if tup['faceta'] not in facetes_added:
                header_name = tup['faceta']
                keywords.append({'title': tup['faceta'],
                                 'value': tup['faceta'],
                                 'header':  True,
                                 'header-obj': ''})
                facetes_added.append(tup['faceta'])

            keywords.append({'title': tup['valor'],
                             'value': tup['valor'],
                             'header': False,
                             'checked': tup['valor'] in checked,
                             'header-obj': header_name})
        return keywords
    except:
        return None

def get_servei(self):
    context = aq_inner(self.context)
    for obj in aq_chain(context):
        if IServeiTIC.providedBy(obj):
            return obj
    return None
