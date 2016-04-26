from five import grok

from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC


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
            return "{0}/@@images/image_item".format(
                self.context.absolute_url())
        elif self.context.image:
            return "{0}/@@images/image".format(
                self.context.absolute_url())
        else:
            return "++genweb++serveistic/capcalera.jpg"
