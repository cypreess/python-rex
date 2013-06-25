import re
import unittest
from rex import rex


class TestRex(unittest.TestCase):
    def test_no_action(self):
        r = rex('/test/')
        self.assertEqual(r.action, 'm')
        self.assertEqual(r.pattern, 'test')
        self.assertEqual(r.flags, 0)


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

    def test_s_action(self):
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

