# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import implements
from zope.formlib import form

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _


class IIndicadorsPortlet(IPortletDataProvider):
    count = schema.Int(
        title=_(u"Nombre màxim d'indicadors"),
        required=True,
        defaultFactory=lambda: 5)

    count_category = schema.Int(
        title=_(u"Nombre màxim de categories"),
        required=False,
        defaultFactory=lambda: None)


class Assignment(base.Assignment):
    implements(IIndicadorsPortlet)

    def __init__(self, count=5, count_category=None, showdata=True):
        self.count = count
        self.count_category = count_category
        self.showdata = showdata

    @property
    def title(self):
        return _(u"Indicadors")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/indicadors.pt')

    def js_retrieve(self):
        return """
    $(document).ready(function()
    {{
        var url = '{url}';
        var count = {count};
        var count_category = {count_category};
        retrieve_indicadors(url, count, count_category);
    }});
       """.format(
            url="retrieve_indicadors",
            count=self.data.count,
            count_category=self.data.count_category
            if self.data.count_category else "''")


class AddForm(base.AddForm):
        form_fields = form.Fields(IIndicadorsPortlet)
        label = _(u"Afegeix portlet d'indicadors")
        description = _(u"Llistat d'indicadors associats a un Servei TIC")

        def create(self, data):
            return Assignment(
                count=data.get('count', 5),
                count_category=data.get('count_category', None),
                showdata=data.get('showdata', True))


class EditForm(base.EditForm):
    form_fields = form.Fields(IIndicadorsPortlet)
    label = _(u"Edita el portlet d'indicadors")
    description = _(u"Llistat d'indicadors associats amb un Servei TIC")
