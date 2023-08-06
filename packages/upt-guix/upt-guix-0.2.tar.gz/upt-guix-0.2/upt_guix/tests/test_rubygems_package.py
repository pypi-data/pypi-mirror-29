# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import unittest

import upt

from upt_guix.upt_guix import GuixRubyPackage


class TestRubyGemsPackage(unittest.TestCase):
    def setUp(self):
        self.guix_pkg = GuixRubyPackage()

    def test_guix_name(self):
        input_output = [
            ('bundler', 'bundler'),
            ('Ascii85', 'ruby-ascii85'),
            ('rubypants', 'ruby-rubypants'),
            ('ruby-rc4', 'ruby-rc4'),
        ]

        for rubygems_name, guix_name in input_output:
            self.assertEqual(self.guix_pkg._guix_name(rubygems_name),
                             guix_name)

    def test_url(self):
        self.guix_pkg.upt_pkg = upt.Package('rubypants', '0.6.0')
        expected = '''(origin
              (method url-fetch)
              (uri (rubygems-uri "rubypants" version))
              (sha256
               (base32
                "XXX"))))'''
        source = self.guix_pkg._source()
        self.assertEqual(source, expected)


if __name__ == '__main__':
    unittest.main()
