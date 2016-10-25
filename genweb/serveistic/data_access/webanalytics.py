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

    def __init__(self, json_keyfile_dict):
        self._service = GoogleAnalyticsReporter.get_service(
            api_name=GoogleAnalyticsReporter.API_NAME,
            api_version=GoogleAnalyticsReporter.API_VERSION,
            scope=GoogleAnalyticsReporter.SCOPE,
            json_keyfile_dict=json_keyfile_dict)

    @staticmethod
    def get_service(api_name, api_version, scope, json_keyfile_dict):
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                json_keyfile_dict, scopes=scope)
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
