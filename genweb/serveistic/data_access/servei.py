class ServeiDataReporter(object):
    def __init__(self, catalog):
        self.catalog = catalog

    def list_by_review_state(self, review_state):
        return self.list(review_state=review_state)

    def list(self, review_state=None):
        filters = dict(
            portal_type='serveitic')
        if review_state:
            filters['review_state'] = review_state
        return self.catalog.searchResults(filters)
