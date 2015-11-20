# -*- coding: utf-8 -*-
from five import grok
from plone.directives import dexterity

from zope import schema
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText

from genweb.serveistic import _

from zope.interface import implements
from plone.dexterity.content import Item

from plone.app.users.userdataschema import checkEmailAddress
from zope.app.container.interfaces import IObjectAddedEvent




from AccessControl import Unauthorized
from AccessControl import getSecurityManager

from z3c.form import button

from genweb.serveistic.interfaces import IGenwebServeisticLayer

from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.event import notify
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.security import checkPermission

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.dexterity.utils import createContentInContainer

from plone.indexer import indexer
from plone.memoize.view import memoize_contextless
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager
from plone.registry.interfaces import IRegistry


from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets.navigation import Assignment as NavPortletAssignment
from genweb.theme.browser.interfaces import IHomePageView
from genweb.theme.browser.views import HomePageBase


class IInitializedServeiTIC(Interface):
    """
        A Servei TIC that has been succesfully initialized
    """


class IServeiTIC(form.Schema):
    """ Tipus Servei TIC
    """

    serveiDescription = RichText(
        title=_(u"Body"),
        required=False,
    )

    responsable = schema.Text(
        title=_(u"Nom responsable"),
        description=_(u"Nom responsable del servei"),
        required=False,
    )

    responsableMail = schema.TextLine(
        title=_(u'From mail'),
        description=_(u'Enter the from used in the mail form'),
        required=False,
        constraint=checkEmailAddress
    )

    image = NamedBlobImage(
        title=_(u"Image"),
        description=_(u""),
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
    # grok.name('subhome')
    grok.template('serveitic_view')


# class View(dexterity.DisplayForm):
#     """ View form
#     """
#     grok.context(IServeiTIC)
#     grok.template('serveitic_view')


class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(IServeiTIC)


@grok.subscribe(IServeiTIC, IObjectAddedEvent)
def initialize_servei(serveitic, event):

    # Create default content containers

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
    createContentInContainer(elservei, 'Document', title='Manual usuari', checkConstraints=False)
    createContentInContainer(elservei, 'Document', title='Manual administrador', checkConstraints=False)
    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(manuals)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Document', 'File', 'Folder'))
    behavior.setImmediatelyAddableTypes(('Document', 'File', 'Folder'))

    ajuda = createContentInContainer(serveitic, 'Folder', title='Ajuda', checkConstraints=False)
    createContentInContainer(serveitic, 'Folder', title='FAQs', checkConstraints=False)
    createContentInContainer(elservei, 'Document', title='Casos us', checkConstraints=False)
    createContentInContainer(elservei, 'Document', title='Errors coneguts', checkConstraints=False)

    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(ajuda)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Document', 'File', 'Folder'))
    behavior.setImmediatelyAddableTypes(('Document', 'File', 'Folder'))

    documentacio = createContentInContainer(serveitic, 'Folder', title='Documentació', checkConstraints=False)
    createContentInContainer(serveitic, 'Folder', title='Documentació tècnica', checkConstraints=False)
    createContentInContainer(serveitic, 'Folder', title='Documentació de referència', checkConstraints=False)
    links = createContentInContainer(serveitic, 'Folder', title='Enllaços', checkConstraints=False)

    behavior = ISelectableConstrainTypes(links)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Link',))
    behavior.setImmediatelyAddableTypes(('Link',))

    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(documentacio)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Document', 'File', 'Folder'))
    behavior.setImmediatelyAddableTypes(('Document', 'File', 'Folder'))

    suggeriments = createContentInContainer(serveitic, 'Folder', title='suggeriments', checkConstraints=False)
    createContentInContainer(elservei, 'Document', title='Suggeriments', checkConstraints=False)
    # Set on them the allowable content types
    behavior = ISelectableConstrainTypes(suggeriments)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(('Document', 'File', 'Folder'))
    behavior.setImmediatelyAddableTypes(('Document', 'File', 'Folder'))

    # Add portlets programatically
    # target_manager = queryUtility(IPortletManager, name='plone.leftcolumn', context=ServeiTIC)
    # target_manager_assignments = getMultiAdapter((ServeiTIC, target_manager), IPortletAssignmentMapping)
    # from ulearn.theme.portlets.profile import Assignment as profileAssignment
    # from ulearn.theme.portlets.thinnkers import Assignment as thinnkersAssignment
    # from ulearn.theme.portlets.communities import Assignment as communitiesAssignment
    # from ulearn.theme.portlets.stats import Assignment as statsAssignment
    # from plone.app.portlets.portlets.navigation import Assignment as navigationAssignment
    # target_manager_assignments['profile'] = profileAssignment()
    # target_manager_assignments['navigation'] = navigationAssignment(root=u'/{}'.format(ServeiTIC.id))
    # target_manager_assignments['communities'] = communitiesAssignment()
    # target_manager_assignments['thinnkers'] = thinnkersAssignment()
    # target_manager_assignments['stats'] = statsAssignment()

    # # Blacklist the right column portlets on documents
    # right_manager = queryUtility(IPortletManager, name=u"plone.rightcolumn")
    # blacklist = getMultiAdapter((documents, right_manager), ILocalPortletAssignmentManager)
    # blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

    # # Blacklist the right column portlets on photos
    # right_manager = queryUtility(IPortletManager, name=u"plone.rightcolumn")
    # blacklist = getMultiAdapter((photos, right_manager), ILocalPortletAssignmentManager)
    # blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

    # # Blacklist the right column portlets on links
    # right_manager = queryUtility(IPortletManager, name=u"plone.rightcolumn")
    # blacklist = getMultiAdapter((links, right_manager), ILocalPortletAssignmentManager)
    # blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

    # # Blacklist the right column portlets on events
    # right_manager = queryUtility(IPortletManager, name=u"plone.rightcolumn")
    # blacklist = getMultiAdapter((events, right_manager), ILocalPortletAssignmentManager)
    # blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

    # # Blacklist the right column portlets on discussion
    # right_manager = queryUtility(IPortletManager, name=u"plone.rightcolumn")
    # blacklist = getMultiAdapter((discussion, right_manager), ILocalPortletAssignmentManager)
    # blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

    # Reindex all created objects
    elservei.reindexObject()
    manuals.reindexObject()
    ajuda.reindexObject()
    documentacio.reindexObject()
    suggeriments.reindexObject()

    # Mark ServeiTIC as initialitzated, to avoid  previous
    # folder creations to trigger modify event
    alsoProvides(serveitic, IInitializedServeiTIC)


class ServeiTIC(Item):
    implements(IServeiTIC)
