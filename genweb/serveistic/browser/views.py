from five import grok
from plone import api
from zope.interface import Interface
from genweb.serveistic.interfaces import IGenwebServeisticLayer
from Products.CMFCore.utils import getToolByName
from genweb.theme.browser.views import HomePageBase
from genweb.theme.browser.interfaces import IHomePageView
from plone.app.layout.navigation.interfaces import INavigationRoot

order_by_type = {"Folder": 1, "Document": 2, "File": 3, "Link": 4, "Image": 5}


class FilteredContentsSearchView(HomePageBase):
    """ Filtered content search view for every folder. """
    grok.name('homepage')
    grok.implements(IHomePageView)
    grok.context(INavigationRoot)
    grok.template('filtered_contents_search_stic')
    grok.layer(IGenwebServeisticLayer)

    def update(self):
        self.query = self.request.form.get('q', '')
        if self.request.form.get('t', ''):
            self.tags = [v for v in self.request.form.get('t').split(',')]
        else:
            self.tags = []

    def get_contenttags_by_query(self):
        pc = getToolByName(self.context, "portal_catalog")
        path = self.context.getPhysicalPath()
        path = "/".join(path)

        def quotestring(s):
            return '"%s"' % s

        def quote_bad_chars(s):
            bad_chars = ["(", ")"]
            for char in bad_chars:
                s = s.replace(char, quotestring(char))
            return s

        if not self.query and not self.tags:
            return self.getContent()

        if not self.query == '':
            multispace = u'\u3000'.encode('utf-8')
            for char in ('?', '-', '+', '*', multispace):
                self.query = self.query.replace(char, ' ')

            query = self.query.split()
            query = " AND ".join(query)
            query = quote_bad_chars(query) + '*'

            if self.tags:
                r_results = pc.searchResults(path=path,
                                             SearchableText=query,
                                             Subject={'query': self.tags,
                                                      'operator': 'and'},
                                             sort_on='sortable_title',
                                             sort_order='ascending')
            else:
                r_results = pc.searchResults(path=path,
                                             SearchableText=query,
                                             sort_on='sortable_title',
                                             sort_order='ascending')

            items = [{'obj': r} for r in r_results]
            return items

        else:
            r_results = pc.searchResults(path=path,
                                         Subject={'query': self.tags,
                                                  'operator': 'and'},
                                         sort_on='sortable_title',
                                         sort_order='ascending',
                                         portal_type='serveitic')

            items = [{'obj': r} for r in r_results]
            return items

    def get_container_path(self):
        return self.context.absolute_url()

    def getContent(self):
        portal = api.portal.get()
        catalog = getToolByName(portal, 'portal_catalog')
        path = self.context.getPhysicalPath()
        path = "/".join(path)

        r_results_parent = catalog.searchResults(portal_type='serveitic',
                                                 path={'query': path,
                                                       'depth': 1},
                                                 sort_on='sortable_title',
                                                 sort_order='ascending')

        items = [{'obj': r} for r in r_results_parent]
        return items


class SearchFilteredContentAjax(FilteredContentsSearchView):
    """ Ajax helper for filtered content search view for every folder. """
    grok.name('search_filtered_content_stic')
    grok.context(Interface)
    grok.template('filtered_contents_search_ajax_stic')
    grok.layer(IGenwebServeisticLayer)
