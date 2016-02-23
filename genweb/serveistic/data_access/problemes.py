import logging

from genweb.serveistic.ws_client.problems import ClientException

logger = logging.getLogger(name='genweb.serveistic')


class ProblemesDataReporter(object):
    def __init__(self, client):
        self.client = client

    def list_by_product_id(self, product_id, count=None):
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
