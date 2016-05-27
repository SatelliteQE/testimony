# -*- encoding: utf-8 -*-
"""DocString manipulation methods to create test reports"""
from __future__ import print_function

import ast
import collections
import itertools
import json
import os
import sys
import textwrap

from decimal import Decimal
from testimony.constants import (
    AUTO_REPORT,
    BUGS_REPORT,
    CLR_ERR,
    CLR_GOOD,
    MANUAL_REPORT,
    PRINT_AUTO_TC,
    PRINT_INVALID_DOC,
    PRINT_MANUAL_TC,
    PRINT_NO_DOC,
    PRINT_NO_MINIMUM_DOC_TC,
    PRINT_REPORT,
    PRINT_TC_AFFECTED_BUGS,
    PRINT_TOTAL_TC,
    SUMMARY_REPORT,
    TAGS_REPORT,
    VALIDATE_DOCSTRING_REPORT,
)

try:
    import termcolor
    HAS_TERMCOLOR = True
except ImportError as exception:
    HAS_TERMCOLOR = False

SETTINGS = {
    'json': False,
    'nocolor': False,
}


def indent(text, prefix, predicate=None):
    """Adds 'prefix' to the beginning of selected lines in 'text'.

    If 'predicate' is provided, 'prefix' will only be added to the lines
    where 'predicate(line)' is True. If 'predicate' is not provided,
    it will default to adding 'prefix' to all non-empty lines that do not
    consist solely of whitespace characters.

    PS.: From Python 3.3+ textwrap.indent.
    """
    if predicate is None:
        def predicate(line):
            return line.strip()

    def prefixed_lines():
        for line in text.splitlines(True):
            yield (prefix + line if predicate(line) else line)
    return ''.join(prefixed_lines())


def is_test_module(filename):
    """Return ``True`` if the ``filename`` matches an expected test
    module name.
    """
    return filename.startswith('test_') and filename.endswith('.py')


class TestFunction(object):
    """Class that wraps a ``ast.FunctionDef`` instance and provide useful
    information for creating the reports.

    An instance of ``TestFunction`` will proxy attribute lookups to the wrapped
    ``ast.FunctionDef`` in order to make easy access to atribute like
    ``name``.

    """

    #: A sentinel to make sure the proxied attribute lookup to ``function_def``
    #: is not available.
    _undefined = object()

    def __init__(self, function_def, parent_class=None, testmodule=None):
        #: A ``ast.FunctionDef`` instance used to extract information
        self.docstring = ast.get_docstring(function_def)
        self.function_def = function_def
        self.name = function_def.name
        self.parent_class = parent_class.name
        self.parent_class_def = parent_class
        self.testmodule = testmodule.path
        self.module_def = testmodule
        self.assertion = None
        self.bugs = None
        self.feature = None
        self.setup = None
        self.status = None
        self.steps = None
        self.tags = None
        self.test = None
        self.test_type = None
        self.skipped_lines = []
        self.unexpected_tags = {}
        self._parse_docstring()

    def _parse_tags(self, docstring):
        """Parses the docstring and returns the expected tags, unexpected tags
        and the docstring lines of the unexpected tags.

        For example in the following docstring (using single quote to demo)::

            '''First line

            @expected_tag1: value
            @expected_tag2: value2
            @unexpected_tag1: value
            @unexpected_tag2: value2
            '''

        Will return a tuple with the following content::

            (
                {'expected_tag1': 'value', 'expected_tag2': 'value2'},
                {'unexpected_tag1': 'value', 'unexpected_tag2': 'value2'},
                ['@unexpected_tag1: value', '@unexpected_tag2: value2']
            )
        """
        if docstring is None:
            return {}, {}, []
        valid_tags = [
            'assert',
            'bz',
            'feature',
            'setup',
            'status',
            'steps',
            'tags',
            'type',
        ]
        expected_tags = {}
        unexpected_tags = {}
        unexpected_lines = []
        for line in docstring.split('@'):
            # Remove trailing spaces
            line = line.rstrip()
            # Sometimes there are double new line
            # characters in the middle.  We need
            # only one of those to print
            line = line.replace('\n\n', '\n')
            if len(line) > 0 and ':' in line:
                tag, value = line.split(':', 1)
                tag = tag.lower()
                value = value.strip()
                if tag in valid_tags:
                    if tag == 'bz':
                        value = [bz.strip() for bz in value.split(',')]
                    expected_tags[tag] = value
                else:
                    unexpected_tags[tag] = value
                    unexpected_lines.append(line)
        return expected_tags, unexpected_tags, unexpected_lines

    def _parse_docstring(self):
        """Parses the test docstring extracting expected values.

        If the expected tags is not spelled right they will not be parsed.
        """
        if self.docstring is None:
            return

        # Create the contexts
        tags, unexpected_tags, _ = self._parse_tags(
            ast.get_docstring(self.module_def))
        class_tags, class_unexpected_tags, _ = self._parse_tags(
            ast.get_docstring(self.parent_class_def))
        function_tags, function_unexpected_tags, self.skipped_lines = (
            self._parse_tags(self.docstring))

        # Update context dictionaries
        tags.update(class_tags)
        tags.update(function_tags)
        unexpected_tags.update(class_unexpected_tags)
        unexpected_tags.update(function_unexpected_tags)

        for tag, value in tags.items():
            if tag == 'bz':
                tag = 'bugs'
            if tag == 'assert':
                tag = 'assertion'
            if tag == 'type':
                tag = 'test_type'
            setattr(self, tag, value)
        self.unexpected_tags = unexpected_tags

        # Always use the first line of docstring as test case name
        if self.test is None:
            self.test = self.docstring.strip().split('\n')[0]

    @property
    def automated(self):
        """Indicate if the test case is automated or not."""
        if self.status and self.status.lower() == 'manual':
            return False
        return True

    @property
    def has_valid_docstring(self):
        """Returns ``True`` if at least feature and assert tags are defined.
        """
        return (
            self.assertion is not None and
            self.feature is not None and
            self.test is not None
        )

    def to_dict(self):
        """Return the information in dict format.

        This is a helper for converting to JSON.
        """
        return {
            'assertion': self.assertion,
            'automated': self.automated,
            'bugs': self.bugs,
            'feature': self.feature,
            'name': self.name,
            'parent_class': self.parent_class,
            'setup': self.setup,
            'skipped-lines': self.skipped_lines,
            'status': self.status,
            'steps': self.steps,
            'tags': self.tags,
            'test': self.test,
            'test_type': self.test_type,
            'unexpected-tags': self.unexpected_tags,
        }

    def __str__(self):
        output = []
        if self.test is not None:
            output.append('Test: ' + self.test)
        if self.feature is not None:
            output.append('Feature: ' + self.feature)
        if self.assertion is not None:
            output.append('Assert: ' + self.assertion)
        if self.setup is not None:
            output.append('Setup: ' + self.setup)
        if self.steps is not None:
            output.append('Steps: ' + self.steps)
        if self.bugs is not None:
            output.append('Bugs: ' + ', '.join(self.bugs))
        if self.status is not None:
            output.append('Status: ' + self.status)
        if self.tags is not None:
            output.append('Tags: ' + self.tags)
        if self.test_type is not None:
            output.append('Type: ' + self.test_type)
        if self.skipped_lines:
            output.append(
                'Skipped lines:\n' +
                '\n'.join([
                    textwrap.fill(
                        line,
                        initial_indent=' ' * 2,
                        subsequent_indent=' ' * 4
                    )
                    for line in self.skipped_lines
                ])
            )
        return '\n'.join(output)


def main(report, paths, json_output, nocolor, tags):
    """Main function for testimony project

    Expects a valid report type and valid directory paths, hopefully argparse
    is taking care of validation

    """
    SETTINGS['json'] = json_output
    SETTINGS['nocolor'] = nocolor
    SETTINGS['input_tags'] = tags

    if report == SUMMARY_REPORT:
        report_function = summary_report
    elif report == PRINT_REPORT:
        report_function = print_report
    elif report == VALIDATE_DOCSTRING_REPORT:
        report_function = validate_docstring_report
    elif report == BUGS_REPORT:
        report_function = bugs_report
    elif report == MANUAL_REPORT:
        report_function = manual_report
    elif report == AUTO_REPORT:
        report_function = auto_report
    elif report == TAGS_REPORT:
        report_function = tags_report

    sys.exit(report_function(get_testcases(paths)))


def print_testcases(testcases, test_filter='all'):
    """Print the list of test cases.

    :param testcases: A dict where the key is a path and value is a list of
        found testcases on that path.
    :param test_filter: One of all, automated or manual. Indicates if will be
        printed all testcases or just automated ones or just manual ones.
    """
    result = {}
    for path, tests in testcases.items():
        if test_filter == 'automated':
            tests = filter(
                lambda t: t.automated and t.docstring is not None, tests)
        elif test_filter == 'manual':
            tests = filter(lambda t: not t.automated, tests)
        result[path] = [test.to_dict() for test in tests]

        if not SETTINGS['json']:
            print('{0}\n{1}\n'.format(
                colored(path, attrs=['bold']), '=' * len(path)))
            if len(tests) == 0:
                print('No {0}test cases found.\n'.format(
                    '' if test_filter not in ('automated', 'manual')
                    else test_filter + ' '
                ))
            for index, value in enumerate(tests):
                print('TC {0}\n{1}\n'.format(index + 1, value))

    if SETTINGS['json']:
        print(json.dumps(result))
        return 0


def print_report(testcases):
    """All test cases report."""
    print_testcases(testcases)


def auto_report(testcases):
    """Automated test cases report."""
    print_testcases(testcases, 'automated')


def manual_report(testcases):
    """Manual test cases report."""
    print_testcases(testcases, 'manual')


def summary_report(testcases):
    """Summary about the test cases report."""
    count = automated = manual = no_docstring = 0
    for testcase in itertools.chain(*testcases.values()):
        count += 1
        if testcase.docstring is None:
            no_docstring += 1
            continue
        if testcase.automated:
            automated += 1
        else:
            manual += 1

    manual_percent = float(Decimal(manual) / Decimal(count) * 100)
    automated_percent = float(Decimal(automated) / Decimal(count) * 100)
    no_docstring_percent = float(Decimal(no_docstring) / Decimal(count) * 100)
    summary_result = {
        'count': count,
        'automated': automated,
        'automated_percent': automated_percent,
        'manual': manual,
        'manual_percent': manual_percent,
        'no_docstring': no_docstring,
        'no_docstring_percent': no_docstring_percent,
    }

    if SETTINGS['json']:
        print(json.dumps(summary_result))
        return 0

    print(colored(PRINT_TOTAL_TC, attrs=['bold']) % summary_result['count'])
    print(colored(PRINT_AUTO_TC, attrs=['bold']) %
          summary_result['automated'] +
          '({0:.0f}%)'.format(summary_result['automated_percent']))
    print(colored(PRINT_MANUAL_TC, attrs=['bold']) %
          summary_result['manual'] +
          '({0:.0f}%)'.format(summary_result['manual_percent']))
    print(colored(PRINT_NO_DOC, attrs=['bold']) %
          summary_result['no_docstring'] +
          '({0:.0f}%)'.format(summary_result['no_docstring_percent']))


def validate_docstring_report(testcases):
    """Check for presence of invalid docstrings report."""
    result = {}
    invalid_docstring_count = 0
    invalid_tags_docstring_count = 0
    minimum_docstring_count = 0
    missing_docstring_count = 0
    testcase_count = 0
    for path, tests in testcases.items():
        testcase_count += len(tests)
        for testcase in tests:
            issues = []
            if not testcase.docstring:
                issues.append('Missing docstring.')
                missing_docstring_count += 1
            if not testcase.has_valid_docstring:
                issues.append(
                    'Docstring should have at least feature and assert tags'
                )
                minimum_docstring_count += 1
            if testcase.skipped_lines:
                issues.append('Unexpected tags found:\n{0}'.format(
                    indent('\n'.join(testcase.skipped_lines), '  ')
                ))
                invalid_tags_docstring_count += 1
            if issues:
                if path not in result:
                    result[path] = {}
                result[path][testcase.name] = issues
                invalid_docstring_count += 1

    if SETTINGS['json']:
        print(json.dumps(result))
        return

    for path, testcases in result.items():
        print('{0}\n{1}\n'.format(path, '=' * len(path)))
        for testcase, issues in testcases.items():
            print('{0}\n{1}\n'.format(testcase, '-' * len(testcase)))
            print(
                '\n'.join(['* {0}'.format(issue) for issue in issues]) + '\n')

    if invalid_docstring_count == 0:
        color = CLR_GOOD
    else:
        color = CLR_ERR
    print(colored(PRINT_INVALID_DOC, attrs=['bold']) % colored(
        '{0}/{1} ({2:.02f}%)'.format(
            invalid_docstring_count,
            testcase_count,
            float(invalid_docstring_count)/testcase_count * 100
        ),
        color
    ))
    if missing_docstring_count == 0:
        color = CLR_GOOD
    else:
        color = CLR_ERR
    print(colored(PRINT_NO_DOC.strip(), attrs=['bold']) % colored(
        '{0}/{1} ({2:.02f}%)'.format(
            missing_docstring_count,
            testcase_count,
            float(missing_docstring_count)/testcase_count * 100
        ),
        color
    ))
    if minimum_docstring_count == 0:
        color = CLR_GOOD
    else:
        color = CLR_ERR
    print(colored(PRINT_NO_MINIMUM_DOC_TC, attrs=['bold']) % colored(
        '{0}/{1} ({2:.02f}%)'.format(
            minimum_docstring_count,
            testcase_count,
            float(minimum_docstring_count)/testcase_count * 100
        ),
        color
    ))
    if invalid_tags_docstring_count == 0:
        color = CLR_GOOD
    else:
        color = CLR_ERR
    print(
        colored('Test cases with invalid tags: %s', attrs=['bold']) % colored(
            '{0}/{1} ({2:.02f}%)'.format(
                invalid_tags_docstring_count,
                testcase_count,
                float(invalid_tags_docstring_count)/testcase_count * 100
            ),
            color))

    if len(result) > 0:
        return -1


def bugs_report(testcases):
    """List test cases affected by bugs report."""
    result = {}
    affected_count = 0
    testcase_count = 0
    for path, tests in testcases.items():
        testcase_count += len(tests)
        for testcase in tests:
            if not testcase.bugs:
                continue
            for bug in testcase.bugs:
                if bug not in result:
                    result[bug] = {}
                if path not in result[bug]:
                    result[bug][path] = []
                result[bug][path].append(testcase.name)
                affected_count += 1

    if SETTINGS['json']:
        print(json.dumps(result))
        return

    for bug, paths in result.items():
        msg = 'Test cases affected by {0}'.format(bug)
        print('{0}\n{1}\n'.format(msg, '=' * len(msg)))
        for path, names in paths.items():
            print('{0}\n{1}\n'.format(path, '-' * len(path)))
            print('\n'.join(['* {0}'.format(name) for name in names]) + '\n')

    print(colored(
        PRINT_TC_AFFECTED_BUGS % '{0}/{1} ({2:.02f}%)'.format(
            affected_count,
            testcase_count,
            float(affected_count)/testcase_count * 100
        ),
        attrs=['bold']
    ))


def tags_report(testcases):
    """Lists the test cases matching the input tag."""
    result = {
        'tagged_testcases': [],
    }
    if not SETTINGS['input_tags']:
        print('Input tags required for this report.  See testimony --help')
        sys.exit()
    # Change the input tags to lower case
    input_tags_list = {tag.lower() for tag in SETTINGS['input_tags']}
    for _, tests in testcases.items():
        for testcase in tests:
            if testcase.tags:
                testcase_tags_list = {
                    tag.lower().strip()
                    for tag in testcase.tags.split(',')
                }
                # Check if any items in either list match. If so, derive the
                # full path of the test case. Expected sample output:
                # `tests.test_sample.Testsample1.test_positive_login_1`
                if testcase_tags_list.intersection(input_tags_list):
                    value = testcase.testmodule
                    if testcase.parent_class:
                        value = value + '.' + testcase.parent_class
                    value = value + '.' + testcase.name
                    value = value.replace('/', '.')
                    value = value.replace('.py', '', 1)
                    result['tagged_testcases'].append(value)
    if SETTINGS['json']:
        print(json.dumps(result))
        return
    print(result['tagged_testcases'])


def get_testcases(paths):
    """Walk each path in ``paths`` and return the test cases found.

    :param path: List o directories to find test modules and test cases.
    :return: A dict mapping a test module path and its test cases.
    """
    testmodules = []
    for path in paths:
        if os.path.isfile(path):
            if is_test_module(os.path.basename(path)):
                testmodules.append(path)
            continue
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                if is_test_module(filename):
                    testmodules.append(os.path.join(dirpath, filename))
    testcases = collections.OrderedDict()
    for testmodule in testmodules:
        testcases[testmodule] = []
        with open(testmodule) as handler:
            root = ast.parse(handler.read())
            root.path = testmodule
            for node in ast.iter_child_nodes(root):
                if isinstance(node, ast.ClassDef):
                    testcases[testmodule].extend([
                        TestFunction(subnode, node, root)
                        for subnode in ast.iter_child_nodes(node)
                        if isinstance(subnode, ast.FunctionDef) and
                        subnode.name.startswith('test_')
                    ])
                elif (isinstance(node, ast.FunctionDef) and
                      node.name.startswith('test_')):
                    # Module's test functions
                    testcases[testmodule].append(
                        TestFunction(node, testmodule=root)
                    )
    return testcases


def colored(text, color=None, attrs=None):
    """Use termcolor.colored if available otherwise return the same string."""
    if HAS_TERMCOLOR and not SETTINGS['nocolor']:
        return termcolor.colored(text, color=color, attrs=attrs)
    else:
        return text
