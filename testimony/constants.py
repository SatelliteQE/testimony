# -*- encoding: utf-8 -*-
"""Defines various constants"""

# Per termcolor webpage, these are the available colors:
# grey, red, green, yellow, blue, magenta, cyan, white
CLR_RESOURCE = 'cyan'
CLR_ERR = 'red'
CLR_GOOD = 'green'

PRINT_REPORT = 'print'
SUMMARY_REPORT = 'summary'
VALIDATE_DOCSTRING_REPORT = 'validate_docstring'
BUGS_REPORT = 'bugs'
MANUAL_REPORT = 'manual'
AUTO_REPORT = 'auto'
TAGS_REPORT = 'tags'

REPORT_TAGS = (
    PRINT_REPORT,
    SUMMARY_REPORT,
    VALIDATE_DOCSTRING_REPORT,
    BUGS_REPORT,
    MANUAL_REPORT,
    AUTO_REPORT,
    TAGS_REPORT,
)

PRINT_TOTAL_TC = 'Total Number of test cases:      %s'
PRINT_AUTO_TC = 'Total Number of automated cases: %d '
PRINT_MANUAL_TC = 'Total Number of manual cases:    %d '
PRINT_NO_DOC = 'Test cases with no docstrings:   %s '
PRINT_PARSE_ERR = '!!!!!Exception in parsing DocString!!!!!'
PRINT_TC_AFFECTED_BUGS = '\nTotal Number of test cases affected by bugs: %s'
PRINT_INVALID_DOC = 'Total Number of invalid docstrings:  %s'
PRINT_DOC_MISSING = 'Docstring missing. Please update. '
PRINT_NO_MINIMUM_DOC_TC = 'Test cases missing minimal docstrings:  %s'
PRINT_NO_MINIMUM_DOC = 'Need feature, test and assert at the minimum'
