import pathlib


def pytest_ignore_collect(collection_path: pathlib.Path, config):
    if str(collection_path).endswith('fixture'):
        return True
