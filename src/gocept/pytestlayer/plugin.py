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


def pytest_sessionstart(session):
    session.zopelayer_state = fixture.ZopeLayerState()


def pytest_runtest_teardown(item, nextitem):
    state = item.session.zopelayer_state

    if hasattr(nextitem, 'cls') and hasattr(nextitem.cls, 'layer'):
        state.keep = state.current & set(inspect.getmro(nextitem.cls.layer))
    else:
        state.keep.clear()
