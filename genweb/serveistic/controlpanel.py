# -*- coding: utf-8 -*-


from zope import schema
from plone.supermodel import model
from plone.directives import form
from plone.app.registry.browser import controlpanel
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from z3c.form import button
from Products.statusmessages.interfaces import IStatusMessage

from genweb.core import GenwebMessageFactory as _


class ITableFacetes(form.Schema):
    faceta = schema.Choice(
        title=_(u'Faceta'),
        vocabulary='genweb.serveistic.vocabularies.facets',
        required=False)
    valor = schema.TextLine(
        title=_(u'Valor'),
        required=False)


class IServeisTICControlPanelSettings(model.Schema):
    """ Global Genweb settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    model.fieldset(
        'Servei Web Problemes',
        _(u'Servei Web Problemes'),
        fields=['ws_endpoint', 'ws_login_username', 'ws_login_password'])

    ws_endpoint = schema.TextLine(
        title=_(u'URL'),
        required=False)

    ws_login_username = schema.TextLine(
        title=_(u'Usuari'),
        required=False)

    ws_login_password = schema.TextLine(
        title=_(u'Contrasenya'),
        required=False)

    model.fieldset('Facetes', _(u'Facetes'), fields=['facetes_table'])
    form.widget(facetes_table=DataGridFieldFactory)
    facetes_table = schema.List(
        title=_(u'Facetes'),
        description=_(
            u'help_facetes_table',
            default=u'Afegir els valors per facetes de cerca'),
        value_type=DictRow(
            title=_(u'help_facetes_table'),
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
