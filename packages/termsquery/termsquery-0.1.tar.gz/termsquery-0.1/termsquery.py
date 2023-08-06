""" Boolean expressions to query containers.


Expressions grammar:

expr ::= and_expr { '|' and_expr}*
and_expr ::= item { '&' item }*
item ::= term
    | ~item
    | (expr)
"""
import re
from collections import namedtuple


class SyntaxError(Exception):
    pass


_Token = namedtuple('_Token', ['type', 'value', 'position'])


def _gen_tokens(pattern, text):
    for m in pattern.finditer(text):
        token = _Token(m.lastgroup, m.group(), m.span())
        if token.type == 'WS':
            continue
        yield token


class Expr:
    def eval(self, container):
        raise NotImplementedError


class UnaryExpr(Expr):
    def __init__(self, operand):
        self.operand = operand


class BinaryExpr(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class NotExpr(UnaryExpr):
    def eval(self, container):
        return not self.operand.eval(container)


class AndExpr(BinaryExpr):
    def eval(self, container):
        return self.left.eval(container) and self.right.eval(container)


class OrExpr(BinaryExpr):
    def eval(self, container):
        return self.left.eval(container) or self.right.eval(container)


class Term(Expr):
    def __init__(self, value):
        self.value = value

    def eval(self, container):
        return self.value in container


class _Parser:
    PATTERNS = [
        '(?P<TERM>(\w+|".*?"))',  # word or smth in quotes
        '(?P<LPAREN>\()',
        '(?P<RPAREN>\))',
        '(?P<AND>\&)',
        '(?P<OR>\|)',
        '(?P<NOT>\~)',
        '(?P<WS>\s+)',
        '(?P<ANY>.+?)'
    ]
    MASTER_PATTERN = re.compile('|'.join(PATTERNS))

    def __init__(self):
        self.terms = []
        self.expression = None

    def parse(self, text):
        self._tokens = _gen_tokens(self.MASTER_PATTERN, text)
        self._tok = None
        self._nexttok = None
        self._advance()
        self.expression = self._expr()
        if self._nexttok != None:
            raise SyntaxError('Unexpected token %s, position: %s' % (self._nexttok.value, self._nexttok.position))

    def _advance(self):
        self._tok, self._nexttok = self._nexttok, next(self._tokens, None)

    def _accept(self, toktype):
        if self._nexttok and self._nexttok.type == toktype:
            self._advance()
            return True
        return False

    def _expr(self):
        exprval = self._and_expr()
        while self._accept('OR'):
            right = self._and_expr()
            exprval = OrExpr(exprval, right)
        return exprval

    def _and_expr(self):
        exprval = self._item()
        while self._accept('AND'):
            right = self._item()
            exprval = AndExpr(exprval, right)
        return exprval

    def _item(self):
        if self._accept('NOT'):
            return NotExpr(self._expr())
        if self._accept('TERM'):
            if self._tok.value[0] == '"':
                term = Term(self._tok.value[1:-1])
            else:
                term = Term(self._tok.value)
            self.terms.append(term)
            return term
        if self._accept('LPAREN'):
            exprval = self._expr()
            if not self._accept('RPAREN'):
                raise SyntaxError('Right parenthesis is missing')
            return exprval
        raise SyntaxError('Unexpected token %s, position: %s' % (self._nexttok.value, self._nexttok.position))


class TermsQuery:
    def __init__(self, expression_source):
        parser = _Parser()
        parser.parse(expression_source)
        self.expression = parser.expression
        self.terms = tuple(parser.terms)

    def __call__(self, container):
        return self.expression.eval(container)

    def convert_values(self, conversion_function):
        """convert terms values"""
        for term in self.terms:
            term.value = conversion_function(term.value)
