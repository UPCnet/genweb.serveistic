# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import implements
from zope.formlib import form

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _


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

    def js_retrieve(self):
        return """
    $(document).ready(function()
    {{
        var url = '{url}';
        var count = {count};
        retrieve_problemes(url, count);
    }});
       """.format(
            url="retrieve_problemes",
            count=self.data.count)


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
