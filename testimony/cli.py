# coding=utf-8
"""Testimony CLI utilities."""
import click

from testimony import SETTINGS, constants, main


@click.command()
@click.option('-j', '--json', help='JSON output', is_flag=True)
@click.option('-n', '--nocolor', default=False, help='Color output',
              is_flag=True)
@click.option('--tokens', help='Comma separated list of expected tokens')
@click.option(
    '--minimum-tokens', help='Comma separated list of minimum expected tokens')
@click.option(
    '--token-values', help='Comma separated list of allowed values for first' \
    ' token entered in tokens')
@click.argument('report', type=click.Choice(constants.REPORT_TAGS))
@click.argument('path', nargs=-1, type=click.Path(exists=True))
def testimony(
        json, nocolor, tokens, minimum_tokens, token_values, report, path):
    """Inspect and report on the Python test cases."""
    if tokens:
        SETTINGS['tokens'] = [
            token.strip().lower() for token in tokens.split(',')]
    if minimum_tokens:
        SETTINGS['minimum_tokens'] = [
            token.strip().lower() for token in minimum_tokens.split(',')]
    if token_values:
        SETTINGS['token_values'] = [
            token.strip().lower() for token in token_values.split(',')]
    main(report, path, json, nocolor)
