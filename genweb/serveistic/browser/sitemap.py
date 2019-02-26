from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.interface import implements

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFPlone.browser.interfaces import ISitemapView


class SitemapView(BrowserView):
    implements(ISitemapView)

    item_template = ViewPageTemplateFile('templates/sitemap-item.pt')

    def createSiteMap(self):
        context = aq_inner(self.context)
        view = getMultiAdapter((context, self.request),
                               name='sitemap_builder_view')
        data = view.siteMap()
        return self._renderLevel(children=data.get('children', []))

    def _renderLevel(self, children=[]):
        output = ''
        for node in children:
            output += '<li class="navTreeItem visualNoMarker">\n'
            output += self.item_template(node=node)
            output += '</li>\n'

        return output