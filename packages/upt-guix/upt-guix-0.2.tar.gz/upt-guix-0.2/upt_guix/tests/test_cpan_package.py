# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import unittest

import upt

from upt_guix.upt_guix import GuixCPANPackage


class TestGuixCPANPackage(unittest.TestCase):
    def setUp(self):
        self.guix_pkg = GuixCPANPackage()

    def test_guix_name(self):
        self.assertEqual(self.guix_pkg._guix_name('test-pod'),
                         'perl-test-pod')

    def test_url(self):
        self.guix_pkg.upt_pkg = upt.Package('test-pod', '1.51')
        self.guix_pkg.upt_pkg.download_urls = [
            'https://cpan.metacpan.org/authors/id/E/ET/ETHER/'
            'Test-Pod-1.51.tar.gz'
        ]
        expected = '''(origin
              (method url-fetch)
              (uri (string-append "mirror://cpan/authors/id/E/ET/ETHER/"
                                  "Test-Pod-" version ".tar.gz"))
              (sha256
               (base32
                "XXX"))))'''
        source = self.guix_pkg._source()
        self.assertEqual(source, expected)

    def test_url_no_url(self):
        self.guix_pkg.upt_pkg = upt.Package('test-pod', '1.51')
        self.guix_pkg.upt_pkg.download_urls = []
        expected = '''(origin
              (method url-fetch)
              (uri (string-append XXX))
              (sha256
               (base32
                "XXX"))))'''
        source = self.guix_pkg._source()
        self.assertEqual(source, expected)


if __name__ == '__main__':
    unittest.main()
