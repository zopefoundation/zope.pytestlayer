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


class PatchedDocTestSuite:

    def __init__(self, suite):
        self._suite = suite

    def __call__(self, *args, **kw):
        result = None
        if args:
            if not isinstance(args[0], str):
                result = args[0]
        return self.run(result)

    def __getattr__(self, name):
        return getattr(self._suite, name)

    def __setattr__(self, name, value):
        if name == '_suite':
            self.__dict__[name] = value
        else:
            setattr(self._suite, name, value)


def DocTestSuite(*args, **kw):
    """A DocTestSuite whose tests are detectable by zope.pytestlayer.

    See https://github.com/zope/zope.pytestlayer/issues/4
    """
    layer = kw.pop('layer', NOOP_LAYER)
    suite = doctest.DocTestSuite(*args, **kw)
    suite.layer = layer
    return PatchedDocTestSuite(suite)


def layered(suite, layer=NOOP_LAYER):
    """XXX
    """
    suite.layer = layer
    return PatchedDocTestSuite(suite)
