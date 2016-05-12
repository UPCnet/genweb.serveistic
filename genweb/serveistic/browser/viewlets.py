# -*- coding: utf-8 -*-

from five import grok
from AccessControl import getSecurityManager
from Acquisition import aq_inner, aq_chain

from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.view import memoize_contextless
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from plone.app.layout.viewlets.interfaces import IPortalTop, IPortalHeader
from plone.app.layout.viewlets.interfaces import IBelowContent
from plone.app.layout.viewlets.common import ManagePortletsFallbackViewlet
from plone.app.layout.navigation.interfaces import INavigationRoot

from genweb.core.interfaces import IHomePage
from genweb.core.utils import genweb_config, pref_lang
from genweb.theme.browser.viewlets import gwFooter

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.utilities import serveistic_config

grok.context(Interface)


class viewletBase(grok.Viewlet):
    grok.baseclass()

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()

    def genweb_config(self):
        return genweb_config()


class gwGlobalSectionsViewlet(GlobalSectionsViewlet, viewletBase):
    grok.name('genweb.globalsections')
    grok.viewletmanager(IPortalTop)
    grok.layer(IGenwebServeisticLayer)

    index = ViewPageTemplateFile('viewlets_templates/sections.pt')

    allowed_section_types = ['Folder', 'Collection', 'Document', 'serveitic']

    def get_servei(self):
        context = aq_inner(self.context)
        for obj in aq_chain(context):
            if IServeiTIC.providedBy(obj):
                return obj

    def show_menu(self):
        return not self.genweb_config().treu_menu_horitzontal and self.portal_tabs

    def menuPrincipal(self):
        """ returns folders (menu-principal)"""
        urltool = getToolByName(self.context, 'portal_url')
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        # Obtain all folders in first level "published" o "visible"
        lang = pref_lang()
        servei = self.get_servei()
        subpath = servei.id
        path = urltool.getPortalPath() + '/' + lang + '/' + subpath

        folders = portal_catalog.searchResults(portal_type=self.allowed_section_types,
                                               path=dict(query=path, depth=1),
                                               sort_on='getObjPositionInParent')
        results = []
        for fold in folders:
            if (fold.portal_type in self.allowed_section_types):
                if fold.exclude_from_nav is not True:
                    results.append(dict(name=fold.Title,
                                        url=fold.getURL(),
                                        id=fold.getId,
                                        description=fold.Description))

        return results

    def menu(self):
        """ returns subfolders (submenus) for the dropdown in navbar"""
        urltool = getToolByName(self.context, 'portal_url')
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        # Obtain all folders in first level "published" o "visible"
        lang = pref_lang()
        servei = self.get_servei()
        subpath = servei.id
        path = urltool.getPortalPath() + '/' + lang + '/' + subpath
        folders = portal_catalog.searchResults(portal_type=self.allowed_section_types,
                                               path=dict(query=path, depth=1),
                                               sort_on='getObjPositionInParent')

        subfolders = {}
        for fold in folders:
            if (fold.portal_type in self.allowed_section_types):
                if fold.exclude_from_nav is not True:
                    subfolders[fold.getId] = self.SubMenu(fold.getPath())
        return subfolders

    def SubMenu(self, path):
        """ Get subfolders of current folder for create submenu"""
        path = path
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        subfolders = portal_catalog.searchResults(portal_type=self.allowed_section_types,
                                                  path=dict(query=path, depth=1),
                                                  sort_on='getObjPositionInParent')

        results = []
        for fold in subfolders:
            if (fold.portal_type in self.allowed_section_types):
                if fold.exclude_from_nav is not True:
                    results.append(dict(name=fold.Title,
                                        url=fold.getURL(),
                                        id=fold.getId,
                                        description=fold.Description))

        return results

from genweb.theme.browser.viewlets import gwHeader


class HeaderGWServeistic(gwHeader):
    grok.name('genweb.header')
    grok.viewletmanager(IPortalHeader)
    grok.template('header')
    grok.layer(IGenwebServeisticLayer)

    def get_image_class(self):
            return 'l3-image'

    def get_servei(self):
        context = aq_inner(self.context)
        for obj in aq_chain(context):
            if IServeiTIC.providedBy(obj):
                return obj
        return None

    def get_html_title(self):
        return getattr(
            self.genweb_config(),
            'html_title_{}'.format(self.pref_lang()), '')

    def get_title(self):
        servei = self.get_servei()
        if servei:
            return servei.title
        else:
            title = getattr(self.genweb_config(), 'html_title_{}'.format(self.pref_lang()))
            if title:
                return title
            else:
                return u''

    def get_servei_title(self):
        return self.get_servei().title if self.get_servei() else ''

    def get_url_root(self):
        return getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state').portal_url()

    def get_url_servei(self):
        return self.get_servei().absolute_url_path()

    @property
    def url_serveistic_servei(self):
        return serveistic_config().url_info_serveistic

    def isServei(self):
        if self.get_servei():
            return True
        else:
            return False

    def is_anonymous(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state")
        return portal_state.anonymous()


class PortalHeaderGWServeistic(gwHeader):
    grok.name('plone.header')
    grok.viewletmanager(IPortalTop)
    grok.template('portal_header')
    grok.layer(IGenwebServeisticLayer)

    IMAGE_CROPPED_WIDTH = 1280
    IMAGE_CROPPED_HEIGHT = 130

    def get_servei(self):
        context = aq_inner(self.context)
        for obj in aq_chain(context):
            if IServeiTIC.providedBy(obj):
                return obj

    @property
    def img_cropped_url(self):
        return self.get_servei().restrictedTraverse('@@images').scale(
            'image',
            width=PortalHeaderGWServeistic.IMAGE_CROPPED_WIDTH,
            height=PortalHeaderGWServeistic.IMAGE_CROPPED_HEIGHT,
            direction="down").absolute_url()


class gwManagePortletsFallbackViewletMixin(object):
    """ The override for the manage_portlets_fallback viewlet for IPloneSiteRoot
    """

    render = ViewPageTemplateFile('viewlets_templates/manage_portlets_fallback.pt')

    def getPortletContainerPath(self):
        context = aq_inner(self.context)

        container_url = context.absolute_url()

        # Portlet container will be in the context,
        # Except in the portal root, when we look for an alternative
        if INavigationRoot.providedBy(self.context):
            pc = getToolByName(context, 'portal_catalog')
            # Add the use case of mixin types of IHomepages. The main ones of a
            # non PAM-enabled site and the possible inner ones.
            result = pc.searchResults(object_provides=IHomePage.__identifier__,
                                      portal_type='Document',
                                      Language=pref_lang())

            if result:
                # Return the object without forcing a getObject()
                container_url = result[0].getURL()

        return container_url

    def managePortletsURL(self):
        return "%s/%s" % (self.getPortletContainerPath(), '@@manage-homeportlets')

    def available(self):
        secman = getSecurityManager()

        if secman.checkPermission('Genweb: Manage home portlets', self.context):
            return True
        else:
            return False


class gwManagePortletsFallbackViewletForIHomePage(gwManagePortletsFallbackViewletMixin, ManagePortletsFallbackViewlet, viewletBase):
    """ The override for the manage_portlets_fallback viewlet for IHomePage
    """
    grok.context(IServeiTIC)
    grok.name('serveitic.manage_portlets_fallback')
    grok.viewletmanager(IBelowContent)
    grok.layer(IGenwebServeisticLayer)


class serveiticFooter(gwFooter):
    grok.name('genweb.footer')
    grok.template('footer')
    grok.layer(IGenwebServeisticLayer)
