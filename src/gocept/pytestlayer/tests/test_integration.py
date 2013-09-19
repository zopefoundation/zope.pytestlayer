import os.path
import pytest
import re
import subprocess
import sys


normalizers = [
    ('\d+\.\d+ seconds', 'N.NNN seconds'),
    ('\.py:\d+: ', '.py:NN: '),
]


@pytest.fixture('module')
def where(request):
    '''
    Add a normalizer that depends on the session.
    to make tests results independent from the place where pytest is started
    '''
    relative = request.fspath.relto(request.session.fspath)
    from_src = os.path.join(
        'src', 'gocept', 'pytestlayer', 'tests', 'test_integration.py'
    )
    root = re.escape(relative.replace(from_src, ''))
    normalizers.append(
        (root, '')
    )


def run_pytest(name, *args):
    cmd = [
        sys.argv[0], '-v',
        os.path.join(os.path.dirname(__file__), 'fixture', name)
        ]
    cmd.extend(args)
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    output = process.stdout.read()
    for pattern, replacement in normalizers:
        output = re.sub(pattern, replacement, output)
    lines = output.splitlines(True)
    # Sometimes the output ends with an escape sequence so omitting them to
    # make tests happy:
    if lines[-1] == '\x1b[?1034h':
        lines.pop(-1)
    return lines


def join(lines, start=2, end=1):
    return '\n'.join(
        line.rstrip() for line in lines[start:-end] if line.strip()) + '\n'


def test_single_layer(where):
    lines = run_pytest('single_layer')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 1 items
src/gocept/pytestlayer/tests/fixture/single_layer/test_core.py:NN: FooTest.test_dummy
Set up single_layer.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/single_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down single_layer.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 1 passed in ' in lines[-1]


def test_single_layer_with_unattached_base_layer(where):
    lines = run_pytest('single_layer_with_unattached_base_layer')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 1 items
src/gocept/pytestlayer/tests/fixture/single_layer_with_unattached_base_layer/test_core.py:NN: FooTest.test_dummy
Set up single_layer_with_unattached_base_layer.test_core.BarLayer in N.NNN seconds.
Set up single_layer_with_unattached_base_layer.test_core.FooLayer in N.NNN seconds.
testSetUp bar
testSetUp foo
src/gocept/pytestlayer/tests/fixture/single_layer_with_unattached_base_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
testTearDown bar
Tear down single_layer_with_unattached_base_layer.test_core.FooLayer in N.NNN seconds.
Tear down single_layer_with_unattached_base_layer.test_core.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 1 passed in ' in lines[-1]


def test_single_layer_with_unattached_base_layer_select_layer(where):
    lines = run_pytest(
        'single_layer_with_unattached_base_layer', '-k', 'BarLayer'
    )
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 1 items
src/gocept/pytestlayer/tests/fixture/single_layer_with_unattached_base_layer/test_core.py:NN: FooTest.test_dummy
Set up single_layer_with_unattached_base_layer.test_core.BarLayer in N.NNN seconds.
Set up single_layer_with_unattached_base_layer.test_core.FooLayer in N.NNN seconds.
testSetUp bar
testSetUp foo
src/gocept/pytestlayer/tests/fixture/single_layer_with_unattached_base_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
testTearDown bar
Tear down single_layer_with_unattached_base_layer.test_core.FooLayer in N.NNN seconds.
Tear down single_layer_with_unattached_base_layer.test_core.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 1 passed in ' in lines[-1]


def test_single_layer_in_two_modules(where):
    lines = run_pytest('single_layer_in_two_modules')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/single_layer_in_two_modules/test_core.py:NN: FooTest.test_dummy
Set up single_layer_in_two_modules.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/single_layer_in_two_modules/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/single_layer_in_two_modules/test_second_module.py:NN: FooTest.test_dummy
testSetUp foo
src/gocept/pytestlayer/tests/fixture/single_layer_in_two_modules/test_second_module.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down single_layer_in_two_modules.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]


def test_single_layered_suite(where):
    lines = run_pytest('single_layered_suite')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 1 items
src/gocept/pytestlayer/tests/fixture/single_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/single_layered_suite/doctest.txt
Set up single_layered_suite.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/single_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/single_layered_suite/doctest.txt PASSED
testTearDown foo
Tear down single_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 1 passed in ' in lines[-1]


def test_shared_with_layered_suite(where):
    lines = run_pytest('shared_with_layered_suite')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/shared_with_layered_suite/test_core.py:NN: FooTest.test_dummy
Set up shared_with_layered_suite.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/shared_with_layered_suite/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/shared_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/shared_with_layered_suite/doctest.txt
testSetUp foo
src/gocept/pytestlayer/tests/fixture/shared_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/shared_with_layered_suite/doctest.txt PASSED
testTearDown foo
Tear down shared_with_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]


def test_with_and_without_layer(where):
    lines = run_pytest('with_and_without_layer')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/with_and_without_layer/test_core.py:NN: UnitTest.test_dummy PASSED
src/gocept/pytestlayer/tests/fixture/with_and_without_layer/test_core.py:NN: FooTest.test_dummy
Set up with_and_without_layer.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/with_and_without_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down with_and_without_layer.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]


def test_two_dependent_layers(where):
    lines = run_pytest('two_dependent_layers')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test_core.py:NN: FooTest.test_dummy
Set up two_dependent_layers.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test_core.py:NN: BarTest.test_dummy
Set up two_dependent_layers.test_core.BarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
src/gocept/pytestlayer/tests/fixture/two_dependent_layers/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
testTearDown foo
Tear down two_dependent_layers.test_core.BarLayer in N.NNN seconds.
Tear down two_dependent_layers.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]


def test_two_dependent_layered_suites(where):
    lines = run_pytest('two_dependent_layered_suites')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/two_dependent_layered_suites/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/two_dependent_layered_suites/foo.txt
Set up two_dependent_layered_suites.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/two_dependent_layered_suites/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/two_dependent_layered_suites/foo.txt PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/two_dependent_layered_suites/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/two_dependent_layered_suites/bar.txt
Set up two_dependent_layered_suites.test_core.BarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
src/gocept/pytestlayer/tests/fixture/two_dependent_layered_suites/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/two_dependent_layered_suites/bar.txt PASSED
testTearDown bar
testTearDown foo
Tear down two_dependent_layered_suites.test_core.BarLayer in N.NNN seconds.
Tear down two_dependent_layered_suites.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]


def test_two_independent_layers(where):
    lines = run_pytest('two_independent_layers')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test_core.py:NN: FooTest.test_dummy
Set up two_independent_layers.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down two_independent_layers.test_core.FooLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test_core.py:NN: BarTest.test_dummy
Set up two_independent_layers.test_core.BarLayer in N.NNN seconds.
testSetUp bar
src/gocept/pytestlayer/tests/fixture/two_independent_layers/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
Tear down two_independent_layers.test_core.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]


@pytest.mark.xfail(
    reason='ordering by layers does not optimize for fewer set-ups')
def test_keep_layer_across_test_classes(where):
    lines = run_pytest('keep_layer_across_test_classes')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 3 items
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: FooTest.test_dummy
Set up keep_layer_across_test_classes.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: FooBarTest.test_dummy
Set up keep_layer_across_test_classes.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down keep_layer_across_test_classes.test_core.FooBarLayer in N.NNN seconds.
Tear down keep_layer_across_test_classes.test_core.FooLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: BarTest.test_dummy
Set up keep_layer_across_test_classes.test_core.BarLayer in N.NNN seconds.
testSetUp bar
src/gocept/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
Tear down keep_layer_across_test_classes.test_core.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 3 passed in ' in lines[-1]


def test_order_by_layer(where):
    lines = run_pytest('order_by_layer')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 4 items
src/gocept/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: FooTest.test_dummy
Set up order_by_layer.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down order_by_layer.test_core.FooLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: BarTest.test_dummy
Set up order_by_layer.test_core.BarLayer in N.NNN seconds.
testSetUp bar
src/gocept/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
src/gocept/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: Bar2Test.test_dummy
testSetUp bar
src/gocept/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: Bar2Test.test_dummy PASSED
testTearDown bar
src/gocept/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: FooBarTest.test_dummy
Set up order_by_layer.test_core.FooLayer in N.NNN seconds.
Set up order_by_layer.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/gocept/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down order_by_layer.test_core.FooBarLayer in N.NNN seconds.
Tear down order_by_layer.test_core.BarLayer in N.NNN seconds.
Tear down order_by_layer.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 4 passed in ' in lines[-1]


def test_order_with_layered_suite(where):
    lines = run_pytest('order_with_layered_suite')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 6 items
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooTest.test_dummy
Set up order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foo.txt
testSetUp foo
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foo.txt PASSED
testTearDown foo
Tear down order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: BarTest.test_dummy
Set up order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
testSetUp bar
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: Bar2Test.test_dummy
testSetUp bar
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: Bar2Test.test_dummy PASSED
testTearDown bar
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooBarTest.test_dummy
Set up order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
Set up order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt
testSetUp foo
testSetUp bar
testSetUp foobar
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 6 passed in ' in lines[-1]


def test_order_with_layered_suite_select_layer(where):
    lines = run_pytest('order_with_layered_suite', '-k', 'FooLayer')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 6 items
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooTest.test_dummy
Set up order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foo.txt
testSetUp foo
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foo.txt PASSED
testTearDown foo
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooBarTest.test_dummy
Set up order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
Set up order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt
testSetUp foo
testSetUp bar
testSetUp foobar
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines, end=2)
    assert "2 tests deselected by '-kFooLayer" in lines[-2]
    assert '4 passed, 2 deselected in' in lines[-1]


def test_order_with_layered_suite_select_doctest(where):
    lines = run_pytest('order_with_layered_suite', '-k', 'foobar and txt')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 6 items
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt
Set up order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
Set up order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
Set up order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/gocept/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines, end=2)
    assert "5 tests deselected by '-kfoobar and txt" in lines[-2]
    assert '1 passed, 5 deselected in' in lines[-1]


def test_works_even_without_any_setup_or_teardown_methods(where):
    lines = run_pytest('no_setup_or_teardown')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 1 items
src/gocept/pytestlayer/tests/fixture/no_setup_or_teardown/test_core.py:NN: FooTest.test_dummy PASSED
""" == join(lines)
    assert '=== 1 passed in ' in lines[-1]


def test_nice_error_message_if_layer_has_no_bases(where):
    lines = run_pytest('bad_layer')
    assert """\
has no __bases__ attribute. Layers may be of two sorts: class or instance with __bases__ attribute.\
""" in join(lines)
    assert '=== 1 error in ' in lines[-1]

def test_creating_different_fixtures_for_layers_with_the_same_name(where):
    lines = run_pytest('layers_with_same_name')
    assert """\
plugins: gocept.pytestlayer
collecting ... collected 2 items
src/gocept/pytestlayer/tests/fixture/layers_with_same_name/test_core.py:NN: FooTest.test_dummy
Set up layers_with_same_name.test_core.TestLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/layers_with_same_name/test_core.py:NN: FooTest.test_dummy PASSED
Tear down layers_with_same_name.test_core.TestLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/layers_with_same_name/test_core.py:NN: BarTest.test_dummy
Set up layers_with_same_name.test_core.TestLayer in N.NNN seconds.
src/gocept/pytestlayer/tests/fixture/layers_with_same_name/test_core.py:NN: BarTest.test_dummy PASSED
Tear down layers_with_same_name.test_core.TestLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed in ' in lines[-1]
