# -*- coding: utf-8 -*-

from py2cpp.util.tuple_parser import parse

#===============================================================================
# parse

def test_tuple_parse():
    assert parse('(aaa, bbb, ccc)') == ('aaa', 'bbb', 'ccc')
    assert parse('(aaa, bbb, ccc,)') == ('aaa', 'bbb', 'ccc')
    assert parse('(aaa,)') == ('aaa',)
    assert parse('(list of aaa,)') == ('list of aaa',)
    assert parse('(tuple, (in tuple,))') == ('tuple', ('in tuple',))
    # Error
    assert parse('(aaa)') == ()
    assert parse('(aaa') == ()
    assert parse('(aaa, ())') == ()
