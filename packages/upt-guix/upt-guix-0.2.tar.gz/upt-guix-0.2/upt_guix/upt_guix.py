# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import upt


class GuixPackage(object):
    def create_package(self, upt_pkg, output=None):
        self.upt_pkg = upt_pkg
        self.guix_name = self._guix_name(upt_pkg.name)
        self.pkg_str = f"""\
(define-public {self.guix_name}
  (package
    (name "{self.guix_name}")
    (version "{upt_pkg.version}")
    (source {self._source()})
    (build-system {self._build_system()})
    (inputs
     `({self._inputs()}))
    (native-inputs
     `({self._native_inputs()}))
    (propagated-inputs
     `({self._propagated_inputs()}))
    (home-page "{upt_pkg.homepage}")
    (synopsis "{self._synopsis()}")
    (description "XXX")
    (license {self._license()})))"""

    def _guix_name(self, pkg_name):
        raise NotImplementedError()

    def _build_system(self):
        raise NotImplementedError()

    def _source(self):
        raise NotImplementedError()

    def _format_inputs(self, frontend_inputs):
        inputs = []
        first = True
        # TODO: We completely dismiss the requirement specifiers. This means we
        # may not know that some of the package dependencies are actually
        # outdated in Guix.
        for requirement in frontend_inputs:
            if first:
                first = False
                spaces = ''
            else:
                spaces = ' ' * 7
            req_name = self._guix_name(requirement.name)
            inputs.append(f'{spaces}("{req_name}" ,{req_name})')
        return '\n'.join(inputs)

    def _inputs(self):
        return ''

    def _native_inputs(self):
        return self._format_inputs(self.upt_pkg.requirements.get('test', []))

    def _propagated_inputs(self):
        return self._format_inputs(self.upt_pkg.requirements.get('run', []))

    def _synopsis(self):
        synopsis = self.upt_pkg.summary
        if synopsis.endswith('.') and not synopsis.endswith('etc.'):
            synopsis = synopsis[:-1]
        if synopsis.startswith('a ') or synopsis.startswith('A '):
            synopsis = synopsis[2:]
        if synopsis.startswith('an ') or synopsis.startswith('An '):
            synopsis = synopsis[3:]
        return synopsis.capitalize()

    def _license(self):
        all_licenses = {
            'Apache-1.1': 'asl1.1',
            'Apache-2.0': 'asl2.0',
            'Artistic-2.0': 'artistic2.0',
            'Artistic-1.0-Perl': 'perl-license',
            'BSL-1.0': 'boost1.0',
            'BSD-2-Clause': 'bsd-2',
            'BSD-3-Clause': 'bsd-3',
            'CC0-1.0': 'cc0',
            'CECILL-B': 'cecill-b',
            'CECILL-C': 'cecill-c',
            'CECILL-2.1': 'cecill',
            'ClArtistic': 'clarified-artistic',
            'CDDL-1.0': 'cddl1.0',
            'CPL-1.0': 'cpl1.0',
            'EPL-1.0': 'epl1.0',
            'AGPL-3.0-only': 'agpl3',
            'AGPL-3.0-or-later': 'agpl3+',
            'GPL-2.0-only': 'gpl2',
            'GPL-2.0-or-later': 'gpl2+',
            'GPL-3.0': 'gpl3',
            'GPL-3.0-or-later': 'gpl3+',
            'LGPL-2.0-only': 'lgpl2.0',
            'LGPL-2.0-or-later': 'lgpl2.0+',
            'LGPL-2.1-only': 'lgpl2.1',
            'LGPL-2.1-or-later': 'lgpl2.1+',
            'LGPL-3.0-only': 'lgpl3',
            'LGPL-3.0-or-later': 'lgpl3+',
            'ISC': 'isc',
            'LPPL-1.3c': 'lppl1.3c',
            'MirOS': 'miros',
            'MS-PL': 'ms-pl',
            'MIT': 'expat',
            'MPL-1.0': 'mpl1.0',
            'MPL-1.1': 'mpl1.1',
            'MPL-2.0': 'mpl2.0',
            'Python-2.0': 'psfl',
            'QPL-1.0': 'qpl',
            'Sleepycat': 'sleepycat',
            'NCSA': 'ncsa',
            'W3C': 'w3c',
            'wxWindows': 'wxwindows3.1+',
            # Special case: upt could not guess.
            'unknown': '#f',
        }

        def _pick_license(spdx_id):
            try:
                license_symbol = all_licenses.get(spdx_id, '#f')
                if license_symbol == '#f':
                    return '#f'
                else:
                    return f'license:{license_symbol}'
            except KeyError:
                return '#f'

        if len(self.upt_pkg.licenses) == 0:
            return '#f'
        elif len(self.upt_pkg.licenses) == 1:
            return _pick_license(self.upt_pkg.licenses[0].spdx_identifier)
        else:
            licenses = [_pick_license(l.spdx_identifier)
                        for l in self.upt_pkg.licenses]
            return f'(list {" ".join(licenses)})'


class GuixCPANPackage(GuixPackage):
    def _guix_name(self, name):
        name = name.replace('::', '-')
        if name.startswith('perl-'):
            return name.lower()
        else:
            return f'perl-{name.lower()}'

    def _build_system(self):
        return 'perl-build-system'

    def _source(self):
        try:
            url = f'"{self.upt_pkg.download_urls[0]}"'
            url = url.replace('https://cpan.metacpan.org', 'mirror://cpan')
            url = url.replace(self.upt_pkg.version, '" version "')
            url = ('/"\n' + ' ' * 34 + '"').join(url.rsplit('/', 1))
        except IndexError:
            url = 'XXX'

        # TODO: compute the sha256 sum of the source and print it using the
        # nix-base32 format.
        return f"""(origin
              (method url-fetch)
              (uri (string-append {url}))
              (sha256
               (base32
                "XXX"))))"""


class GuixPythonPackage(GuixPackage):
    def create_package(self, upt_pkg, output=None):
        super().create_package(upt_pkg, output)
        py2_name = self.guix_name.replace('python-', 'python2-')
        self.pkg_str += f'\n\n(define-public {py2_name}\n'
        self.pkg_str += f'  (package-with-python2 {self.guix_name}))'

    @staticmethod
    def _guix_name(name):
        name = name.lower()
        if name.startswith('python-'):
            return name
        else:
            return f'python-{name}'

    def _build_system(self):
        return 'python-build-system'

    def _source(self):
        # TODO: compute the sha256 sum of the source and print it using the
        # nix-base32 format.
        return f"""(origin
              (method url-fetch)
              (uri (pypi-uri "{self.upt_pkg.name}" version))
              (sha256
               (base32
                "XXX"))))"""


class GuixRubyPackage(GuixPackage):
    def _guix_name(self, name):
        # Special case.
        if name == 'bundler':
            return name

        name = name.replace('_', '-')
        if name.startswith('ruby-'):
            return name.lower()
        else:
            return f'ruby-{name.lower()}'

    @staticmethod
    def _build_system():
        return 'ruby-build-system'

    def _source(self):
        # TODO: compute the sha256 sum of the source and print it using the
        # nix-base32 format.
        return f"""(origin
              (method url-fetch)
              (uri (rubygems-uri "{self.upt_pkg.name}" version))
              (sha256
               (base32
                "XXX"))))"""


class Guix(upt.Backend):
    name = 'guix'

    def create_package(self, upt_pkg, output=None):
        pkg_classes = {
            'cpan': GuixCPANPackage,
            'pypi': GuixPythonPackage,
            'rubygems': GuixRubyPackage,
        }

        try:
            pkg_cls = pkg_classes[upt_pkg.frontend]
        except KeyError:
            raise upt.UnhandledFrontendError(self.name, upt_pkg.frontend)

        packager = pkg_cls()
        packager.create_package(upt_pkg, output)
        print(packager.pkg_str)
