# -*- coding: utf-8 -*-
from zope.interface import implements
from plone import api
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from souper.soup import get_soup
from genweb.core.utils import pref_lang

from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from zope.formlib import form
from zope import schema

import requests


class IBannersPortlet(IPortletDataProvider):
    """ A portlet which can show actived.
    """

    root = schema.Choice(
            title=_(u"label_navigation_root_path", default=u"Root node"),
            description=_(u'help_navigation_root',
                          default=u"You may search for and choose a folder "
                                   "to act as the root of the navigation tree. "
                                   "Leave blank to use the Plone site root."),
            required=True,
            source=SearchableTextSourceBinder({'is_folderish': True},
                                              default_query='path:/portlets'))


class Assignment(base.Assignment):
    implements(IBannersPortlet)

    title = _(u'label_banner_serveis', default=u'Blanquerna Banner Serveis')
    root = None

    def __init__(self, root=None):
        self.root = root


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('templates/bannersportlet.pt')

    def getServices(self):
        """ return list of user service to show in portlet """
        resul = []
        portal = api.portal.get()
        path_portlet = "/".join(portal.getPhysicalPath()) + self.data.root
        catalog = getToolByName(portal, 'portal_catalog')
        records = catalog.searchResults(portal_type='Services',
                                        path={'query': path_portlet},
                                        sort_on='getObjPositionInParent')

        for record in records:
            import ipdb;ipdb.set_trace()
            resul.append({'url': record[1].attrs['url'],
                          'imgUrl': record[1].attrs['url']
                          })

        return resul


class AddForm(base.AddForm):
    form_fields = form.Fields(IBannersPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Edit Banner Portlet")
    description = _(u"This portlet displays banners in folder.")

    def create(self, data):
        return Assignment(root=data.get('root', ""))


class EditForm(base.EditForm):
    form_fields = form.Fields(IBannersPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Edit banner Portlet")
    description = _(u"This portlet displays banners in folder.")
