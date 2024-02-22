# coding=utf-8
"""Testimony CLI utilities."""
import click

from testimony import SETTINGS, config, constants, main


@click.command()
@click.option('-j', '--json', help='JSON output', is_flag=True)
@click.option('-m', '--markdown', help='mardown output', is_flag=True)
@click.option('-n', '--nocolor', default=False, help='Color output',
              is_flag=True)
@click.option('--tokens', help='Comma separated list of expected tokens')
@click.option(
    '--minimum-tokens', help='Comma separated list of minimum expected tokens')
@click.option(
    '-c', '--config', 'config_file', type=click.File(),
    help='Configuration file (YAML)')
@click.argument('report', type=click.Choice(constants.REPORT_TAGS))
@click.argument('path', nargs=-1, type=click.Path(exists=True))
def testimony(
        json, markdown, nocolor, tokens, minimum_tokens, config_file,
        report, path):
    """Inspect and report on the Python test cases."""
    if config_file:
        SETTINGS['tokens'] = config.parse_config(config_file)
    if tokens:
        config.update_tokens_dict(SETTINGS['tokens'], tokens)
    if minimum_tokens:
        config.update_tokens_dict(
            SETTINGS['tokens'], minimum_tokens, {'required': True})
    main(report, path, json, markdown, nocolor)
