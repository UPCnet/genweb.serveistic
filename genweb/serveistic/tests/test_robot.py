import unittest

import robotsuite
from genweb.serveistic.testing import ROBOT_TESTING
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('./robot/'
                'test_serveistic_is_installed.robot'),
                layer=ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite('./robot/'
                'test_add_servei.robot'),
                layer=ROBOT_TESTING),
    ])
    return suite
