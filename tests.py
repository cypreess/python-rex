import re
import unittest
import rex as rex_module
from rex import rex, rex_clear_cache


class TestRex(unittest.TestCase):
    def test_value_error(self):
        self.assertRaises(ValueError, rex, '/test')
        self.assertRaises(ValueError, rex, 'm/test')
        self.assertRaises(ValueError, rex, 's/test/')
        self.assertRaises(ValueError, rex, 's//test/')

    def test_no_action(self):
        r = rex('/test/')
        self.assertEqual(r.action, 'm')
        self.assertEqual(r.pattern, 'test')
        self.assertEqual(r.flags, 0)

    def test_str(self):
        m = "This is dog!" == rex('/[a-z]+!/')
        self.assertEqual(str(m), 'dog!')

    def test_unicode(self):
        m = "This is dog!" == rex('/[a-z]+!/')
        self.assertEqual(unicode(m), u'dog!')

    def test_no_action_ex(self):
        r = rex('!test!')
        self.assertEqual(r.action, 'm')
        self.assertEqual(r.pattern, 'test')
        self.assertEqual(r.flags, 0)

    def test_m_action(self):
        r = rex('m/test/')
        self.assertEqual(r.action, 'm')
        self.assertEqual(r.pattern, 'test')
        self.assertEqual(r.flags, 0)

    def test_m_action_ex(self):
        r = rex('m!test!')
        self.assertEqual(r.action, 'm')
        self.assertEqual(r.pattern, 'test')
        self.assertEqual(r.flags, 0)

    def test_s_action(self):
        r = rex('s/test/ohh/')
        self.assertEqual(r.action, 's')
        self.assertEqual(r.pattern, 'test')
        self.assertEqual(r.replacement, 'ohh')
        self.assertEqual(r.flags, 0)

    def test_s_action_flags(self):
        r = rex('/test/im')
        self.assertEqual(r.action, 'm')
        self.assertEqual(r.pattern, 'test')
        self.assertEqual(r.flags, re.I | re.M)

    def test_s_action_bad(self):
        self.assertRaises(ValueError, rex, '/test/imH')

    def test_m_true(self):
        self.assertTrue("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))

    def test_m_false(self):
        self.assertFalse("Aa 9-9  xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))

    def test_m_value(self):
        self.assertEqual('88', ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))['t'])
        self.assertEqual('88', ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))[2])
        self.assertEqual(None, ("Aa 9-9 88 xx" == rex('/([0-9-]+) (?P<t>[0-9-]+)/'))['tttt'])

    def test_s(self):
        self.assertEqual('This is a dog', "This is a cat" == rex('s/cat/dog/'))

    def test_s_i(self):
        self.assertEqual('This is a dog', "This is a cat" == rex('s/CAT/dog/i'))

    def test_s_multi(self):
        self.assertEqual('This is a dog dog dog dog', "This is a cat cat cat cat" == rex('s/cat/dog/'))

    def test_cache(self):
        rex('s/cache/test/')

        self.assertIn('s/cache/test/', rex_module.REX_CACHE)

    def test_cache_2(self):
        a = rex('s/cache/test/')
        b = rex('s/cache/test/')
        self.assertEqual(a is b, True)

    def test_no_cache_2(self):
        a = rex('s/cache/test/', cache=False)
        b = rex('s/cache/test/', cache=False)
        self.assertEqual(a is b, False)

    def test_not_cache(self):
        rex('s/cache/test1/', cache=False)
        self.assertNotIn('s/cache/test1/', rex_module.REX_CACHE)

    def test_clear_cache(self):
        rex('s/cache/test/')
        rex_clear_cache()
        self.assertNotIn('s/cache/test/', rex_module.REX_CACHE)


if __name__ == '__main__':
    unittest.main()