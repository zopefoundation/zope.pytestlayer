from gocept.pytestlayer import fixture


class LayerClass(object):
    pass


layer = LayerClass()


def test_get_layer_name_accounts_layers_importable_by_an_arbitrary_name():
    assert 'gocept.pytestlayer.tests.test_layer.layer' == \
        fixture.get_layer_name(layer)
