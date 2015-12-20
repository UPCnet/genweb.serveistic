from five import grok
from plone.indexer import indexer
from genweb.serveistic.content.notificaciotic import INotificacioTIC


@indexer(INotificacioTIC)
def notifTipus(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``context.tipus`` value and index it.
    """
    return context.tipus
grok.global_adapter(notifTipus, name='tipus')
