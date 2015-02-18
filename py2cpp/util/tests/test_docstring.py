# -*- coding: utf-8 -*-

import pytest

from .. import docstring

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
]

#===============================================================================
# get_type_hints

def test_simple_param():
    result = docstring.get_type_hints(DOCSTRINGS[0])
    assert result == {
        'params': {
            'x': 'str',
        },
        'rtype': 'void',
    }

def test_simple_type():
    result = docstring.get_type_hints(DOCSTRINGS[1])
    assert result == {
        'params': {
            'x': 'str',
        },
        'rtype': 'void',
    }

def test_simple_rtype():
    result = docstring.get_type_hints(DOCSTRINGS[2])
    assert result == {
        'params': {},
        'rtype': 'str',
    }
