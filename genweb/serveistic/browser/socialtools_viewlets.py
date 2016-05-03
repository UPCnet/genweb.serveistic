from five import grok
from Acquisition import aq_inner
from plone.app.layout.viewlets.interfaces import IAboveContentTitle

from genweb.theme.browser.viewlets import viewletBase
from genweb.serveistic.interfaces import IGenwebServeisticLayer
from genweb.serveistic.content.serveitic import IServeiTIC


class socialtoolsViewlet(viewletBase):
    grok.name('genweb.socialtools')
    grok.template('socialtools')
    grok.viewletmanager(IAboveContentTitle)
    grok.layer(IGenwebServeisticLayer)

    def getData(self):
        Title = aq_inner(self.context).Title()
        contextURL = self.context.absolute_url()

        return dict(Title=Title, URL=contextURL)

    def is_social_tools_enabled(self):
        return not self.genweb_config().treu_icones_xarxes_socials

    def is_servei(self):
        return IServeiTIC.providedBy(self.context)

    @property
    def url_rss(self):
        return "{0}/notificacions/RSS".format(
            self.context.absolute_url()) if self.is_servei() else ''
