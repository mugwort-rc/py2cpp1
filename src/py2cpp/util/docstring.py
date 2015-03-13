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


class Type(object):
    def __init__(self, type, child=None):
        self.type = type
        self.child = child

    def __repr__(self):
        if self.child is not None:
            return '<{} of {}>'.format(self.type, repr(self.child))
        return '<{}>'.format(self.type)

    def __eq__(self, rhs):
        return self.type == rhs.type and self.child == rhs.child

    @staticmethod
    def create(type):
        return Type(type)


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
    if text.startswith('list of') or text.startswith('dict of'):
        child = detect_type(text[7:].strip())
        return Type(text[:4], child)
    return Type.create(text)
