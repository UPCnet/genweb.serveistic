# -*- coding: utf-8 -*-

import unicodedata

from zope import schema
from plone.supermodel import model

from genweb.core import GenwebMessageFactory as _

from plone.directives import form
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow

from plone.app.registry.browser import controlpanel

from z3c.form import button
from Products.statusmessages.interfaces import IStatusMessage
from five import grok
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


class ITableTitleFaceta(form.Schema):
    faceta = schema.TextLine(title=_(u'Títol faceta'),
             required=False)


class getFacetesTitles(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IServeisTICControlPanelSettings, check=False)
        items = []

        if settings.title_faceta_table is not None:
            for item in settings.title_faceta_table:
                token = unicodedata.normalize('NFKD', item['faceta']).encode('ascii', 'ignore').lower()
                items.append(SimpleVocabulary.createTerm(
                    item['faceta'],
                    token,
                    item['faceta'],))
        return SimpleVocabulary(items)

grok.global_utility(getFacetesTitles, name="availableTitleFacetes")


class ITableFacetes(form.Schema):
    faceta = schema.Choice(title=_(u'Faceta'),
             vocabulary='availableTitleFacetes',
             required=False)
    valor = schema.TextLine(title=_(u'Valor'),
        required=False)


class IServeisTICControlPanelSettings(model.Schema):
    """ Global Genweb settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    model.fieldset('Facetes',
                  _(u'Facetes'),
                  fields=['title_faceta_table', 'facetes_table'])

    form.widget(title_faceta_table=DataGridFieldFactory)
    title_faceta_table = schema.List(title=_(u'Faceta'),
                                description=_(u'desc_title_faceta_table',
                                       default=u'Afegir títol de facetes'),
                                value_type=DictRow(title=_(u'help_facetes_table'),
                                                   schema=ITableTitleFaceta),
                                required=False
                                     )

    form.widget(facetes_table=DataGridFieldFactory)
    facetes_table = schema.List(title=_(u'Facetes'),
                                description=_(u'help_facetes_table',
                                       default=u'Afegir els valors per facetes de cerca'),
                                value_type=DictRow(title=_(u'help_facetes_table'),
                                                   schema=ITableFacetes),
                                required=False
                                )


class ServeisTICControlPanelSettingsForm(controlpanel.RegistryEditForm):

    schema = IServeisTICControlPanelSettings
    id = 'ServeisTICControlPanelSettingsForm'
    label = _(u'Genweb ServeisTIC settings')
    description = _(u'help_serveistic_settings_editform',
                    default=u'ServeisTIC configuration.')

    def updateFields(self):
        super(ServeisTICControlPanelSettingsForm, self).updateFields()

    def updateWidgets(self):
        super(ServeisTICControlPanelSettingsForm, self).updateWidgets()

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u'Changes saved'),
                                                      'info')
        self.context.REQUEST.RESPONSE.redirect('@@serveistic-controlpanel')

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u'Edit cancelled'),
                                                      'info')
        self.request.response.redirect('%s/%s' % (self.context.absolute_url(),
                                                 self.control_panel_view))


class ServeisTICControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ServeisTICControlPanelSettingsForm
