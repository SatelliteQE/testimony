# -*- encoding: utf-8 -*-
"""Main module for testimony"""

import argparse
import os.path

from testimony import main
from testimony.constants import REPORT_TAGS


def file_or_dir_arg(arg):
    """Checks if a path argument is a file or a directory."""
    if os.path.isdir(arg) or os.path.isfile(arg):
        return arg
    else:
        msg = '%s is not a file or a directory' % arg
        raise argparse.ArgumentTypeError(msg)


def parse_args():
    """Argument parser for testimony"""
    parser = argparse.ArgumentParser(
        description='Inspects and report on the Python test cases.',
        prog='testimony')
    parser.add_argument(
        'report', type=str, choices=REPORT_TAGS,
        metavar='REPORT',
        help='report type, possible values: %s' % ', '.join(REPORT_TAGS))
    parser.add_argument(
        'paths', metavar='PATH', type=file_or_dir_arg, nargs='+',
        help='a list of paths to look for tests cases')
    parser.add_argument(
        '-j', '--json', action='store_true', help='JSON output')
    parser.add_argument(
        '-n', '--nocolor', action='store_true', help='Do not use color option')
    parser.add_argument(
        '-t',
        '--tags',
        nargs='*',
        help='space separated tags to search.  Note: Always run this '
             'only in the root of the project where test cases are stored'
    )
    args = parser.parse_args()
    return args


def run(args):
    """Run testimony with given args"""
    main(args.report, args.paths, args.json, args.nocolor, args.tags)

if __name__ == "__main__":
    run(parse_args())
