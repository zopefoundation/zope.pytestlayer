import logging
import unittest

log = logging.getLogger('zopelayer')
log.addHandler(logging.StreamHandler())


class FooLayer(object):

    @classmethod
    def setUp(cls):
        log.info('\nsetUp foo')
        cls.layer_foo = 'layer foo'

    @classmethod
    def tearDown(cls):
        log.info('tearDown foo')
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
