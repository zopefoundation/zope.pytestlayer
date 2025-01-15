import unittest

from zope.pytestlayer.testing import log_to_terminal


class FooLayer:

    @classmethod
    def setUp(cls):
        cls.layer_foo = 'layer foo'

    @classmethod
    def tearDown(cls):
        del cls.layer_foo

    @classmethod
    def testSetUp(cls):
        log_to_terminal(cls.pytest_request, 'testSetUp foo')
        cls.test_foo = 'test foo'

    @classmethod
    def testTearDown(cls):
        log_to_terminal(cls.pytest_request, 'testTearDown foo')
        del cls.test_foo


def test_can_access_layer_via_fixture(foo_layer):
    assert 'layer foo' == foo_layer.layer_foo
    assert 'test foo' == foo_layer.test_foo


class FooTest(unittest.TestCase):

    layer = FooLayer

    def test_accesses_fixture_with_generated_name_for_layer(self):
        self.assertEqual('layer foo', self.layer.layer_foo)
        self.assertEqual('test foo', self.layer.test_foo)
