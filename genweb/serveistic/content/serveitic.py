# -*- coding: utf-8 -*-

from zope import schema

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
    title = schema.TextLine(
        title=_(u"Títol"),
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

    image = BlobImage(
        title=_(u"Imatge capcalera"),
        description=_(u"Mida recomanada de la imatge 1280x130 pixels"),
        required=False,
    )

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
