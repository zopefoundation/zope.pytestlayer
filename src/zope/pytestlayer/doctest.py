import doctest


class NoOpLayer:
    """Layer needed for zope.pytestlayer to find and run doctests.

    See https://github.com/zope/zope.pytestlayer/issues/4
    """

    __name__ = 'NoOpLayer'
    __bases__ = ()

    def setUp(self):
        pass

    def tearDown(self):
        pass


NOOP_LAYER = NoOpLayer()


def DocTestSuite(*args, **kw):
    """A DocTestSuite whose tests are detectable by zope.pytestlayer.

    See https://github.com/zope/zope.pytestlayer/issues/4
    """
    layer = kw.pop('layer', NOOP_LAYER)
    suite = doctest.DocTestSuite(*args, **kw)
    suite.layer = layer
    return suite
