#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Acquisition import aq_inner, aq_chain
from plone import api
from zope import schema
from zope.interface import implements
from zope.formlib import form

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

from genweb.core.utils import pref_lang

from DateTime.DateTime import DateTime
from genweb.serveistic.utilities import get_servei
from genweb.serveistic.content.serveitic import IServeiTIC


class INotificationsPortlet(IPortletDataProvider):
    """A portlet which can render a list of notificacions.
    """


class Assignment (base.Assignment):
    implements(INotificationsPortlet)

    def __init__(self, count=5, showdata=True):
        self.count = count
        self.showdata = showdata

    @property
    def title(self):
        return _(u"Notificacions TIC")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/notificacions_tic.pt')

    # def get_servei(self):
    #     context = aq_inner(self.context)
    #     for obj in aq_chain(context):
    #         if IServeiTIC.providedBy(obj):
    #             return obj
    #     return None

    def retNotificacions(self):
        """retorna les dades necessaries de les notificacions del portal per pintar-les al portlet"""
        lang = pref_lang()
        resultats = []
        pc = getToolByName(self.context, 'portal_catalog')
        notificacions = pc.searchResults(portal_type='notificaciotic',
                                         sort_on='effective',
                                         lang=lang,
                                         sort_order='reverse',
                                         review_state='published')
        for notificacio in notificacions:
            data = DateTime(notificacio.effective).strftime('%d/%m/%Y')
            not_tip = notificacio.getObject()
            dades_not = {"data": data,
                         "titol": notificacio.Title,
                         "desc": notificacio.Description,
                         "url": notificacio.getURL(),
                         "tipus": not_tip.tipus}
            resultats.append(dades_not)
        return resultats

    def getNotifFolder(self):
        servei = get_servei(self)
        path = servei.getPhysicalPath()
        path = "/".join(path)
        notificacio_folder = path + '/notificacions'
        return notificacio_folder


class AddForm(base.AddForm):
        form_fields = form.Fields(INotificationsPortlet)
        label = _(u"Add Notifications portlet")
        description = _(u"Aquest portlet mostra les notificacions")

        def create(self, data):
            return Assignment(count=data.get('count', 5), showdata=data.get('showdata', True))


class EditForm(base.EditForm):
    form_fields = form.Fields(INotificationsPortlet)
    label = _(u"Edit Notificactions Portlet")
    description = _(u"This portlet displays recent Notifications Items.")
