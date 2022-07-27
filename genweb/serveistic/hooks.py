# -*- coding: utf-8 -*-
from Acquisition import aq_chain
from five import grok

from genweb.serveistic.content.serveitic import IServeiTIC
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from Products.CMFCore.utils import getToolByName


def Added(content, event):
    """ MAX hooks main handler """

    servei = findContainerServei(content)
    if not servei:
        # If file we are creating is not inside a servei folder
        return

    servei_tags = servei.subject
    addTagsToObject(servei_tags, content)


@grok.subscribe(IServeiTIC, IObjectModifiedEvent)
def serveiModifyAddSubjects(content, event):
    """ Servei modified handler """

    pc = getToolByName(content, "portal_catalog")
    servei_tags = content.subject
    path = "/".join(content.getPhysicalPath())
    r_results = pc.searchResults(portal_type=('Document', 'Link', 'File'),
                                 path=path)

    for brain in r_results:
        obj = brain.getObject()
        addTagsToObject(servei_tags, obj)

    content.es_faceta_1 = content.ca_faceta_1
    content.en_faceta_1 = content.ca_faceta_1

    content.es_faceta_2 = content.ca_faceta_2
    content.en_faceta_2 = content.ca_faceta_2

    content.es_faceta_3 = content.ca_faceta_3
    content.en_faceta_3 = content.ca_faceta_3

    content.es_faceta_4 = content.ca_faceta_4
    content.en_faceta_4 = content.ca_faceta_4

    content.es_faceta_5 = content.ca_faceta_5
    content.en_faceta_5 = content.ca_faceta_5

    content.es_faceta_6 = content.ca_faceta_6
    content.en_faceta_6 = content.ca_faceta_6

    content.es_faceta_7 = content.ca_faceta_7
    content.en_faceta_7 = content.ca_faceta_7

    content.es_faceta_8 = content.ca_faceta_8
    content.en_faceta_8 = content.ca_faceta_8

    content.reindexObject()


# --------------- helpers ---------------

def addTagsToObject(servei_tags, obj):
    tags = []
    object_tags = list(obj.subject)
    [tags.append(tag) for tag in servei_tags if tag not in object_tags]
    obj.subject = tuple(sum([object_tags, tags], []))
    obj.reindexObject()


def findContainerServei(content):
    for parent in aq_chain(content):
        if IServeiTIC.providedBy(parent):
            return parent

    return None
