import httplib2

from apiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import HttpAccessTokenRefreshError


class GoogleAnalyticsReporterException(Exception):
    pass


class GoogleAnalyticsReporter(object):
    API_NAME = 'analytics'
    API_VERSION = 'v3'
    SCOPE = ['https://www.googleapis.com/auth/analytics.readonly']

    def __init__(self, service_account_email, key_file_location):
        self._service = GoogleAnalyticsReporter.get_service(
            api_name=GoogleAnalyticsReporter.API_NAME,
            api_version=GoogleAnalyticsReporter.API_VERSION,
            scope=GoogleAnalyticsReporter.SCOPE,
            service_account_email=service_account_email,
            key_file_location=key_file_location)

    @staticmethod
    def get_service(api_name, api_version, scope, service_account_email,
                    key_file_location):
        try:
            credentials = ServiceAccountCredentials.from_p12_keyfile(
                service_account_email, key_file_location, scopes=scope)
            return build(
                api_name,
                api_version,
                http=credentials.authorize(httplib2.Http()))
        except Exception as e:
            raise GoogleAnalyticsReporterException(
                "Cannot build service ({0})".format(e))

    def query(self, query):
        try:
            return self._service.data().ga().get(**query).execute()
        except (TypeError, HttpAccessTokenRefreshError, HttpError) as e:
            raise GoogleAnalyticsReporterException(
                "Error when executing query ({0})".format(e))
