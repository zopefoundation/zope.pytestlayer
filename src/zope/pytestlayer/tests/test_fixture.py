from .. import fixture


class Layer:
    pass


def test_create_accepts_dotted_names_of_layers():
    fixtures = sorted(fixture.create(
        'zope.pytestlayer.tests.test_fixture.Layer').keys())
    assert 3 == len(fixtures)
    assert fixtures[0].startswith(
        'zope_layer_class_zope_pytestlayer_tests_test_fixture_Layer_')
    assert fixtures[1].startswith(
        'zope_layer_function_zope_pytestlayer_tests_test_fixture_Layer_')
    assert fixtures[2].startswith(
        'zope_layer_session_zope_pytestlayer_tests_test_fixture_Layer_')
