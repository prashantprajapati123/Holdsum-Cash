from random import Random

from django.test import TestCase

from .yodlee import gen_password, get_yodlee_password


class YodleePasswordTest(TestCase):
    def test_get_yodlee_password(self):
        # brute forced a seed that would fail the Yodlee password requirements
        r = Random(323)
        pw = gen_password(r)
        self.assertEqual(pw, 'xxdetjbrvokkoznlgpbzitxlc86412')
        clean = get_yodlee_password(pw)
        self.assertEqual(clean, 'xdetjbrvokoznlgpbzitxlc86412')
