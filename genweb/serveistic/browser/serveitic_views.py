# -*- coding: utf-8 -*-

from five import grok

from plone.dexterity.utils import createContentInContainer
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from zope.app.container.interfaces import IObjectAddedEvent
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides

from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from genweb.theme.browser.interfaces import IHomePageView
from genweb.theme.browser.views import HomePageBase
from genweb.banners.portlets.bannersportlet import Assignment \
    as GenwebBannersAssignment

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.content.serveitic import IInitializedServeiTIC
from genweb.serveistic.portlets.bannersportlet import Assignment as \
    BannersAssignment
from genweb.serveistic.portlets.notificacions_tic import Assignment as \
    NotificacionsAssignment
from genweb.serveistic.portlets.problemes import Assignment as \
    ProblemesAssignment
from genweb.serveistic.data.folder_structure import folder_structure


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


@grok.subscribe(IServeiTIC, IObjectAddedEvent)
def initialize_servei(serveitic, event):
    # Configure portlets
    assignments = get_portlet_assignments(
        serveitic, 'plone.leftcolumn')
    assignments['banners'] = GenwebBannersAssignment()
    assignments['banners_serveistic'] = BannersAssignment()

    assignments = get_portlet_assignments(
        serveitic, 'genweb.portlets.HomePortletManager3')
    assignments['notificacions'] = NotificacionsAssignment()

    assignments = get_portlet_assignments(
        serveitic, 'genweb.portlets.HomePortletManager4')
    assignments['problemes'] = ProblemesAssignment()

    # Create folder structure
    for folder_data in folder_structure:
        folder = createContentInContainer(
            serveitic,
            folder_data[1],
            title=folder_data[0],
            checkConstraints=False,
            exclude_from_nav=folder_data[2])
        for folder_content in folder_data[4]:
            content = createContentInContainer(
                folder,
                folder_content[1],
                title=folder_content[0],
                checkConstraints=False,
                exclude_from_nav=folder_content[2],
                allow_discussion=folder_content[3])
            if len(folder_content) > 4:
                behavior = ISelectableConstrainTypes(content)
                behavior.setConstrainTypesMode(1)
                behavior.setLocallyAllowedTypes(folder_content[4])
                behavior.setImmediatelyAddableTypes(folder_content[4])
        behavior = ISelectableConstrainTypes(folder)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(folder_data[3])
        behavior.setImmediatelyAddableTypes(folder_data[3])
        folder.reindexObject()

    # Mark ServeiTIC as initialized to prevent previous folder creations from
    # triggering the modify event
    alsoProvides(serveitic, IInitializedServeiTIC)
