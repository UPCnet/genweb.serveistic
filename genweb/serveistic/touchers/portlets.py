from five import grok
from zope.component import queryUtility, getMultiAdapter
from zope.interface import alsoProvides
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from plone.portlets.interfaces import (
    IPortletManager, IPortletAssignmentMapping)

from genweb.serveistic.portlets.indicadors import Assignment as \
    IndicadorsAssignment


class PortletIndicadorsReinstallAll(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('touch_portlet_indicadors_reinstall_all')
    grok.require('cmf.ManagePortal')

    def render(self):
        self._disable_csrf_protection()

        service_id_updated = []
        catalog = getToolByName(self.context, 'portal_catalog')
        for servei in catalog.searchResults(portal_type='serveitic'):
            assignments = self._get_portlet_assignments(
                servei.getObject(), 'genweb.portlets.HomePortletManager5')
            if 'indicadors' in assignments:
                del assignments['indicadors']
            assignments['indicadors'] = IndicadorsAssignment(
                count_indicator=5, count_category=4)
            service_id_updated.append(servei.id)

        report = "{0} serveis have been updated:\n\n".format(
            len(service_id_updated))
        report += '\n'.join(sorted(service_id_updated))
        return report

    def _disable_csrf_protection(self):
        from plone.protect.interfaces import IDisableCSRFProtection
        alsoProvides(self.request, IDisableCSRFProtection)

    def _get_portlet_assignments(self, context, name):
        portlet_manager = queryUtility(
            IPortletManager,
            name=name,
            context=context)
        return getMultiAdapter(
            (context, portlet_manager), IPortletAssignmentMapping)
