import pytest
import imp

from gocept.pytestlayer import fixture


class LayerModule(pytest.Collector):

    def __init__(self, name, obj, parent, layer):
        self.tcname = name
        self.tcobj = obj
        name = fixture.get_function_fixture_name(layer)
        super(LayerModule, self).__init__('', parent)
        self.layer = layer
        self.obj = self.module_from_layer(layer)

    def module_from_layer(self, layer):
        module = imp.new_module(self.name)
        module.__dict__.update(fixture._create(layer))
        return module

    def collect(self):
        self.session._fixturemanager.parsefactories(self)
        yield collect_with_layer(self.parent, self.tcname, self.tcobj, self.layer)

    def reportinfo(self):
        return self.name, None, 'layermodule'


def collect_with_layer(collector, name, obj, layer):
    fixture_name = fixture.get_function_fixture_name(layer)
    usefixtures = pytest.mark.usefixtures(fixture_name)
    usefixtures(obj)
    py_unittest = get_py_unittest(collector)
    return py_unittest.pytest_pycollect_makeitem(collector, name, obj)


def get_py_unittest(collector):
    return collector.session.config.pluginmanager.getplugin('unittest')
