from DateTime.DateTime import DateTime


class NotificacioDataReporter(object):
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

    def list_by_servei(self, servei):
        results = []
        notificacions = self.catalog.searchResults(
            portal_type='notificaciotic',
            sort_on='effective',
            sort_order='reverse',
            review_state='published',
            path={
                'query': self.get_path(servei)
            })
        for notificacio in notificacions:
            results.append({
                "data": DateTime(notificacio.effective).strftime('%d/%m/%Y'),
                "titol": notificacio.Title,
                "descripcio": notificacio.Description,
                "url": notificacio.getURL()})
        return results
