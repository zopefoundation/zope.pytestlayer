import types
import unittest
import pytest
import fixture


def query_layered_testsuite(obj):
    if (isinstance(obj, types.FunctionType) and obj.__name__ == 'test_suite'):
        suite = obj()
        if isinstance(suite, unittest.TestSuite):
            return suite


class LayeredTestSuite(pytest.Class):

    def collect(self):
        suite = self.obj()
        for item, layer in walk_suite(suite):
            yield LayeredTestCaseInstance(str(item), item, self, layer)


class LayeredTestCaseInstance(pytest.Collector):

    def __init__(self, name, obj, parent, layer):
        self.name = name
        self.obj = obj
        self.layer = layer
        super(pytest.Collector, self).__init__(name, parent=parent)

    def collect(self):
        py_unittest = get_py_unittest(self)
        yield LayeredTestCaseFunction(
            py_unittest.TestCaseFunction('runTest', parent=self),
            self.layer
        )

    def reportinfo(self):
        pass


class LayeredTestCaseFunction(pytest.Function):

    def __init__(self, context, layer):
        self.context = context
        self.layer = layer

    def __getattr__(self, name):
        return getattr(self.context, name)

    def setup(self):
        self.context._testcase = self.parent.obj
        if hasattr(self, "_request"):
            fixture_name = fixture.get_function_fixture_name(self.layer)
            self._request.getfuncargvalue(fixture_name)

    def reportinfo(self):
        return 'test_suite', None, self.context.parent.obj.shortDescription()


def walk_suite(suite):
    if isinstance(suite, unittest.TestSuite):
        has_layer = hasattr(suite, 'layer')
        for item in suite:
            if isinstance(item, unittest.TestCase) and has_layer:
                yield item, suite.layer
            else:
                for result in walk_suite(item):
                    yield result


def get_py_unittest(collector):
    return collector.session.config.pluginmanager.getplugin('unittest')
