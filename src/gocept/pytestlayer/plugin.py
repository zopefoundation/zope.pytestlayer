from gocept.pytestlayer import fixture
import inspect
import pytest
import unittest


@pytest.mark.tryfirst
def pytest_pycollect_makeitem(collector, name, obj):
    # this works because of two things:
    # * this plugin is called before the pytest unittest collector (if it
    #   wasn't, it wouldn't be called at all after the pytest collector has
    #   detected a unittest test case)
    # * usefixtures works in-place
    # * as long as we return None the original unittest collector is called
    try:
        isunit = issubclass(obj, unittest.TestCase)
    except TypeError:
        isunit = False
    if isunit and hasattr(obj, 'layer'):
        if obj.layer not in fixture.LAYERS:
            raise RuntimeError(
                'There is no fixture for layer `%(layer_name)s`.\n'
                'You have to create it using:\n'
                'globals().update(gocept.pytestlayer.fixture.create('
                '%(layer_name)s)\n'
                'in `conftest.py`.' % {
                    'layer_name': fixture.get_layer_name(obj.layer)})
        pytest.mark.usefixtures(fixture.get_function_name(obj.layer))(obj)


def pytest_collection_modifyitems(session, config, items):
    items_by_layer = {}
    for item in items:
        if hasattr(item, 'cls') and hasattr(item.cls, 'layer'):
            layer = item.cls.layer
        else:
            layer = None
        items_by_layer.setdefault(layer, []).append(item)
    ordered_layers = order_by_bases(filter(bool, items_by_layer))
    items[:] = items_by_layer.get(None, [])
    for layer in ordered_layers:
        items.extend(items_by_layer.get(layer, []))


def order_by_bases(layers):
    """Order the layers from least to most specific (bottom to top)
    """
    gathered = []
    for layer in reversed(layers):
        gather_layers(layer, gathered)
    gathered.reverse()
    seen = set()
    result = []
    for layer in gathered:
        if layer not in seen:
            seen.add(layer)
            if layer in layers:
                result.append(layer)
    return result


def gather_layers(layer, result):
    if layer is not object:
        result.append(layer)
    for b in layer.__bases__:
        gather_layers(b, result)


def pytest_sessionstart(session):
    session.zopelayer_state = fixture.ZopeLayerState()


def pytest_runtest_teardown(item, nextitem):
    state = item.session.zopelayer_state

    if hasattr(nextitem, 'cls') and hasattr(nextitem.cls, 'layer'):
        state.keep = state.current & set(inspect.getmro(nextitem.cls.layer))
    else:
        state.keep.clear()
