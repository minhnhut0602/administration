#
# spec file for package qt5keychain
#
# Copyright (c) 2012 Klaas Freitag <freitag@owncloud.com>, ownCloud GmbH.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes, issues or comments via http://github.com/owncloud/mirall/issues
#

%_oc_package_header
%_use_oc_qt5_as_default
%define use_devtoolset 0
%if 0%{?el6} || 0%{?el7}
%define use_devtoolset 1
%endif

%define _soversion 1

Name:           @PACKAGE_NAME_PREFIX@-qt5keychain
BuildRequires:  @PACKAGE_NAME_PREFIX@-filesystem

BuildRequires:  cmake
%if 0%{?use_devtoolset}
BuildRequires: devtoolset-4-gcc-c++
%else
BuildRequires: gcc-c++
%endif

BuildRequires:  @PACKAGE_NAME_PREFIX@-libqt5-qtbase-devel @PACKAGE_NAME_PREFIX@-libqt5-qttools-devel @PACKAGE_NAME_PREFIX@-libqt5-qtwebkit-devel

Version:        0.7.0
Release:        0
Summary:        A cross platform password store library
License:        MIT
Group:          Development/Libraries/C and C++
Url:            https://github.com/frankosterfeld/qtkeychain
Source0:        qtkeychain-%{version}.tar.gz
%if 0%{?rhel_version} || 0%{?centos_version}
Patch1:         cmake.diff
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
use qtkeychain to store passwords easy and secure on Linux, Windows and
Mac.


%package -n %{name}%{_soversion}
Summary:        A cross platform password store library
Group:          Development/Libraries/C and C++
# https://github.com/owncloud/client/issues/4506
Obsoletes:	@PACKAGE_NAME_PREFIX@-qtkeychain-qt5 <= %{version}


%description -n %{name}%{_soversion}
use qtkeychain to store passwords easy and secure on Linux, Windows and
Mac.

%package devel
Summary:        A cross platform password store library
Group:          Development/Libraries/C and C++
AutoReqProv:    on
Requires:       @PACKAGE_NAME_PREFIX@-qt5keychain%{_soversion} = %{version}


%description devel
use qtkeychain to store passwords easy and secure on Linux, Windows and
Mac.

This package contains development files for libqtkeychain.

%prep
%setup -q -n qtkeychain-%{version}
%if 0%{?rhel_version} || 0%{?centos_version}
%patch1 -p1
%endif

%build

%if 0%{?use_devtoolset}
source /opt/rh/devtoolset-4/enable
%endif

export LD_LIBRARY_PATH=%{_libqt5_libdir}:$LD_LIBRARY_PATH
export PATH=%{_libqt5_bindir}:$PATH
mkdir build
pushd build

cmake .. \
    -DCMAKE_INSTALL_PREFIX=%{_libqt5_prefix} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_VERBOSE_MAKEFILE=ON \
    -DQT_QMAKE_EXECUTABLE="%{_libqt5_libdir}/qt5/bin/qmake" \
%ifarch %arm ppc ppc64
    -DWITH_CRASHREPORTER=OFF \
    -DWITH_BREAKPAD=OFF \
%endif
    -DBUILD_RELEASE=ON \
    -DQT_TRANSLATIONS_DIR=%{_libqt5_prefix}/share/qt5/translations

%__make %{?jobs:-j%jobs} || %__make -j1
popd

%install
%if 0%{?use_devtoolset}
source /opt/rh/devtoolset-4/enable
%endif

pushd build
%make_install
popd

# https://github.com/owncloud/enterprise/issues/1399 -- no file conflicts with other soversions.
# FIXME: We currently still obsolete our older soversion -- that should not be needed.

pushd $RPM_BUILD_ROOT/%{_libqt5_prefix}/share/qt5/translations
# make sure there is an soversion in the name.
for f in *keychain_*; do
  new=$(echo $f | sed -e 's@keychain@keychain%{_soversion}@')
  mv $f $new
done
popd


%post -n %{name}%{_soversion} -p /sbin/ldconfig

%postun -n %{name}%{_soversion} -p /sbin/ldconfig

%files -n %{name}%{_soversion}
%defattr(-,root,root)
%{_libqt5_libdir}/libqt5keychain.so.*
%dir %{_libqt5_datadir}/translations/
%{_libqt5_datadir}/translations/qtkeychain*.qm
%doc COPYING ReadMe.txt

%files devel
%defattr(-,root,root)
%{_libqt5_prefix}/include/qt5keychain
%{_libqt5_libdir}/cmake
%{_libqt5_libdir}/libqt5keychain.so

%changelog
