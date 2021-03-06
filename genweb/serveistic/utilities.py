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


class PrestadorVocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Proveïdor / Unitat"


class UbicacioVocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Usuaris"


class TipologiaVocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Servei / Àrea"


class AmbitVocabulary(FacetValuesVocabularyBase):
    def __init__(self):
        self.facet_id = u"Àmbit"
