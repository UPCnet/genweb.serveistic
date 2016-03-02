from five import grok

from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.utilities import get_ws_problemes_client, get_servei
from genweb.serveistic.data_access.problemes import ProblemesDataReporter


class Problemes(grok.View):
    grok.name('problemes_list')
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('problemes')

    @property
    def product_id(self):
        servei = get_servei(self)
        return servei.product_id if servei.product_id else ''

    @property
    def servei_path(self):
        servei = get_servei(self)
        return '/'.join(servei.getPhysicalPath())


class RetrieveProblemes(grok.View):
    grok.name('retrieve_problemes')
    grok.context(Interface)
    grok.layer(IGenwebServeisticLayer)
    grok.template('retrieve_problemes')

    def parse_parameters(self):
        product_id = self.request.form.get('product_id', None)
        servei_path = self.request.form.get('servei_path', None)
        try:
            count = int(self.request.form.get('count', None))
        except (TypeError, ValueError):
            count = None
        return product_id, servei_path, count

    @property
    def count(self):
        return self.parse_parameters()[2]

    @property
    def problemes_href(self):
        return "problemes_list"

    @property
    def problemes(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        ws_client = get_ws_problemes_client()
        reporter = ProblemesDataReporter(catalog, ws_client)

        product_id, servei_path, count = self.parse_parameters()

        if product_id:
            return reporter.list_by_product_id(product_id, count)
        elif servei_path:
            return reporter.list_by_servei_path(servei_path, count)
        else:
            return None
