import doctest
import gocept.runner.testing
import unittest
import zope.app.testing.functional


flags = doctest.ELLIPSIS


def test_suite():
    suite = unittest.TestSuite()
    test = zope.app.testing.functional.FunctionalDocFileSuite(
        'README.rst',
        package='gocept.runner',
        optionflags=flags)
    test.layer = gocept.runner.testing.layer
    suite.addTest(test)

    suite.addTest(doctest.DocFileSuite(
        'appmain.rst',
        'once.rst',
        package='gocept.runner',
        optionflags=flags))

    return suite
