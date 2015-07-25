#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import graken, Parser


__version__ = (2015, 7, 25, 20, 56, 55, 5)

__all__ = [
    'mask_ir_Parser',
    'mask_ir_Semantics',
    'main'
]


class mask_ir_Parser(Parser):
    def __init__(self, whitespace=None, nameguard=None, **kwargs):
        super(mask_ir_Parser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=None,
            eol_comments_re=None,
            ignorecase=None,
            **kwargs
        )

    @graken()
    def _comment_(self):
        self._pattern(r'#[^\n]*$')

    @graken()
    def _eol_(self):
        self._pattern(r'$\n')

    @graken()
    def _empty_line_(self):
        self._pattern(r'[\t ]*')
        self._eol_()

    @graken()
    def _indent_(self):
        self._pattern(r'[\t ]+')

    @graken()
    def _indent_opt_(self):
        self._pattern(r'[\t ]*')

    @graken()
    def _identifier_(self):
        self._pattern(r'[a-zA-Z0-9_.-]+')

    @graken()
    def _expr_(self):
        self._pattern(r'[^\n]*')

    @graken()
    def _assign_(self):
        self._identifier_()
        self.ast['to'] = self.last_node
        self._indent_()
        self._token('=')
        self._indent_()
        self._expr_()
        self.ast['val'] = self.last_node
        self._eol_()

        self.ast._define(
            ['to', 'val'],
            []
        )

    @graken()
    def _rule_(self):
        self._token('rule')
        self._indent_()
        self._identifier_()
        self.ast['name'] = self.last_node
        self._indent_opt_()
        self._eol_()

        def block1():
            self._indent_()
            self._assign_()
            self.ast['vars'] = self.last_node
        self._closure(block1)

        self.ast._define(
            ['name', 'vars'],
            []
        )

    @graken()
    def _path_(self):
        self._pattern(r'[^\n\t: ]+')

    @graken()
    def _path_list_(self):
        self._indent_()
        self._path_()
        self.ast.setlist('@', self.last_node)

        def block1():
            self._indent_()
            self._path_()
            self.ast.setlist('@', self.last_node)
        self._closure(block1)

    @graken()
    def _build_(self):
        self._token('build')
        self._path_list_()
        self.ast['outputs'] = self.last_node
        self._indent_opt_()
        self._token(':')
        self._indent_opt_()
        self._identifier_()
        self.ast['rule_name'] = self.last_node
        self._path_list_()
        self.ast['inputs'] = self.last_node
        self._indent_opt_()
        self._eol_()

        def block3():
            self._indent_()
            self._assign_()
            self.ast['vars'] = self.last_node
        self._closure(block3)

        self.ast._define(
            ['outputs', 'rule_name', 'inputs', 'vars'],
            []
        )

    @graken()
    def _manifest_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._empty_line_()
                with self._option():
                    self._comment_()
                with self._option():
                    self._assign_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._rule_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._build_()
                    self.ast.setlist('@', self.last_node)
                self._error('no available options')
        self._closure(block0)
        self._check_eof()


class mask_ir_Semantics(object):
    def comment(self, ast):
        return ast

    def eol(self, ast):
        return ast

    def empty_line(self, ast):
        return ast

    def indent(self, ast):
        return ast

    def indent_opt(self, ast):
        return ast

    def identifier(self, ast):
        return ast

    def expr(self, ast):
        return ast

    def assign(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def path(self, ast):
        return ast

    def path_list(self, ast):
        return ast

    def build(self, ast):
        return ast

    def manifest(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None, nameguard=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = mask_ir_Parser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace,
        nameguard=nameguard)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in mask_ir_Parser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for mask_ir_.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-n', '--no-nameguard', action='store_true',
                        dest='no_nameguard',
                        help="disable the 'nameguard' feature")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(
        args.file,
        args.startrule,
        trace=args.trace,
        whitespace=args.whitespace,
        nameguard=not args.no_nameguard
    )
