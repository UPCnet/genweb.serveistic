# -*- coding: utf-8 -*-
from five import grok
from plone.directives import dexterity

from zope import schema
from plone.directives import form
from plone.namedfile.file import NamedBlobImage
from plone.app.textfield import RichText

from genweb.serveistic import _

from zope.interface import implements
from plone.dexterity.content import Item

from plone.app.users.userdataschema import checkEmailAddress
from zope.app.container.interfaces import IObjectAddedEvent

from genweb.serveistic.interfaces import IGenwebServeisticLayer

from zope.component import getMultiAdapter
from zope.component import queryUtility

from zope.interface import Interface
from zope.interface import alsoProvides

from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.dexterity.utils import createContentInContainer

from plone.portlets.interfaces import IPortletManager

from plone.portlets.interfaces import IPortletAssignmentMapping
from genweb.theme.browser.interfaces import IHomePageView
from genweb.theme.browser.views import HomePageBase

import pkg_resources


class IInitializedServeiTIC(Interface):
    """
        A Servei TIC that has been succesfully initialized
    """


class IServeiTIC(form.Schema):
    """ Tipus Servei TIC
    """

    title = schema.TextLine(
        title=_(u"Títol"),
        description=_(u""),
        required=True,
    )

    description = schema.Text(
        title=_(u"Descripció"),
        description=_(u"Descripció del servei que es veurà al buscador"),
        required=False,
    )

    serveiDescription = RichText(
        title=_(u"Breu resum del servei"),
        required=False,
    )

    responsable = schema.TextLine(
        title=_(u"Nom responsable"),
        description=_(u"Nom responsable del servei"),
        required=False,
    )

    responsableMail = schema.TextLine(
        title=_(u'Email responsable'),
        description=_(u'Adreça e-mail del responsable del servei'),
        required=False,
        constraint=checkEmailAddress
    )

    image = NamedBlobImage(
        title=_(u"Imatge capcalera"),
        description=_(u"Mida imatge recomanada de 1280x130 pixels"),
        required=False,
    )


class IInitializedPortlets(Interface):
    """
    Marker interface to mark wether the default portlets have been initialized
    """


class View(HomePageBase):
    grok.implements(IHomePageView)
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('serveitic_view')


class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(IServeiTIC)


@grok.subscribe(IServeiTIC, IObjectAddedEvent)
def initialize_servei(serveitic, event):
    egglocation = pkg_resources.get_distribution('genweb.serveistic').location

    # Add navigation and banners portlets
    target_manager = queryUtility(IPortletManager, name='plone.leftcolumn', context=serveitic)
    target_manager_assignments = getMultiAdapter((serveitic, target_manager), IPortletAssignmentMapping)
    from plone.app.portlets.portlets.navigation import Assignment as navigationAssignment
    from genweb.banners.portlets.bannersportlet import Assignment as bannersAssignment
    target_manager_assignments['banner'] = bannersAssignment()
    target_manager_assignments['navigation'] = navigationAssignment(topLevel=0, bottomLevel=2, currentFolderOnly='True')

    target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager1', context=serveitic)
    target_manager_assignments = getMultiAdapter((serveitic, target_manager), IPortletAssignmentMapping)
    target_manager_assignments['banner'] = bannersAssignment()

    elservei = createContentInContainer(serveitic, 'Folder', title='El servei', checkConstraints=False)
    createContentInContainer(elservei, 'Document', title='Descripció del servei', checkConstraints=False)
    createContentInContainer(elservei, 'Document', title='Normativa', checkConstraints=False)
    createContentInContainer(elservei, 'Document', title='Procediments', checkConstraints=False)
    createContentInContainer(elservei, 'Document', title='Evolució del servei', checkConstraints=False)
    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(elservei)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Document', 'File', 'Folder'))
    behavior.setImmediatelyAddableTypes(('Document', 'File', 'Folder'))

    manuals = createContentInContainer(serveitic, 'Folder', title='Manuals', checkConstraints=False)
    createContentInContainer(manuals, 'Document', title='Manual usuari', checkConstraints=False)
    createContentInContainer(manuals, 'Document', title='Manual administrador', checkConstraints=False)
    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(manuals)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Document', 'File', 'Folder'))
    behavior.setImmediatelyAddableTypes(('Document', 'File', 'Folder'))

    ajuda = createContentInContainer(serveitic, 'Folder', title='Ajuda', checkConstraints=False)
    createContentInContainer(ajuda, 'Folder', title='FAQs', checkConstraints=False)
    createContentInContainer(ajuda, 'Document', title='Casos us', checkConstraints=False)
    createContentInContainer(ajuda, 'Document', title='Errors coneguts', checkConstraints=False)
    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(ajuda)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Document', 'File', 'Folder'))
    behavior.setImmediatelyAddableTypes(('Document', 'File', 'Folder'))

    documentacio = createContentInContainer(serveitic, 'Folder', title='Documentació', checkConstraints=False)
    createContentInContainer(documentacio, 'Folder', title='Documentació tècnica', checkConstraints=False)
    createContentInContainer(documentacio, 'Folder', title='Documentació de referència', checkConstraints=False)
    links = createContentInContainer(documentacio, 'Folder', title='Enllaços', checkConstraints=False)
    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(links)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Link',))
    behavior.setImmediatelyAddableTypes(('Link',))

    behavior = ISelectableConstrainTypes(documentacio)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Document', 'File', 'Folder'))
    behavior.setImmediatelyAddableTypes(('Document', 'File', 'Folder'))

    suggeriments = createContentInContainer(serveitic, 'Folder', title='Suggeriments', checkConstraints=False)
    createContentInContainer(suggeriments, 'Document', title='Suggeriments', checkConstraints=False, exclude_from_nav=True, allow_discussion=True)
    suggeriments.setDefaultPage('suggeriments')
    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(suggeriments)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Document', 'File', 'Folder'))
    behavior.setImmediatelyAddableTypes(())

    notificacions = createContentInContainer(serveitic, 'Folder', title='Notificacions', description='Notificacions del servei', exclude_from_nav=True, checkConstraints=False)
    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(notificacions)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('notificaciotic',))
    behavior.setImmediatelyAddableTypes(('notificaciotic',))

    banners = createContentInContainer(serveitic, 'BannerContainer', title='Banners', exclude_from_nav=True, checkConstraints=False)
    data_banner = open('{}/genweb/serveistic/resources/banner_eATIC.png'.format(egglocation)).read()
    createContentInContainer(banners, 'Banner', title='ATIC', remoteUrl='http://eatic.upc.edu', open_link_in_new_window=True, image=NamedBlobImage(data=data_banner, filename=u'banner_eATIC.png'))
    image_file = NamedBlobImage(data=data_banner, contentType='image/png', filename=u'banner_eATIC.png')
    createContentInContainer(banners, 'Banner', title='ATIC', image=image_file)

    # Reindex all created objects
    elservei.reindexObject()
    manuals.reindexObject()
    ajuda.reindexObject()
    documentacio.reindexObject()
    suggeriments.reindexObject()
    banners.reindexObject()
    notificacions.reindexObject()

    # Mark ServeiTIC as initialitzated, to avoid  previous
    # folder creations to trigger modify event
    alsoProvides(serveitic, IInitializedServeiTIC)


class ServeiTIC(Item):
    implements(IServeiTIC)
