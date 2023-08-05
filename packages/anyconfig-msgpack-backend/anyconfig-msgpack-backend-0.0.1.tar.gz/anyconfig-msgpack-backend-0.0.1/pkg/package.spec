%global bename msgpack
%global pkgname anyconfig-%{bename}-backend

%global desctxt \
This is a backend module for python-anyconfig to load and dump MessagePack\
data.\
\
python-anyconfig is a python library to provide common APIs to load and dump\
various configuration files like INI, JSON and YAML.

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        0.0.1
Release:        1%{?dist}
Summary:        Backend module for python-anyconfig to load and dump MessagePack data
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/ssato/python-anyconfig-msgpack-backend
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?rhel} == 7
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description %{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{summary}
Requires:       python2-anyconfig
Requires:       python2-msgpack
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desctxt}

%if %{with python3}
%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-anyconfig
Requires:       python3-msgpack
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}
%endif

%prep
%autosetup   -n %{pkgname}-%{version}

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%files       -n python2-%{pkgname}
%doc README.rst
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files       -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*
%endif

%changelog
* Sat Feb 10 2018 Satoru SATOH <ssato@redhat.com> - 0.0.1-1
- Initial packaging
