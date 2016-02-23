# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import implements
from zope.formlib import form

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

from genweb.serveistic.utilities import get_servei


class IProblemesPortlet(IPortletDataProvider):
    count = schema.Int(
        title=_(u'Nombre màxim de problemes'),
        required=True,
        defaultFactory=lambda: 5)


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
    def product_id(self):
        serveitic = get_servei(self)
        return serveitic.product_id if serveitic.product_id else ''

    @property
    def count(self):
        return self.data.count

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
    description = _(u"Llistat de problemes associats amb un Servei TIC")
