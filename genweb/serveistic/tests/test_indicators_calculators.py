import unittest
from mock import Mock, patch

from genweb.serveistic.indicators.calculators import SessionsSourceServei


class TestIndicatorsCalculators(unittest.TestCase):
    def setUp(self):
        pass

    # Test build_source_re
    @patch('genweb.serveistic.indicators.calculators.getToolByName')
    def test_bsre_should_return_empty_re_if_no_services(self, mock_getToolByName):
        with patch('genweb.serveistic.indicators.calculators.SessionsSourceServei._build_source_re'):
            calculator = SessionsSourceServei('mock_context')

        with patch('genweb.serveistic.data_access.servei.ServeiDataReporter.list_by_review_state',
                   side_effect=([], )):
            source_re = calculator._build_source_re()
            self.assertEqual('^$', source_re)

    @patch('genweb.serveistic.indicators.calculators.getToolByName')
    def test_bsre_should_return_services_re_if_services(self, mock_getToolByName):
        with patch('genweb.serveistic.indicators.calculators.SessionsSourceServei._build_source_re'):
            calculator = SessionsSourceServei('mock_context')

        with patch('genweb.serveistic.data_access.servei.ServeiDataReporter.list_by_review_state',
                   side_effect=([
                       Mock(website_url='http://domain1.com/a/b/c.html'),
                       Mock(website_url='http://domain2.com/a/b/c.html'),
                            ], )):
            source_re = calculator._build_source_re()
            self.assertEqual('^domain1\\.com|domain2\\.com$', source_re)

    @patch('genweb.serveistic.indicators.calculators.getToolByName')
    def test_bsre_should_return_services_re_if_services_with_url_none(self, mock_getToolByName):
        with patch('genweb.serveistic.indicators.calculators.SessionsSourceServei._build_source_re'):
            calculator = SessionsSourceServei('mock_context')

        with patch('genweb.serveistic.data_access.servei.ServeiDataReporter.list_by_review_state',
                   side_effect=([
                       Mock(website_url='http://domain1.com/a/b/c.html'),
                       Mock(website_url=None),
                       Mock(website_url='http://domain2.com/a/b/c.html'),
                            ], )):
            source_re = calculator._build_source_re()
            self.assertEqual('^domain1\\.com|domain2\\.com$', source_re)

    @patch('genweb.serveistic.indicators.calculators.getToolByName')
    def test_bsre_should_return_services_re_if_services_with_url_empty(self, mock_getToolByName):
        with patch('genweb.serveistic.indicators.calculators.SessionsSourceServei._build_source_re'):
            calculator = SessionsSourceServei('mock_context')

        with patch('genweb.serveistic.data_access.servei.ServeiDataReporter.list_by_review_state',
                   side_effect=([
                       Mock(website_url='http://domain1.com/a/b/c.html'),
                       Mock(website_url=''),
                       Mock(website_url='http://domain2.com/a/b/c.html'),
                            ], )):
            source_re = calculator._build_source_re()
            self.assertEqual('^domain1\\.com|domain2\\.com$', source_re)

    # Test extract_url_domain_re
    @patch('genweb.serveistic.indicators.calculators.SessionsSourceServei._build_source_re')
    def test_eud_should_remove_protocol(self, mock_build_source_re):
        calculator = SessionsSourceServei('mock_context')
        domain = calculator._extract_url_domain_re('http://domain.com')
        self.assertEqual('domain\\.com', domain)
        domain = calculator._extract_url_domain_re('ftp://domain.com')
        self.assertEqual('domain\\.com', domain)

    @patch('genweb.serveistic.indicators.calculators.SessionsSourceServei._build_source_re')
    def test_eud_should_remove_path_after_domain(self, mock_build_source_re):
        calculator = SessionsSourceServei('mock_context')
        domain = calculator._extract_url_domain_re('domain.com/1/3/4.html')
        self.assertEqual('domain\\.com', domain)

    @patch('genweb.serveistic.indicators.calculators.SessionsSourceServei._build_source_re')
    def test_eud_should_remove_backslash_after_domain(self, mock_build_source_re):
        calculator = SessionsSourceServei('mock_context')
        domain = calculator._extract_url_domain_re('domain.com/')
        self.assertEqual('domain\\.com', domain)

    @patch('genweb.serveistic.indicators.calculators.SessionsSourceServei._build_source_re')
    def test_eud_should_remove_protocol_and_path(self, mock_build_source_re):
        calculator = SessionsSourceServei('mock_context')
        domain = calculator._extract_url_domain_re(
            'http://domain.com/1/two/3.html')
        self.assertEqual('domain\\.com', domain)
