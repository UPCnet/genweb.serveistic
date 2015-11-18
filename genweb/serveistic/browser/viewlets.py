# -*- coding: utf-8 -*-
import re
from five import grok
from plone import api

from cgi import escape
from Acquisition import aq_inner
from AccessControl import getSecurityManager
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.component.hooks import getSite

from plone.memoize.view import memoize_contextless

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import PersonalBarViewlet, GlobalSectionsViewlet, PathBarViewlet
from plone.app.layout.viewlets.common import SearchBoxViewlet, TitleViewlet, ManagePortletsFallbackViewlet
from plone.app.layout.viewlets.interfaces import IHtmlHead, IPortalTop, IPortalHeader, IBelowContent
from plone.app.layout.viewlets.interfaces import IPortalFooter, IAboveContentTitle, IAboveContentBody
from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.ATContentTypes.interface.news import IATNewsItem
from genweb.core.adapters import IImportant

from genweb.core.interfaces import IHomePage
from genweb.core.utils import genweb_config, havePermissionAtRoot, pref_lang

from genweb.theme.browser.interfaces import IGenwebTheme
from genweb.alternatheme.browser.viewlets import gwManagePortletsFallbackViewlet
from genweb.serveistic.interfaces import IGenwebServeisticLayer

from plone.app.collection.interfaces import ICollection
from genweb.core import HAS_CAS
from zope.security import checkPermission

import random
from genweb.core import GenwebMessageFactory as _
from DateTime.DateTime import DateTime

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


# class gwGlobalSectionsViewlet(GlobalSectionsViewlet, viewletBase):
#     grok.name('genweb.globalsections')
#     grok.viewletmanager(IPortalTop)
#     grok.layer(IGenwebServeisticLayer)

#     index = ViewPageTemplateFile('viewlets_templates/sections.pt')

#     allowed_section_types = ['Folder', 'Collection', 'Document', 'serveitic']

#     def menuPrincipal(self):
#         """ returns folders (menu-principal)"""
#         portal_catalog = getToolByName(self.context, 'portal_catalog')
#         import ipdb; ipdb.set_trace( )
#         url = '/' + api.portal.getSite().getId()
#         lang = self.context.portal_languages.getPreferredLanguage()
#         if lang == 'ca':
#             path = url + '/' + lang
#         else:
#             path = url + '/en'

#         folders = portal_catalog.searchResults(portal_type=self.allowed_section_types,
#                                                path={'query': path, 'depth': 1},
#                                                review_state='published',
#                                                Language=lang,
#                                                sort_on='getObjPositionInParent')
#         results = []
#         for fold in folders:
#             if (fold.portal_type in self.allowed_section_types):
#                 if fold.exclude_from_nav is not True:
#                     if fold.Description == '':
#                         description = fold.Title
#                     else:
#                         description = fold.Description
#                     results.append(dict(name=fold.Title.decode('utf-8').upper(),
#                                         url=fold.getURL(),
#                                         id=fold.getId,
#                                         description=description))

#         return results

#     def menu(self):
#         """ returns subfolders (submenus) for the dropdown in navbar"""
#         portal_catalog = getToolByName(self.context, 'portal_catalog')
#         # Obtain all folders in first level "published""
#         url = '/' + api.portal.getSite().getId()
#         lang = self.context.portal_languages.getPreferredLanguage()
#         if lang == 'es':
#             path = url + '/' + lang
#         else:
#             path = url + '/en'

#         folders = portal_catalog.searchResults(portal_type=self.allowed_section_types,
#                                                path={'query': path, 'depth': 1},
#                                                review_state='published',
#                                                Language=lang,
#                                                sort_on='getObjPositionInParent')
#         subfolders = {}
#         for fold in folders:
#             if (fold.portal_type in self.allowed_section_types):
#                 if fold.exclude_from_nav is not True:
#                     subfolders[fold.getId] = self.SubMenu(fold.getPath())
#         return subfolders

#     def SubMenu(self, path):
#         """ Get subfolders of current folder for create submenu"""
#         portal_catalog = getToolByName(self.context, 'portal_catalog')
#         subfolders = portal_catalog.searchResults(portal_type=self.allowed_section_types,
#                                                   path={'query': path, 'depth': 1},
#                                                   review_state='published',
#                                                   sort_on='getObjPositionInParent')
#         results = []
#         for fold in subfolders:
#             if (fold.portal_type in self.allowed_section_types):
#                 if fold.exclude_from_nav is not True:
#                     results.append(dict(name=fold.Title,
#                                         url=fold.getURL(),
#                                         id=fold.getId,
#                                         description=fold.Description))
#         return results

class gwGlobalSectionsViewlet(GlobalSectionsViewlet, viewletBase):
    grok.name('genweb.globalsections')
    grok.viewletmanager(IPortalTop)
    grok.layer(IGenwebServeisticLayer)

    index = ViewPageTemplateFile('viewlets_templates/sections.pt')

    allowed_section_types = ['Folder', 'Collection', 'Document', 'serveitic']

    def show_menu(self):
        return not self.genweb_config().treu_menu_horitzontal and self.portal_tabs

    def menuPrincipal(self):
        """ returns folders (menu-principal)"""
        urltool = getToolByName(self.context, 'portal_url')
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        # Obtain all folders in first level "published" o "visible"
        path = urltool.getPortalPath() + '/ca'
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
        path = urltool.getPortalPath() + '/ca'
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
