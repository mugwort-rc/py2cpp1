# -*- coding: utf-8 -*-

import pytest

from .. import docstring
from ..docstring import Type

DOCSTRINGS = [
    # 0: test_simple_param
    """
    :param str x:
    """,
    # 1: test_simple_type
    """
    :type x: str
    """,
    # 2: test_simple_rtype
    """
    :rtype: str
    """,
    # 3: test_list_param
    """
    :param list of str x:
    """,
    # 4: test_list_type
    """
    :type x: list of str
    """,
    # 5: test_list_rtype
    """
    :rtype: list of str
    """,
    # 6: test_dict_param
    """
    :param dict of str x:
    """,
    # 7: test_dict_type
    """
    :type x: dict of str
    """,
    # 8: test_dict_rtype
    """
    :rtype: dict of str
    """,
]

#===============================================================================
# get_type_hints

def test_simple_param():
    result = docstring.get_type_hints(DOCSTRINGS[0])
    assert result == {
        'params': {
            'x': Type('str'),
        },
        'rtype': Type('void'),
    }

def test_simple_type():
    result = docstring.get_type_hints(DOCSTRINGS[1])
    assert result == {
        'params': {
            'x': Type('str'),
        },
        'rtype': Type('void'),
    }

def test_simple_rtype():
    result = docstring.get_type_hints(DOCSTRINGS[2])
    assert result == {
        'params': {},
        'rtype': Type('str'),
    }

def test_list_param():
    result = docstring.get_type_hints(DOCSTRINGS[3])
    assert result == {
        'params': {
            'x': Type('list', Type('str')),
        },
        'rtype': Type('void'),
    }

def test_list_type():
    result = docstring.get_type_hints(DOCSTRINGS[4])
    assert result == {
        'params': {
            'x': Type('list', Type('str')),
        },
        'rtype': Type('void'),
    }

def test_list_rtype():
    result = docstring.get_type_hints(DOCSTRINGS[5])
    assert result == {
        'params': {},
        'rtype': Type('list', Type('str')),
    }

def test_dict_param():
    result = docstring.get_type_hints(DOCSTRINGS[6])
    assert result == {
        'params': {
            'x': Type('dict', Type('str')),
        },
        'rtype': Type('void'),
    }

def test_dict_type():
    result = docstring.get_type_hints(DOCSTRINGS[7])
    assert result == {
        'params': {
            'x': Type('dict', Type('str')),
        },
        'rtype': Type('void'),
    }

def test_dict_rtype():
    result = docstring.get_type_hints(DOCSTRINGS[8])
    assert result == {
        'params': {},
        'rtype': Type('dict', Type('str')),
    }
