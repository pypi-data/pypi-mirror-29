# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import sqlite3

import upt


class OpenBSDPackage(object):
    SQLPORTS_DB = '/usr/local/share/sqlports'

    def __init__(self):
        try:
            self.conn = sqlite3.connect(self.SQLPORTS_DB)
        except sqlite3.OperationalError:
            self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.conn is not None:
            self.conn.close()

    def _to_openbsd_fullpkgpath(self, name):
        if self.conn is not None:
            query = 'SELECT FULLPKGPATH FROM PORTS WHERE PKGSPEC=?'
            cursor = self.conn.execute(query, (f'{name}-*', ))
            result = cursor.fetchone()
            if result is not None:
                return result[0]

        # The database cannot be used, or we could not find the row we wanted.
        # Let's return something anyway, and let the maintainer fix this.
        return f'xxx/{name}'

    def create_package(self, upt_pkg, output=None):

        self.upt_pkg = upt_pkg
        self.pkg_str = f'''# $OpenBSD$

COMMENT =\t\t{self._summary()}

{self._version_info()}
DISTNAME =\t\t{self._distname()}
PKGNAME =\t\t{self._pkgname()}

CATEGORIES =\t\tXXX

HOMEPAGE =\t\t{upt_pkg.homepage}

MAINTAINER =\t\t{self._maintainer()}

{self._license_info()}

MODULES =\t\t{self._modules()}
{self._lang_specific_mods()}

{self._dependencies()}

.include <bsd.port.mk>'''

    def _summary(self):
        summary = self.upt_pkg.summary
        if summary.endswith('.') and not summary.endswith('etc.'):
            summary = summary[:-1]
        if summary.startswith('a ') or summary.startswith('A '):
            summary = summary[2:]
        if summary.startswith('an ') or summary.startswith('An '):
            summary = summary[3:]
        return f'{summary[:1].lower()}{summary[1:]}'

    def _pkgname(self):
        raise NotImplementedError()

    def _version_info(self):
        raise NotImplementedError()

    def _distname(self):
        raise NotImplementedError()

    def _maintainer(self):
        return f'XXX XXX <xxx@xxx.xxx>'

    def _license_info(self):
        """Return a string containing license information.

        The returned string contains:
        - a comment describing the package licenses;
        - a line setting 'PERMIT_PACKAGE_CDROM' (set to 'Yes' when we are sure
          that the license is 'good', and to 'XXX' otherwise).
        """
        out = ''
        permit_package_cdrom = bool(self.upt_pkg.licenses)

        # Based on infrastructure/lib/OpenBSD/PortGen/License.pm, found in
        # the OpenBSD ports.
        good_licenses = (
            upt.licenses.GNUAfferoGeneralPublicLicenseThreeDotZero,
            upt.licenses.ApacheLicenseOneDotOne,
            upt.licenses.ApacheLicenseTwoDotZero,
            upt.licenses.ArtisticLicenseOneDotZero,
            upt.licenses.ArtisticLicenseTwoDotZero,
            upt.licenses.BSDTwoClauseLicense,
            upt.licenses.GNUGeneralPublicLicenseTwo,
            upt.licenses.GNUGeneralPublicLicenseThree,
            upt.licenses.GNULesserGeneralPublicLicenseTwoDotOne,
            upt.licenses.GNULesserGeneralPublicLicenseTwoDotOnePlus,
            upt.licenses.MITLicense,
            upt.licenses.BSDThreeClauseLicense,
            upt.licenses.PerlLicense,
            upt.licenses.RubyLicense,
            upt.licenses.QPublicLicenseOneDotZero,
            upt.licenses.ZlibLicense,
        )

        # First, a comment describing the package license(s).
        for license in self.upt_pkg.licenses:
            out += f'# {license.spdx_identifier}\n'
            permit_package_cdrom &= isinstance(license, good_licenses)

        if not out:
            out = '# TODO: check licenses\n'

        # Then, let's fill in PERMIT_PACKAGE_CDROM.
        if permit_package_cdrom:
            out += 'PERMIT_PACKAGE_CDROM =\tYes'
        else:
            # If no license info was returned by the frontend, or even if we
            # could not be 100% sure that the license was a "good" one, we
            # should not assume that PERMIT_PACKAGE_CDROM should be set to
            # 'No': instead, let's make sure the maintainer checks the license
            # themselves.
            out += 'PERMIT_PACKAGE_CDROM =\tXXX'

        return out

    def _modules(self):
        raise NotImplementedError()

    def _lang_specific_mods(self):
        raise NotImplementedError()

    def _dependencies(self, flavor=''):
        """Return a string defining {RUN,TEST}_DEPENDS.

        The flavor parameter may be set to something language-specific, such as
        ${MODPY_FLAVOR}'. This allows us to factorize most of the code here,
        and have simpler language-specific implementations.
        """
        def _to_openbsd_fullpkgpath(req):
            openbsd_name = self._normalized_openbsd_name(req.name)
            fullpkgpath = self._to_openbsd_fullpkgpath(openbsd_name)
            return fullpkgpath

        def _format_upt_reqs(upt_reqs):
            out = ''
            reqs = [f'{_to_openbsd_fullpkgpath(req)}{flavor}'
                    for req in upt_reqs]
            if reqs:
                out += f'\t\t{reqs[0]}'
                for req in reqs[1:]:
                    out += f' \\\n\t\t\t{req}'
                out += '\n'
            return out

        out = ''
        for kind in ('run', 'test'):
            reqs = _format_upt_reqs(self.upt_pkg.requirements.get(kind, []))
            if reqs:
                out += f'{kind.upper()}_DEPENDS ={reqs}'
        return out

    @staticmethod
    def _normalized_openbsd_name(name):
        """Return an OpenBSD-compatible version of a package name.

        The result of this function should be the same thing as the
        fullpkgpath, but without the leading "<category>/". For instance, the
        'requests' package in Python has 'www/py-requests' as its fullpkgpath,
        and _normalized_openbsd_name('requests') should return 'py-requests'.
        """
        raise NotImplementedError()


class OpenBSDPerlPackage(OpenBSDPackage):
    def _pkgname(self):
        return f'p5-${{DISTNAME}}'

    def _version_info(self):
        return f'VERSION =\t\t{self.upt_pkg.version}'

    def _distname(self):
        name = self._normalized_openbsd_name(self.upt_pkg.name)
        return f'{name}-${{VERSION}}'

    def _modules(self):
        return 'cpan'

    def _lang_specific_mods(self):
        return ''

    def _dependencies(self):
        # XXX: The CPAN frontend does not yet provide info about requirements.
        return f''

    @staticmethod
    def _normalized_openbsd_name(name):
        name = name.replace('::', '-')
        return name


class OpenBSDPythonPackage(OpenBSDPackage):
    def create_package(self, upt_pkg, output=None):
        super().create_package(upt_pkg, output)

    def _pkgname(self):
        openbsd_name = self._normalized_openbsd_name(self.upt_pkg.name)
        return f'{openbsd_name}-${{MODPY_EGG_VERSION}}'

    @staticmethod
    def _normalized_openbsd_name(name):
        name = name.lower()
        if name == 'py':
            return 'py-py'

        if name.startswith('python-'):
            name = name[7:]
        elif name.startswith('py-'):
            name = name[3:]
        elif name.startswith('py'):
            name = name[2:]
        return f'py-{name}'

    def _version_info(self):
        return f'MODPY_EGG_VERSION =\t{self.upt_pkg.version}'

    def _distname(self):
        return f'{self.upt_pkg.name}-${{MODPY_EGG_VERSION}}'

    def _modules(self):
        return 'lang/python'

    def _lang_specific_mods(self):
        out = 'MODPY_SETUPTOOLS =\tYes # Probably\n'
        out += 'MODPY_PI =\t\tYes'
        return out

    def _dependencies(self):
        return super()._dependencies(flavor='${MODPY_FLAVOR}')


class OpenBSDRubyPackage(OpenBSDPackage):
    def _pkgname(self):
        return f'ruby-${{DISTNAME}}'

    def _version_info(self):
        return f'VERSION =\t\t{self.upt_pkg.version}'

    def _distname(self):
        name = self._normalized_openbsd_name(self.upt_pkg.name)
        return f'{name}-${{VERSION}}'

    def _modules(self):
        return 'lang/ruby'

    def _lang_specific_mods(self):
        return 'CONFIGURE_STYLE =\truby gem # XXX Maybe "ext" as well'

    def _dependencies(self):
        out = ''
        if 'run' in self.upt_pkg.requirements:
            out += 'BUILD_DEPENDS =\t\t${RUN_DEPENDS}\n'
        out += super()._dependencies(flavor=',${MODRUBY_FLAVOR}')
        return out

    @staticmethod
    def _normalized_openbsd_name(name):
        name = name.lower()
        if not name.startswith('ruby-'):
            name = f'ruby-{name}'
        return name


class OpenBSD(upt.Backend):
    name = 'openbsd'

    def create_package(self, upt_pkg, output=None):
        pkg_classes = {
            'pypi': OpenBSDPythonPackage,
            'cpan': OpenBSDPerlPackage,
            'rubygems': OpenBSDRubyPackage,
        }

        try:
            pkg_cls = pkg_classes[upt_pkg.frontend]
        except KeyError:
            raise upt.UnhandledFrontendError(self.name, upt_pkg.frontend)

        with pkg_cls() as packager:
            packager.create_package(upt_pkg, output)
            print(packager.pkg_str)
