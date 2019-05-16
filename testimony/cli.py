# coding=utf-8
"""Testimony CLI utilities."""
import click
import yaml

from testimony import SETTINGS, constants, main


@click.command()
@click.option('-j', '--json', help='JSON output', is_flag=True)
@click.option('-n', '--nocolor', default=False, help='Color output',
              is_flag=True)
@click.option('--tokens', help='Comma separated list of expected tokens')
@click.option(
    '--minimum-tokens', help='Comma separated list of minimum expected tokens')
@click.option(
    '--token-values', help='Yaml file with allowed values per token')
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
        with open(token_values, 'r') as fp:
            data = yaml.load(fp, Loader=yaml.SafeLoader)
            SETTINGS['token_values'] = {k.lower(): v for k, v in data.items()}
    main(report, path, json, nocolor)
