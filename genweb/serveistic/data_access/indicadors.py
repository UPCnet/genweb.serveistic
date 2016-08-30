import logging

from genweb.core.indicators.client import ClientException
from genweb.serveistic.content.serveitic import (
    is_valid_service_indicators_order,
    parse_service_indicators_order)

logger = logging.getLogger(name='genweb.serveistic')


class IndicadorsDataReporterException(Exception):
    pass


class IndicadorsDataReporter(object):
    def __init__(self, client):
        self.client = client

    def list_by_service_id_and_indicators_order(
            self, service_id, indicators_order,
            count_indicator=None, count_category=None):
        if not indicators_order:
            return self.list_by_service_id(
                service_id, count_indicator, count_category)
        if count_indicator == 0 or count_category == 0:
            return []
        if not is_valid_service_indicators_order(indicators_order):
            raise IndicadorsDataReporterException(
                "Indicators order is not valid")

        m = IndicadorsMatrixDataReporter(self.client, service_id)
        indicators = []
        count_category_cur = 0
        for indicator_i, categories_is in parse_service_indicators_order(
                indicators_order):
            categories = []
            for category_i in categories_is:
                try:
                    categories.append(
                        self._category_to_dict(m[indicator_i, category_i]))
                    count_category_cur += 1
                    if count_category and count_category_cur >= count_category:
                        break
                except IndexError:
                    logger.warning(
                        "IndexError when accessing category {0}, {1} in "
                        "list_by_service_id_and_indicators_order".format(
                            indicator_i, category_i))
                    continue
            try:
                indicators.append(
                    self._indicator_to_dict(m[indicator_i], categories))
                if count_indicator and len(indicators) >= count_indicator:
                    break
                if count_category and count_category_cur >= count_category:
                    break
            except IndexError:
                logger.warning(
                    "IndexError when accessing indicator {0} in "
                    "list_by_service_id_and_indicators_order".format(
                        indicator_i))
                continue
        return indicators

    def list_by_service_id(
            self, service_id, count_indicator=None, count_category=None):
        indicators = []
        count_category_cur = 0
        try:
            for indicator in self.client.list_indicators(
                    service_id, count_indicator):
                categories = []
                for category in self.client.list_categories(
                        service_id, indicator.identifier):
                    categories.append(self._category_to_dict(category))
                    count_category_cur += 1
                    if (count_category and
                            count_category_cur >= count_category):
                        break

                indicators.append(
                    self._indicator_to_dict(indicator, categories))
                if (count_category and
                        count_category_cur >= count_category):
                    break
        except ClientException as e:
            raise IndicadorsDataReporterException(
                "Error when listing indicators ({0})".format(e))
        return indicators

    def _category_to_dict(self, category):
        return dict(
            identifier=category.identifier,
            description=category.description,
            date_modified=category.date_modified.strftime(
                            "%d/%m/%Y %H:%M") if category.date_modified else '',
            value=category.value)

    def _indicator_to_dict(self, indicator, categories):
        return dict(
            identifier=indicator.identifier,
            description=indicator.description,
            date_modified=indicator.date_modified.strftime(
                        '%d/%m/%Y') if indicator.date_modified else '',
            categories=categories)


class IndicadorsMatrixDataReporter(object):
    """
    1-based index matrix that provides indicators of a specific service.
    """
    def __init__(self, client, service_id):
        self._client = client
        self._service_id = service_id
        self._indicators = None
        self._categories = {}

    def __getitem__(self, item):
        if type(item) == int:
            return self._getitem_from_int(item)
        elif (type(item) == tuple and len(item) == 2 and
              type(item[0]) == int and type(item[1]) == int):
            return self._getitem_from_tuple(item)
        else:
            raise TypeError(
                "item must be either an integer or a 2-integer tuple")

    def _getitem_from_int(self, item):
        if not self._indicators:
            self._retrieve_indicators()
        if not 1 <= item <= len(self._indicators):
            raise IndexError
        return self._indicators[item - 1]

    def _getitem_from_tuple(self, item):
        indicator_index, category_index = item
        indicator = self[indicator_index]
        if indicator_index not in self._categories:
            self._retrieve_categories(indicator_index, indicator.identifier)
        if not 1 <= category_index <= len(self._categories[indicator_index]):
            raise IndexError
        return self._categories[indicator_index][category_index - 1]

    def _retrieve_categories(self, indicator_index, indicator_id):
        self._categories[indicator_index] = self._client.list_categories(
            self._service_id, indicator_id)

    def _retrieve_indicators(self):
        self._indicators = self._client.list_indicators(self._service_id)
