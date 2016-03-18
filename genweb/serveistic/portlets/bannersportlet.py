# -*- coding: utf-8 -*-
from zope.interface import implements
from plone import api
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

from genweb.serveistic.utilities import get_servei
from genweb.serveistic.data_access.banner import BannerDataReporter


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
        reporter = BannerDataReporter(
            getToolByName(api.portal.get(), 'portal_catalog'))
        return reporter.list_by_servei(get_servei(self))

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
