# -*- coding: utf-8 -*-

import re

from collective import dexteritytextindexer
from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.app.textfield import RichText
from plone.app.users.userdataschema import checkEmailAddress
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.dexterity.content import Item
from plone.directives import form
from plone.namedfile.field import NamedBlobImage as BlobImage
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import implements
from zope.interface import Interface
from zope.interface import Invalid

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
        default=u'Explica en poques paraules la funcionalitat principal del servei. Aquesta és la frase que apareix en el cercador de serveis',
    )

    dexteritytextindexer.searchable('serveiDescription')
    serveiDescription = RichText(
        title=_(u"Breu resum del servei"),
        required=False,
        default=IRichText['text'].fromUnicode(
            u"""<p><strong>RESPON A LA PREGUNTA: Quin és el benefici per l'usuari d'utilitzar el servei</strong></p>
                <p>Emplena la descripció del servei amb la proposta de valor del servei.</p>
                <p>Explica-hi per quina raó ha d’utilitzar el servei l’usuari. Utilitza les següents fórmules de redacció:</p>
                <p>-          <b>Acció</b> (imperatiu, segona persona del singular) + <b>objecte + [qualitat/avantatge]</b></p>
                <p>“Rep i envia missatges de correu electrònic des de qualsevol lloc” “Llegeix llibres amb el mòbil” “Obre, edita i crea documents en línia”</p>
                <p> </p>
                <p>Nota: en les etiquetes posa totes les paraules que puguin identificar el servei </p>"""
        ),
    )

    dexteritytextindexer.searchable('website_url')
    website_url = schema.TextLine(
        title=_(u"URL"),
        description=_(u"Direcció URL del web del servei"),
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
        description=_(u"Mida recomanada de la imatge 1920x82 pixels"),
        required=False,
    )

    image_item = BlobImage(
        title=_(u"Imatge del servei en el resultat de cerca"),
        description=_(u"Es mostrarà com a imatge del servei en els resultats "
                      u"del cercador de Serveis TIC (mida recomanada 180x50 "
                      u"pixels)"),
        required=False)

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

    read_permission(popular='cmf.ManagePortal')
    write_permission(popular='cmf.ManagePortal')
    popular = schema.Bool(
        title=_("Popular"),
        required=False,
        default=False)

    directives.omitted('prestador')
    prestador = schema.List(
        title=_(u"Prestador"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.prestador'))

    directives.omitted('ubicacio')
    ubicacio = schema.List(
        title=_(u"Ubicació"),
        required=False,
        value_type=schema.Choice(
            vocabulary="genweb.serveistic.vocabularies.ubicacio"))

    directives.omitted('tipologia')
    tipologia = schema.List(
        title=_(u"Tipologia"),
        required=False,
        value_type=schema.Choice(
            vocabulary="genweb.serveistic.vocabularies.tipologia"))

    directives.omitted('ambit')
    ambit = schema.List(
        title=_(u"Àmbit"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.ambit'))

    ca_faceta_1 = schema.List(
        title=_(u"Faceta 1"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.cafaceta1'))

    ca_faceta_2 = schema.List(
        title=_(u"Faceta 2"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.cafaceta2'))

    ca_faceta_3 = schema.List(
        title=_(u"Faceta 3"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.cafaceta3'))

    ca_faceta_4 = schema.List(
        title=_(u"Faceta 4"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.cafaceta4'))

    ca_faceta_5 = schema.List(
        title=_(u"Faceta 5"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.cafaceta5'))

    ca_faceta_6 = schema.List(
        title=_(u"Faceta 6"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.cafaceta6'))

    ca_faceta_7 = schema.List(
        title=_(u"Faceta 7"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.cafaceta7'))

    ca_faceta_8 = schema.List(
        title=_(u"Faceta 8"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.cafaceta8'))

    directives.omitted('es_faceta_1')
    es_faceta_1 = schema.List(
        title=_(u"Faceta 1"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.esfaceta1'))

    directives.omitted('es_faceta_2')
    es_faceta_2 = schema.List(
        title=_(u"Faceta 2"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.esfaceta2'))

    directives.omitted('es_faceta_3')
    es_faceta_3 = schema.List(
        title=_(u"Faceta 3"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.esfaceta3'))

    directives.omitted('es_faceta_4')
    es_faceta_4 = schema.List(
        title=_(u"Faceta 4"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.esfaceta4'))

    directives.omitted('es_faceta_5')
    es_faceta_5 = schema.List(
        title=_(u"Faceta 5"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.esfaceta5'))

    directives.omitted('es_faceta_6')
    es_faceta_6 = schema.List(
        title=_(u"Faceta 6"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.esfaceta6'))

    directives.omitted('es_faceta_7')
    es_faceta_7 = schema.List(
        title=_(u"Faceta 7"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.esfaceta7'))

    directives.omitted('es_faceta_8')
    es_faceta_8 = schema.List(
        title=_(u"Faceta 8"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.esfaceta8'))

    directives.omitted('en_faceta_1')
    en_faceta_1 = schema.List(
        title=_(u"Faceta 1"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.enfaceta1'))

    directives.omitted('en_faceta_2')
    en_faceta_2 = schema.List(
        title=_(u"Faceta 2"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.enfaceta2'))

    directives.omitted('en_faceta_3')
    en_faceta_3 = schema.List(
        title=_(u"Faceta 3"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.enfaceta3'))

    directives.omitted('en_faceta_4')
    en_faceta_4 = schema.List(
        title=_(u"Faceta 4"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.enfaceta4'))

    directives.omitted('en_faceta_5')
    en_faceta_5 = schema.List(
        title=_(u"Faceta 5"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.enfaceta5'))

    directives.omitted('en_faceta_6')
    en_faceta_6 = schema.List(
        title=_(u"Faceta 6"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.enfaceta6'))

    directives.omitted('en_faceta_7')
    en_faceta_7 = schema.List(
        title=_(u"Faceta 7"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.enfaceta7'))

    directives.omitted('en_faceta_8')
    en_faceta_8 = schema.List(
        title=_(u"Faceta 8"),
        required=False,
        value_type=schema.Choice(
            vocabulary='genweb.serveistic.vocabularies.enfaceta8'))


class IInitializedPortlets(Interface):
    """
    Marker interface to mark wether the default portlets have been initialized
    """


class ServeiTIC(Item):
    implements(IServeiTIC)
