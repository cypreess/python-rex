# import re
# import unittest
# import six
# import rex as rex_module
# from rex import rex, rex_clear_cache, RexMatch
#
#
# class TestRex(unittest.TestCase):
#     def test_value_error(self):
#         self.assertRaises(ValueError, rex, '/test')
#         self.assertRaises(ValueError, rex, 'm/test')
#         self.assertRaises(ValueError, rex, 's/test/')
#         self.assertRaises(ValueError, rex, 's//test/')
#
#     def test_no_action(self):
#         r = rex('/test/')
#         self.assertEqual(r.action, 'm')
#         self.assertEqual(r.pattern, 'test')
#         self.assertEqual(r.flags, 0)
#
#     def test_str(self):
#         m = "This is dog!" == rex('/[a-z]+!/')
#         self.assertEqual(str(m), 'dog!')
#
#
#     def test_empty_str(self):
#         m = "This is dog!" == rex('/[0-9]+!/')
#         self.assertEqual(str(m), '')
#
#     def test_unicode(self):
#         m = "This is dog!" == rex('/[a-z]+!/')
#         self.assertEqual(m.__unicode__(), u'dog!')
#
#     def test_empty_unicode(self):
#         m = "This is dog!" == rex('/[0-9]+!/')
#         self.assertEqual(m.__unicode__(), u'')
#
#     def test_no_action_ex(self):
#         r = rex('!test!')
#         self.assertEqual(r.action, 'm')
#         self.assertEqual(r.pattern, 'test')
#         self.assertEqual(r.flags, 0)
#
#     def test_m_action(self):
#         r = rex('m/test/')
#         self.assertEqual(r.action, 'm')
#         self.assertEqual(r.pattern, 'test')
#         self.assertEqual(r.flags, 0)
#
#     def test_m_action_ex(self):
#         r = rex('m!test!')
#         self.assertEqual(r.action, 'm')
#         self.assertEqual(r.pattern, 'test')
#         self.assertEqual(r.flags, 0)
#
#     def test_s_action(self):
#         r = rex('s/test/ohh/')
#         self.assertEqual(r.action, 's')
#         self.assertEqual(r.pattern, 'test')
#         self.assertEqual(r.replacement, 'ohh')
#         self.assertEqual(r.flags, 0)
#
#     def test_s_action_flags(self):
#         r = rex('/test/im')
#         self.assertEqual(r.action, 'm')
#         self.assertEqual(r.pattern, 'test')
#         self.assertEqual(r.flags, re.I | re.M)
#
#     # def test_s_action_bad(self):
#     #     self.assertRaises(ValueError, rex, '/test/imH')
#
#     def test_m_true(self):
#         self.assertTrue("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))
#
#     def test_m_true_orthodox(self):
#         self.assertTrue(rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx"))
#
#     def test_m_false_noncache(self):
#         self.assertTrue(
#             rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx", cache=False))
#         self.assertFalse(
#             rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa bb cc xx", cache=False))
#
#     def test_m_false(self):
#         self.assertFalse("Aa 9-9  xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))
#
#     def test_m_false_orthodox(self):
#         self.assertFalse(rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9  xx"))
#
#     def test_m_value(self):
#         self.assertEqual('88',
#                          ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))[
#                              't'])
#         self.assertEqual('88',
#                          ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))[
#                              2])
#         self.assertEqual(None,
#                          ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))[
#                              'tttt'])
#
#     def test_m_value_orthodox(self):
#         self.assertEqual('88',
#                          rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx")[
#                              't'])
#         self.assertEqual('88',
#                          rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx")[2])
#         self.assertEqual(None,
#                          rex('/([0-9-]+) (?P<t>[0-9-]+)/', "Aa 9-9 88 xx")[
#                              'tttt'])
#
#     def test_m_true_call(self):
#         r = rex('/([0-9-]+) (?P<t>[0-9-]+)/')
#         self.assertTrue(r("Aa 9-9 88 xx"))
#
#     def test_m_false_call(self):
#         r = rex('/([0-9-]+) (?P<t>[0-9-]+)/')
#         self.assertFalse(r("Aa 9-9  xx"))
#
#     def test_s(self):
#         self.assertEqual('This is a dog', "This is a cat" == rex('s/cat/dog/'))
#
#     def test_s_i(self):
#         self.assertEqual('This is a dog',
#                          "This is a cat" == rex('s/CAT/dog/i'))
#
#     def test_s_multi(self):
#         self.assertEqual('This is a dog dog dog dog',
#                          "This is a cat cat cat cat" == rex('s/cat/dog/'))
#
#
#     def test_s_orthodox(self):
#         self.assertEqual('This is a dog', rex('s/cat/dog/', "This is a cat"))
#
#     def test_s_i_orthodox(self):
#         self.assertEqual('This is a dog', rex('s/CAT/dog/i', "This is a cat"))
#
#     def test_s_multi_orthodox(self):
#         self.assertEqual('This is a dog dog dog dog',
#                          rex('s/cat/dog/', "This is a cat cat cat cat"))
#
#     def test_cache(self):
#         rex('s/cache/test/')
#
#         self.assertIn('s/cache/test/', rex_module.REX_CACHE)
#
#     def test_cache_2(self):
#         a = rex('s/cache/test/')
#         b = rex('s/cache/test/')
#         self.assertEqual(a is b, True)
#
#     def test_no_cache_2(self):
#         a = rex('s/cache/test/', cache=False)
#         b = rex('s/cache/test/', cache=False)
#         self.assertEqual(a is b, False)
#
#     def test_not_cache(self):
#         rex('s/cache/test1/', cache=False)
#         self.assertNotIn('s/cache/test1/', rex_module.REX_CACHE)
#
#     def test_clear_cache(self):
#         rex('s/cache/test/')
#         rex_clear_cache()
#         self.assertNotIn('s/cache/test/', rex_module.REX_CACHE)
#
#
#     def test_rex_match(self):
#         rm = RexMatch(((0, 'some match'), ('a', 1), ('b', 2)))
#         self.assertEqual(rm['a'], 1)
#         self.assertEqual(rm['b'], 2)
#         self.assertEqual(str(rm), 'some match')
#         self.assertEqual(rm.__unicode__(), u'some match')
#
#     def test_rex_match_empty(self):
#         rm = RexMatch()
#         self.assertEqual(rm['a'], None)
#         self.assertEqual(rm['b'], None)
#         self.assertEqual(str(rm), '')
#         self.assertEqual(rm.__unicode__(), u'')
#
#     def test_rex_match_get_empty(self):
#         rm = RexMatch((('c', None),))
#         self.assertEqual(rm.get('a'), None)
#         self.assertEqual(rm.get('a', 'b'), 'b')
#         self.assertEqual(rm.get('c', 'b'), 'b')
#
#     def test_rex_group(self):
#         m = "This is cat! A kitten is a cat but not a dog." == rex('/[a-z]+!.*(kitten\s\S{2}).*but.*(dog)\./')
#         self.assertEqual(m, rex.group)
#
#
# if __name__ == '__main__':
#     unittest.main()
