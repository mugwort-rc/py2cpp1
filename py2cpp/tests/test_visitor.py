# -*- coding: utf-8 -*-

import ast

import pytest
import six
py2only = pytest.mark.skipif('six.PY3')
py3only = pytest.mark.skipif('six.PY2')

from ..visitor import SourceGenerator

def parse_source(src):
    return ast.parse(src).body[0]

def parse_expr(src):
    return parse_source(src).value

def generate(node):
    visitor = SourceGenerator()
    return visitor.visit(node)

#===============================================================================
# generators

SOURCES = {
    # Statements
    'Assert': "assert True",
    'Assign': "a = 72",
    'AugAssign': "a += 72",
    'ImportFrom': "from a import b",
    'Import': "import a",
    'Expr': "a",
    'FunctionDef': "def a():  pass",
    'ClassDef': "class a:  pass",
    'If': "if test:  pass",
    'For': "for i in range(72):  pass",
    'While': "while True:  pass",
    'With': "with True:  pass",
    'Pass': "pass",
    'Print': "print abc",
    'Delete': "del abc",
    'TryExcept': "try:  pass\nexcept:  pass",
    'TryFinally': "try:  pass\nfinally:  pass",
    'Global': "global a",
    'Nonlocal': "nonlocal a",
    'Return': "return a",
    'Break': "break",
    'Continue': "continue",
    'Raise': "raise a",
    # Expressions
    'Attribute': "a.b",
    'Call': "a()",
    'Name': "a",
    'Str': "'str'",
    'Bytes': "b'byte'",
    'Num': "72",
    'Tuple': "(a,b)",
    'List': "[]",
    'Set': "{a, b}",
    'Dict': "{}",
    'BinOp': "a & b",
    'BoolOp': "a and b",
    'Compare': "a == b",
    'UnaryOp': "not a",
    'Subscript': "a[:]",
    'Slice': "a[:]",  # node.slice
    'ExtSlice': "a[:,]",  # node.slice
    'Yield': "yield",
    'Lambda': "lambda: 72",
    'Ellipsis2': "a[...]",  # node.slice
    'Ellipsis3': "...",
    'ListComp': "[x for x in a]",
    'GeneratorExp': "(x for x in a)",
    'SetComp': "{x for x in a}",
    'DictComp': "{x:y for x in a}",
    'IfExp': "1 if True else 0",
    'Starred': "*a",
    'Repr': "`a`",
    # Helper Nodes
    'alias': "import a as b",  # node.names[0]
    'comprehension': "[x for x in a if a]",  # node.value.generators[0]
    'excepthandler': "try:  pass\nexcept:  pass",  # node.handlers[0]
    'arguments': "def func(a, b, c):  pass",  # node.args
}


# Statements

def gen_Assert():
    return parse_source(SOURCES['Assert'])

def gen_Assign():
    return parse_source(SOURCES['Assign'])

def gen_AugAssign():
    return parse_source(SOURCES['AugAssign'])

def gen_ImportFrom():
    return parse_source(SOURCES['ImportFrom'])

def gen_Import():
    return parse_source(SOURCES['Import'])

def gen_Expr():
    return parse_source(SOURCES['Expr'])

def gen_FunctionDef():
    return parse_source(SOURCES['FunctionDef'])

def gen_ClassDef():
    return parse_source(SOURCES['ClassDef'])

def gen_If():
    return parse_source(SOURCES['If'])

def gen_For():
    return parse_source(SOURCES['For'])

def gen_While():
    return parse_source(SOURCES['While'])

def gen_With():
    return parse_source(SOURCES['With'])

def gen_Pass():
    return parse_source(SOURCES['Pass'])

def gen_Print():
    return parse_source(SOURCES['Print'])

def gen_Delete():
    return parse_source(SOURCES['Delete'])

def gen_TryExcept():
    return parse_source(SOURCES['TryExcept'])

def gen_TryFinally():
    return parse_source(SOURCES['TryFinally'])

def gen_Global():
    return parse_source(SOURCES['Global'])

def gen_Nonlocal():
    return parse_source(SOURCES['Nonlocal'])

def gen_Return():
    return parse_source(SOURCES['Return'])

def gen_Break():
    return parse_source(SOURCES['Break'])

def gen_Continue():
    return parse_source(SOURCES['Continue'])

def gen_Raise():
    return parse_source(SOURCES['Raise'])

# Expressions

def gen_Attribute():
    return parse_expr(SOURCES['Attribute'])

def gen_Call():
    return parse_expr(SOURCES['Call'])

def gen_Name():
    return parse_expr(SOURCES['Name'])

def gen_Str():
    return parse_expr(SOURCES['Str'])

def gen_Bytes():
    return parse_expr(SOURCES['Bytes'])

def gen_Num():
    return parse_expr(SOURCES['Num'])

def gen_Tuple():
    return parse_expr(SOURCES['Tuple'])

def gen_List():
    return parse_expr(SOURCES['List'])

def gen_Set():
    return parse_expr(SOURCES['Set'])

def gen_Dict():
    return parse_expr(SOURCES['Dict'])

def gen_BinOp():
    return parse_expr(SOURCES['BinOp'])

def gen_BoolOp():
    return parse_expr(SOURCES['BoolOp'])

def gen_Compare():
    return parse_expr(SOURCES['Compare'])

def gen_UnaryOp():
    return parse_expr(SOURCES['UnaryOp'])

def gen_Subscript():
    return parse_expr(SOURCES['Subscript'])

def gen_Slice():
    return parse_expr(SOURCES['Slice']).slice

def gen_ExtSlice():
    return parse_expr(SOURCES['ExtSlice']).slice

def gen_Yield():
    return parse_expr(SOURCES['Yield'])

def gen_Lambda():
    return parse_expr(SOURCES['Lambda'])

def gen_Ellipsis():
    if six.PY2:
        return parse_expr(SOURCES['Ellipsis2']).slice
    else:
        return parse_expr(SOURCES['Ellipsis3'])

def gen_ListComp():
    return parse_expr(SOURCES['ListComp'])

def gen_GeneratorExp():
    return parse_expr(SOURCES['GeneratorExp'])

def gen_SetComp():
    return parse_expr(SOURCES['SetComp'])

def gen_DictComp():
    return parse_expr(SOURCES['DictComp'])

def gen_IfExp():
    return parse_expr(SOURCES['IfExp'])

def gen_Starred():
    return parse_expr(SOURCES['Starred'])

def gen_Repr():
    return parse_expr(SOURCES['Repr'])

# Helper Nodes

def gen_alias():
    return parse_source(SOURCES['alias']).names[0]

def gen_comprehension():
    return parse_source(SOURCES['comprehension']).value.generators[0]

def gen_excepthandler():
    return parse_source(SOURCES['excepthandler']).handlers[0]

def gen_arguments():
    return parse_source(SOURCES['arguments']).args

#===============================================================================
# source generator

# Statements

@py2only
def test_Print():
    node = gen_Print()
    result = generate(node)
    assert result == 'std::cout << abc << std::endl;'

# Expressions

def test_Name():
    node = gen_Name()
    result = generate(node)
    assert result == 'a'

def test_Str():
    node = gen_Str()
    result = generate(node)
    assert result == '"str"'
