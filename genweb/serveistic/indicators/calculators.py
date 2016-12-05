import re
import json

from Products.CMFCore.utils import getToolByName

from genweb.core.indicators import Calculator, CalculatorException
from genweb.serveistic.utilities import serveistic_config
from genweb.serveistic.data_access.servei import ServeiDataReporter
from genweb.serveistic.data_access.webanalytics import (
    GoogleAnalyticsReporter, GoogleAnalyticsReporterException)


class ServeiNumber(Calculator):
    def calculate(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        reporter = ServeiDataReporter(catalog)
        return len(reporter.list_by_review_state('published'))


class GoogleAnalyticsCalculator(Calculator):
    def _get_reporter(self):
        try:
            return GoogleAnalyticsReporter(
                json.loads(serveistic_config().ga_key_json))
        except (TypeError, ValueError) as e:
            raise CalculatorException(
                "Invalid GA JSON key ({0})".format(e))
        except GoogleAnalyticsReporterException as e:
            raise CalculatorException(
                "Cannot instantiate GA reporter ({0})".format(e))

    def _get_ids(self):
        if serveistic_config().ga_view_id:
            return "ga:{0}".format(serveistic_config().ga_view_id)
        return None


class SessionsCalculator(GoogleAnalyticsCalculator):
    def __init__(self, context):
        super(SessionsCalculator, self).__init__(context)
        self._start_date = None
        self._end_date = None
        self._filters = None

    def calculate(self):
        try:
            results = self._get_reporter().query(dict(
                ids=self._get_ids(),
                start_date=self._start_date,
                end_date=self._end_date,
                metrics='ga:sessions',
                filters=self._filters))
            return int(results['totalsForAllResults']['ga:sessions'])
        except GoogleAnalyticsReporterException as e:
            raise CalculatorException("Error when querying GA ({0})".format(e))


class SessionsDeltaMonth(SessionsCalculator):
    def __init__(self, context):
        super(SessionsDeltaMonth, self).__init__(context)
        self._start_date = '30daysAgo'
        self._end_date = '1daysAgo'


class SessionsDeltaWeek(SessionsCalculator):
    def __init__(self, context):
        super(SessionsDeltaWeek, self).__init__(context)
        self._start_date = '7daysAgo'
        self._end_date = '1daysAgo'


class SessionsDeltaDay(SessionsCalculator):
    def __init__(self, context):
        super(SessionsDeltaDay, self).__init__(context)
        self._start_date = '1daysAgo'
        self._end_date = '1daysAgo'


class SessionsTargetHome(SessionsCalculator):
    def __init__(self, context):
        super(SessionsTargetHome, self).__init__(context)
        self._filters = 'ga:pagePath=~^/ca/?$'


class SessionsSourceSearchEngine(SessionsCalculator):
    def __init__(self, context):
        super(SessionsSourceSearchEngine, self).__init__(context)
        self._filters = 'ga:medium==organic'


class SessionsSourceServei(SessionsCalculator):
    def calculate(self):
        self._filters = self._build_filters()
        return super(SessionsSourceServei, self).calculate()

    def _build_filters(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        reporter = ServeiDataReporter(catalog)
        servei_filters = [
            self._build_filter_from_url(servei.website_url)
            for servei in reporter.list_by_review_state('published')
            if servei.website_url]
        return ",".join(servei_filters) if servei_filters else "ga:source=~^$"

    def _build_filter_from_url(self, url):
        return "ga:source=~^{0}$".format(
            self._extract_url_domain_re(url))

    def _extract_url_domain_re(self, url):
        return re.escape(self._remove_path(self._remove_protocol(url)))

    def _remove_protocol(self, url):
        after_protocol = url.split('://')[1:2]
        return after_protocol[0] if after_protocol else url

    def _remove_path(self, url):
        return url.split('/')[0]


class SessionsDeltaMonthTargetHome(SessionsDeltaMonth, SessionsTargetHome):
    pass


class SessionsDeltaMonthSourceSearchEngine(
        SessionsDeltaMonth, SessionsSourceSearchEngine):
    pass


class SessionsDeltaMonthSourceServei(
        SessionsDeltaMonth, SessionsSourceServei):
    pass


class SessionsDeltaWeekTargetHome(SessionsDeltaWeek, SessionsTargetHome):
    pass


class SessionsDeltaWeekSourceSearchEngine(
        SessionsDeltaWeek, SessionsSourceSearchEngine):
    pass


class SessionsDeltaWeekSourceServei(
        SessionsDeltaWeek, SessionsSourceServei):
    pass


class SessionsDeltaDayTargetHome(SessionsDeltaDay, SessionsTargetHome):
    pass


class SessionsDeltaDaySourceSearchEngine(
        SessionsDeltaDay, SessionsSourceSearchEngine):
    pass


class SessionsDeltaDaySourceServei(
        SessionsDeltaDay, SessionsSourceServei):
    pass
