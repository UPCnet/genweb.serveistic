

class BannerDataReporter(object):
    def __init__(self, catalog):
        self.catalog = catalog

    def get_path(self, obj):
        """
        Return a Plone object's path tentatively.
        """
        if 'getPath' in dir(obj):
            return obj.getPath()
        elif 'getPhysicalPath' in dir(obj):
            return '/'.join(obj.getPhysicalPath())
        else:
            return None

    def list_by_servei(self, servei, count=None):
        results = self.catalog.searchResults(
            portal_type='Banner',
            review_state=('published', 'intranet'),
            path={'query': self.get_path(servei) + '/banners'},
            sort_on='getObjPositionInParent')
        return results[:count] if count else results

    def list_by_path(self, path, count=None):
        results = self.catalog.searchResults(
            portal_type='Banner',
            review_state=('published', 'intranet'),
            path={'query': path},
            sort_on='getObjPositionInParent')
        return results[:count] if count else results
