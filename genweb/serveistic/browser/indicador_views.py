from five import grok

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.utilities import get_ws_indicadors_client
from genweb.serveistic.data_access.indicadors import IndicadorsDataReporter


class Indicadors(grok.View):
    grok.name('indicadors_list')
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('indicadors')

    @property
    def js_define_url_retrieve(self):
        return "var url_retrieve_indicadors = 'retrieve_indicadors';"

    @property
    def js_define_count(self):
        return "var count = '';"

    @property
    def js_define_count_category(self):
        return "var count_category = '';"


class RetrieveIndicadors(grok.View):
    grok.name('retrieve_indicadors')
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('retrieve_indicadors')

    def parse_parameters(self):
        try:
            count = int(self.request.form.get('count', None))
        except (TypeError, ValueError):
            count = None

        try:
            count_category = int(self.request.form.get('count_category', None))
        except (TypeError, ValueError):
            count_category = None

        return count, count_category

    @property
    def count(self):
        return self.parse_parameters()[0]

    @property
    def indicadors_href(self):
        return "indicadors_list"

    @property
    def indicadors(self):
        ws_client = get_ws_indicadors_client()
        reporter = IndicadorsDataReporter(ws_client)

        service_id = self.context.service_id
        count, count_category = self.parse_parameters()

        if service_id:
            return reporter.list_by_service_id(
                service_id, count, count_category)
        else:
            return None
