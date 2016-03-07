# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import implements
from plone.directives import form
from plone.dexterity.content import Item
from Products.CMFPlone import PloneMessageFactory as _


class IProblema(form.Schema):
    title = schema.TextLine(
        title=_(u"Assumpte"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Descripció"),
        required=False,
    )

    data_creacio = schema.Date(
        title=_(u"Data de creació"),
        required=False,
    )

    url = schema.TextLine(
        title=_(u"URL"),
        description=_(
            u"Direcció URL amb informació addicional sobre el problema"),
        required=False)

    data_resolucio = schema.Date(
        title=_(u"Data estimada de resolució"),
        required=False,
    )


class Problema(Item):
    implements(IProblema)
