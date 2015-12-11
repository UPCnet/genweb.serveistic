# -*- coding: utf-8 -*-
from zope.interface import implements
from plone import api
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _


class IBannersPortlet(IPortletDataProvider):
    """ A portlet which can show actived.
    """


class Assignment(base.Assignment):
    implements(IBannersPortlet)

    title = _(u'label_banner_serveis', default=u'Serveis Tic Banners')


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('templates/bannersportlet.pt')

    def portal_url(self):
        return self.portal().absolute_url()

    def portal(self):
        return api.portal.get()

    def getBanners(self):
        """ return list of user service to show in portlet """

        portal = api.portal.get()
        path_portlet = "/".join(self.context.getPhysicalPath()) + '/banners'
        catalog = getToolByName(portal, 'portal_catalog')
        return catalog.searchResults(portal_type='Banner',
                                     review_state=['published', 'intranet'],
                                     path={'query': path_portlet},
                                     sort_on='getObjPositionInParent')

    def getAltAndTitle(self, altortitle, open_in_new_window):
        """ Funcio que extreu idioma actiu i afegeix al alt i al title de les imatges del banner
            el literal Obriu l'enllac en una finestra nova.
        """
        if open_in_new_window:
            return '%s, %s' % (altortitle.decode('utf-8'), self.portal().translate(_('obrir_link_finestra_nova', default=u"(obriu en una finestra nova)")))
        else:
            return '%s' % (altortitle.decode('utf-8'))


class AddForm(base.AddForm):
    form_fields = []

    def create(self, data):
        return Assignment()
