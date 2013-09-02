from .test import FooLayer
from gocept.pytestlayer.fixture import create


pytest_plugins = ('zopelayer', 'capturelog')
globals().update(create(FooLayer))
