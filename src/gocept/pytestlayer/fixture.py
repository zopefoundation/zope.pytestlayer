import re
import time


class ZopeLayerState(object):

    def __init__(self):
        self.current = set()
        self.keep = set()


def timed(request, func, text):
    write = bool(request.config.option.verbose)
    reporter = request.config.pluginmanager.getplugin(
        'terminalreporter')
    if write:
        reporter.ensure_newline()
        reporter.write(text)
        start = time.time()
    func()
    if write:
        time_taken = time.time() - start
        reporter.write("{:.3f}".format(time_taken), green=1, bold=1)
        reporter.write_line(" seconds.")


def class_fixture(request, layer):
    state = request.session.zopelayer_state
    reporter = request.config.pluginmanager.getplugin(
        'terminalreporter')
    layer_name = get_layer_name(layer)

    def setUp():
        layer.setUp()
        state.current.add(layer)

    if layer not in state.current:
        timed(request, setUp, "Set up {} in ".format(layer_name))

    def tearDown():
        layer.tearDown()
        state.current.remove(layer)

    def conditional_teardown():
        if layer not in state.keep:
            timed(request, tearDown, "Tear down {} in ".format(layer_name))

    request.addfinalizer(conditional_teardown)


def function_fixture(request, layer):
    layer.testSetUp()
    request.addfinalizer(layer.testTearDown)


TEMPLATE = """\
import pytest
from gocept.pytestlayer.fixture import (
    class_fixture, function_fixture, LAYERS)

@pytest.fixture(scope='class')
def {class_name}(request{base_class_names}):
    "Depends on {base_class_names}"
    class_fixture(request, LAYERS['{layer_name}'])

@pytest.fixture(scope='function')
def {function_name}(request, {class_name}{base_function_names}):
    "Depends on {base_function_names}"
    function_fixture(request, LAYERS['{layer_name}'])
"""


def get_layer_name(layer):
    return '%s.%s' % (layer.__module__, layer.__name__)


def make_identifier(string):
    # Replaces things between words into underscores:
    return re.sub('\W|^(?=\d)', '_', string)


def get_function_name(layer):
    return 'zope_layer_function_' + make_identifier(get_layer_name(layer))


def get_class_name(layer):
    return 'zope_layer_class_' + make_identifier(get_layer_name(layer))


class Layers(dict):
    """Layers where fixtures are created for."""

    def add(self, layer):
        self[get_layer_name(layer)] = layer

    def __contains__(self, layer_or_layer_name):
        if not isinstance(layer_or_layer_name, basestring):
            layer_name = get_layer_name(layer_or_layer_name)
        else:
            layer_name = layer_or_layer_name
        return super(Layers, self).__contains__(layer_name)


LAYERS = Layers()
LAYERS.add(object)  # We do not need to create a fixture for `object`


def create(*layers):
    """Create fixtures for given layers and their bases."""
    ns = {}
    for layer in layers:
        ns.update(_create_single(layer))
    return ns


def _create_single(layer):
    """Actually create a fixtures for a single layer and its bases."""
    if layer in LAYERS:
        return {}
    LAYERS.add(layer)

    class_name = get_class_name(layer)
    function_name = get_function_name(layer)
    code = TEMPLATE.format(
        layer_name=get_layer_name(layer),
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

    # Recurse into bases:
    ns.update(create(*layer.__bases__))

    return ns
