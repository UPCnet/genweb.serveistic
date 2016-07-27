import logging

from genweb.serveistic.ws_client.indicators import ClientException

logger = logging.getLogger(name='genweb.serveistic')


class IndicadorsDataReporter(object):
    def __init__(self, client):
        self.client = client

    def _remove_prefix(self, text, prefix):
        if text.startswith(prefix + ' -'):
            return text[len(prefix + ' -'):]
        return text

    def list_by_service_id(self, service_id, count, count_category_max=None):
        indicators = []
        count_category = 0
        try:
            for indicator in self.client.list_indicators(service_id, count):
                categories = []
                for category in self.client.list_categories(
                        service_id, indicator.identifier):
                    categories.append({
                        'identifier': category.identifier,
                        'description': self._remove_prefix(
                            category.description, indicator.description),
                        'date_modified': category.date_modified.strftime(
                            "%d/%m/%Y %H:%M") if category.date_modified else '',
                        'value': category.value})
                    count_category += 1
                    if (count_category_max and
                            count_category >= count_category_max):
                        break

                indicators.append({
                    'identifier':
                        indicator.identifier,
                    'description': indicator.description,
                    'date_modified': indicator.date_modified.strftime(
                        '%d/%m/%Y') if indicator.date_modified else '',
                    'categories': categories
                    })
                if (count_category_max and
                        count_category >= count_category_max):
                    break
        except ClientException as e:
            logger.warning("ClientException: {0}".format(e.message))
            indicators = None
        return indicators
