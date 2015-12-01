# -*- coding: utf-8 -*-
import zope.component
import zope.interface
import zope.schema
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textarea
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from genweb.serveistic.widgets.interfaces import ISubjectChooserWidget
from Products.CMFCore.utils import getToolByName


class SubjectChooserWidget(textarea.TextAreaWidget):
    """Widget for adding new keywords and autocomplete with the ones in the
    system."""

    zope.interface.implementsOnly(ISubjectChooserWidget)
    klass = u"subject-chooser-widget"
    display_template = ViewPageTemplateFile('subject_chooser_display.pt')
    input_template = ViewPageTemplateFile('subject_chooser_input.pt')

    # JavaScript template
    js_template = u"""\
    (function($) {
        $().ready(function() {
            var newValues = '%(newtags)s';
            var oldValues = [%(oldtags)s];
            $('#%(id)s').data('klass','%(klass)s');
            keywordTokenInputActivate('%(id)s', newValues, oldValues);
        });
    })(jQuery);
    """

    def subjects_list(self):
        """
        """
        # subjects_tool = getToolByName(self.context, 'portal_keywords_categorization')
        # checked = self.value.split('\n')
        val = [{'header': True, 'value': 'acti', 'title': 'Activitats'},
         {'header': False, 'checked': False, 'value': u'Aikido', 'title': u'Aikido'},
         {'header': False, 'checked': False, 'value': u'Balls', 'title': u'Balls'},
         {'header': False, 'checked': False, 'value': u'Bridge', 'title': u'Bridge'}]
        # return subjects_tool.keywords(checked=checked)
        return val

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)


@zope.interface.implementer(interfaces.IFieldWidget)
def SubjectChooserFieldWidget(field, request):
    """IFieldWidget factory for TokenInputWidget."""
    return widget.FieldWidget(field, SubjectChooserWidget(request))
