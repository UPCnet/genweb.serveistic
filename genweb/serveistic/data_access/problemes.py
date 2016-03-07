import logging

from genweb.serveistic.ws_client.problems import ClientException

logger = logging.getLogger(name='genweb.serveistic')


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
                        if problema.date_creation else u'-',
                    'topic': problema.topic,
                    'url': problema.url})
        except ClientException as e:
            logger.warning("ClientException: {0}".format(e.message))
            problemes = None
        return problemes

    def list_by_servei_path(self, servei_path, count):
        problemes = []
        for problema in self.catalog.searchResults(
                portal_type="problema",
                path={"query": servei_path, "depth": 2}):
            problema_obj = problema.getObject()
            problemes.append({
                'date_creation':
                    problema_obj.data_creacio.strftime('%d/%m/%Y')
                    if problema_obj.data_creacio else u'-',
                'topic': problema_obj.title,
                'url': problema_obj.url if problema_obj.url else
                'problemes/{0}'.format(problema_obj.id)
                })
        problemes = sorted(
            problemes,
            key=lambda x: x['date_creation'],
            reverse=True)
        return problemes[:count] if count else problemes
