# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

import argparse
import os.path

from testimony import main
from testimony.constants import REPORT_TAGS


def dir_arg(arg):
    """Checks if a path argument is a directory"""
    if os.path.isdir(arg):
        return arg
    else:
        msg = '%s is not a directory' % arg
        raise argparse.ArgumentTypeError(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Inspects and report on the Python test cases.',
            prog='testimony')
    parser.add_argument('report', type=str, choices=REPORT_TAGS,
            metavar='REPORT',
            help='report type, possible values: %s' % ', '.join(REPORT_TAGS))
    parser.add_argument('paths', metavar='PATH', type=dir_arg, nargs='+',
            help='a list of paths to look for tests cases')

    args = parser.parse_args()
    main(args.report, args.paths)
