# coding=utf-8
"""Testimony CLI utilities."""
import click

from testimony import main
from testimony.constants import REPORT_TAGS


@click.command()
@click.option('-j', '--json', help='JSON output', is_flag=True)
@click.option('-n', '--nocolor', default=False, help='Color output',
              is_flag=True)
@click.option(
    '-t', '--tag', multiple=True,
    help='specify a tag to search. This option can be specified multiple '
         'times. Note: Always run this only in the root of the project where '
         'test cases are stored'
)
@click.argument('report', type=click.Choice(REPORT_TAGS))
@click.argument('path', nargs=-1, type=click.Path(exists=True))
def testimony(json, nocolor, tag, report, path):
    """Inspects and report on the Python test cases."""
    main(report, path, json, nocolor, tag)
