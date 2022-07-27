# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from genweb.upc.browser.interfaces import IGenwebUPC


class IGenwebServeisticLayer(IGenwebUPC):
    """Marker interface that defines a Zope 3 browser layer."""
