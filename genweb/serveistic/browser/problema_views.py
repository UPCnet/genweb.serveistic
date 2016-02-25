from five import grok

from zope.interface import Interface

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.utilities import get_ws_problemes_client, get_servei
from genweb.serveistic.data_access.problemes import ProblemesDataReporter


class Problemes(grok.View):
    grok.name('problemes')
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('problemes')

    @property
    def product_id(self):
        serveitic = get_servei(self)
        return serveitic.product_id if serveitic.product_id else ''


class RetrieveProblemes(grok.View):
    grok.name('retrieve_problemes')
    grok.context(Interface)
    grok.layer(IGenwebServeisticLayer)
    grok.template('retrieve_problemes')

    def parse_parameters(self):
        product_id = self.request.form.get('product_id', None)
        try:
            count = int(self.request.form.get('count', None))
        except (TypeError, ValueError):
            count = None
        return product_id, count

    @property
    def count(self):
        return self.parse_parameters()[1]

    @property
    def problemes_href(self):
        return "problemes"

    @property
    def problemes(self):
        reporter = ProblemesDataReporter(get_ws_problemes_client())
        product_id, count = self.parse_parameters()
        return reporter.list_by_product_id(product_id, count)
