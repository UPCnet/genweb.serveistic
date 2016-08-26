from Products.CMFCore.utils import getToolByName

from genweb.core.indicators import Calculator
from genweb.serveistic.data_access.servei import ServeiDataReporter


class ServeiNumber(Calculator):
    def calculate(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        reporter = ServeiDataReporter(catalog)
        return len(reporter.list_by_review_state('published'))
