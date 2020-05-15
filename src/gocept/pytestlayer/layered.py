from gocept.pytestlayer import fixture
import unittest
import pytest
import _pytest


class LayeredTestSuite(pytest.Class):

    def collect(self):
        suite = self.obj()
        for item, layer in walk_suite(suite):
            fixture.parsefactories(self.parent, layer)
            yield LayeredTestCaseInstance(item, self, layer)


class LayeredTestCaseInstance(pytest.Collector):

    def __init__(self, obj, parent, layer):
        testname = repr(obj)  # fantastic doctest API :(
        super(pytest.Collector, self).__init__(testname, parent=parent)
        # store testcase instance and layer
        # to pass them to function
        self.obj = obj
        self.layer = layer
        self.extra_keyword_matches.update(fixture.get_keywords(layer))

    def collect(self):
        yield LayeredTestCaseFunction('runTest', parent=self)

    def reportinfo(self):
        pass


class LayeredTestCaseFunction(_pytest.unittest.TestCaseFunction):

    def __init__(self, name, parent):
        description = get_description(parent)
        keywords = get_keywords(description)
        super(LayeredTestCaseFunction, self).__init__(
            name, parent=parent,
            keywords=keywords
        )
        self.layer = self.parent.layer
        self.tc_description = description
        self._testcase = self.parent.obj

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
        _testcase = self._testcase
        super(LayeredTestCaseFunction, self).teardown()
        # Do not die with a meaningless error message when rerunning doctests:
        self._testcase = _testcase

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
                for result in walk_suite(item):
                    yield result
