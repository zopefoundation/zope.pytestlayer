import os.path
import subprocess
import sys


def run_pytest(name):
    process = subprocess.Popen(
        [sys.argv[0], '-s', '-v',
         os.path.join(os.path.dirname(__file__), 'fixture', name, 'test.py')],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    raw_output = process.stdout.read()
    return [line.rstrip() + '\n' for line in raw_output.splitlines()]


def stripped(lines):
    return ''.join(line for line in lines[2:-1] if line != '\n')


def test_single_layer():
    lines = run_pytest('single_layer')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 1 items
src/gocept/pytestlayer/tests/fixture/single_layer/test.py:35: FooTest.test_dummy
setUp foo
testSetUp foo
PASSED
testTearDown foo
tearDown foo
""" == stripped(lines)
    assert '=== 1 passed in ' in lines[-1]


def test_two_dependent_layers():
    lines = run_pytest('two_dependent_layers')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test.py:58: FooTest.test_dummy
setUp foo
testSetUp foo
PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test.py:69: BarTest.test_dummy
setUp bar
testSetUp foo
testSetUp bar
PASSED
testTearDown bar
testTearDown foo
tearDown bar
tearDown foo
""" == stripped(lines)
    assert '=== 2 passed in ' in lines[-1]


def test_integration():
    lines = run_pytest('integration')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 1 items
src/gocept/pytestlayer/tests/fixture/integration/test.py:35: FooTest.test_dummy
setUp foo
testSetUp foo
PASSED
testTearDown foo
tearDown foo
""" == stripped(lines)
    assert '=== 1 passed in ' in lines[-1]


def test_nice_error_message_if_no_fixture_for_layer():
    lines = run_pytest('missing_fixture')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 0 items / 1 errors
==================================== ERRORS ====================================
 ERROR collecting src/gocept/pytestlayer/tests/fixture/missing_fixture/test.py _
src/gocept/pytestlayer/plugin.py:27: in pytest_pycollect_makeitem
>                       'layer_name': get_layer_name(obj.layer)})
E               RuntimeError: There is no fixture for layer `missing_fixture.test.FooLayer`.
E               You have to create it using:
E               globals().update(gocept.pytestlayer.fixture.create(missing_fixture.test.FooLayer)
E               in `conftest.py`.
""" == stripped(lines)
    assert '=== 1 error in ' in lines[-1]
