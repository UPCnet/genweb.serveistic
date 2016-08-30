import logging

from five import grok

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.utilities import get_ws_indicadors_client
from genweb.serveistic.data_access.indicadors import (
    IndicadorsDataReporter, IndicadorsDataReporterException)

logger = logging.getLogger(name='genweb.serveistic')


class Indicadors(grok.View):
    grok.name('indicadors_list')
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('indicadors')

    def js_retrieve(self):
        return """
    $(document).ready(function()
    {{
        var url = '{url}';
        retrieve_indicadors(url, '', '');
    }});
       """.format(url="retrieve_indicadors")


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
        reporter = IndicadorsDataReporter(get_ws_indicadors_client())

        service_id = self.context.service_id
        service_indicators_order = self.context.service_indicators_order
        count_indicator, count_category = self.parse_parameters()

        if not service_id:
            return None

        try:
            return reporter.list_by_service_id_and_indicators_order(
                service_id, service_indicators_order,
                count_indicator, count_category)
        except IndicadorsDataReporterException as e:
            logger.warning(
                "Error when reporting indicators ({0})".format(e))
            return None
