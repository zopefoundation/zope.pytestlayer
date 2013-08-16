from .fixture import get_function_name as get_fixture_name
import pytest
import unittest


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
        pytest.mark.usefixtures(get_fixture_name(obj.layer))(obj)
