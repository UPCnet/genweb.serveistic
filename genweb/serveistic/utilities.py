# -*- coding: utf-8 -*-

from zope.component import getUtility, queryUtility
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.registry.interfaces import IRegistry
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Acquisition import aq_inner, aq_chain
from eea.faceted.vocabularies.utils import IVocabularyFactory
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot

from genweb.serveistic.controlpanel import IServeisTICControlPanelSettings
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.config_helper import facets_vocabulary
from genweb.serveistic.ws_client.problems import Client as ProblemesClient
from genweb.core.indicators.client import Client as IndicadorsClient


def build_vocabulary(values):
    return SimpleVocabulary([
        SimpleTerm(title=_(value), value=value, token=token)
        for token, value in enumerate(values)])


def serveistic_config():
    """ Funcio que retorna les configuracions del controlpanel """
    registry = queryUtility(IRegistry)
    return registry.forInterface(IServeisTICControlPanelSettings)


def get_servei(self):
    context = aq_inner(self.context)
    for obj in aq_chain(context):
        if IServeiTIC.providedBy(obj):
            return obj
    return None


def get_ws_problemes_client():
    endpoint = serveistic_config().ws_problemes_endpoint
    login_username = serveistic_config().ws_problemes_login_username
    login_password = serveistic_config().ws_problemes_login_password
    return ProblemesClient(endpoint, login_username, login_password)


def get_ws_indicadors_client():
    endpoint = serveistic_config().ws_indicadors_endpoint
    return IndicadorsClient(endpoint)


def get_referer_path(context, request):
    if referer_is_current(request):
        return getNavigationRoot(context)
    try:
        return request.getHeader('referer').replace(
            get_site_url(context), get_site_path(context))
    except (AttributeError, TypeError):
        return None


def referer_is_current(request):
    if request.getHeader('referer'):
        return (get_clean_url(request.getHeader('referer')) ==
                get_clean_url(request.getURL()))
    return True


def get_clean_url(url):
    return url.split('?')[0].split('@')[0]


def get_site_url(context):
    portal_url = getToolByName(context, 'portal_url')
    return portal_url.getPortalObject().absolute_url()


def get_site_path(context):
    portal_url = getToolByName(context, 'portal_url')
    return '/'.join(portal_url.getPortalObject().getPhysicalPath())


class FacetsVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        return facets_vocabulary


class FacetValuesVocabularyBase(object):
    """
    Base class that represents a vocabulary containing the defined values for
    a facet taken from the 'facetes_tables' property of the Serveis TIC plugin
    settings. The name of the facet the values of which are retrieved is
    specified in self.facet_id.
    """
    implements(IVocabularyFactory)

    def __init__(self):
        self.facet_id = ""
        self.lang = ""

    def __call__(self, context):
        facets = serveistic_config().facetes_table
        facets = [] if facets is None else facets

        vocabulary = []
        for facet in facets:
            if facet['faceta'] == self.facet_id and facet['valor']:
                vocabulary.append(SimpleTerm(
                    value=getUtility(IIDNormalizer).normalize(facet['valor'].encode('utf-8')),
                    title=facet['valor' + self.lang].encode('utf-8') if facet['valor' + self.lang] else '-'
                ))

        return SimpleVocabulary(vocabulary)


class PrestadorVocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Proveïdor / Unitat"
        self.lang = u""


class UbicacioVocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Usuaris"
        self.lang = u""


class TipologiaVocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Servei / Àrea"
        self.lang = u""


class AmbitVocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Àmbit"
        self.lang = u""


class CAFaceta1Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 1"
        self.lang = u""


class CAFaceta2Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 2"
        self.lang = u""


class CAFaceta3Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 3"
        self.lang = u""


class CAFaceta4Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 4"
        self.lang = u""


class CAFaceta5Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 5"
        self.lang = u""


class CAFaceta6Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 6"
        self.lang = u""


class CAFaceta7Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 7"
        self.lang = u""


class CAFaceta8Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 8"
        self.lang = u""


class ESFaceta1Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 1"
        self.lang = u"_es"


class ESFaceta2Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 2"
        self.lang = u"_es"


class ESFaceta3Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 3"
        self.lang = u"_es"


class ESFaceta4Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 4"
        self.lang = u"_es"


class ESFaceta5Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 5"
        self.lang = u"_es"


class ESFaceta6Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 6"
        self.lang = u"_es"


class ESFaceta7Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 7"
        self.lang = u"_es"


class ESFaceta8Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 8"
        self.lang = u"_es"


class ENFaceta1Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 1"
        self.lang = u"_en"


class ENFaceta2Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 2"
        self.lang = u"_en"


class ENFaceta3Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 3"
        self.lang = u"_en"


class ENFaceta4Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 4"
        self.lang = u"_en"


class ENFaceta5Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 5"
        self.lang = u"_en"


class ENFaceta6Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 6"
        self.lang = u"_en"


class ENFaceta7Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 7"
        self.lang = u"_en"


class ENFaceta8Vocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Faceta 8"
        self.lang = u"_en"
