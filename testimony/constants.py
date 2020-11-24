# coding=utf-8
"""Defines various constants."""

# Per termcolor webpage, these are the available colors: grey, red, green,
# yellow, blue, magenta, cyan, white
CLR_ERR = 'red'
CLR_GOOD = 'green'

PRINT_REPORT = 'print'
SUMMARY_REPORT = 'summary'
VALIDATE_DOCSTRING_REPORT = 'validate'

REPORT_TAGS = (
    PRINT_REPORT,
    SUMMARY_REPORT,
    VALIDATE_DOCSTRING_REPORT,
)

TOKEN_TYPES = [
    'choice',
]

DEFAULT_TOKENS = (
    'assert',
    'bz',
    'feature',
    'setup',
    'status',
    'steps',
    'tags',
    'test',
    'type',
)

DEFAULT_MINIMUM_TOKENS = (
    'assert',
    'feature',
    'test',
)

PRINT_INVALID_DOC = 'Total number of invalid docstrings'
PRINT_INVALID_VALUE = 'Test cases with unexpected token values in docstrings'
PRINT_UNEXPECTED_DOC_TC = 'Test cases with unexpected tags'
PRINT_NO_DOC = 'Test cases with no docstrings'
PRINT_NO_MINIMUM_DOC_TC = 'Test cases missing minimal docstrings'
PRINT_TOTAL_TC = 'Total number of tests'
PRINT_RST_PARSING_ISSUE = 'Test cases with unparseable docstrings'
