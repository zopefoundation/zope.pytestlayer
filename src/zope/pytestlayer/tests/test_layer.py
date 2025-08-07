from zope.pytestlayer import fixture


class LayerClass:
    pass


layer = LayerClass()


def test_get_layer_name_accounts_layers_importable_by_an_arbitrary_name():
    assert 'pytestlayer.tests.test_layer.layer' == \
        fixture.get_layer_name(layer)
