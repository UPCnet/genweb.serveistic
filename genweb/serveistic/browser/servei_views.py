# -*- coding: utf-8 -*-

from five import grok

from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.dexterity.utils import createContentInContainer
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

from zope.app.container.interfaces import IObjectAddedEvent
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import alsoProvides

from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from genweb.theme.browser.interfaces import IHomePageView
from genweb.theme.browser.views import HomePageBase

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.content.serveitic import IInitializedServeiTIC
from genweb.serveistic.portlets.bannersportlet import Assignment as \
    BannersAssignment
from genweb.serveistic.portlets.notificacions import Assignment as \
    NotificacionsAssignment
from genweb.serveistic.portlets.problemes import Assignment as \
    ProblemesAssignment
from genweb.serveistic.portlets.indicadors import Assignment as \
    IndicadorsAssignment
from genweb.serveistic.data.folder_structure import folder_structure

import unicodedata


class View(HomePageBase):
    grok.implements(IHomePageView)
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)

    @property
    def descripcio(self):
        return self.context.serveiDescription.raw \
            if self.context.serveiDescription else ""


def get_portlet_assignments(context, name):
    portlet_manager = queryUtility(
        IPortletManager,
        name=name,
        context=context)
    return getMultiAdapter(
        (context, portlet_manager), IPortletAssignmentMapping)


def createContentInFolder(folder_directori, folder_content):
    # Create content
    if folder_content[1] != "Folder":
        content_props = {
            'title': folder_content[0],
            'checkConstraints': False,
            'exclude_from_nav': folder_content[2],
            'allow_discussion': folder_content[3]}
        if folder_content[6] is not None:
            content_props['description'] = folder_content[6]
        if folder_content[7] is not None:
            content_props['text'] = IRichText['text'].fromUnicode(folder_content[7])
        if folder_content[5] is not None:
            content_props['layout'] = folder_content[5]
        content = createContentInContainer(
            folder_directori, folder_content[1], **content_props)
        if folder_content[4] is not None:
            behavior = ISelectableConstrainTypes(content)
            behavior.setConstrainTypesMode(1)
            behavior.setLocallyAllowedTypes(folder_content[4])
            behavior.setImmediatelyAddableTypes(folder_content[4])
    else:
        createFolderAndContents(folder_directori, folder_content)


def createFolderAndContents(folder_directori, folder_data):
    # Create folder
    folder_props = {
        'title': folder_data[0],
        'checkConstraints': False,
        'exclude_from_nav': folder_data[2],
        'allow_discussion': folder_data[3]}
    if folder_data[5] is not None:
        folder_props['layout'] = folder_data[5]
    folder = createContentInContainer(folder_directori, folder_data[1], **folder_props)

    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(folder_data[4])
    behavior.setImmediatelyAddableTypes(folder_data[4])
    folder.reindexObject()

    # Create a contents
    for folder_content in folder_data[7]:
        createContentInFolder(folder, folder_content)

    if folder_data[6] is not None:
        folder.setDefaultPage(folder_data[6])


@grok.subscribe(IServeiTIC, IObjectAddedEvent)
def initialize_servei(serveitic, event):
    # If it is a copy do not execute
    if 'copy_of_' in event.newName:
        return

    # Configure portlets
    assignments = get_portlet_assignments(
        serveitic, 'plone.leftcolumn')
    if 'banners_global' not in assignments:
        assignments['banners_global'] = BannersAssignment(banner_type=u"Global")
    if 'banners_local' not in assignments:
        assignments['banners_local'] = BannersAssignment(banner_type=u"Local")

    assignments = get_portlet_assignments(
        serveitic, 'genweb.portlets.HomePortletManager3')
    if 'notificacions' not in assignments:
        assignments['notificacions'] = NotificacionsAssignment()

    assignments = get_portlet_assignments(
        serveitic, 'genweb.portlets.HomePortletManager4')
    if 'problemes' not in assignments:
        assignments['problemes'] = ProblemesAssignment()

    assignments = get_portlet_assignments(
        serveitic, 'genweb.portlets.HomePortletManager5')
    if 'indicadors' not in assignments:
        assignments['indicadors'] = IndicadorsAssignment()

    # Create folder structure
    normalizer = getUtility(IIDNormalizer)
    for folder_data in folder_structure:
        try:
            if isinstance(folder_data[0], str):
                flattened = unicodedata.normalize('NFKD', folder_data[0].decode('utf-8')).encode('ascii', errors='ignore')
            else:
                flattened = unicodedata.normalize('NFKD', folder_data[0]).encode('ascii', errors='ignore')

            if normalizer.normalize(flattened) not in serveitic:
                createFolderAndContents(serveitic, folder_data)
        except:
            createFolderAndContents(serveitic, folder_data)

    # Mark ServeiTIC as initialized to prevent previous folder creations from
    # triggering the modify event
    alsoProvides(serveitic, IInitializedServeiTIC)

    # Facetas
    serveitic.es_faceta_1 = serveitic.ca_faceta_1
    serveitic.en_faceta_1 = serveitic.ca_faceta_1

    serveitic.es_faceta_2 = serveitic.ca_faceta_2
    serveitic.en_faceta_2 = serveitic.ca_faceta_2

    serveitic.es_faceta_3 = serveitic.ca_faceta_3
    serveitic.en_faceta_3 = serveitic.ca_faceta_3

    serveitic.es_faceta_4 = serveitic.ca_faceta_4
    serveitic.en_faceta_4 = serveitic.ca_faceta_4

    serveitic.es_faceta_5 = serveitic.ca_faceta_5
    serveitic.en_faceta_5 = serveitic.ca_faceta_5

    serveitic.es_faceta_6 = serveitic.ca_faceta_6
    serveitic.en_faceta_6 = serveitic.ca_faceta_6

    serveitic.es_faceta_7 = serveitic.ca_faceta_7
    serveitic.en_faceta_7 = serveitic.ca_faceta_7

    serveitic.es_faceta_8 = serveitic.ca_faceta_8
    serveitic.en_faceta_8 = serveitic.ca_faceta_8

    serveitic.reindexObject()
