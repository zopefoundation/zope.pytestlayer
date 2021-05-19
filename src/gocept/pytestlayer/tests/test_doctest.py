from gocept.pytestlayer.doctest import DocTestSuite


class Dummy:
    """This class has a doctest.

    It tests the workaround for
    https://github.com/gocept/gocept.pytestlayer/issues/4

    >>> print('foobar.')
    foobar.
    """


def test_suite():
    return DocTestSuite('gocept.pytestlayer.tests.test_doctest')
