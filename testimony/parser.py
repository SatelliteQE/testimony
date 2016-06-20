# coding=utf-8
"""Docstring parser utilities for Testimony."""
import re

from testimony.constants import DEFAULT_MINIMUM_TOKENS, DEFAULT_TOKENS

TOKEN_RE = re.compile(r'^@(\w+):\s+([^@]+)(\n|$)', flags=re.MULTILINE)


class DocstringParser(object):
    """Parse docstring extracting tokens."""

    def __init__(self, tokens=None, minimum_tokens=None):
        """Initialize the parser with expected tokens and the minimum set."""
        if tokens is None:
            self.tokens = DEFAULT_TOKENS
        else:
            self.tokens = tokens
        if minimum_tokens is None:
            self.minimum_tokens = DEFAULT_MINIMUM_TOKENS
        else:
            self.minimum_tokens = minimum_tokens
        self.minimum_tokens = set(self.minimum_tokens)
        self.tokens = set(self.tokens)
        if not self.minimum_tokens.issubset(self.tokens):
            raise ValueError('tokens should contain minimum_tokens')

    def parse(self, docstring=None):
        """Parse the docstring and return the valid and invalid tokens.

        For example in the following docstring (using single quote to demo)::

            '''Docstring content.

            More docstring content.

            @valid_tag1: value1
            @valid_tag2: value2
            @invalid_tag1: value1
            @invalid_tag2: value2
            '''

        Will return a tuple with the following content::

            (
                {'valid_tag1': 'value1', 'valid_tag2': 'value2'},
                {'invalid_tag1': 'value1', 'invalid_tag2': 'value2'},
            )
        """
        if docstring is None:
            return {}, {}
        valid_tokens = {}
        invalid_tokens = {}
        for match in TOKEN_RE.finditer(docstring):
            token = match.group(1).strip().lower()
            value = match.group(2).strip()
            if token in self.tokens:
                valid_tokens[token] = value
            else:
                invalid_tokens[token] = value
        return valid_tokens, invalid_tokens

    def validate_tokens(self, tokens):
        """Check if the ``tokens`` is a superset of ``minimum_tokens``."""
        return self.minimum_tokens.issubset(tokens)
