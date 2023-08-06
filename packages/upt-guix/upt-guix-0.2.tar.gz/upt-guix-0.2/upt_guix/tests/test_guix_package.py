# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import unittest


import upt
from upt_guix.upt_guix import GuixPackage


class TestGuixPackage(unittest.TestCase):
    def setUp(self):
        self.guix_pkg = GuixPackage()

    def test_synopsis(self):
        self.guix_pkg.upt_pkg = upt.Package('foo', '42')

        self.guix_pkg.upt_pkg.summary = 'A framework'
        self.assertEqual(self.guix_pkg._synopsis(), 'Framework')

        self.guix_pkg.upt_pkg.summary = 'a framework'
        self.assertEqual(self.guix_pkg._synopsis(), 'Framework')

        self.guix_pkg.upt_pkg.summary = 'An animal'
        self.assertEqual(self.guix_pkg._synopsis(), 'Animal')

        self.guix_pkg.upt_pkg.summary = 'an animal'
        self.assertEqual(self.guix_pkg._synopsis(), 'Animal')

        self.guix_pkg.upt_pkg.summary = 'No period.'
        self.assertEqual(self.guix_pkg._synopsis(), 'No period')

        self.guix_pkg.upt_pkg.summary = 'thing'
        self.assertEqual(self.guix_pkg._synopsis(), 'Thing')

    def test_licenses(self):
        licenses = []
        self.guix_pkg.upt_pkg = upt.Package('foo', 42, licenses=licenses)
        self.assertEqual(self.guix_pkg._license(), '#f')

        licenses = [upt.licenses.UnknownLicense()]
        self.guix_pkg.upt_pkg = upt.Package('foo', 42, licenses=licenses)
        self.assertEqual(self.guix_pkg._license(), '#f')

        licenses = [upt.licenses.BSDThreeClauseLicense()]
        self.guix_pkg.upt_pkg = upt.Package('foo', 42, licenses=licenses)
        self.assertEqual(self.guix_pkg._license(), 'license:bsd-3')

        licenses = [upt.licenses.BSDTwoClauseLicense(),
                    upt.licenses.BSDThreeClauseLicense()]
        self.guix_pkg.upt_pkg = upt.Package('foo', 42, licenses=licenses)
        self.assertEqual(self.guix_pkg._license(),
                         '(list license:bsd-2 license:bsd-3)')


if __name__ == '__main__':
    unittest.main()
