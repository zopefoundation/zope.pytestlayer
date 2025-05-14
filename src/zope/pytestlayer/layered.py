import unittest

import _pytest.unittest
import pytest

from zope.pytestlayer import fixture


class LayeredTestSuite(pytest.Class):

    def collect(self):
        suite = self.obj()
        for item, layer in walk_suite(suite):
            fixture.parsefactories(self.parent, layer)
            yield LayeredTestCaseInstance.from_parent(
                parent=self, obj=item, layer=layer)


class LayeredTestCaseInstance(_pytest.unittest.UnitTestCase):

    @classmethod
    def from_parent(cls, parent, obj, layer, **kw):
        testname = repr(obj)  # fantastic doctest API :(
        instance = super(pytest.Collector, cls).from_parent(
            parent=parent, name=testname)
        # store testcase instance and layer
        # to pass them to function
        instance.obj = obj
        instance.layer = layer
        instance.extra_keyword_matches.update(fixture.get_keywords(layer))
        return instance

    def collect(self):
        yield LayeredTestCaseFunction.from_parent(parent=self, name='runTest')

    def reportinfo(self):
        pass


class LayeredTestCaseFunction(_pytest.unittest.TestCaseFunction):

    _instance = None

    @classmethod
    def from_parent(cls, parent, name, **kw):
        description = get_description(parent)
        keywords = get_keywords(description)
        function = super().from_parent(
            parent=parent,
            name=name,
            keywords=keywords,
        )
        function.layer = function.parent.layer
        function.tc_description = description
        function._instance = function.parent.obj
        return function

    def setup(self):
        # This is actually set in the base class, but as we want to modify
        # `self._request` in our way, we do not make a super call here.
        # It has to be None or a bound method to be called during tearDown.
        self._explicit_tearDown = None
        if hasattr(self, "_request"):
            # call function fixture (testSetUp)
            fixture_name = fixture.get_fixture_name(
                self.layer, scope='function')
            self._request.getfixturevalue(fixture_name)

    def teardown(self):
        _instance = self._instance
        super().teardown()
        # Do not die with a meaningless error message when rerunning doctests:
        self._instance = _instance

    def reportinfo(self):
        return ('test_suite', None, self.tc_description)


def get_description(collector):
    description = str(collector.obj)
    fspath = collector.session.fspath.strpath
    return description.replace(fspath, '')


def get_keywords(description):
    words = [word for word in description.split()]
    keywords = {}
    for word in words:
        keywords[word] = True
    return keywords


def walk_suite(suite):
    if isinstance(suite, unittest.TestSuite):
        has_layer = hasattr(suite, 'layer')
        for item in suite:
            if isinstance(item, unittest.TestCase) and has_layer:
                fixture.raise_if_bad_layer(suite.layer)
                yield item, suite.layer
            else:
                yield from walk_suite(item)
