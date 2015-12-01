# -*- coding: utf-8 -*-
"""Init and utils."""

from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.autoform.interfaces import WIDGETS_KEY
from plone.directives.form.schema import TEMP_KEY
from zope import schema as _schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('genweb.serveistic')


widget = 'genweb.serveistic.widgets.subject_chooser.SubjectChooserFieldWidget'
_directives_values = ICategorization.queryTaggedValue(TEMP_KEY)
if _directives_values:
    # groked form
    _directives_values.setdefault(WIDGETS_KEY, {})
    _directives_values[WIDGETS_KEY]['subjects'] = widget
else:
    # plone 4.3 not groked form
    _widget_values = ICategorization.queryTaggedValue(WIDGETS_KEY, {})
    _widget_values['subjects'] = widget
    ICategorization.setTaggedValue(WIDGETS_KEY, _widget_values)

_schema.getFields(ICategorization)['subjects'].index_name = 'Subject'


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
