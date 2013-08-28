from .test import FooBarLayer
from gocept.pytestlayer.fixture import create


globals().update(create(FooBarLayer))
