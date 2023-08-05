# -*- coding: utf-8 -*-
#
# Copyright (c), 2016-2018, SISSA (International School for Advanced Studies).
# All rights reserved.
# This file is distributed under the terms of the MIT License.
# See the file 'LICENSE' in the root directory of the present
# distribution, or http://opensource.org/licenses/MIT.
#
# @author Davide Brunato <brunato@sissa.it>
#
"""
This module contains an XPath parser and other XPath related classes and functions.
"""
import re
from decimal import Decimal
from collections import MutableSequence
from abc import ABCMeta

from .exceptions import XMLSchemaXPathError, XMLSchemaSyntaxError
from .qnames import reference_to_qname


_RE_SPLIT_PATH = re.compile(r'/(?![^{}]*})')


def split_path(path):
    return _RE_SPLIT_PATH.split(path)


#
# XPath tokenizer
def get_xpath_tokenizer_pattern(symbols):
    tokenizer_pattern_template = r"""
        ('[^']*' | "[^"]*" | \d+(?:\.\d?)? | \.\d+) |   # Literals (strings or numbers)
        (%s|[%s]) |                                     # Symbols
        ((?:{[^}]+\})?[^/\[\]()@=|\s]+) |               # References and other names   
        \s+                                             # Skip extra spaces
    """

    def tokens_escape(s):
        s = re.escape(s)
        if s[-2:] == r'\(':
            s = '%s\s*%s' % (s[:-2], s[-2:])
        elif s[-4:] == r'\:\:':
            s = '%s\s*%s' % (s[:-4], s[-4:])
        return s

    symbols.sort(key=lambda x: -len(x))
    fence = len([i for i in symbols if len(i) > 1])
    return tokenizer_pattern_template % (
        '|'.join(map(tokens_escape, symbols[:fence])),
        ''.join(map(re.escape, symbols[fence:]))
    )


##
# XPath 1.0 and 2.0 symbols (functions are followed by '(' and axis are followed by '::'
#
XPATH_1_SYMBOLS = [
    'processing-instruction(', 'descendant-or-self::', 'following-sibling::',
    'preceding-sibling::', 'ancestor-or-self::', 'descendant::', 'attribute::',
    'following::', 'namespace::', 'preceding::', 'ancestor::', 'comment(', 'parent::',
    'child::', 'self::', 'text(', 'node(', 'and', 'mod', 'div', 'or',
    '..', '//', '!=', '<=', '>=', '(', ')', '[', ']', '.', '@', ',', '/', '|', '*',
    '-', '=', '+', '<', '>',

    # XPath Core function library
    'last(', 'position(', 'count(', 'id(', 'local-name(',   # Node set functions
    'namespace-uri(', 'name(',
    'string(', 'concat(', 'starts-with(', 'contains(',      # String functions
    'substring-before(', 'substring-after(', 'substring(',
    'string-length(', 'normalize-space(', 'translate(',
    'boolean(', 'not(', 'true(', 'false('                   # Boolean functions
]

XPATH_2_SYMBOLS = XPATH_1_SYMBOLS + [
    'union', 'intersect',
]

RELATIVE_PATH_TOKENS = {s for s in XPATH_2_SYMBOLS if s.endswith("::")} | {
    '(integer)', '(string)', '(decimal)', '(ref)', '*', '@', '..', '.', '(', '/'
}


#
# XPath parser based on Vaughan Pratt's algorithm.
# ref: http://effbot.org/zone/simple-top-down-parsing.htm
class TokenMeta(ABCMeta):
    """
    Token metaclass for register token classes.
    """
    registry = {}

    def __new__(mcs, name, bases, dict_):
        dict_['name'] = name
        lbp = dict_['lbp'] = dict_.pop('lbp', 0)
        nud = dict_.pop('nud', None)
        led = dict_.pop('led', None)

        try:
            token_class = mcs.registry[name]
        except KeyError:
            token_class = super(TokenMeta, mcs).__new__(mcs, "_%s_Token" % name, bases, dict_)
        else:
            if lbp > token_class.lbp:
                token_class.lbp = lbp

        if callable(nud):
            token_class.nud = nud
        if callable(led):
            token_class.led = led

        return token_class

    def __init__(cls, name, bases, dict_):
        cls.registry[dict_['name']] = cls
        super(TokenMeta, cls).__init__(name, bases, dict_)


class Token(MutableSequence):
    """
    Token class for defining a parser based on Pratt's method.

    :param value: the token value, its default is name.
    """
    __metaclass__ = TokenMeta

    name = None     # the token identifier, key in the symbol table.

    def __init__(self, value=None):
        self.value = value if value is not None else self.name
        self._operands = []

    def __getitem__(self, i):
        return self._operands[i]

    def __setitem__(self, i, item):
        self._operands[i] = item

    def __delitem__(self, i):
        del self._operands[i]

    def __len__(self):
        return len(self._operands)

    def insert(self, i, item):
        self._operands.insert(i, item)

    def __repr__(self):
        return u"<%s '%s' at %#x>" % (self.__class__.__name__, self.value, id(self))

    def __cmp__(self, other):
        return self.name == other.name and self.value == other.value

    @property
    def arity(self):
        return len(self)

    def nud(self):
        """Null denotation method"""
        raise XMLSchemaSyntaxError("Undefined operator for %r." % self.name)

    def led(self, left):
        """Left denotation method"""
        raise XMLSchemaSyntaxError("Undefined operator for %r." % self.name)

    def sed(self, context, results):
        """Select denotation method"""
        raise XMLSchemaSyntaxError("Undefined operator for %r." % self.name)

    def iter(self):
        for t in self[:1]:
            for token in t.iter():
                yield token
        yield self
        for t in self[1:]:
            for token in t.iter():
                yield token

    def iter_select(self, context):
        return self.sed(context, [context])

    def expected(self, name):
        if self.name != name:
            raise XMLSchemaXPathError("Expected %r token, found %r." % (name, str(self.value)))

    def unexpected(self, name=None):
        if not name or self.name == name:
            raise XMLSchemaXPathError("Unexpected %r token." % str(self.value))

    #
    # XPath selectors
    @staticmethod
    def self_selector():
        def select_self(_context, results):
            for elem in results:
                yield elem
        return select_self

    def descendant_selector(self):
        def select_descendants(context, results):
            results = self[0].sed(context, results)
            for elem in results:
                if elem is not None:
                    for e in elem.iter(self[1].value):
                        if e is not elem:
                            yield e
        return select_descendants

    def child_selector(self):
        def select_child(context, results):
            results = self[0].sed(context, results)
            return self[1].sed(context, results)
        return select_child

    def children_selector(self):
        def select_children(_context, results):
            for elem in results:
                if elem is not None:
                    for e in elem:
                        if self.value is None or e.tag == self.value:
                            yield e
        return select_children

    def value_selector(self):
        def select_value(_context, results):
            for elem in results:
                if elem is not None:
                    yield self.value
        return select_value

    # @attribute
    def attribute_selector(self):
        key = self.value

        def select_attribute(_context, results):
            if key is None:
                for elem in results:
                    if elem is not None:
                        for attr in elem.attrib.values():
                            yield attr
            elif '{' == key[0]:
                for elem in results:
                    if elem is not None and key in elem.attrib:
                        yield elem.attrib[key]
            else:
                for elem in results:
                    if elem is None:
                        continue
                    elif key in elem.attrib:
                        yield elem.attrib[key]

        return select_attribute

    # @attribute='value'
    def attribute_value_selector(self):
        key = self.value
        value = self[0].value

        def select_attribute_value(_context, results):
            if key is not None:
                for elem in results:
                    if elem is not None:
                        yield elem.get(key) == value
            else:
                for elem in results:
                    if elem is not None:
                        for attr in elem.attrib.values():
                            yield attr == value
        return select_attribute_value

    def find_selector(self):
        def select_find(_context, results):
            for elem in results:
                if elem is not None:
                    if elem.find(self.value) is not None:
                        yield elem
        return select_find

    def subscript_selector(self):
        value = self[1].value
        if value > 0:
            index = value - 1
        elif value == 0 or self[1].name not in ('last(', 'position('):
            index = None
        else:
            index = value

        def select_subscript(context, results):
            results = self[0].sed(context, results)
            if index is not None:
                try:
                    yield [elem for elem in results][index]
                except IndexError:
                    return
        return select_subscript

    def predicate_selector(self):
        def select_predicate(context, results):
            results = self[0].sed(context, results)
            for elem in results:
                if elem is not None:
                    predicate_results = list(self[1].sed(context, [elem]))
                    if predicate_results and any(predicate_results):
                        yield elem
        return select_predicate

    @staticmethod
    def parent_selector():
        def select_parent(context, results):
            parent_map = context.parent_map
            results_parents = []
            for elem in results:
                try:
                    parent = parent_map[elem]
                except KeyError:
                    pass
                else:
                    if parent not in results_parents:
                        results_parents.append(parent)
                        yield parent
        return select_parent

    # [tag='value']
    def tag_value_selector(self):
        def select_tag_value(_context, results):
            for elem in results:
                if elem is not None:
                    for e in elem.findall(self.name):
                        if "".join(e.itertext()) == self.value:
                            yield elem
                            break
        return select_tag_value

    def disjunction_selector(self):
        def select_disjunction(context, results):
            left_results = list(self[0].sed(context, results))
            right_results = list(self[1].sed(context, results))
            for elem in left_results:
                yield elem
            for elem in right_results:
                yield elem
        return select_disjunction

    def conjunction_selector(self):
        def select_conjunction(context, results):
            right_results = set(self[1].sed(context, results))
            for elem in self[0].sed(context, results):
                if elem in right_results:
                    yield elem
        return select_conjunction


#
# Helper functions/decorators
def symbol(name, lbp=0):
    """
    Create or update a token class. If the symbol is already registered
    just update the left binding power if it has a greater value.

    :param name: An identifier name for this token class and for its objects.
    :param lbp: Left binding power, default to 0.
    :return: Custom token class.
    """
    return TokenMeta(name.strip(), (Token,), {'lbp': lbp})


def register_symbols(*names, **kwargs):
    """
    Create or update token classes for a sequence of symbols. Pass a keyword argument 
    'lbp' for setting a left binding power greater than 0. If a symbol is already 
    registered just update the left binding power if it has a greater value.

    :param names: A tuple of identifiers for token classes and for their objects.
    """
    lbp = kwargs.pop('lbp', 0)
    for name in names:
        TokenMeta(name.strip(), (Token,), {'lbp': lbp})


def register_nud(*names, **kwargs):
    """
    Decorator to register a function as the null denotation method for a token class.
    Pass a keyword argument 'lbp' for setting a left binding power greater than 0.

    :param names: A tuple of identifiers for token classes and for their objects.
    """
    def nud_decorator(func):
        lbp = kwargs.pop('lbp', 0)
        for name in names:
            TokenMeta(name.strip(), (Token,), {'lbp': lbp, 'nud': func})
        return func

    return nud_decorator


def register_led(*names, **kwargs):
    """
    Decorator to register a function as the left denotation method for a token class.
    Pass a keyword argument 'lbp' for setting a left binding power greater than 0.

    :param names: A tuple of identifiers for token classes and for their objects.
    """
    def led_decorator(func):
        lbp = kwargs.get('lbp', 0)
        for name in names:
            TokenMeta(name.strip(), (Token,), {'lbp': lbp, 'led': func})
        return func

    return led_decorator


#
# XPath parser globals and main cycle
def dummy_advance(_name=None):
    return symbol('(end)')


advance = dummy_advance  # Replaced by active parser
current_token = None
next_token = None


def expression(rbp=0):
    """
    Recursive expression parser for expressions. Calls token.nud() and then 
    advance until the right binding power is less the left binding power of 
    the next token, invoking the led() method on the following token.

    :param rbp: right binding power for the expression.
    :return: left token.
    """
    global current_token, next_token
    advance()
    left = current_token.nud()
    while rbp < next_token.lbp:
        advance()
        left = current_token.led(left)
    return left


#
# XPath parser token registration
@register_nud('(end)')
def end_nud(self):
    return self


@register_nud('(string)', '(decimal)', '(integer)')
def value_nud(self):
    self.sed = self.value_selector()
    return self


@register_nud('(ref)')
def ref_token_nud(self):
    self.sed = self.children_selector()
    return self


@register_nud('*')
def star_token_nud(self):
    if next_token.name not in ('/', '[', '(end)', ')'):
        next_token.unexpected()
    self.value = None
    self.sed = self.children_selector()
    return self


@register_led('*', lbp=45)
def star_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(45))
    self.value = left.value + self[1].value
    return self


@register_nud('@', 'attribute::')
def attribute_token_nud(self):
    self.insert(0, advance())
    if self[0].name not in ('*', '(ref)'):
        raise XMLSchemaXPathError("invalid attribute specification for XPath.")
    if next_token.name != '=':
        self.sed = self[0].attribute_selector()
    else:
        advance('=')
        self[0].insert(0, advance('(string)'))
        self.sed = self[0].attribute_value_selector()
    return self


@register_led('or', lbp=20)
def or_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(20))
    self.sed = self.disjunction_selector()
    return self


@register_led('and', lbp=25)
def and_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(25))
    self.sed = self.conjunction_selector()
    return self


@register_nud('=', '!=', '<', '>', '<=', '>=', lbp=30)
def compare_token_nud(self):
    self.insert(0, expression(30))
    return self


@register_led('=', '!=', '<', '>', '<=', '>=', lbp=30)
def compare_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(30))
    return self


@register_nud('+')
def plus_token_nud(self):
    self.insert(0, expression(75))
    if not isinstance(self[0].value, int):
        raise XMLSchemaXPathError("an integer value is required: %r." % self[0])
    self.value = self[0].value
    return self


@register_led('+', lbp=40)
def plus_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(40))
    self.value = left.value + self[1].value
    return self


@register_nud('-')
def minus_token_nud(self):
    self.insert(0, expression(75))
    if not isinstance(self[0].value, int):
        raise XMLSchemaXPathError("an integer value is required: %r." % self[0])
    self.value = - self[0].value
    return self


@register_led('-', lbp=40)
def minus_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(40))
    self.value = left.value - self[1].value
    return self


@register_led('div', lbp=45)
def div_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(45))
    return self


@register_led('mod', lbp=45)
def mod_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(45))
    return self


@register_led('union', '|', lbp=50)
def union_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(50))
    self.sed = self.disjunction_selector()
    return self


@register_nud('.', 'self::node()', lbp=60)
def self_token_nud(self):
    self.sed = self.self_selector()
    return self


@register_nud('..', 'parent::node()', lbp=60)
def parent_token_nud(self):
    self.sed = self.parent_selector()
    return self


@register_nud('ancestor::', lbp=60)
def parent_token_nud(self):
    self.sed = self.parent_selector()
    return self


@register_nud('/')
def child_nud(_self):
    current_token.unexpected()


@register_led('/', lbp=80)
def child_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(100))
    if self[1].name not in RELATIVE_PATH_TOKENS:
        raise XMLSchemaXPathError("invalid child %r." % self[1])
    self.sed = self.child_selector()
    return self


@register_nud('child::', lbp=80)
def child_axis_nud(self):
    if next_token.name not in ('(ref)', '*'):
        raise XMLSchemaXPathError("invalid child axis %r." % next_token)
    self.insert(0, expression(80))
    self.sed = self[0].sed
    return self


@register_led('//', lbp=80)
def descendant_token_led(self, left):
    self.insert(0, left)
    self.insert(1, expression(100))
    if self[1].name not in RELATIVE_PATH_TOKENS:
        raise XMLSchemaXPathError("invalid descendant %r." % self[1])
    if self[0].name in ('*', '(ref)'):
        delattr(self[0], 'sed')
        self.value = self[0].value
    else:
        self.value = None
    self.sed = self.descendant_selector()
    return self


@register_nud('(', lbp=90)
def group_token_nud(self):
    next_token.unexpected(')')
    self.insert(0, expression())
    advance(')')
    return self[0]


@register_nud(')')
@register_led(')')
def right_round_bracket_token(*_args, **_kwargs):
    current_token.unexpected()


@register_nud('[', lbp=90)
def predicate_token_nud(_self):
    current_token.unexpected()


@register_led('[', lbp=90)
def predicate_token_led(self, left):
    next_token.unexpected(']')
    self.insert(0, left)
    self.insert(1, expression())
    if isinstance(self[1].value, int):
        self.sed = self.subscript_selector()
    else:
        self.sed = self.predicate_selector()
    advance(']')
    return self


@register_nud(']')
@register_led(']')
def predicate_close_token(*_args, **_kwargs):
    current_token.unexpected(']')


@register_nud('last(')
def last_function_token_nud(self):
    advance(')')
    if next_token.name == '-':
        advance('-')
        self.insert(0, advance('(integer)'))
        self.value = -1 - self[0].value
    else:
        self.value = -1
    return self


@register_nud('position(')
def position_function_token_nud(self):
    advance(')')
    advance('=')
    self.insert(0, expression(90))
    if not isinstance(self[0].value, int):
        raise XMLSchemaXPathError("an integer expression is required: %r." % self[0].value)
    self.value = self[0].value
    return self


##
# XPath parsers
#

class XPathParserMeta(ABCMeta):
    """
    XPathParser metaclass for creating versioned parsers.
    """
    def __init__(cls, name, bases, dict_):
        cls.VERSION = dict_.pop('version', 1)
        cls.token_table = dict_.pop('token_table', None)
        cls._tokenizer_pattern = re.compile(get_xpath_tokenizer_pattern(XPATH_2_SYMBOLS), re.VERBOSE)
        cls._NOT_ALLOWED_OPERATORS = {k for k in TokenMeta.registry if k not in cls.token_table}
        super(XPathParserMeta, cls).__init__(name, bases, dict_)


class XPathParserBase(object):
    """
    XPath expression iterator parser class.

    :param path: XPath expression.
    :param namespaces: optional prefix to namespace map.
    """
    __metaclass__ = XPathParserMeta
    token_table = ()
    _tokenizer_pattern = None
    _NOT_ALLOWED_OPERATORS = None

    def __init__(self, path, namespaces=None):
        if not path:
            raise XMLSchemaXPathError("empty XPath expression.")
        elif path[-1] == '/':
            raise XMLSchemaXPathError("invalid path: %r" % path)
        if path[:1] == "/":
            path = "." + path

        self.path = path
        self.namespaces = namespaces if namespaces is not None else {}

    def __iter__(self):
        self._tokens = iter(self._tokenizer_pattern.finditer(self.path))

    def __next__(self):
        token = self.advance()
        if token.name == '(end)':
            raise StopIteration()
        return token

    next = __next__

    def advance(self, name=None):
        global current_token, next_token
        if name:
            next_token.expected(name)

        while True:
            try:
                match = next(self._tokens)
            except StopIteration:
                current_token, next_token = next_token, self.token_table['(end)']()
                break
            else:
                current_token = next_token
                literal, operator, ref = match.groups()
                if operator is not None:
                    try:
                        next_token = self.token_table[operator.replace(' ', '')]()
                    except KeyError:
                        raise XMLSchemaXPathError("unknown operator %r." % operator)
                    else:
                        if operator in self._NOT_ALLOWED_OPERATORS:
                            raise XMLSchemaXPathError("not allowed operator %r." % operator)
                    break
                elif literal is not None:
                    if literal[0] in '\'"':
                        next_token = self.token_table['(string)'](literal.strip("'\""))
                    elif '.' in literal:
                        next_token = self.token_table['(decimal)'](Decimal(literal))
                    else:
                        next_token = self.token_table['(integer)'](int(literal))
                    break
                elif ref is not None:
                    if ':' in ref:
                        value = reference_to_qname(ref, self.namespaces)
                    else:
                        value = ref  # default namespace can't be applied to paths
                    next_token = self.token_table['(ref)'](value)
                    break
                elif str(match.group()).strip():
                    raise XMLSchemaXPathError("unexpected token: %r" % match)

        return current_token

    def parse(self):
        global advance
        advance = self.advance
        self.__iter__()
        advance()
        root_token = expression()
        if next_token.name != '(end)':
            next_token.unexpected()
        return root_token


def create_xpath_parser(name, version, symbols):
    return XPathParserMeta(
        name,
        (XPathParserBase,),
        {
            'version': version,
            'token_table': {
                k: v for k, v in TokenMeta.registry.items()
                if k in symbols or k in {'(integer)', '(string)', '(decimal)', '(ref)', '(end)'}
            }
        }
    )


XPath1Parser = create_xpath_parser('XPath1Parser', version=1, symbols=XPATH_1_SYMBOLS)
XPath2Parser = create_xpath_parser('XPath2Parser', version=2, symbols=XPATH_2_SYMBOLS)


_selector_cache = {}


def xsd_iterfind(context, path, namespaces=None):
    if path[:1] == "/":
        path = "." + path

    path_key = (id(context), path)
    try:
        return _selector_cache[path_key].iter_select(context)
    except KeyError:
        pass

    parser = XPath1Parser(path, namespaces)
    selector = parser.parse()
    if len(_selector_cache) > 100:
        _selector_cache.clear()
    _selector_cache[path] = selector
    return selector.iter_select(context)


def relative_path(path, levels, namespaces=None):
    """
    Return a relative XPath expression.
    
    :param path: An XPath expression.
    :param levels: Number of path levels to remove.
    :param namespaces: is an optional mapping from namespace 
    prefix to full qualified name.
    :return: a string with a relative XPath expression.
    """
    parser = XPath1Parser(path, namespaces)
    token_tree = parser.parse()
    path_parts = [t.value for t in token_tree.iter()]
    i = 0
    if path_parts[0] == '.':
        i += 1
    if path_parts[i] == '/':
        i += 1
    for value in path_parts[i:]:
        if levels <= 0:
            break
        if value == '/':
            levels -= 1
        i += 1
    return ''.join(path_parts[i:])


class XPathSelector(object):

    def __init__(self, path, namespaces=None, parser=XPath2Parser):
        self.parser = parser(path, namespaces)
        self._selector = self.parser.parse()

    def __repr__(self):
        return u'%s(path=%r, namespaces=%r, parser=%s)' % (
            self.__class__.__name__, self.path, self.namespaces, self.parser.__class__.__name__
        )

    @property
    def path(self):
        return self.parser.path

    @property
    def namespaces(self):
        return self.parser.namespaces

    def iter_select(self, context):
        return self._selector.iter_select(context)


class ElementPathMixin(object):
    """
    Mixin class that defines the ElementPath API.
    """
    @property
    def tag(self):
        return getattr(self, 'name')

    @property
    def attrib(self):
        return getattr(self, 'attributes')

    def iterfind(self, path, namespaces=None):
        """
        Generates all matching XSD/XML element declarations by path.

        :param path: is an XPath expression that considers the schema as the root element \
        with global elements as its children.
        :param namespaces: is an optional mapping from namespace prefix to full name.
        :return: an iterable yielding all matching declarations in the XSD/XML order.
        """
        return xsd_iterfind(self, path, namespaces or self.xpath_namespaces)

    def find(self, path, namespaces=None):
        """
        Finds the first XSD/XML element or attribute matching the path.

        :param path: is an XPath expression that considers the schema as the root element \
        with global elements as its children.
        :param namespaces: an optional mapping from namespace prefix to full name.
        :return: The first matching XSD/XML element or attribute or ``None`` if there is not match.
        """
        return next(xsd_iterfind(self, path, namespaces or self.xpath_namespaces), None)

    def findall(self, path, namespaces=None):
        """
        Finds all matching XSD/XML elements or attributes.

        :param path: is an XPath expression that considers the schema as the root element \
        with global elements as its children.
        :param namespaces: an optional mapping from namespace prefix to full name.
        :return: a list containing all matching XSD/XML elements or attributes. An empty list \
        is returned if there is no match.
        """
        return list(xsd_iterfind(self, path, namespaces or self.xpath_namespaces))

    @property
    def xpath_namespaces(self):
        if hasattr(self, 'namespaces'):
            namespaces = {k: v for k, v in self.namespaces.items() if k}
            if hasattr(self, 'xpath_default_namespace'):
                namespaces[''] = self.xpath_default_namespace
            return namespaces

    def iter(self, name=None):
        raise NotImplementedError

    def iterchildren(self, name=None):
        raise NotImplementedError
