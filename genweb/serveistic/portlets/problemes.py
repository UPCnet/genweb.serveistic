# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.formlib import form

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

from genweb.serveistic.utilities import get_servei


class IProblemesPortlet(IPortletDataProvider):
    pass


class Assignment(base.Assignment):
    implements(IProblemesPortlet)

    def __init__(self, count=5, showdata=True):
        self.count = count
        self.showdata = showdata

    @property
    def title(self):
        return _(u"Problemes")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/problemes.pt')

    @property
    def problemes(self):
        return [
            {'data': '14/02/2016', 'url': '/url1/', 'titol': 'Problema 1'},
            {'data': '21/11/2015', 'url': '/url2/', 'titol': 'Problema 2'},
            ]

    @property
    def problemes_href(self):
        return "/".join(get_servei(self).getPhysicalPath()) + '/problemes'


class AddForm(base.AddForm):
        form_fields = form.Fields(IProblemesPortlet)
        label = _(u"Afegeix portlet de problemes")
        description = _(u"Llistat de problemes associats a un Servei TIC")

        def create(self, data):
            return Assignment(
                count=data.get('count', 5),
                showdata=data.get('showdata', True))


class EditForm(base.EditForm):
    form_fields = form.Fields(IProblemesPortlet)
    label = _(u"Edita el portlet de problemes")
    description = _(u"Llistat de problemes associats a un Servei TIC")
