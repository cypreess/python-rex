# import unittest
import re

from pytest import raises

import rex as rex_module
from rex import rex_clear_cache, RexMatch, rex


def test_value_error():
    raises(ValueError, rex, '/test')
    raises(ValueError, rex, 'm/test')
    raises(ValueError, rex, 's/test/')
    raises(ValueError, rex, 's//test/')


def test_no_action():
    r = rex('/test/')
    assert r.action == 'm'
    assert r.pattern == 'test'
    assert r.flags == 0


def test_str():
    m = "This is dog!" == rex('/[a-z]+!/')
    assert str(m) == 'dog!'


def test_empty_str():
    m = "This is dog!" == rex('/[0-9]+!/')
    assert str(m) == ''


def test_unicode():
    m = "This is dog!" == rex('/[a-z]+!/')
    assert m.__unicode__() == u'dog!'


def test_empty_unicode():
    m = "This is dog!" == rex('/[0-9]+!/')
    assert m.__unicode__() == u''


def test_no_action_ex():
    r = rex('!test!')
    assert r.action == 'm'
    assert r.pattern == 'test'
    assert r.flags == 0


def test_m_action():
    r = rex('m/test/')
    assert r.action == 'm'
    assert r.pattern == 'test'
    assert r.flags == 0


def test_m_action_ex():
    r = rex('m!test!')
    assert r.action == 'm'
    assert r.pattern == 'test'
    assert r.flags == 0


def test_s_action():
    r = rex('s/test/ohh/')
    assert r.action == 's'
    assert r.pattern == 'test'
    assert r.replacement == 'ohh'
    assert r.flags == 0


def test_s_action_flags():
    r = rex('/test/im')
    assert r.action == 'm'
    assert r.pattern == 'test'
    assert r.flags == re.I | re.M


#
#     # def test_s_action_bad():
#     #     self.assertRaises(ValueError, rex, '/test/imH')
#
def test_m_true():
    assert ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))


def test_m_true_orthodox():
    assert rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx")


def test_m_false_noncache():
    assert rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx", cache=False)
    assert not rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa bb cc xx", cache=False)


def test_m_false():
    assert not ("Aa 9-9  xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))


def test_m_false_orthodox():
    assert not rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9  xx")


def test_m_value():
    assert ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))['t'] == '88'
    assert ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))[2] == '88'
    assert ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))['tttt'] is None


def test_m_value_orthodox():
    assert rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx")['t'] == '88'
    assert rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx")[2] == '88'
    assert rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx")['tttt'] is None


def test_m_true_call():
    r = rex('/([0-9-]+) (?P<t>[0-9-]+)/')
    assert r("Aa 9-9 88 xx")


def test_m_false_call():
    r = rex('/([0-9-]+) (?P<t>[0-9-]+)/')
    assert not r("Aa 9-9  xx")


def test_s():
    s = ("This is a cat" == rex('s/cat/dog/'))
    assert s == 'This is a dog'


def test_s_i():
    s = "This is a cat" == rex('s/CAT/dog/i')
    assert s == 'This is a dog'


def test_s_multi():
    s = "This is a cat cat cat cat" == rex('s/cat/dog/')
    assert s == 'This is a dog dog dog dog'


def test_s_orthodox():
    assert rex('s/cat/dog/', "This is a cat") == 'This is a dog'


def test_s_i_orthodox():
    assert rex('s/CAT/dog/i', "This is a cat") == 'This is a dog'


def test_s_multi_orthodox():
    assert rex('s/cat/dog/', "This is a cat cat cat cat") == 'This is a dog dog dog dog'


def test_cache():
    rex('s/cache/test/')
    assert 's/cache/test/' in rex_module.REX_CACHE


def test_cache_2():
    a = rex('s/cache/test/')
    b = rex('s/cache/test/')
    assert a is b


def test_no_cache_2():
    a = rex('s/cache/test/', cache=False)
    b = rex('s/cache/test/', cache=False)
    assert not (a is b)


def test_not_cache():
    rex('s/cache/test1/', cache=False)
    assert not 's/cache/test1/' in rex_module.REX_CACHE


def test_clear_cache():
    rex('s/cache/test/')
    rex_clear_cache()
    assert not 's/cache/test/' in rex_module.REX_CACHE


def test_rex_match():
    rm = RexMatch(((0, 'some match'), ('a', 1), ('b', 2)))
    assert rm['a'] == 1
    assert rm['b'] == 2
    assert str(rm) == 'some match'
    assert rm.__unicode__() == u'some match'


def test_rex_match_empty():
    rm = RexMatch()
    assert rm['a'] is None
    assert rm['b'] is None
    assert str(rm) == ''
    assert rm.__unicode__() == u''


def test_rex_match_get_empty():
    rm = RexMatch((('c', None),))
    assert rm.get('a') is None
    assert rm.get('a', 'b') == 'b'
    assert rm.get('c', 'b') == 'b'


def test_rex_group():
    m = "This is cat! A kitten is a cat but not a dog." == rex('/[a-z]+!.*(kitten\s\S{2}).*but.*(dog)\./')
    assert m == rex.group
