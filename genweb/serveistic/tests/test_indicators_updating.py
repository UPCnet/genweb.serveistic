import unittest

from genweb.core.indicators import ReporterException
from genweb.serveistic.indicators.updating import get_data_to_report


class TestIndicatorsUpdating(unittest.TestCase):
    def setUp(self):
        pass

    # Test get_data_to_report (gdtr)
    def test_gdtr_should_return_registry_if_no_service_specified(self):
        result = get_data_to_report('registry', service=None, indicator=None)
        self.assertEqual('registry', result)

    def test_gdtr_should_return_registry_service_if_no_indicator_specified(self):
        registry = {'service_id': 'service_mock'}
        result = get_data_to_report(registry, 'service_id', None)
        self.assertEqual('service_mock', result)

    def test_gdtr_should_return_registry_service_indicator_if_all_specified(self):
        service_mock = {'indicator_id': 'indicator_mock'}
        registry = {'service_id': service_mock}
        result = get_data_to_report(registry, 'service_id', 'indicator_id')
        self.assertEqual('indicator_mock', result)

    def test_gdtr_should_raise_if_no_indicator_specified_and_service_not_in_registry(self):
        registry = {}
        with self.assertRaises(ReporterException) as e:
            get_data_to_report(registry, 'service_id', None)
        self.assertEqual(
            "Service 'service_id' was not found in registry",
            e.exception.message)

    def test_gdtr_should_raise_if_all_specified_and_service_not_in_registry(self):
        registry = {}
        with self.assertRaises(ReporterException) as e:
            get_data_to_report(registry, 'service_id', 'indicator_id')
        self.assertEqual(
            "Indicator 'indicator_id' of service 'service_id' was "
            "not found in registry",
            e.exception.message)

    def test_gdtr_should_raise_if_all_specified_and_indicator_not_in_service(self):
        service_mock = {}
        registry = {'service_id': service_mock}
        with self.assertRaises(ReporterException) as e:
            get_data_to_report(registry, 'service_id', 'indicator_id')
        self.assertEqual(
            "Indicator 'indicator_id' of service 'service_id' was "
            "not found in registry",
            e.exception.message)
