# coding=utf-8
"""Docstring parser utilities for Testimony."""
from collections import namedtuple
from io import StringIO
from xml.etree import ElementTree

from docutils.core import publish_string
from docutils.parsers.rst import nodes, roles
from docutils.readers import standalone
from docutils.transforms import frontmatter

from testimony.constants import DEFAULT_MINIMUM_TOKENS, DEFAULT_TOKENS

RSTParseMessage = namedtuple('RSTParseMessage', 'line level message')


class _NoDocInfoReader(standalone.Reader):
    """Reader that does not do the DocInfo transformation.

    Extend standalone reader and drop the DocInfo transformation. Without that
    transformation, the first field list element will remain a field list and
    won't be converted to a docinfo element.
    """

    def get_transforms(self):
        """Get default transforms without DocInfo."""
        transforms = standalone.Reader.get_transforms(self)
        transforms.remove(frontmatter.DocInfo)
        return transforms


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

        for role in (
                'data', 'exc', 'func', 'class', 'const', 'attr', 'meth', 'mod',
                'obj'
        ):
            roles.register_generic_role(role, nodes.raw)
            roles.register_generic_role('py:' + role, nodes.raw)

    def parse(self, docstring=None):
        """Parse docstring and report parsing issues, valid and invalid tokens.

        For example in the following docstring (using single quote to demo)::

            '''Docstring content.

            More docstring content.

            :valid_tag1: value1
            :valid_tag2: value2
            :invalid_tag1: value1
            :invalid_tag2: value2
            '''

        Will return a tuple with the following content::

            (
                {'valid_tag1': 'value1', 'valid_tag2': 'value2'},
                {'invalid_tag1': 'value1', 'invalid_tag2': 'value2'},
                [],  # List of RSTParseMessage with any formatting issue found
            )
        """
        if docstring is None:
            return {}, {}, []
        tokens_dict = {}
        valid_tokens = {}
        invalid_tokens = {}

        # Parse the docstring with the docutils RST parser and output the
        # result as XML, this ease the process of getting the tokens
        # information.
        warning_stream = StringIO()
        docstring_xml = publish_string(
            docstring,
            reader=_NoDocInfoReader(),
            settings_overrides={
                'embed_stylesheet': False,
                'input_encoding': 'utf-8',
                'syntax_highlight': 'short',
                'warning_stream': warning_stream,
            },
            writer_name='xml',
        )

        rst_parse_messages = []
        for warning in warning_stream.getvalue().splitlines():
            if not warning or ':' not in warning:
                continue
            warning = warning.split(' ', 2)
            rst_parse_messages.append(RSTParseMessage(
                line=int(warning[0].split(':')[1]),
                level=warning[1].split('/')[0][1:].lower(),
                message=warning[2],
            ))
        warning_stream.close()

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

        return valid_tokens, invalid_tokens, rst_parse_messages

    def validate_tokens(self, tokens):
        """Check if the ``tokens`` is a superset of ``minimum_tokens``."""
        return self.minimum_tokens.issubset(tokens)
