import contextlib
import pytest
import re
import time
import zope.dottedname.resolve


class ZopeLayerState(object):

    def __init__(self):
        self.current = set()
        self.keep = set()


@contextlib.contextmanager
def timer(request, text):
    verbose = request.config.option.verbose > 0
    reporter = request.config.pluginmanager.getplugin('terminalreporter')
    if verbose:
        reporter.ensure_newline()
        reporter.write(text)
        start = time.time()
    yield
    if verbose:
        time_taken = time.time() - start
        reporter.write("{:.3f}".format(time_taken), green=1, bold=1)
        reporter.write_line(" seconds.")


def class_fixture(request, layer):
    state = request.session.zopelayer_state
    layer_name = get_layer_name(layer)

    if layer not in state.current:
        if hasattr(layer, 'setUp'):
            with timer(request, "Set up {} in ".format(layer_name)):
                layer.setUp()
            state.current.add(layer)

    def conditional_teardown():
        if layer not in state.keep:
            if hasattr(layer, 'tearDown'):
                with timer(request, "Tear down {} in ".format(layer_name)):
                    layer.tearDown()
                state.current.remove(layer)

    request.addfinalizer(conditional_teardown)


def function_fixture(request, layer):
    if hasattr(layer, 'testSetUp'):
        layer.testSetUp()

    if hasattr(layer, 'testTearDown'):
        request.addfinalizer(layer.testTearDown)


TEMPLATE = """\
@pytest.fixture(scope='class')
def {class_name}(request{base_class_names}):
    "Depends on {base_class_names}"
    class_fixture(request, layer)

@pytest.fixture(scope='function')
def {function_name}(request, {class_name}{base_function_names}):
    "Depends on {base_function_names}"
    function_fixture(request, layer)
"""


def get_layer_name(layer):
    module = zope.dottedname.resolve.resolve(layer.__module__)
    for key, value in module.__dict__.iteritems():
        if value is layer:
            name = key
            break
    else:
        # As per zope.testrunner conventions, a layer is assumed to have a
        # __name__ even if it's not a class.
        name = layer.__name__
    return '%s.%s' % (layer.__module__, name)


def make_identifier(string):
    # Replaces things between words into underscores:
    return re.sub('\W|^(?=\d)', '_', string)


def get_function_name(layer):
    return 'zope_layer_function_{}_{}'.format(
        make_identifier(get_layer_name(layer)),
        id(layer))


def get_class_name(layer):
    return 'zope_layer_class_{}_{}'.format(
        make_identifier(get_layer_name(layer)),
        id(layer))


LAYERS = set()
LAYERS.add(object)  # We do not need to create a fixture for `object`


def create(*layers):
    """Create fixtures for given layers and their bases."""
    ns = {}
    for layer in layers:
        if isinstance(layer, basestring):
            layer = zope.dottedname.resolve.resolve(layer)
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
        class_name=class_name,
        function_name=function_name,
        base_class_names=''.join(
            ', ' + get_class_name(base)
            for base in layer.__bases__ if base is not object),
        base_function_names=''.join(
            ', ' + get_function_name(base)
            for base in layer.__bases__ if base is not object),
    )

    globs = dict(
        pytest=pytest,
        class_fixture=class_fixture,
        function_fixture=function_fixture,
        layer=layer,
    )
    ns = {}
    exec code in globs, ns

    # Recurse into bases:
    ns.update(create(*layer.__bases__))

    return ns
