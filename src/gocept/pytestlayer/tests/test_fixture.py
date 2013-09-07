from .. import fixture


class Layer(object):
    pass


def test_create_accepts_dotted_names_of_layers():
    fixtures = sorted(fixture._create(
        'gocept.pytestlayer.tests.test_fixture.Layer').keys())
    assert 2 == len(fixtures)
    assert fixtures[0].startswith(
        'zope_layer_class_gocept_pytestlayer_tests_test_fixture_Layer_')
    assert fixtures[1].startswith(
        'zope_layer_function_gocept_pytestlayer_tests_test_fixture_Layer_')
