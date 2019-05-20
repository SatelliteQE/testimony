# coding=utf-8

"""
Parse config for testimony.

Example:

    ---
    Status:
        type: choice
        choices:
            - Manual
            - Automated
    ...

Currently only supported type is 'choice', but in the future more can be added.
"""

import yaml

TOKEN_TYPES = ['choice']


def parse_config(filehandle):
    """Parse the config.

    :param filehandle: File handle to read config from
    """
    data = yaml.load(filehandle, Loader=yaml.SafeLoader)
    return {k.lower(): TokenConfig(k, v) for k, v in data.items()}


def update_tokens_dict(tokens_dict, new_keys, default_value=None):
    """Update dictionary by adding new keys and setting default value."""
    if isinstance(new_keys, str):
        new_keys = [token.strip().lower()
                    for token in new_keys.split(',')
                    if token.strip()]

    if default_value is None:
        default_value = {}

    for key in new_keys:
        if key in tokens_dict:
            tokens_dict[key].update(default_value)
        else:
            tokens_dict[key] = TokenConfig(key, default_value)


class TokenConfig(object):
    """
    Represent config for one token.

    Curently only checks for value.
    """

    def __init__(self, name, config):
        """
        Initialize token config object.

        Takes name of the token and actual config structure as a param
        """
        try:
            config.get('key')
        except AttributeError:
            config = {}

        self.name = name.lower()
        self.required = config.get('required', False)
        self.token_type = None

        if config.get('type') in TOKEN_TYPES:
            self.token_type = config['type']

        if self.token_type == 'choice':
            assert 'choices' in config
            assert isinstance(config['choices'], list)
            casesensitive = config.get('casesensitive', True)
            self.choices = [i if casesensitive else i.lower()
                            for i in config['choices']]

    def update(self, new_values):
        """Update token configuration with dictionary of new values."""
        for key, value in new_values.items():
            setattr(self, key, value)

    def validate(self, what):
        """Ensure that 'what' meets value validation criteria."""
        if self.token_type == 'choice':
            return what.lower() in self.choices
        return True  # assume valid for unknown types
