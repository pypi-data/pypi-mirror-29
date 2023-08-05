# vim:set ft=spec:
#
# -- global settings ----------------------------------------------------------

%global srcname gwpy

Name:           python-%{srcname}
Version:        0.8.0
Release:        1%{?dist}
Summary:        A python package for gravitational-wave astrophysics

License:        GPLv3
URL:            https://gwpy.github.io/
Source0:        https://files.pythonhosted.org/packages/source/g/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-setuptools
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python3-rpm-macros

%description
GWpy is a collaboration-driven Python package providing tools for studying data from ground-based gravitational-wave detectors


# -- python2-gwpy -------------------------------------------------------------

%package -n python2-%{srcname}
Summary:        %{summary}
Requires:       python-six
Requires:       python-dateutil
Requires:       python-enum34
Requires:       numpy
Requires:       scipy
Requires:       python-matplotlib
Requires:       python-astropy
Requires:       lal-python
Requires:       glue

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
GWpy is a collaboration-driven Python package providing tools for studying data from ground-based gravitational-wave detectors


# -- python3x-gwpy ------------------------------------------------------------

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
Requires:       python%{python3_pkgversion}-six
Requires:       python%{python3_pkgversion}-dateutil
Requires:       python%{python3_pkgversion}-numpy
Requires:       python%{python3_pkgversion}-scipy
Requires:       python%{python3_pkgversion}-matplotlib
Requires:       python%{python3_pkgversion}-astropy
Requires:       lal-python%{python3_pkgversion}
Requires:       python%{python3_pkgversion}-glue

%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
GWpy is a collaboration-driven Python package providing tools for studying data from ground-based gravitational-wave detectors

# -- build stages -------------------------------------------------------------

%prep
%autosetup -n %{srcname}-%{version}

%build
# build python3 first
%py3_build
# so that the scripts come from python2
%py2_build

%install
%py3_install
%py2_install

# -- files --------------------------------------------------------------------

%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/*
%{_bindir}/gwpy-plot

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- changelog ----------------------------------------------------------------

%changelog
* Sun Feb 18 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.8.0: development release of GWpy

* Thu Jan 25 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.7.5: packaging bug-fix for gwpy-0.7

* Thu Jan 25 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.7.4: packaging bug-fix for gwpy-0.7

* Wed Jan 24 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.7.3: bug fix release for gwpy-0.7

* Wed Jan 24 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.7.2: bug fix release for gwpy-0.7

* Mon Jan 22 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.7.1

* Fri Jan 19 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.7.0

* Thu Oct 12 2017 Duncan Macleod <duncan.macleod@ligo.org>
- 0.6.2

* Tue Aug 29 2017 Duncan Macleod <duncan.macleod@ligo.org>
- 0.6.1 release

* Fri Aug 18 2017 Duncan Macleod <duncan.macleod@ligo.org>
- 0.6 release

* Wed May 24 2017 Duncan Macleod <duncan.macleod@ligo.org>
- 0.5.2

