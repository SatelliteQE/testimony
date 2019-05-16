# -*- coding: UTF-8 -*-

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

import sys
import yaml

TOKEN_TYPES = ['choice']


def parse_config(filename):
    """Parse the config."""
    try:
        with open(filename, 'r') as fp:
            data = yaml.load(fp, Loader=yaml.SafeLoader)
            return {k.lower(): TokenConfig(k, v) for k, v in data.items()}
    except FileNotFoundError:
        print('ERROR: File {} not found'.format(filename))
        sys.exit(1)


class TokenConfig(object):
    """
    Represent config for one token.

    Curently only chacks for value.
    """

    def __init__(self, name, config):
        """
        Initialize token config object.

        Takes name of the token and actual config structure as a param
        """
        self.name = name.lower()

        assert 'type' in config
        assert config['type'] in TOKEN_TYPES
        self.token_type = config['type']

        if self.token_type == 'choice':
            assert 'choices' in config
            assert isinstance(config['choices'], list)
            self.choices = [i.lower() for i in config['choices']]

    def validate(self, what):
        """Ensure that 'what' meets value validation criteria."""
        if self.token_type == 'choice':
            return what.lower() in self.choices
