# -*- coding: utf-8 -*-

import re

from zope import schema
from zope.interface import Interface, implements, Invalid
from collective import dexteritytextindexer
from plone.directives import form
from plone.namedfile.field import NamedBlobImage as BlobImage
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.app.users.userdataschema import checkEmailAddress

from genweb.serveistic import _


class IInitializedServeiTIC(Interface):
    """
        A Servei TIC that has been successfully initialized
    """


SERVICE_INDICATORS_ORDER_RE = re.compile(
    "^\d+[.]\d+(,[ ]?\d+[.]\d+)*,?$")

SERVICE_INDICATORS_ORDER_ITEM_RE = re.compile(
    "\d+[.]\d+")


def validate_service_indicators_order(order):
    if not is_valid_service_indicators_order(order):
        raise Invalid(_(u"El format ha de ser 3.1, 1.2, 1.3"))
    return True


def is_valid_service_indicators_order(order):
    return True if SERVICE_INDICATORS_ORDER_RE.match(order) else False


def parse_service_indicators_order(order):
    """
    Transform an order string into an order structure. Example:
    Order string: '1.2, 1.3, 3.2, 1.4'
    Order structure: [(1, [2, 3]), (3, [2]), (1, [4])]
    :param order: Order string with format described above.
    :return: Order structure with format described above.
    """
    result = []
    indicator_index_prev = -1
    category_index_list = None
    for match in SERVICE_INDICATORS_ORDER_ITEM_RE.findall(order):
        indicator_index, category_index = match.split('.')
        if indicator_index != indicator_index_prev:
            category_index_list = []
            result.append((int(indicator_index), category_index_list))
            indicator_index_prev = indicator_index
        category_index_list.append(int(category_index))
    return result


class IServeiTIC(form.Schema):
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Títol"),
        required=True,
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Descripció"),
        description=_(u"Descripció del servei que es veurà al buscador"),
        required=False,
    )

    dexteritytextindexer.searchable('serveiDescription')
    serveiDescription = RichText(
        title=_(u"Breu resum del servei"),
        required=False,
    )

    responsable = schema.TextLine(
        title=_(u"Nom del responsable funcional"),
        description=_(u"Nom del responsable funcional del servei"),
        required=False,
    )

    responsableMail = schema.TextLine(
        title=_(u'Email del responsable funcional'),
        description=_(u'Adreça e-mail del responsable funcional del servei'),
        required=False,
        constraint=checkEmailAddress
    )

    image = BlobImage(
        title=_(u"Imatge de capçalera"),
        description=_(u"Mida recomanada de la imatge 1280x130 pixels"),
        required=False,
    )

    image_item = BlobImage(
        title=_(u"Imatge del servei en el resultat de cerca"),
        description=_(u"Es mostrarà com a imatge del servei en els resultats "
                      u"del cercador de Serveis TIC (mida recomanada 180x150 "
                      u"pixels)"),
        required=False
        )

    product_id = schema.TextLine(
        title=_(u"Identificador gn6"),
        description=_(u"Identificador del servei al gn6, s'utilitza per a "
                      u"consultar els problemes relacionats amb el servei"),
        required=False,
        defaultFactory=lambda: u'')

    service_id = schema.TextLine(
        title=_(u"Identificador indicadors"),
        description=_(u"Identificador del servei al servei web d'indicadors, "
                      u"s'utilitza per a consultar els indicadors relacionats "
                      u"amb el servei"),
        required=False,
        defaultFactory=lambda: u'')

    service_indicators_order = schema.TextLine(
        title=(u"Ordre indicadors"),
        description=(
            u"Ordre en el qual es mostren els indicadors relacionats amb el "
            u"servei. Té el format \"3.1, 1.2, 1.3\", on el número abans de "
            u"la coma representa l'ordre original de l'indicador i el de "
            u"després l'ordre original de la categoria"),
        required=False,
        constraint=validate_service_indicators_order)

    prestador = schema.List(
        title=_(u"Prestador"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.prestador'))

    ubicacio = schema.List(
        title=_(u"Ubicació"),
        required=False,
        value_type=schema.Choice(
            vocabulary="genweb.serveistic.vocabularies.ubicacio"))

    tipologia = schema.List(
        title=_(u"Tipologia"),
        required=False,
        value_type=schema.Choice(
            vocabulary="genweb.serveistic.vocabularies.tipologia"))

    ambit = schema.List(
        title=_(u"Àmbit"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.ambit'))


class IInitializedPortlets(Interface):
    """
    Marker interface to mark wether the default portlets have been initialized
    """


class ServeiTIC(Item):
    implements(IServeiTIC)
