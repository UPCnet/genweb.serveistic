# -*- coding: utf-8 -*-

from five import grok
from Products.CMFCore.utils import getToolByName

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.data_access.notificacio import NotificacioDataReporter
from genweb.serveistic.utilities import get_servei


class NotificacioViewHelper(object):
    def get_awesome_icon_class(self, notificacio):
        if notificacio["tipus"] == u"Avís":
            return "fa fa-warning"
        elif notificacio["tipus"] == u"Notificació":
            return "fa fa-info"
        elif notificacio["tipus"] == u"Novetat":
            return "fa fa-exclamation-circle"
        else:
            return ""


class Notificacions(grok.View, NotificacioViewHelper):
    grok.name('notificacions_list')
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('notificacions')

    @property
    def notificacions(self):
        reporter = NotificacioDataReporter(
            getToolByName(self.context, 'portal_catalog'))
        return reporter.list_by_servei(get_servei(self))
