from five import grok
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent

from genweb.serveistic.utilities import serveistic_config
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.indicators.updating import (
    update_indicators,
    update_indicators_if_state)


@grok.subscribe(IServeiTIC, IObjectRemovedEvent)
def update_indicators_on_serveitic_deletion(obj, event):
    update_indicators_if_state(
        obj, ('published',),
        service=serveistic_config().ws_indicadors_service_id,
        indicator='servei-n')


@grok.subscribe(IServeiTIC, IActionSucceededEvent)
def update_indicators_on_serveitic_review_state_change(obj, event):
    update_indicators(
        obj,
        service=serveistic_config().ws_indicadors_service_id,
        indicator='servei-n')
