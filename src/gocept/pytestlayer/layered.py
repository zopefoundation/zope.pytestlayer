import unittest
import pytest
import fixture
import _pytest


class LayeredTestSuite(pytest.Class):

    def collect(self):
        suite = self.obj()
        for item, layer in walk_suite(suite):
            yield LayeredTestCaseInstance(item, self, layer)


class LayeredTestCaseInstance(pytest.Collector):

    def __init__(self, obj, parent, layer):
        super(pytest.Collector, self).__init__('', parent=parent)
        # store testcase instance and layer
        # to pass them to function
        self.obj = obj
        self.layer = layer

    def collect(self):
        yield LayeredTestCaseFunction('runTest', parent=self)

    def reportinfo(self):
        pass


class LayeredTestCaseFunction(_pytest.unittest.TestCaseFunction):

    def __init__(self, name, parent):
        super(LayeredTestCaseFunction, self).__init__(name, parent=parent)
        self.layer = self.parent.layer

    def setup(self):
        self._testcase = self.parent.obj
        if hasattr(self, "_request"):
            # call function fixture (testSetUp)
            fixture_name = fixture.get_function_fixture_name(self.layer)
            self._request.getfuncargvalue(fixture_name)

    def reportinfo(self):
        return 'test_suite', None, self.parent.obj.shortDescription()


def walk_suite(suite):
    if isinstance(suite, unittest.TestSuite):
        has_layer = hasattr(suite, 'layer')
        for item in suite:
            if isinstance(item, unittest.TestCase) and has_layer:
                yield item, suite.layer
            else:
                for result in walk_suite(item):
                    yield result
