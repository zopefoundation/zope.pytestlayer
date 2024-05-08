import types
import unittest

import pytest

from zope.pytestlayer import fixture
from zope.pytestlayer import layered

from ._compat import getmro


@pytest.mark.tryfirst
def pytest_pycollect_makeitem(collector, name, obj):
    # this works because of two things:
    # * this plugin is called before the pytest unittest collector (if it
    #   wasn't, it wouldn't be called at all after the pytest collector has
    #   detected a unittest test case)
    # * usefixtures works in-place

    suite = query_testsuite(obj)
    if suite is not None:
        return layered.LayeredTestSuite.from_parent(
            parent=collector, name=name)
    else:
        layer = query_layer(obj)
        if layer is not None:
            fixture.parsefactories(collector, layer)
            return collect_with_layer(collector, name, obj, layer)


def query_testsuite(obj):
    if (isinstance(obj, types.FunctionType) and obj.__name__ == 'test_suite'):
        suite = obj()
        if isinstance(suite, unittest.TestSuite):
            return suite


def query_layer(obj):
    if has_layer(obj):
        layer = obj.layer
        fixture.raise_if_bad_layer(layer)
        return layer


def has_layer(obj):
    try:
        isunit = issubclass(obj, unittest.TestCase)
    except TypeError:
        isunit = False
    return isunit and hasattr(obj, 'layer')


def pytest_collection_modifyitems(session, config, items):
    items_by_layer = {}
    layers_in_order = []
    for item in items:
        if hasattr(item, 'cls') and hasattr(item.cls, 'layer'):
            layer = item.cls.layer
            layers_in_order.append(layer)
        elif hasattr(item, 'layer'):
            layer = item.layer
            layers_in_order.append(layer)
        else:
            layer = None
        items_by_layer.setdefault(layer, []).append(item)
    ordered_layers = order_by_bases(layers_in_order)
    items[:] = items_by_layer.get(None, [])
    for layer in ordered_layers:
        items.extend(items_by_layer.get(layer, []))


def order_by_bases(layers):
    """Order the layers from least to most specific (bottom to top)
    """
    gathered = []
    for layer in layers:
        gather_layers(layer, gathered)
    seen = set()
    result = []
    for layer in gathered:
        if layer not in seen:
            seen.add(layer)
            if layer in layers:
                result.append(layer)
    return result


def gather_layers(layer, result):
    for b in layer.__bases__:
        gather_layers(b, result)
    if layer is not object:
        result.append(layer)


def pytest_sessionstart(session):
    session.zopelayer_state = fixture.ZopeLayerState()


def pytest_runtest_teardown(item, nextitem):
    state = item.session.zopelayer_state

    if hasattr(nextitem, 'cls') and hasattr(nextitem.cls, 'layer'):
        state.keep = state.current & set(getmro(nextitem.cls.layer))
    elif hasattr(nextitem, 'layer'):
        state.keep = state.current & set(getmro(nextitem.layer))
    else:
        state.keep.clear()


def collect_with_layer(collector, name, obj, layer):
    fixture_name = fixture.LAYERS.get(layer, {}).get(
        'function', fixture.get_fixture_name(layer, 'function'))
    usefixtures = pytest.mark.usefixtures(fixture_name)
    usefixtures(obj)
    py_unittest = get_py_unittest(collector)
    result = py_unittest.pytest_pycollect_makeitem(collector, name, obj)
    result.extra_keyword_matches.update(fixture.get_keywords(layer))
    return result


def get_py_unittest(collector):
    return collector.session.config.pluginmanager.getplugin('unittest')
