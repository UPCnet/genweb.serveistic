from five import grok
from plone import api
from zope.interface import Interface
from genweb.serveistic.interfaces import IGenwebServeisticLayer
from Products.CMFCore.utils import getToolByName
from plone.batching import Batch
order_by_type = {"Folder": 1, "Document": 2, "File": 3, "Link": 4, "Image": 5}


class FilteredContentsSearchView(grok.View):
    """ Filtered content search view for every folder. """
    grok.name('filtered_contents_search_view')
    grok.context(Interface)
    grok.require('genweb.member')
    grok.template('filtered_contents_search_stic')
    grok.layer(IGenwebServeisticLayer)

    def update(self):
        self.query = self.request.form.get('q', '')
        if self.request.form.get('t', ''):
            self.tags = [v for v in self.request.form.get('t').split(',')]
        else:
            self.tags = []

    def get_batched_contenttags(self, query=None, batch=True, b_size=10, b_start=0):
        pc = getToolByName(self.context, "portal_catalog")
        path = self.context.getPhysicalPath()
        path = "/".join(path)
        r_results = pc.searchResults(path=path,
                                     sort_on='sortable_title',
                                     sort_order='ascending')

        items_favorites = self.marca_favoritos(r_results)
        items_nofavorites = self.exclude_favoritos(r_results)

        items = self.ordenar_results(items_favorites, items_nofavorites)

        batch = Batch(items, b_size, b_start)
        return batch

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
                                             Subject={'query': self.tags, 'operator': 'and'},
                                             sort_on='sortable_title',
                                             sort_order='ascending')
            else:
                r_results = pc.searchResults(path=path,
                                             SearchableText=query,
                                             sort_on='sortable_title',
                                             sort_order='ascending')

            items_favorites = self.marca_favoritos(r_results)
            items_nofavorites = self.exclude_favoritos(r_results)

            items = self.ordenar_results(items_favorites, items_nofavorites)

            return items
        else:
            r_results = pc.searchResults(path=path,
                                         Subject={'query': self.tags, 'operator': 'and'},
                                         sort_on='sortable_title',
                                         sort_order='ascending')

            items_favorites = self.marca_favoritos(r_results)
            items_nofavorites = self.exclude_favoritos(r_results)

            items = self.ordenar_results(items_favorites, items_nofavorites)

            return items

    def get_tags_by_query(self):
        pc = getToolByName(self.context, "portal_catalog")

        def quotestring(s):
            return '"%s"' % s

        def quote_bad_chars(s):
            bad_chars = ["(", ")"]
            for char in bad_chars:
                s = s.replace(char, quotestring(char))
            return s

        if not self.query == '':
            multispace = u'\u3000'.encode('utf-8')
            for char in ('?', '-', '+', '*', multispace):
                self.query = self.query.replace(char, ' ')

            query = self.query.split()
            query = " AND ".join(query)
            query = quote_bad_chars(query)
            path = self.context.absolute_url_path()

            r_results = pc.searchResults(path=path,
                                         Subject=query,
                                         sort_on='sortable_title',
                                         sort_order='ascending')

            items_favorites = self.marca_favoritos(r_results)
            items_nofavorites = self.exclude_favoritos(r_results)

            items = self.ordenar_results(items_favorites, items_nofavorites)

            return items
        else:
            return self.get_batched_contenttags(query=None, batch=True, b_size=10, b_start=0)

    def get_container_path(self):
        return self.context.absolute_url()

    def getContent(self):
        portal = api.portal.get()
        catalog = getToolByName(portal, 'portal_catalog')
        path = self.context.getPhysicalPath()
        path = "/".join(path)

        r_results_parent = catalog.searchResults(path={'query': path, 'depth': 1},
                                                 sort_on='sortable_title',
                                                 sort_order='ascending')

        items_favorites = self.favorites_items(path)
        items_nofavorites = self.exclude_favoritos(r_results_parent)

        items = self.ordenar_results(items_favorites, items_nofavorites)

        return items


class SearchFilteredContentAjax(FilteredContentsSearchView):
    """ Ajax helper for filtered content search view for every folder. """
    grok.name('search_filtered_content_stic')
    grok.context(Interface)
    grok.template('filtered_contents_search_ajax_stic')
    grok.layer(IGenwebServeisticLayer)
