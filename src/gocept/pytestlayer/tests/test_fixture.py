from .. import fixture

class Layer(object):
    pass

def test_create_accepts_dotted_names_of_layers():
    assert [
        'zope_layer_class_gocept_pytestlayer_tests_test_fixture_Layer',
        'zope_layer_function_gocept_pytestlayer_tests_test_fixture_Layer'] == \
        fixture.create('gocept.pytestlayer.tests.test_fixture.Layer').keys()
