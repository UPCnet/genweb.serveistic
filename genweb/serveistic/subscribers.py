import logging

from five import grok
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent

from genweb.core.indicators import RegistryException, ReporterException
from genweb.serveistic.utilities import serveistic_config
from genweb.serveistic.content.serveitic import IServeiTIC
from genweb.serveistic.indicators.updating import (
    update_indicators,
    update_indicators_if_state)

logger = logging.getLogger(name='genweb.serveistic.indicators')


@grok.subscribe(IServeiTIC, IObjectRemovedEvent)
def update_indicators_on_serveitic_deletion(obj, event):
    try:
        update_indicators_if_state(
            obj, ('published',),
            service=serveistic_config().ws_indicadors_service_id,
            indicator='servei-n')
        logger.info("Indicators were successfully reported")
    except RegistryException as e:
        logger.warning(
            "Error while loading indicator registry ({0})".format(e))
    except ReporterException as e:
        logger.warning("Error while reporting indicators ({0})".format(e))


@grok.subscribe(IServeiTIC, IActionSucceededEvent)
def update_indicators_on_serveitic_review_state_change(obj, event):
    try:
        update_indicators(
            obj,
            service=serveistic_config().ws_indicadors_service_id,
            indicator='servei-n', after_commit=True)
        logger.info("Indicators were successfully reported")
    except RegistryException as e:
        logger.warning(
            "Error while loading indicator registry ({0})".format(e))
    except ReporterException as e:
        logger.warning("Error while reporting indicators ({0})".format(e))

