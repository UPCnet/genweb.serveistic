from five import grok

from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.browser.app.view import FacetedContainerView
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import queryUtility

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.data_access.notificacio import NotificacioDataReporter
from genweb.serveistic.browser.notificacio_views import NotificacioViewHelper
from genweb.serveistic.controlpanel import IServeisTICControlPanelSettings


class PreviewItem(grok.View):
    """
    Overrides the view with name 'faceted-preview-item' defined in
    eea.facetednavigation.views.
    """
    grok.name('faceted-preview-item')
    grok.context(IServeiTIC)
    grok.layer(IGenwebServeisticLayer)
    grok.template('preview-item')

    SUMMARY_MAX_LENGTH = 210
    SHORT_SUMMARY_MAX_LENGTH = 115

    def summarise(self, text, max_length):
        if text and len(text) > max_length:
            return text[:max_length - 3] + "..."
        return text

    @property
    def description_summary(self):
        return self.summarise(
            self.context.description,
            PreviewItem.SUMMARY_MAX_LENGTH)

    @property
    def description_short_summary(self):
        return self.summarise(
            self.context.description,
            PreviewItem.SHORT_SUMMARY_MAX_LENGTH)

    @property
    def image_src(self):
        if self.context.image_item:
            return "{0}/@@images/image_item/mini".format(
                self.context.absolute_url())
        elif self.context.image:
            return "{0}/@@images/image/mini".format(
                self.context.absolute_url())
        else:
            return "capcalera_mini.jpg"


class FacetedContainerView(FacetedContainerView, NotificacioViewHelper):

    SHORT_SUMMARY_MAX_LENGTH = 115

    @property
    def notificacions(self):
        reporter = NotificacioDataReporter(
            getToolByName(self.context, 'portal_catalog'))
        return reporter.list_by_general()

    def js_searchbox_placeholder(self):
        return """
    $(document).ready(function()
    {{
        $("#c7").attr("placeholder", "{0}");
        $("#c7_button").val("{1}");
    }});
       """.format(self.context.translate('search_serveitic', domain='genweb.serveistic'),
                  self.context.translate('Search', domain='eea'))

    def page_content(self):
        try:
            lang = self.context.language
            if lang == 'ca':
                benvingut = self.context["benvingut"]
            elif lang == 'es':
                benvingut = self.context["bienvenido"]
            elif lang == 'en':
                benvingut = self.context["welcome"]
            else:
                benvingut = self.context["benvingut"]

            wf_tool = getToolByName(self.context, 'portal_workflow')
            tools = getMultiAdapter((self.context, self.request), name='plone_tools')
            workflows = tools.workflow().getWorkflowsFor(benvingut)[0]
            benvingut_workflow = wf_tool.getWorkflowsFor(benvingut)[0].id
            benvingut_status = wf_tool.getStatusOf(benvingut_workflow, benvingut)
            if workflows['states'][benvingut_status['review_state']].id == 'published':
                return benvingut.text.raw
            else:
                return None
        except KeyError:
            return None

    def get_populars(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        serveitics = catalog(portal_type='serveitic', sort_on='sortable_title', path='/'.join(self.context.getPhysicalPath()))
        populars = []
        for item in serveitics:
            serveitic = item.getObject()
            if serveitic.popular:
                populars.append(serveitic)
        return populars

    def summarise(self, text, max_length):
        if text and len(text) > max_length:
            return text[:max_length - 3] + "..."
        return text

    def description_short_summary(self, text):
        return self.summarise(text, FacetedContainerView.SHORT_SUMMARY_MAX_LENGTH)

    def showFilters(self):
        registry = queryUtility(IRegistry)
        serveistic_tool = registry.forInterface(IServeisTICControlPanelSettings)
        return serveistic_tool.show_filters
