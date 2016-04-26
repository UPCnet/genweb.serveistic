# -*- coding: utf-8 -*-

from zope import schema

from collective import dexteritytextindexer
from plone.directives import form
from plone.namedfile.field import NamedBlobImage as BlobImage
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.app.users.userdataschema import checkEmailAddress

from zope.interface import implements
from zope.interface import Interface

from genweb.serveistic import _


class IInitializedServeiTIC(Interface):
    """
        A Servei TIC that has been succesfully initialized
    """


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
