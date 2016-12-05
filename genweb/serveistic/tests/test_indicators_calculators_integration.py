# -*- coding: utf-8 -*-

from transaction import commit
from Products.CMFCore.utils import getToolByName

from genweb.serveistic.testing import IntegrationTestCase
from genweb.serveistic.tests.fixtures import fixtures
from genweb.serveistic.tests.fixtures import indicators_calculators as serveis
from genweb.serveistic.indicators.calculators import SessionsSourceServei


class TestIndicatorsCalculatorsIntegration(IntegrationTestCase):
    def setUp(self):
        self.portal = self.layer['portal']

    def tearDown(self):
        self._remove_serveis()

    def _remove_serveis(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        self.portal.manage_delObjects(
            [servei.id for servei in catalog(portal_type='serveitic')])
        commit()

    # Test SessionsSourceServei (sss)

    def test_sss_source_re_should_not_include_service_with_empty_url(self):
        fixtures.create_and_publish_content(
            self.portal, serveis.servei_domain_empty)
        commit()
        calculator = SessionsSourceServei(self.portal)
        source_re = calculator._build_filters()
        self.assertEqual('ga:source=~^$', source_re)

    def test_sss_source_re_should_not_include_service_with_none_url(self):
        fixtures.create_and_publish_content(
            self.portal, serveis.servei_domain_none)
        commit()
        calculator = SessionsSourceServei(self.portal)
        source_re = calculator._build_filters()
        self.assertEqual('ga:source=~^$', source_re)

    def test_sss_source_re_should_not_include_service_not_published(self):
        fixtures.create_content(self.portal, serveis.servei_domain_none)
        fixtures.create_content(self.portal, serveis.servei_domain_1)
        commit()
        calculator = SessionsSourceServei(self.portal)
        source_re = calculator._build_filters()
        self.assertEqual('ga:source=~^$', source_re)

    def test_sss_source_re_should_include_service_with_url_and_published(self):
        fixtures.create_and_publish_content(
            self.portal, serveis.servei_domain_1)
        commit()
        calculator = SessionsSourceServei(self.portal)
        source_re = calculator._build_filters()
        self.assertEqual('ga:source=~^domain1\\.com$', source_re)

    def test_sss_source_re_should_only_include_services_if_published_and_with_urls(self):
        fixtures.create_and_publish_content(
            self.portal, serveis.servei_domain_empty)
        fixtures.create_and_publish_content(
            self.portal, serveis.servei_domain_none)
        fixtures.create_and_publish_content(
            self.portal, serveis.servei_domain_1)
        fixtures.create_content(
            self.portal, serveis.servei_domain_2)
        fixtures.create_and_publish_content(
            self.portal, serveis.servei_domain_3)
        commit()

        calculator = SessionsSourceServei(self.portal)
        source_re = calculator._build_filters()
        self.assertEqual(
            'ga:source=~^domain1\\.com$,ga:source=~^domain3\\.com$', source_re)

    def test_sss_source_re_should_be_empty_if_all_services_not_published_or_urls_empty_or_none(self):
        fixtures.create_and_publish_content(
            self.portal, serveis.servei_domain_empty)
        fixtures.create_and_publish_content(
            self.portal, serveis.servei_domain_none)
        fixtures.create_content(
            self.portal, serveis.servei_domain_1)
        commit()

        calculator = SessionsSourceServei(self.portal)
        source_re = calculator._build_filters()
        self.assertEqual('ga:source=~^$', source_re)
