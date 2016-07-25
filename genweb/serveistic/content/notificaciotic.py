# -*- coding: utf-8 -*-

from five import grok
from zope import schema
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from z3c.form import interfaces
from plone.directives import form, dexterity
from plone.dexterity.content import Item
from plone.app.textfield import RichText
from Products.CMFPlone import PloneMessageFactory as _

from genweb.serveistic.utilities import build_vocabulary, get_servei


tipus_values = [u"Avís", u"Notificació", u"Novetat"]


class INotificacioTIC(form.Schema):
    title = schema.TextLine(
        title=_(u"Títol"),
        required=True)

    description = schema.Text(
        title=_(u"Descripció"),
        required=False,
    )

    cos = RichText(
        title=_(u"Cos de la notificació"),
        required=True,
    )

    tipus = schema.Choice(
        title=_(u'Tipus de notificació'),
        required=True,
        vocabulary=SimpleVocabulary(build_vocabulary(tipus_values)))

    is_general = schema.Bool(
        title=_(u"Fes que aparegui a la pàgina d'inici"),
        description=_(u"Marca la caixa si vols que la notificació aparegui "
                      u"també a la pàgina d'inici"),
        required=False)


class AddForm(dexterity.AddForm):
    grok.name('notificaciotic')
    grok.context(INotificacioTIC)

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        if not get_servei(self):
            self.widgets['is_general'].mode = interfaces.HIDDEN_MODE
            self.widgets['is_general'].value = True


class Edit(dexterity.EditForm):
    grok.context(INotificacioTIC)

    def updateWidgets(self):
        super(Edit, self).updateWidgets()
        if not get_servei(self):
            self.widgets['is_general'].mode = interfaces.HIDDEN_MODE


class NotificacioTIC(Item):
    implements(INotificacioTIC)
