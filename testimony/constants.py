# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

"""
Defines various constants
"""

# Per termcolor webpage, these are the available colors:
# grey, red, green, yellow, blue, magenta, cyan, white
ANSI_TAGS = [
    {'resource': 'cyan'},
    {'error': 'red'},
    {'good': 'green'},
]

DOCSTRING_TAGS = [
    'feature',
    'test',
    'setup',
    'steps',
    'assert',
    'bz',
    'status']

REPORT_TAGS = [
    'print',
    'summary',
    'validate_docstring',
    'bugs',
    'manual',
    'auto']

PRINT_TOTAL_TC = 'Total Number of test cases:      %s'
PRINT_AUTO_TC = 'Total Number of automated cases: %s'
PRINT_MANUAL_TC = 'Total Number of manual cases:    %s'
PRINT_NO_DOC = 'Test cases with no docstrings:   %s'
PRINT_PARSE_ERR = '!!!!!Exception in parsing DocString!!!!!'
