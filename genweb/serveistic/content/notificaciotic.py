# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from plone.directives import form
from plone.dexterity.content import Item
from Products.CMFPlone import PloneMessageFactory as _

from genweb.serveistic.utilities import build_vocabulary


tipus_values = [u"Avís", u"Notificació", u"Novetat"]


class INotificacioTIC(form.Schema):
    """ Tipus notificacio TIC
    """

    text = schema.Text(
        title=_(u"Cos de la notificació"),
        required=True,
    )

    tipus = schema.Choice(
        title=_(u'Tipus de notificació'),
        required=True,
        vocabulary=SimpleVocabulary(build_vocabulary(tipus_values)))


class NotificacioTIC(Item):
    implements(INotificacioTIC)
