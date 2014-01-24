# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

"""
Defines various constants
"""

# Per termcolor webpage, these are the available colors:
# grey, red, green, yellow, blue, magenta, cyan, white
ANSI_TAGS = [
    {'resource':'cyan'},
    {'error':'yellow'},
    {'good':'green'},
]

DOCSTRING_TAGS = [
    'Feature',
    'Test',
    'Setup',
    'Steps',
    'Assert',
    'BZ',
    'Status']

REPORT_TAGS = [
    'print',
    'summary',
    'validate_docstring',
    'bugs',
    'manual',
    'auto']
