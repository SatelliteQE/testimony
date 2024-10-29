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

Currently only supported types are 'choice' and 'string'
but in the future more can be added.
"""

import yaml

from testimony.constants import TOKEN_TYPES


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

    Includes dynamic decorator handling.
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

        # set token type if available in TOKENS_TYPES
        if config.get('type') in TOKEN_TYPES:
            self.token_type = config['type']

        # additional handling for choice, string, and decorator types
        if self.token_type == 'choice':
            assert 'choices' in config
            assert isinstance(config['choices'], list)
            self.casesensitive = config.get('casesensitive', True)
            self.choices = [i if self.casesensitive else i.lower()
                            for i in config['choices']]

        elif self.token_type == 'decorator':
            # set specific defaults or validation parameters if needed
            self.decorator_name = config.get('decorator_name')
            self.default_value = config.get('default_value', None)

        elif self.token_type == 'string':
            pass

    def update(self, new_values):
        """Update token configuration with dictionary of new values."""
        for key, value in new_values.items():
            setattr(self, key, value)

    def validate(self, what):
        """Ensure that 'what' meets value validation criteria."""
        if self.token_type == 'choice':
            if not self.casesensitive:
                what = what.lower()
            return what in self.choices
        elif self.token_type == 'string':
            return isinstance(what, str)  # validate it's a string
        elif self.token_type == 'decorator':
            # Additional decorator-related validation if needed
            return what == self.default_value or what is not None
        return True  # assume valid for unknown types
