from zope.pytestlayer.doctest import DocTestSuite


class Dummy:
    """This class has a doctest.

    It tests the workaround for
    https://github.com/zope/zope.pytestlayer/issues/4

    >>> print('foobar.')
    foobar.
    """


def test_suite():
    return DocTestSuite('zope.pytestlayer.tests.test_doctest')
