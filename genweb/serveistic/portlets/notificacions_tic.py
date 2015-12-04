#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Acquisition import aq_inner
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

    def retNotificacions(self):
        """ retorna les dades necessaries de les notificacions del portal per
            pintar-les al portlet
        """
        lang = pref_lang()
        resultats = []
        notificacions = self.catalog.searchResults(portal_type='notificaciotic',
                                                   sort_on='effective',
                                                   lang=lang,
                                                   sort_order='reverse',
                                                   review_state='published')
        for notificacio in notificacions:
            data = DateTime(notificacio.effective).strftime('%d/%m/%Y')
            dades_not = {"data": data,
                         "titol": notificacio.Title,
                         "desc": notificacio.Description,
                         "url": notificacio.getURL(),
                         "tipus": notificacio.tipus}
            resultats.append(dades_not)
        return resultats


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
