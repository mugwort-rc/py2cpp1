# -*- coding: utf-8 -*-

import os
import re
import sys

import six

if six.PY3:
    # 2to3 applied library
    BASE_PATH = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(BASE_PATH, '2to3'))

from epydoc.markup.restructuredtext import parse_docstring

from .tuple_parser import parse as tuple_parse


TUPLE_RE = re.compile(r'^\(.*\)$')


class Type(object):
    def __init__(self, type, child=None):
        self.type = type
        self.child = child

    def __repr__(self):
        if self.child is not None:
            return '<{} of {}>'.format(self.type, repr(self.child))
        return '<{}>'.format(self.type)

    def __eq__(self, rhs):
        if type(rhs) != Type:
            return False
        return self.type == rhs.type and self.child == rhs.child

    @staticmethod
    def create(type):
        return Type(type)

class TupleType(object):
    def __init__(self, child=[]):
        self.child = child

    def __repr__(self):
        return '<({})>'.format(', '.join(map(repr, self.child)))

    def __eq__(self, rhs):
        if type(rhs) != TupleType:
            return False
        return self.child == rhs.child

    @staticmethod
    def create(child):
        return TupleType(child)


def get_type_hints(docstring):
    errors = []
    parsed = parse_docstring(docstring, errors)
    root,fields = parsed.split_fields()
    result = {
        'params': {},
        'rtype': Type('void'),
    }
    for field in fields:
        param,type,name = parse_field(field)
        if param == 'param':
            if name in result['params']:
                continue
            result['params'][name] = type
        elif param == 'type':
            result['params'][name] = type
        elif param == 'rtype':
            result['rtype'] = type
    return result

def parse_field(field):
    param = field.tag()
    arg = field.arg()
    body = field.body().to_plaintext(None)
    type,name = None,None
    if param == 'param':
        tmp = re.split(r'\s+', arg)
        type = detect_type(' '.join(tmp[:-1]))
        name = tmp[-1]
    elif param == 'type':
        type = detect_type(body)
        name = arg
    elif param == 'rtype':
        type = detect_type(body)
    return param,type,name

def detect_type(text):
    if TUPLE_RE.match(text):
        return tuple_detect(text)
    if text.startswith('list of') or text.startswith('dict of'):
        child = detect_type(text[7:].strip())
        return Type(text[:4], child)
    return Type.create(text)

def tuple_detect(text):
    data = tuple_parse(str(text))
    return make_tuple_type(data)

def make_tuple_type(data):
    child = []
    for d in data:
        if isinstance(d, str):
            child.append(detect_type(d))
        elif isinstance(d, tuple):
            child.append(make_tuple_type(d))
    return TupleType.create(child)
