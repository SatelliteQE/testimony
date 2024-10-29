# coding=utf-8
"""Testimony CLI utilities."""
import click

from testimony import SETTINGS, config, constants, main

from testimony.parser import DocstringParser  # Import the parser with dynamic loading

@click.command()
@click.option('-j', '--json', help='JSON output', is_flag=True)
@click.option('-m', '--markdown', help='markdown output', is_flag=True)
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
    # load config if possible
    if config_file:
        SETTINGS['tokens'] = config.parse_config(config_file)
    if tokens:
        config.update_tokens_dict(SETTINGS['tokens'], tokens)
    if minimum_tokens:
        config.update_tokens_dict(SETTINGS['tokens'], minimum_tokens, {'required': True})

    # initialize the parser
    parser = DocstringParser(tokens=SETTINGS['tokens'], minimum_tokens=SETTINGS['tokens'].get('required', []))

    # loop through each provided path and parse
    results = []
    for module_path in path:
        try:
            # load and parse module dynamically
            valid_tokens, invalid_tokens, parse_messages = parser.load_and_parse(module_path)
            results.append({
                'module': module_path,
                'valid_tokens': valid_tokens,
                'invalid_tokens': invalid_tokens,
                'parse_messages': parse_messages
            })
        except Exception as e:
            print(f"Error processing module {module_path}: {e}")

    # Generate report
    if json:
        import json as json_lib
        print(json_lib.dumps(results, indent=2))
    elif markdown:
        for result in results:
            print(f"## Report for {result['module']}")
            print("### Valid Tokens")
            for token, value in result['valid_tokens'].items():
                print(f"- **{token}**: {value}")
            print("### Invalid Tokens")
            for token, value in result['invalid_tokens'].items():
                print(f"- **{token}**: {value}")
            print("### Parse Messages")
            for message in result['parse_messages']:
                print(f"- {message}")
    else:
        for result in results:
            print(f"Report for {result['module']}")
            print("Valid Tokens:", result['valid_tokens'])
            print("Invalid Tokens:", result['invalid_tokens'])
            print("Parse Messages:", result['parse_messages'])
