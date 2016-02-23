# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import implements
from zope.formlib import form

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

from genweb.serveistic.utilities import get_servei
from genweb.serveistic.data_access.notificacio import NotificacioDataReporter


class INotificationsPortlet(IPortletDataProvider):
    count = schema.Int(
        title=_(u'Nombre màxim de notificacions'),
        required=True,
        defaultFactory=lambda: 5)


class Assignment(base.Assignment):
    implements(INotificationsPortlet)

    def __init__(self, count=5, showdata=True):
        self.count = count
        self.showdata = showdata

    @property
    def title(self):
        return _(u"Notificacions TIC")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/notificacions_tic.pt')

    @property
    def notificacions(self):
        """
        Retorna les dades necessaries de les notificacions del portal per
        pintar-les al portlet
        """
        reporter = NotificacioDataReporter(
            getToolByName(self.context, 'portal_catalog'))
        return reporter.list_by_servei(get_servei(self), self.data.count)

    @property
    def notificacions_href(self):
        servei = get_servei(self)
        path = servei.getPhysicalPath()
        path = "/".join(path)
        notificacio_folder = path + '/notificacions'
        return notificacio_folder


class AddForm(base.AddForm):
        form_fields = form.Fields(INotificationsPortlet)
        label = _(u"Afegeix portlet de notifications")
        description = _(u"Aquest portlet mostra les notificacions")

        def create(self, data):
            return Assignment(
                count=data.get('count', 5),
                showdata=data.get('showdata', True))


class EditForm(base.EditForm):
    form_fields = form.Fields(INotificationsPortlet)
    label = _(u"Edita el portlet de notificacions")
    description = _(u"Aquest portlet mostra les notificacions d'un servei TIC")
