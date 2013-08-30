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
    layer = query_layer(obj)
    if layer is not None:
        raise_if_unknown_layer(layer)
        fixture_name = fixture.get_function_fixture_name(layer)
        pytest.mark.usefixtures(fixture_name)(obj)


def query_layer(obj):
    try:
        isunit = issubclass(obj, unittest.TestCase)
    except TypeError:
        isunit = False
    if isunit and hasattr(obj, 'layer'):
        return obj.layer


def raise_if_unknown_layer(layer):
    'complaining about unregistered layers'

    if layer not in fixture.LAYERS:
        layer_name = fixture.get_layer_name(layer)
        if layer.__class__ in fixture.LAYERS:
            raise RuntimeError(
                "The layer `%s` is not found its module's namespace." %
                layer_name)
        raise RuntimeError(
            'There is no fixture for layer `%(layer_name)s`.\n'
            'You have to create it using:\n'
            '    from gocept.pytestlayer import fixture\n'
            '    globals().update(fixture.create("%(layer_name)s"))\n'
            'in `conftest.py`.' % {'layer_name': layer_name})


def pytest_collection_modifyitems(session, config, items):
    items_by_layer = {}
    layers_in_order = []
    for item in items:
        if hasattr(item, 'cls') and hasattr(item.cls, 'layer'):
            layer = item.cls.layer
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
        state.keep = state.current & set(inspect.getmro(nextitem.cls.layer))
    else:
        state.keep.clear()


def pytest_ignore_collect(path, config):
    for arg in config.args:
        if arg.endswith('/gocept.pytestlayer'):
            # We are running our own tests, so do not ignore anything:
            return
    if 'gocept/pytestlayer/tests' in path.strpath:
        # Ignore our own tests when testing another package because we need
        # `capturelog` which is only defined as a test dependency of
        # gocept.pytestlayer:
        return True
