import re
import zope.dottedname.resolve


def fixture(request, layer, scope):
    if scope == 'class':
        setup, teardown = 'setUp', 'tearDown'
    elif scope == 'function':
        setup, teardown = 'testSetUp', 'testTearDown'
    getattr(layer, setup)()
    request.addfinalizer(getattr(layer, teardown))


TEMPLATE = """\
import pytest
from gocept.pytestlayer.fixture import fixture, seen

@pytest.fixture(scope='class')
def {class_name}(request{base_class_names}):
    "Depends on {base_class_names}"
    fixture(request, seen['{layer_name}'], 'class')

@pytest.fixture(scope='function')
def {function_name}(request, {class_name}{base_function_names}):
    "Depends on {base_function_names}"
    fixture(request, seen['{layer_name}'], 'function')
"""


def get_layer_name(layer):
    return '%s.%s' % (layer.__module__, layer.__name__)

def make_identifier(string):
    # Replaces things between words into underscores:
    return re.sub('\W|^(?=\d)','_', string)

def get_function_name(layer):
    return 'zope_layer_function_' + make_identifier(get_layer_name(layer))


def get_class_name(layer):
    return 'zope_layer_class_' + make_identifier(get_layer_name(layer))


seen = {'__builtin__.object': object}


def create(layer):
    layer_name = get_layer_name(layer)
    if layer_name in seen:
        return {}
    seen[layer_name] = layer

    class_name = get_class_name(layer)
    function_name = get_function_name(layer)
    code = TEMPLATE.format(
        layer_name=layer_name,
        class_name=class_name,
        function_name=function_name,
        base_class_names=''.join(
            ', ' + get_class_name(base)
            for base in layer.__bases__ if base is not object),
        base_function_names=''.join(
            ', ' + get_function_name(base)
            for base in layer.__bases__ if base is not object),
    )

    ns = {}
    exec code in ns

    for base in layer.__bases__:
        ns.update(create(base))

    return ns
