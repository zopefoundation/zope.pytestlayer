import os.path
import pytest
import re
import subprocess
import sys


normalizers = [
    ('\d+\.\d+ seconds', 'N.NNN seconds'),
    ('\.py:\d+: ', '.py:NN: '),
]


def run_pytest(name):
    process = subprocess.Popen(
        [sys.argv[0], '-s', '-v',
         os.path.join(os.path.dirname(__file__), 'fixture', name, 'test.py')],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    output = process.stdout.read()
    for pattern, replacement in normalizers:
        output = re.sub(pattern, replacement, output)
    return output.splitlines(True)


def join(lines, start=2):
    return '\n'.join(
        line.rstrip() for line in lines[start:-1] if line.strip()) + '\n'


def test_single_layer():
    lines = run_pytest('single_layer')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 1 items
src/gocept/pytestlayer/tests/fixture/single_layer/test.py:NN: FooTest.test_dummy
Set up single_layer.test.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/single_layer/test.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down single_layer.test.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 1 passed in ' in lines[-1]


def test_with_and_without_layer():
    lines = run_pytest('with_and_without_layer')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/with_and_without_layer/test.py:NN: UnitTest.test_dummy PASSED
src/gocept/pytestlayer/tests/fixture/with_and_without_layer/test.py:NN: FooTest.test_dummy
Set up with_and_without_layer.test.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/with_and_without_layer/test.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down with_and_without_layer.test.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]


def test_two_dependent_layers():
    lines = run_pytest('two_dependent_layers')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test.py:NN: FooTest.test_dummy
Set up two_dependent_layers.test.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test.py:NN: BarTest.test_dummy
Set up two_dependent_layers.test.BarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test.py:NN: BarTest.test_dummy PASSED
testTearDown bar
testTearDown foo
Tear down two_dependent_layers.test.BarLayer in N.NNN seconds.
Tear down two_dependent_layers.test.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]


def test_two_independent_layers():
    lines = run_pytest('two_independent_layers')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test.py:NN: FooTest.test_dummy
Set up two_independent_layers.test.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down two_independent_layers.test.FooLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test.py:NN: BarTest.test_dummy
Set up two_independent_layers.test.BarLayer in N.NNN seconds.
testSetUp bar
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test.py:NN: BarTest.test_dummy PASSED
testTearDown bar
Tear down two_independent_layers.test.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]


@pytest.mark.xfail(
    reason='ordering by layers does not optimize for fewer set-ups')
def test_keep_layer_across_test_classes():
    lines = run_pytest('keep_layer_across_test_classes')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 3 items
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test.py:NN: FooTest.test_dummy
Set up keep_layer_across_test_classes.test.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test.py:NN: FooBarTest.test_dummy
Set up keep_layer_across_test_classes.test.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down keep_layer_across_test_classes.test.FooBarLayer in N.NNN seconds.
Tear down keep_layer_across_test_classes.test.FooLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test.py:NN: BarTest.test_dummy
Set up keep_layer_across_test_classes.test.BarLayer in N.NNN seconds.
testSetUp bar
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test.py:NN: BarTest.test_dummy PASSED
testTearDown bar
Tear down keep_layer_across_test_classes.test.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 3 passed in ' in lines[-1]


def test_order_by_layer():
    lines = run_pytest('order_by_layer')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 4 items
src/gocept/pytestlayer/tests/fixture/order_by_layer/test.py:NN: FooTest.test_dummy
Set up order_by_layer.test.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/order_by_layer/test.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down order_by_layer.test.FooLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/order_by_layer/test.py:NN: BarTest.test_dummy
Set up order_by_layer.test.BarLayer in N.NNN seconds.
testSetUp bar
src/gocept/pytestlayer/tests/fixture/order_by_layer/test.py:NN: BarTest.test_dummy PASSED
testTearDown bar
src/gocept/pytestlayer/tests/fixture/order_by_layer/test.py:NN: Bar2Test.test_dummy
testSetUp bar
PASSED
testTearDown bar
src/gocept/pytestlayer/tests/fixture/order_by_layer/test.py:NN: FooBarTest.test_dummy
Set up order_by_layer.test.FooLayer in N.NNN seconds.
Set up order_by_layer.test.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/gocept/pytestlayer/tests/fixture/order_by_layer/test.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down order_by_layer.test.FooBarLayer in N.NNN seconds.
Tear down order_by_layer.test.BarLayer in N.NNN seconds.
Tear down order_by_layer.test.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 4 passed in ' in lines[-1]


def test_works_even_without_any_setup_or_teardown_methods():
    lines = run_pytest('no_setup_or_teardown')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 1 items
src/gocept/pytestlayer/tests/fixture/no_setup_or_teardown/test.py:NN: FooTest.test_dummy PASSED
""" == join(lines)
    assert '=== 1 passed in ' in lines[-1]


def test_nice_error_message_if_no_fixture_for_layer():
    lines = run_pytest('missing_fixture')
    assert """\
E               RuntimeError: There is no fixture for layer `missing_fixture.test.FooLayer`.
E               You have to create it using:
E                   from gocept.pytestlayer import fixture
E                   globals().update(fixture.create("missing_fixture.test.FooLayer"))
E               in `conftest.py`.
""" == join(lines, start=9)
    assert '=== 1 error in ' in lines[-1]


def test_nice_error_message_if_layer_is_not_found_in_module():
    lines = run_pytest('layer_missing_in_module')
    assert """\
RuntimeError: The layer `layer_missing_in_module.test.FooLayer` is not found its module's namespace.
""" in join(lines)
    assert '=== 1 error in ' in lines[-1]

def test_creating_different_fixtures_for_layers_with_the_same_name():
    lines = run_pytest('layers_with_same_name')
    assert """\
plugins: gocept.pytestlayer, capturelog
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/layers_with_same_name/test.py:NN: FooTest.test_dummy
Set up layers_with_same_name.test.TestLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/layers_with_same_name/test.py:NN: FooTest.test_dummy PASSED
Tear down layers_with_same_name.test.TestLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/layers_with_same_name/test.py:NN: BarTest.test_dummy
Set up layers_with_same_name.test.TestLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/layers_with_same_name/test.py:NN: BarTest.test_dummy PASSED
Tear down layers_with_same_name.test.TestLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]
