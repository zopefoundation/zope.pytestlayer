from session_fixture.test_core import FooLayer

import zope.pytestlayer.fixture


pytest_plugins = ('zopelayer', )


globals().update(zope.pytestlayer.fixture.create(
    FooLayer,
    session_fixture_name='foo_layer_session',
    class_fixture_name='foo_layer_class',
    function_fixture_name='foo_layer'))
