# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.interface import implements

from OFS.SimpleItem import SimpleItem
from BTrees.OOBTree import OOBTree

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from lxml import etree
import requests


class IKeywordsCategorizationUtility(Interface):
    """ Utility to manage a registry of the items used in the newsletters
    """

    categories = Attribute(u"keyword categories")


class KeywordsCategorizationUtility(SimpleItem):
    """
    """

    implements(IKeywordsCategorizationUtility)
    categories = None

    def __init__(self):
        """
        """
        self.categories = OOBTree()

    def update(self):
        """
        """
        import ipdb;ipdb.set_trace()
        self.categories = OOBTree()

    def keywords(self, checked=[]):
        """
        """
        import ipdb;ipdb.set_trace()
        factory = getUtility(IVocabularyFactory, 'plone.app.vocabularies.Keywords')
        vocabulary = factory(self)

        keywords_by_filter = []
        terms = []
        # terms = [str(a).decode('utf-8') for a in vocabulary]
        for a in vocabulary:
            terms.append(a.title)

        filter_terms = []

        filters_by_title = sorted(self.filternames.items(), key=lambda x: x[1])

        for filterid, filtertitle in filters_by_title:
            if len(self.categories[filterid]) > 0:
                keywords_by_filter.append({'title': filtertitle,
                                           'value': filterid,
                                           'header':  True})
                for item in self.categories[filterid]:
                    filter_terms.append(item)
                    keywords_by_filter.append({'title': item,
                                               'value': item,
                                               'header': False,
                                               'checked': item in checked})

        total = set(terms)
        existents = set(filter_terms)
        altres = set(existents).symmetric_difference(set(total))
        if altres:
            altres = list(altres)
            altres.sort()
            keywords_by_filter.append({'title': 'Altres',
                                       'value': 'altres',
                                       'header':  True})
            for item in altres:
                keywords_by_filter.append({'title': item,
                                           'value': item,
                                           'header': False,
                                           'checked': item in checked})
        return keywords_by_filter
