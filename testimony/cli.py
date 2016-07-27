# coding=utf-8
"""Testimony CLI utilities."""
import click

from testimony import SETTINGS, constants, main


def _validate_token_prefix(ctx, param, value):
    """Ensure single character for token prefix."""
    if len(value) != 1:
        raise click.BadParameter('token prefix should be a single character.')
    else:
        return value


@click.command()
@click.option('-j', '--json', help='JSON output', is_flag=True)
@click.option('-n', '--nocolor', default=False, help='Color output',
              is_flag=True)
@click.option('--tokens', help='Comma separated list of expected tokens')
@click.option(
    '--minimum-tokens', help='Comma separated list of minimum expected tokens')
@click.option(
    '--token-prefix',
    callback=_validate_token_prefix,
    default=':',
    help='Single character token prefix'
)
@click.argument('report', type=click.Choice(constants.REPORT_TAGS))
@click.argument('path', nargs=-1, type=click.Path(exists=True))
def testimony(
        json, nocolor, tokens, minimum_tokens, token_prefix, report, path):
    """Inspect and report on the Python test cases."""
    if tokens:
        SETTINGS['tokens'] = [token.strip() for token in tokens.split(',')]
    if minimum_tokens:
        SETTINGS['minimum_tokens'] = [
            token.strip() for token in minimum_tokens.split(',')]
    SETTINGS['token_prefix'] = token_prefix
    main(report, path, json, nocolor)
