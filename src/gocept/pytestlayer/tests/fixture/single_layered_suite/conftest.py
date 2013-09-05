from .test import FooLayer
from gocept.pytestlayer.fixture import create


pytest_plugins = ('zopelayer', )
globals().update(create(FooLayer))
