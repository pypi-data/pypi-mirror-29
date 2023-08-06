# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import unittest

import upt

from upt_openbsd.upt_openbsd import OpenBSDRubyPackage


class TestOpenBSDRubyPackage(unittest.TestCase):
    def setUp(self):
        self.obsd_pkg = OpenBSDRubyPackage()
        self.obsd_pkg.upt_pkg = upt.Package('test-pkg', '13.37')
        # Let's pretend the sqlports database is not available.
        self.conn = None

    def test_normalized_openbsd_name(self):
        input_output = [
            ('nokogiri', 'ruby-nokogiri'),
            ('ruby-ole', 'ruby-ole'),
        ]

        for rubygem_name, openbsd_name in input_output:
            self.obsd_pkg.upt_pkg = upt.Package(rubygem_name, '13.37')
            self.assertEqual(
                self.obsd_pkg._normalized_openbsd_name(rubygem_name),
                openbsd_name
            )

    def test_dependencies(self):
        self.obsd_pkg.upt_pkg.requirements = {
            'run': [
                upt.PackageRequirement('foo', ''),
                upt.PackageRequirement('bar', '>1.2')
            ],
            'test': [
                upt.PackageRequirement('baz', '>=3.4')
            ]
        }

        expected = 'BUILD_DEPENDS =\t\t${RUN_DEPENDS}\n'
        expected += 'RUN_DEPENDS =\t\txxx/ruby-foo,${MODRUBY_FLAVOR} \\\n'
        expected += '\t\t\txxx/ruby-bar,${MODRUBY_FLAVOR}\n'
        expected += 'TEST_DEPENDS =\t\txxx/ruby-baz,${MODRUBY_FLAVOR}\n'

        self.assertEqual(self.obsd_pkg._dependencies(), expected)

    def test_dependencies_runtime_only(self):
        self.obsd_pkg.upt_pkg.requirements = {
            'run': [
                upt.PackageRequirement('foo', ''),
                upt.PackageRequirement('bar', '>1.2')
            ],
        }

        expected = 'BUILD_DEPENDS =\t\t${RUN_DEPENDS}\n'
        expected += 'RUN_DEPENDS =\t\txxx/ruby-foo,${MODRUBY_FLAVOR} \\\n'
        expected += '\t\t\txxx/ruby-bar,${MODRUBY_FLAVOR}\n'

        self.assertEqual(self.obsd_pkg._dependencies(), expected)

    def test_dependencies_test_only(self):
        self.obsd_pkg.upt_pkg.requirements = {
            'test': [
                upt.PackageRequirement('baz', '>=3.4')
            ]
        }

        expected = 'TEST_DEPENDS =\t\txxx/ruby-baz,${MODRUBY_FLAVOR}\n'

        self.assertEqual(self.obsd_pkg._dependencies(), expected)


if __name__ == '__main__':
    unittest.main()
