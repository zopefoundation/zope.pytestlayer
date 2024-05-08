import os.path
import re
import subprocess
import sys

import pytest


normalizers = [
    (r'\d+\.\d+ seconds', 'N.NNN seconds'),
    (r'\.py:\d+: ', '.py:NN: '),
    (r'\.txt::runTest <- test_suite ', '.txt '),
    (r'\.txt::runTest ', '.txt '),
    (r'\.py::(test_suite)::/', r'.py <- \1: /'),
    (r'\.py::(test)', r'.py:NN: \1'),
    (r'\.py::(.*Test)::', r'.py:NN: \1.'),
    # Compatibility with pytest >= 7.3 which adds this line:
    (r'configfile: pytest.ini', ''),
    # With pytest >= 3.3.0 progress is reported after a test result.
    # matches [NNN%], [ NN%] and [  N%]
    (r'PASSED \[\s*\d{1,3}%\]', 'PASSED'),
    # needed to omit all other loaded plugins.
    (r'plugins:.*(zope.pytestlayer).*\n', 'plugins: zope.pytestlayer\n'),
]


@pytest.fixture(scope='module')
def where(request):
    '''
    Add a normalizer that depends on the session.
    to make tests results independent from the place where pytest is started
    '''
    relative = request.fspath.relto(request.session.fspath)
    from_src = os.path.join(
        'src', 'zope', 'pytestlayer', 'tests', 'test_integration.py'
    )
    root = re.escape(relative.replace(from_src, ''))
    root_2 = str(request.session.fspath)
    normalizers.extend([
        (root, ''),
        (root_2, '')
    ])


def run_pytest(name, *args):
    cmd = [
        sys.argv[0], '-vs', '-p', 'no:removestalebytecode',
        '--disable-pytest-warnings',
        os.path.join(os.path.dirname(__file__), 'fixture', name),
    ]
    cmd.extend(args)
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    output = process.stdout.read().decode('latin-1')
    for pattern, replacement in normalizers:
        output = re.sub(pattern, replacement, output)
    lines = output.splitlines(True)
    # Sometimes the output ends with an escape sequence so omitting them to
    # make tests happy:
    if lines[-1] == '\x1b[?1034h':
        lines.pop(-1)
    return lines


def join(lines, start=4, end=1):
    return '\n'.join(
        line.rstrip() for line in lines[start:-end] if line.strip()) + '\n'


def test_single_layer(where):
    lines = run_pytest('single_layer')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 1 item
src/zope/pytestlayer/tests/fixture/single_layer/test_core.py:NN: FooTest.test_dummy single_layer.test_core.FooLayer
Set up single_layer.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/single_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down single_layer.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 1 passed' in lines[-1]


def test_single_layer_with_unattached_base_layer(where):
    lines = run_pytest('single_layer_with_unattached_base_layer')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 1 item
src/zope/pytestlayer/tests/fixture/single_layer_with_unattached_base_layer/test_core.py:NN: FooTest.test_dummy single_layer_with_unattached_base_layer.test_core.BarLayer
Set up single_layer_with_unattached_base_layer.test_core.BarLayer in N.NNN seconds.
single_layer_with_unattached_base_layer.test_core.FooLayer
Set up single_layer_with_unattached_base_layer.test_core.FooLayer in N.NNN seconds.
testSetUp bar
testSetUp foo
src/zope/pytestlayer/tests/fixture/single_layer_with_unattached_base_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
testTearDown bar
Tear down single_layer_with_unattached_base_layer.test_core.FooLayer in N.NNN seconds.
Tear down single_layer_with_unattached_base_layer.test_core.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 1 passed' in lines[-1]


def test_single_layer_with_unattached_base_layer_select_layer(where):
    lines = run_pytest(
        'single_layer_with_unattached_base_layer', '-k', 'BarLayer'
    )
    assert """\
plugins: zope.pytestlayer
collecting ... collected 1 item
src/zope/pytestlayer/tests/fixture/single_layer_with_unattached_base_layer/test_core.py:NN: FooTest.test_dummy single_layer_with_unattached_base_layer.test_core.BarLayer
Set up single_layer_with_unattached_base_layer.test_core.BarLayer in N.NNN seconds.
single_layer_with_unattached_base_layer.test_core.FooLayer
Set up single_layer_with_unattached_base_layer.test_core.FooLayer in N.NNN seconds.
testSetUp bar
testSetUp foo
src/zope/pytestlayer/tests/fixture/single_layer_with_unattached_base_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
testTearDown bar
Tear down single_layer_with_unattached_base_layer.test_core.FooLayer in N.NNN seconds.
Tear down single_layer_with_unattached_base_layer.test_core.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 1 passed' in lines[-1]


def test_single_layer_in_two_modules(where):
    lines = run_pytest('single_layer_in_two_modules')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 2 items
src/zope/pytestlayer/tests/fixture/single_layer_in_two_modules/test_core.py:NN: FooTest.test_dummy single_layer_in_two_modules.test_core.FooLayer
Set up single_layer_in_two_modules.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/single_layer_in_two_modules/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/zope/pytestlayer/tests/fixture/single_layer_in_two_modules/test_second_module.py:NN: FooTest.test_dummy
testSetUp foo
src/zope/pytestlayer/tests/fixture/single_layer_in_two_modules/test_second_module.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down single_layer_in_two_modules.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed' in lines[-1]


def test_single_layered_suite(where):
    lines = run_pytest('single_layered_suite')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 1 item
src/zope/pytestlayer/tests/fixture/single_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/single_layered_suite/doctest.txt single_layered_suite.test_core.FooLayer
Set up single_layered_suite.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/single_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/single_layered_suite/doctest.txt PASSED
testTearDown foo
Tear down single_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 1 passed' in lines[-1]


def test_shared_with_layered_suite(where):
    lines = run_pytest('shared_with_layered_suite')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 2 items
src/zope/pytestlayer/tests/fixture/shared_with_layered_suite/test_core.py:NN: FooTest.test_dummy shared_with_layered_suite.test_core.FooLayer
Set up shared_with_layered_suite.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/shared_with_layered_suite/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/zope/pytestlayer/tests/fixture/shared_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/shared_with_layered_suite/mydoctest.txt
testSetUp foo
src/zope/pytestlayer/tests/fixture/shared_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/shared_with_layered_suite/mydoctest.txt PASSED
testTearDown foo
Tear down shared_with_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed' in lines[-1]


def test_with_and_without_layer(where):
    lines = run_pytest('with_and_without_layer')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 2 items
src/zope/pytestlayer/tests/fixture/with_and_without_layer/test_core.py:NN: UnitTest.test_dummy PASSED
src/zope/pytestlayer/tests/fixture/with_and_without_layer/test_core.py:NN: FooTest.test_dummy with_and_without_layer.test_core.FooLayer
Set up with_and_without_layer.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/with_and_without_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down with_and_without_layer.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed' in lines[-1]


def test_two_dependent_layers(where):
    lines = run_pytest('two_dependent_layers')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 2 items
src/zope/pytestlayer/tests/fixture/two_dependent_layers/test_core.py:NN: FooTest.test_dummy two_dependent_layers.test_core.FooLayer
Set up two_dependent_layers.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/two_dependent_layers/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/zope/pytestlayer/tests/fixture/two_dependent_layers/test_core.py:NN: BarTest.test_dummy two_dependent_layers.test_core.BarLayer
Set up two_dependent_layers.test_core.BarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
src/zope/pytestlayer/tests/fixture/two_dependent_layers/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
testTearDown foo
Tear down two_dependent_layers.test_core.BarLayer in N.NNN seconds.
Tear down two_dependent_layers.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed' in lines[-1]


def test_two_dependent_layered_suites(where):
    lines = run_pytest('two_dependent_layered_suites')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 2 items
src/zope/pytestlayer/tests/fixture/two_dependent_layered_suites/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/two_dependent_layered_suites/foo.txt two_dependent_layered_suites.test_core.FooLayer
Set up two_dependent_layered_suites.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/two_dependent_layered_suites/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/two_dependent_layered_suites/foo.txt PASSED
testTearDown foo
src/zope/pytestlayer/tests/fixture/two_dependent_layered_suites/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/two_dependent_layered_suites/bar.txt two_dependent_layered_suites.test_core.BarLayer
Set up two_dependent_layered_suites.test_core.BarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
src/zope/pytestlayer/tests/fixture/two_dependent_layered_suites/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/two_dependent_layered_suites/bar.txt PASSED
testTearDown bar
testTearDown foo
Tear down two_dependent_layered_suites.test_core.BarLayer in N.NNN seconds.
Tear down two_dependent_layered_suites.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed' in lines[-1]


def test_two_independent_layers(where):
    lines = run_pytest('two_independent_layers')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 2 items
src/zope/pytestlayer/tests/fixture/two_independent_layers/test_core.py:NN: FooTest.test_dummy two_independent_layers.test_core.FooLayer
Set up two_independent_layers.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/two_independent_layers/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down two_independent_layers.test_core.FooLayer in N.NNN seconds.
src/zope/pytestlayer/tests/fixture/two_independent_layers/test_core.py:NN: BarTest.test_dummy two_independent_layers.test_core.BarLayer
Set up two_independent_layers.test_core.BarLayer in N.NNN seconds.
testSetUp bar
src/zope/pytestlayer/tests/fixture/two_independent_layers/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
Tear down two_independent_layers.test_core.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed' in lines[-1]


@pytest.mark.xfail(
    reason='ordering by layers does not optimize for fewer set-ups')
def test_keep_layer_across_test_classes(where):
    lines = run_pytest('keep_layer_across_test_classes')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 3 items
src/zope/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: FooTest.test_dummy order_by_layer.test_core.FooLayer
Set up keep_layer_across_test_classes.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/zope/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: FooBarTest.test_dummy order_by_layer.test_core.BarLayer
Set up keep_layer_across_test_classes.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/zope/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down keep_layer_across_test_classes.test_core.FooBarLayer in N.NNN seconds.
Tear down keep_layer_across_test_classes.test_core.FooLayer in N.NNN seconds.
src/zope/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: BarTest.test_dummy order_by_layer.test_core.FooLayer
Set up keep_layer_across_test_classes.test_core.BarLayer in N.NNN seconds.
testSetUp bar
src/zope/pytestlayer/tests/fixture/keep_layer_across_test_classes/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
Tear down keep_layer_across_test_classes.test_core.BarLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 3 passed' in lines[-1]


def test_order_by_layer(where):
    lines = run_pytest('order_by_layer')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 4 items
src/zope/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: FooTest.test_dummy order_by_layer.test_core.FooLayer
Set up order_by_layer.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
Tear down order_by_layer.test_core.FooLayer in N.NNN seconds.
src/zope/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: BarTest.test_dummy order_by_layer.test_core.BarLayer
Set up order_by_layer.test_core.BarLayer in N.NNN seconds.
testSetUp bar
src/zope/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
src/zope/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: Bar2Test.test_dummy
testSetUp bar
src/zope/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: Bar2Test.test_dummy PASSED
testTearDown bar
src/zope/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: FooBarTest.test_dummy order_by_layer.test_core.FooLayer
Set up order_by_layer.test_core.FooLayer in N.NNN seconds.
order_by_layer.test_core.FooBarLayer
Set up order_by_layer.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/zope/pytestlayer/tests/fixture/order_by_layer/test_core.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down order_by_layer.test_core.FooBarLayer in N.NNN seconds.
Tear down order_by_layer.test_core.BarLayer in N.NNN seconds.
Tear down order_by_layer.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 4 passed' in lines[-1]


def test_order_with_layered_suite(where):
    lines = run_pytest('order_with_layered_suite')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 6 items
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooTest.test_dummy order_with_layered_suite.test_core.FooLayer
Set up order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foo.txt
testSetUp foo
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foo.txt PASSED
testTearDown foo
Tear down order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: BarTest.test_dummy order_with_layered_suite.test_core.BarLayer
Set up order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
testSetUp bar
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: BarTest.test_dummy PASSED
testTearDown bar
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: Bar2Test.test_dummy
testSetUp bar
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: Bar2Test.test_dummy PASSED
testTearDown bar
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooBarTest.test_dummy order_with_layered_suite.test_core.FooLayer
Set up order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
order_with_layered_suite.test_core.FooBarLayer
Set up order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt
testSetUp foo
testSetUp bar
testSetUp foobar
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 6 passed' in lines[-1]


def test_order_with_layered_suite_select_layer(where):
    lines = run_pytest('order_with_layered_suite', '-k', 'FooLayer')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 6 items / 2 deselected / 4 selected
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooTest.test_dummy order_with_layered_suite.test_core.FooLayer
Set up order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooTest.test_dummy PASSED
testTearDown foo
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foo.txt
testSetUp foo
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foo.txt PASSED
testTearDown foo
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooBarTest.test_dummy order_with_layered_suite.test_core.BarLayer
Set up order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
order_with_layered_suite.test_core.FooBarLayer
Set up order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py:NN: FooBarTest.test_dummy PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt
testSetUp foo
testSetUp bar
testSetUp foobar
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines, end=2)
    assert '4 passed, 2 deselected' in lines[-1]


def test_order_with_layered_suite_select_doctest(where):
    lines = run_pytest('order_with_layered_suite', '-k', 'foobar and txt')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 6 items / 5 deselected / 1 selected
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt order_with_layered_suite.test_core.FooLayer
Set up order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
order_with_layered_suite.test_core.BarLayer
Set up order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
order_with_layered_suite.test_core.FooBarLayer
Set up order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
testSetUp foo
testSetUp bar
testSetUp foobar
src/zope/pytestlayer/tests/fixture/order_with_layered_suite/test_core.py <- test_suite: /src/zope/pytestlayer/tests/fixture/order_with_layered_suite/foobar.txt PASSED
testTearDown foobar
testTearDown bar
testTearDown foo
Tear down order_with_layered_suite.test_core.FooBarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.BarLayer in N.NNN seconds.
Tear down order_with_layered_suite.test_core.FooLayer in N.NNN seconds.
""" == join(lines, end=2)
    assert '1 passed, 5 deselected' in lines[-1]


def test_works_even_without_any_setup_or_teardown_methods(where):
    lines = run_pytest('no_setup_or_teardown')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 1 item
src/zope/pytestlayer/tests/fixture/no_setup_or_teardown/test_core.py:NN: FooTest.test_dummy PASSED
""" == join(lines)
    assert '=== 1 passed' in lines[-1]


def test_nice_error_message_if_layer_has_no_bases(where):
    lines = run_pytest('bad_layer')
    assert """\
has no __bases__ attribute. Layers may be of two sorts: class or instance with __bases__ attribute.\
""" in join(lines)
    assert '1 error in ' in lines[-1]


def test_creating_different_fixtures_for_layers_with_the_same_name(where):
    lines = run_pytest('layers_with_same_name')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 2 items
src/zope/pytestlayer/tests/fixture/layers_with_same_name/test_core.py:NN: FooTest.test_dummy layers_with_same_name.test_core.TestLayer
Set up layers_with_same_name.test_core.TestLayer in N.NNN seconds.
src/zope/pytestlayer/tests/fixture/layers_with_same_name/test_core.py:NN: FooTest.test_dummy PASSED
Tear down layers_with_same_name.test_core.TestLayer in N.NNN seconds.
src/zope/pytestlayer/tests/fixture/layers_with_same_name/test_core.py:NN: BarTest.test_dummy layers_with_same_name.test_core.TestLayer
Set up layers_with_same_name.test_core.TestLayer in N.NNN seconds.
src/zope/pytestlayer/tests/fixture/layers_with_same_name/test_core.py:NN: BarTest.test_dummy PASSED
Tear down layers_with_same_name.test_core.TestLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed' in lines[-1]


def test_selection_of_doctest_names(where):
    lines = run_pytest('single_layered_suite', '-k', 'mydoctest')
    assert "1 deselected" in join(lines)


def test_fixture_create_allows_overriding_names(where):
    lines = run_pytest('custom_fixture_name')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 2 items
src/zope/pytestlayer/tests/fixture/custom_fixture_name/test_core.py:NN: test_can_access_layer_via_fixture custom_fixture_name.test_core.FooLayer
Set up custom_fixture_name.test_core.FooLayer in N.NNN seconds.
testSetUp foo
src/zope/pytestlayer/tests/fixture/custom_fixture_name/test_core.py:NN: test_can_access_layer_via_fixture PASSED
testTearDown foo
src/zope/pytestlayer/tests/fixture/custom_fixture_name/test_core.py:NN: FooTest.test_accesses_fixture_with_generated_name_for_layer
testSetUp foo
src/zope/pytestlayer/tests/fixture/custom_fixture_name/test_core.py:NN: FooTest.test_accesses_fixture_with_generated_name_for_layer PASSED
testTearDown foo
Tear down custom_fixture_name.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed' in lines[-1]


def test_if_session_fixture_is_used_class_fixtures_are_ignored(where):
    lines = run_pytest('session_fixture')
    assert """\
plugins: zope.pytestlayer
collecting ... collected 2 items
src/zope/pytestlayer/tests/fixture/session_fixture/test_core.py:NN: test_can_access_layer_via_fixture session_fixture.test_core.FooLayer
Set up session_fixture.test_core.FooLayer in N.NNN seconds.
src/zope/pytestlayer/tests/fixture/session_fixture/test_core.py:NN: test_can_access_layer_via_fixture PASSED
src/zope/pytestlayer/tests/fixture/session_fixture/test_core.py:NN: FooTest.test_accesses_fixture_with_generated_name_for_layer
testSetUp foo
src/zope/pytestlayer/tests/fixture/session_fixture/test_core.py:NN: FooTest.test_accesses_fixture_with_generated_name_for_layer PASSED
testTearDown foo
Tear down session_fixture.test_core.FooLayer in N.NNN seconds.
""" == join(lines)
    assert '=== 2 passed' in lines[-1]
