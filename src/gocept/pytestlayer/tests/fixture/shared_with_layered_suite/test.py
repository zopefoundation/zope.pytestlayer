import logging
import doctest
import unittest
from plone.testing import layered


log = logging.getLogger('zopelayer')
log.addHandler(logging.StreamHandler())


class FooLayer(object):

    @classmethod
    def setUp(cls):
        cls.layer_foo = 'layer foo'

    @classmethod
    def tearDown(cls):
        del cls.layer_foo

    @classmethod
    def testSetUp(cls):
        log.info('testSetUp foo')
        cls.test_foo = 'test foo'

    @classmethod
    def testTearDown(cls):
        log.info('\ntestTearDown foo')
        del cls.test_foo


class FooTest(unittest.TestCase):

    layer = FooLayer

    def test_dummy(self):
        self.assertEqual('layer foo', self.layer.layer_foo)
        self.assertEqual('test foo', self.layer.test_foo)


def test_suite():
    suite = unittest.TestSuite()

    OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'doctest.txt',
                optionflags=OPTIONFLAGS,
            ),
            layer=FooLayer,
        ),
    ])
    return suite
