from custom_fixture_name.test_core import FooLayer
import gocept.pytestlayer.fixture


pytest_plugins = ('zopelayer', )


globals().update(gocept.pytestlayer.fixture.create(
    FooLayer,
    class_fixture_name='foo_layer_class',
    function_fixture_name='foo_layer'))
