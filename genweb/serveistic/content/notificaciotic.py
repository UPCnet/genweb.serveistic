# -*- coding: utf-8 -*-

from five import grok

from zope import schema
from plone.directives import form
from Products.CMFPlone import PloneMessageFactory as _

from DateTime import DateTime


from plone.directives import dexterity

from zope.interface import implements
from plone.dexterity.content import Item

from genweb.serveistic.interfaces import IGenwebServeisticLayer

from genweb.theme.browser.interfaces import IHomePageView
from genweb.theme.browser.views import HomePageBase


from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

tipus_not = SimpleVocabulary(
    [SimpleTerm(value=u'avis', title=_(u'Avís')),
     SimpleTerm(value=u'notificacio', title=_(u'Notificació')),
     SimpleTerm(value=u'novetat', title=_(u'Novetat'))]
)


class INotificacioTIC(form.Schema):
    """ Tipus notificacio TIC
    """

    text = schema.Text(
        title=_(u"Cos de la notificació"),
        description=_(u''),
        required=True,
    )

    tipus = schema.Choice(
        title=_(u'Tipus de notificació'),
        description=_(u''),
        required=True,
        vocabulary=tipus_not,
    )


class View(dexterity.DisplayForm):
    grok.context(INotificacioTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('notificaciotic_view')

    def retNotificacions(self):
        """ retorna les dades necessaries de les notificacions del portal per
            pintar-les a la columna dreta
        """
        resultats = []
        notificacions = self.catalog.searchResults(portal_type='notificaciotic', sort_on='effective', sort_order='reverse', review_state='internally_published')
        for notificacio in notificacions:
            data = DateTime(notificacio.effective).strftime('%d/%m/%Y')
            dades_not = {"data": data, "titol": notificacio.Title, "desc": notificacio.Description, "url": notificacio.getURL(), "tipus": notificacio.tipus}
            resultats.append(dades_not)
        return resultats


class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(INotificacioTIC)


class NotificacioTIC(Item):
    implements(INotificacioTIC)
