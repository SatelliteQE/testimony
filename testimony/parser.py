# coding=utf-8
"""Docstring parser utilities for Testimony."""
from docutils.core import publish_string
from xml.etree import ElementTree

from testimony.constants import DEFAULT_MINIMUM_TOKENS, DEFAULT_TOKENS


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
        tokens_dict = {}
        valid_tokens = {}
        invalid_tokens = {}

        # Parse the docstring with the docutils RST parser and output the
        # result as XML, this ease the process of getting the tokens
        # information.
        docstring_xml = publish_string(docstring, writer_name='xml')
        root = ElementTree.fromstring(docstring_xml)
        tokens = root.findall('./field_list/field')
        for token in tokens:
            token_name = token.find('./field_name').text.lower()
            value_el = token.find('./field_body/')
            if value_el is None:
                invalid_tokens[token_name] = ''
                continue
            if value_el.tag == 'paragraph':
                value = value_el.text
            if value_el.tag == 'enumerated_list':
                value_lst = map(lambda elem: elem.text,
                                value_el.findall('./list_item/paragraph'))
                list_enum = list(enumerate(value_lst, start=1))
                steps = map(lambda val: u'{}. {}'.format(val[0], val[1]),
                            list_enum)
                value = '\n'.join(steps)
            tokens_dict[token_name] = value

        for token, value in tokens_dict.items():
            if token in self.tokens:
                valid_tokens[token] = value
            else:
                invalid_tokens[token] = value

        return valid_tokens, invalid_tokens

    def validate_tokens(self, tokens):
        """Check if the ``tokens`` is a superset of ``minimum_tokens``."""
        return self.minimum_tokens.issubset(tokens)
