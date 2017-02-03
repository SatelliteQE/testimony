# coding=utf-8
"""Docstring manipulation methods to create test reports."""
from __future__ import print_function, unicode_literals

import ast
import collections
import itertools
import json
import os
import sys
import textwrap

from testimony.constants import (
    CLR_ERR,
    CLR_GOOD,
    PRINT_INVALID_DOC,
    PRINT_NO_DOC,
    PRINT_NO_MINIMUM_DOC_TC,
    PRINT_REPORT,
    PRINT_TOTAL_TC,
    SUMMARY_REPORT,
    VALIDATE_DOCSTRING_REPORT,
)
from testimony.parser import DocstringParser

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
    """Add 'prefix' to the beginning of selected lines in 'text'.

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
    """Indicate if ``filename`` match a test module file name."""
    return filename.startswith('test_') and filename.endswith('.py')


class TestFunction(object):
    """Wrapper for ``ast.FunctionDef`` which parse docstring information.

    The ``tokens`` and ``invalid_tokens`` parameters provide meaningful
    information about the test.
    """

    def __init__(self, function_def, parent_class=None, testmodule=None):
        """A ``ast.FunctionDef`` instance used to extract information."""
        self.docstring = ast.get_docstring(function_def)
        self.function_def = function_def
        self.name = function_def.name
        self.parent_class = parent_class.name
        self.parent_class_def = parent_class
        self.class_docstring = ast.get_docstring(self.parent_class_def)
        self.testmodule = testmodule.path
        self.module_def = testmodule
        self.module_docstring = ast.get_docstring(self.module_def)
        self.pkginit = os.path.join(
            os.path.dirname(self.testmodule), '__init__.py')
        if os.path.exists(self.pkginit):
            self.pkginit_def = ast.parse(''.join(open(self.pkginit)))
            self.pkginit_docstring = ast.get_docstring(self.pkginit_def)
        else:
            self.pkginit_def = None
            self.pkginit_docstring = None
        self.tokens = {}
        self.invalid_tokens = {}
        self.parser = DocstringParser(
            SETTINGS.get('tokens'),
            SETTINGS.get('minimum_tokens'),
        )
        self._parse_docstring()

    def _parse_docstring(self):
        """Parse module, class and function docstrings.

        ``tokens`` and ``invalid_tokens`` attributes will be updated  with the
        parsed values.
        """
        if self.docstring is None:
            return

        # Parse module, class and function docstrings. Every loop updates the
        # already defined tokens and invalid_tokens. The order of processing
        # ensures that function docstring has more priority over class and
        # module docstrings respectively.
        docstrings = [
            self.pkginit_docstring,
            self.module_docstring,
            self.class_docstring,
            self.docstring,
        ]
        for docstring in docstrings:
            if docstring and not isinstance(docstring, type(u'')):
                docstring = docstring.decode('utf-8')
            tokens, invalid_tokens = self.parser.parse(docstring)
            self.tokens.update(tokens)
            self.invalid_tokens.update(invalid_tokens)

        # Always use the first line of docstring as test case name
        if self.tokens.get('test') is None:
            if docstring and not isinstance(docstring, type(u'')):
                docstring = self.docstring.decode('utf-8')
            self.tokens['test'] = docstring.strip().split('\n')[0]

    @property
    def has_valid_docstring(self):
        """Indicate if the docstring has the minimum tokens."""
        return self.parser.validate_tokens(self.tokens)

    def to_dict(self):
        """Return tokens invalid-tokens as a dict."""
        return {
            'tokens': self.tokens.copy(),
            'invalid-tokens': self.invalid_tokens.copy(),
        }

    def __str__(self):
        """String representation for a test and its tokens."""
        output = []
        for token, value in sorted(self.tokens.items()):
            output.append('{0}:\n{1}\n'.format(
                token.capitalize(), indent(value, ' ')))
        if self.invalid_tokens:
            output.append(
                'Unexpected tokens:\n' +
                '\n'.join([
                    textwrap.fill(
                        '{0}: {1}'.format(key.capitalize(), value),
                        initial_indent=' ' * 2,
                        subsequent_indent=' ' * 4
                    )
                    for key, value in sorted(self.invalid_tokens.items())
                ])
            )
        return '\n'.join(output)


def main(report, paths, json_output, nocolor):
    """Main function for testimony project.

    Expects a valid report type and valid directory paths, hopefully argparse
    is taking care of validation
    """
    SETTINGS['json'] = json_output
    SETTINGS['nocolor'] = nocolor

    if report == SUMMARY_REPORT:
        report_function = summary_report
    elif report == PRINT_REPORT:
        report_function = print_report
    elif report == VALIDATE_DOCSTRING_REPORT:
        report_function = validate_docstring_report
    sys.exit(report_function(get_testcases(paths)))


def print_report(testcases):
    """Print the list of test cases.

    :param testcases: A dict where the key is a path and value is a list of
        found testcases on that path.
    """
    result = {}
    for path, tests in testcases.items():
        result[path] = [test.to_dict() for test in tests]
        if not SETTINGS['json']:
            print('{0}\n{1}\n'.format(
                colored(path, attrs=['bold']), '=' * len(path)))
            if len(tests) == 0:
                print('No test cases found.\n')
            for test in tests:
                print('{0}\n{1}\n\n{2}\n'.format(
                    test.name, '-' * len(test.name), test))

    if SETTINGS['json']:
        print(json.dumps(result))
        return 0


def summary_report(testcases):
    """Summary about the test cases report."""
    count = no_docstring = 0
    tokens_count = collections.defaultdict(lambda: 0)
    for testcase in itertools.chain(*testcases.values()):
        count += 1
        if testcase.docstring is None:
            no_docstring += 1
        for token in testcase.tokens.keys():
            tokens_count[token] += 1

    def percentage(value):
        """Calculate the percentage of the value on the total."""
        return value / float(count) * 100
    summary_result = {
        'count': count,
        'no_docstring': no_docstring,
        'tokens': dict(tokens_count),
    }

    if SETTINGS['json']:
        print(json.dumps(summary_result))
        return 0

    column_size = max([len(column) for column in itertools.chain(
        [PRINT_TOTAL_TC, PRINT_NO_DOC],
        tokens_count.keys(),
    )])
    value_column_size = max([len(column) for column in itertools.chain(
        [str(count), str(no_docstring)],
        [str(value) for value in tokens_count.values()],
    )])
    value_fmt = '{{}}:{{}}{{: >{}}} ({{:05.2f}}%)'.format(value_column_size)
    print('{}:{}{}'.format(
        PRINT_TOTAL_TC,
        ' ' * (column_size - len(PRINT_TOTAL_TC) + 2),
        count
    ))
    print(value_fmt.format(
        PRINT_NO_DOC,
        ' ' * (column_size - len(PRINT_NO_DOC) + 2),
        no_docstring,
        percentage(no_docstring)
    ))
    for token, value in sorted(tokens_count.items()):
        print(value_fmt.format(
            token.capitalize(),
            ' ' * (column_size - len(token) + 2),
            value,
            percentage(value)
        ))


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
                    'Docstring should have at least {} token(s)'.format(
                        ', '.join(sorted(testcase.parser.minimum_tokens))
                    )
                )
                minimum_docstring_count += 1
            if testcase.invalid_tokens:
                issues.append('Unexpected tokens:\n{0}'.format(
                    indent(
                        '\n'.join([
                            '{0}: {1}'.format(key.capitalize(), value)
                            for key, value in
                            sorted(testcase.invalid_tokens.items())
                        ]),
                        '  '
                    )
                ))
                invalid_tags_docstring_count += 1
            if issues:
                result.setdefault(
                    path, collections.OrderedDict())[testcase.name] = issues
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
    print('{}: {}'.format(
        PRINT_TOTAL_TC,
        testcase_count,
    ))
    print('{}: {} ({:05.02f}%)'.format(
        PRINT_INVALID_DOC,
        colored(invalid_docstring_count, color, attrs=['bold']),
        float(invalid_docstring_count)/testcase_count * 100
    ))
    if missing_docstring_count == 0:
        color = CLR_GOOD
    else:
        color = CLR_ERR
    print('{}: {} ({:.02f}%)'.format(
        PRINT_NO_DOC.strip(),
        colored(missing_docstring_count, color, attrs=['bold']),
        float(missing_docstring_count)/testcase_count * 100
    ))
    if minimum_docstring_count == 0:
        color = CLR_GOOD
    else:
        color = CLR_ERR
    print('{}: {} ({:.02f}%)'.format(
        PRINT_NO_MINIMUM_DOC_TC,
        colored(minimum_docstring_count, color, attrs=['bold']),
        float(minimum_docstring_count)/testcase_count * 100
    ))
    if invalid_tags_docstring_count == 0:
        color = CLR_GOOD
    else:
        color = CLR_ERR
    print('{}: {} ({:.02f}%)'.format(
        'Test cases with invalid tags',
        colored(invalid_tags_docstring_count, color, attrs=['bold']),
        float(invalid_tags_docstring_count)/testcase_count * 100
    ))

    if len(result) > 0:
        return -1


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
