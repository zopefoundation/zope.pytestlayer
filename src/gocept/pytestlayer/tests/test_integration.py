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


def test_with_and_without_layer():
    lines = run_pytest('with_and_without_layer')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/with_and_without_layer/test.py:35: FooTest.test_dummy
setUp foo
testSetUp foo
PASSED
testTearDown foo
tearDown foo
src/gocept/pytestlayer/tests/fixture/with_and_without_layer/test.py:42: UnitTest.test_dummy PASSED
""" == stripped(lines)
    assert '=== 2 passed in ' in lines[-1]


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


def test_two_independent_layers():
    lines = run_pytest('two_independent_layers')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test.py:58: FooTest.test_dummy
setUp foo
testSetUp foo
PASSED
testTearDown foo
tearDown foo
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test.py:69: BarTest.test_dummy
setUp bar
testSetUp bar
PASSED
testTearDown bar
tearDown bar
""" == stripped(lines)
    assert '=== 2 passed in ' in lines[-1]


def test_keep_layer_across_test_classes():
    lines = run_pytest('keep_layer_across_test_classes')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 3 items
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test.py:81: FooTest.test_dummy
setUp foo
testSetUp foo
PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test.py:92: FooBarTest.test_dummy
setUp bar
setUp foobar
testSetUp foo
testSetUp bar
testSetUp foobar
PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
tearDown foobar
tearDown foo
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test.py:105: BarTest.test_dummy
testSetUp bar
PASSED
testTearDown bar
tearDown bar
""" == stripped(lines)
    assert '=== 3 passed in ' in lines[-1]
