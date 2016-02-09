# -*- coding: utf-8 -*-

from zope.component import getUtility, queryUtility
from zope.interface import Interface, Attribute, implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.registry.interfaces import IRegistry
from plone.i18n.normalizer.interfaces import IIDNormalizer
from OFS.SimpleItem import SimpleItem
from Acquisition import aq_inner, aq_chain
from eea.faceted.vocabularies.utils import IVocabularyFactory

from genweb.serveistic.controlpanel import IServeisTICControlPanelSettings
from genweb.serveistic.content.serveitic import IServeiTIC


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


class FacetVocabulary(object):
    """
    Base class that represents a vocabulary containing the defined values for
    a facet taken from the 'facetes_tables' property of the Serveis TIC plugin
    settings. The name of the facet the values of which are retrieved is
    specified in self.facet_id.
    """
    implements(IVocabularyFactory)

    def __init__(self):
        self.facet_id = ""

    def __call__(self, context):
        facets = serveistic_config().facetes_table
        facets = [] if facets is None else facets
        facet_values = [facet_pair['valor']
                        for facet_pair in facets
                        if facet_pair['faceta'] == self.facet_id]
        return SimpleVocabulary([
            SimpleTerm(
                token=index,
                value=getUtility(IIDNormalizer).normalize(
                    value.encode('utf-8')),
                title=value.encode('utf-8'))
            for index, value in enumerate(facet_values)])


class PrestadorVocabulary(FacetVocabulary):
    def __init__(self):
        self.facet_id = "prestador"


class UbicacioVocabulary(FacetVocabulary):
    def __init__(self):
        self.facet_id = "ubicacio"


class TipologiaVocabulary(FacetVocabulary):
    def __init__(self):
        self.facet_id = "tipologia"


class AmbitVocabulary(FacetVocabulary):
    def __init__(self):
        self.facet_id = "ambit"
