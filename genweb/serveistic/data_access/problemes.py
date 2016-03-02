import logging
import datetime

from genweb.serveistic.ws_client.problems import ClientException

logger = logging.getLogger(name='genweb.serveistic')


def get_sortable_key_by_date(obj, prop_name='data_creacio'):
    """
    Given an object A with a 'prop_name' property with type datetime.date,
    returns a string that can be used to compare A with B, so that
    A < B is true when A.data is older than B.data. If data is None, then
    the oldest possible date is considered.
    """
    getattr(obj, prop_name, None)
    return (getattr(obj, prop_name, None) and
            getattr(obj, prop_name).strftime('%Y%m%d') or
            datetime.datetime(1900, 1, 1).strftime('%Y%m%d'))


class ProblemesDataReporter(object):
    def __init__(self, catalog, client):
        self.catalog = catalog
        self.client = client

    def list_by_product_id(self, product_id, count):
        problemes = []
        try:
            for problema in self.client.list_problems(product_id, count):
                problemes.append({
                    'date_creation':
                        problema.date_creation.strftime('%d/%m/%Y')
                        if problema.date_creation else u'',
                    'topic': problema.topic,
                    'url': problema.url})
        except ClientException as e:
            logger.warning("ClientException: {0}".format(e.message))
            problemes = None
        return problemes

    def list_by_servei_path(self, servei_path, count):
        problemes = []
        for problema in sorted(
            self.catalog.searchResults(
                portal_type="problema",
                path={"query": servei_path, "depth": 2}
                ), key=get_sortable_key_by_date):
            problema_obj = problema.getObject()
            problemes.append({
                'date_creation':
                    problema_obj.data_creacio.strftime('%d/%m/%Y')
                    if problema_obj.data_creacio else u'',
                'topic': problema_obj.title,
                'url': 'problemes/{0}'.format(problema_obj.id)
                })
        return problemes[:count] if count else problemes
