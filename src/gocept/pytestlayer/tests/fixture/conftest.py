def pytest_ignore_collect(path, config):
    if path.strpath.endswith('fixture'):
        return True
