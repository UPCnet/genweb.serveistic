from five import grok

from Products.CMFCore.utils import getToolByName

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.utilities import get_ws_problemes_client
from genweb.serveistic.data_access.problemes import ProblemesDataReporter


class Problemes(grok.View):
    grok.name('problemes_list')
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('problemes')

    @property
    def js_define_url_retrieve(self):
        return "var url_retrieve_problemes = 'retrieve_problemes';"

    @property
    def js_define_count(self):
        return "var count = '';"


class RetrieveProblemes(grok.View):
    grok.name('retrieve_problemes')
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('retrieve_problemes')

    def parse_parameters(self):
        try:
            count = int(self.request.form.get('count', None))
        except (TypeError, ValueError):
            count = None
        return count

    @property
    def count(self):
        return self.parse_parameters()

    @property
    def problemes_href(self):
        return "problemes_list"

    @property
    def problemes(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        ws_client = get_ws_problemes_client()
        reporter = ProblemesDataReporter(catalog, ws_client)

        product_id = self.context.product_id
        servei_path = '/'.join(self.context.getPhysicalPath())
        count = self.parse_parameters()

        if product_id:
            return reporter.list_by_product_id(product_id, count)
        elif servei_path:
            return reporter.list_by_servei_path(servei_path, count)
        else:
            return None
