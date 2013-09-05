from .test import FooLayer, BarLayer
from gocept.pytestlayer.fixture import create


pytest_plugins = ('zopelayer', )
globals().update(create(FooLayer, BarLayer))
