from .test import FooLayer, BarLayer, FooBarLayer
from gocept.pytestlayer.fixture import create


pytest_plugins = ('zopelayer', 'capturelog')
globals().update(create(FooLayer, BarLayer, FooBarLayer))
