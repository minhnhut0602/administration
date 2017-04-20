#
# spec file for package qt5-qtbase
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# from oc-filesystem
%_oc_package_header

%if ! 0%{?rhel_version} || 0%{?rhel} > 6
%define have_egl 1
%else
%define have_egl 0
%endif


# Distro specific switches
%define use_devtoolset 0
%if 0%{?el6} || 0%{?el7}
%if ! 0%{?rhel_version}
%define use_devtoolset 1
%endif
%endif

%if 0%{?el6} || 0%{?el7}
%global use_qt_xkbcommon 1
%endif

%if ! 0%{?use_qt_xkbcommon}
%global xcb -xcb
%define xkbcommon   -system-xkbcommon
%else
%global xkbcommon   -qt-xkbcommon -qt-xkbcommon-x11 -xkb-config-root %{_datadir}/X11/xkb/
%global xcb -qt-xcb
%endif


%define qt5_snapshot 0
%define journald 0

Name:           @PACKAGE_NAME_PREFIX@-libqt5-qtbase
Version:        5.6.2
Release:        0
Summary:        C++ Program Library, Core Components
License:        GPL-3.0 or SUSE-LGPL-2.1-with-digia-exception-1.1
Group:          System/Libraries
Url:            http://qt.digia.com
%define base_name libqt5
%define real_version 5.6.2
%define so_version 5.6.2
%define tar_version qtbase-opensource-src-%{real_version}
Source:         %{tar_version}.tar.xz
# to get mtime of file:
Source1:        qt5-qtbase.changes
Source2:        macros.qt5
Source3:        baselibs.conf
Source99:       qt5-qtbase-rpmlintrc
# patches 0-1000 are openSUSE and/or non-upstream(able) patches #
# PATCH-FIX-SUSE libqt5-Fix-Gujarati-font.patch bnc#878292 fix broken Gujarati font rendering
Patch3:         libqt5-Fix-Gujarati-font.patch
# Patch-FIX-SUSE libqt5-do-not-use-shm-if-display-name-doesnt-look-local.patch -- bnc#888858
Patch5:         libqt5-do-not-use-shm-if-display-name-doesnt-look-local.patch
# PATCH-FIX-OPENSUSE disable-rc4-ciphers-bnc865241.diff bnc#865241-- Exclude rc4 ciphers from being used by default
Patch6:         disable-rc4-ciphers-bnc865241.diff
Patch7:         tell-the-truth-about-private-api.patch
# patches 1000-2000 and above from upstream 5.6 branch #
Patch1003:      xcb-Dont-send-QtWindowNoState-event-when-hiding-minimized-window.patch
Patch1004:      XCB-Drop-from-external-app-fix-keyboard-modifier-state.patch
Patch1005:      xcb-Use-the-state-of-the-key-event-to-process-it.patch
Patch1006:      Stop-unloading-plugins-in-QPluginLoader-and-QFactoryLoader.patch
Patch1007:      Make-QDBusConnectionPrivaterelaySignal-be-called-in-the-right-thread.patch
Patch1008:      Merge-the-QDBusMetaTypes-custom-information-to-QDBusConnectionManager.patch
Patch1009:      Fix-some-QtDBus-crashes-during-application-destruction.patch
# patches 2000-3000 and above from upstream 5.7 branch #

BuildRequires: @PACKAGE_NAME_PREFIX@-filesystem

BuildRequires:  pkgconfig(alsa)
BuildRequires:  cups-devel
%if 0%{?use_devtoolset}
%if 0%{?rhel_version}
BuildRequires: gcc-c++ > 4.8.0
%else
BuildRequires: devtoolset-4-gcc-c++
%endif
%else
BuildRequires: gcc-c++
%endif
BuildRequires:  libjpeg-devel
BuildRequires:  libmng-devel
BuildRequires:  mysql-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  pkgconfig
%if ! 0%{?rhel_version}
BuildRequires:  pkgconfig(mtdev)
%endif
%if %qt5_snapshot
#to create the forwarding headers
BuildRequires:  perl
%endif
BuildRequires:  postgresql-devel
BuildRequires:  unixODBC-devel
BuildRequires:  pkgconfig(dbus-1)
%if %have_egl
BuildRequires:  pkgconfig(egl)
%endif
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  libicu-devel
BuildRequires:  pkgconfig(libpulse)
%if ! 0%{?centos_version} && ! 0%{?rhel_version}
BuildRequires:  tslib-devel
%endif
%if ! 0%{?rhel_version}
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-keysyms-devel
%endif
%if ! 0%{?el6}
%if ! 0%{?rhel_version}
BuildRequires:  xcb-util-renderutil-devel
%endif
%global sqlite -system-sqlite
BuildRequires: pkgconfig(sqlite3) >= 3.7
%else
%global sqlite %nil
%endif
%if ! 0%{?rhel_version}
BuildRequires:  xcb-util-wm-devel
%endif
#BuildRequires:  xorg-x11-devel
BuildRequires:  xz
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
%if 0%{?is_opensuse}
BuildRequires:  pkgconfig(harfbuzz)
%endif
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(sm)
%if ! 0%{?use_qt_xkbcommon}
BuildRequires:  pkgconfig(xkbcommon) >= 0.4.1
BuildRequires:  pkgconfig(xkbcommon-x11) >= 0.4.1
BuildRequires:  pkgconfig(libinput)
%endif

BuildRequires:  pkgconfig(inputproto)
%if %journald
BuildRequires:  pkgconfig(libsystemd-journal)
%endif
# to get cmake(...) autoprovides
BuildRequires:  cmake
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Qt is a set of libraries for developing applications.

This package contains base tools, like string, xml, and network
handling.


%define libqt5_prefix		%{_oc_prefix}
%define libqt5_libdir		%{_oc_libdir}
%define libqt5_archdatadir	%{_oc_libdir}/qt5
%define libqt5_bindir		%{libqt5_archdatadir}/bin
%define libqt5_datadir		%{_oc_datadir}/qt5
%define libqt5_docdir		%{_docdir}/@PACKAGE_NAME_PREFIX@-qt5
%define libqt5_examplesdir	%{libqt5_archdatadir}/examples
%define libqt5_includedir	%{_oc_includedir}/qt5
%define libqt5_importdir	%{libqt5_archdatadir}/imports
%define libqt5_libexecdir	%{libqt5_archdatadir}/libexec
%define libqt5_plugindir	%{libqt5_archdatadir}/plugins
%define libqt5_sysconfdir	%{_sysconfdir}/xdg
%define libqt5_translationdir	%{libqt5_datadir}/translations

%prep
%setup -q -n qtbase-opensource-src-%{real_version}
# % patch3 -p1
# % patch5 -p1
# % patch6 -p1
# % patch7 -p1
# % patch1003 -p1
# % patch1004 -p1
# % patch1005 -p1
# % patch1006 -p1
# % patch1007 -p1
# % patch1008 -p1
# % patch1009 -p1

# be sure not to use them
rm -r src/3rdparty/{libjpeg,freetype,libpng,zlib}
#rm -r mkspecs/features/qt_module.prf.orig
#rm -r qtimageformats/src/3rdparty/{libtiff,libmng}

%package devel
Summary:        Qt Development Kit
Group:          Development/Libraries/X11
# External deps shall be found via pkgconfig
Requires:       %{name}-common-devel
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Concurrent-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5DBus-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Network-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5OpenGL-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5PlatformHeaders-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5PrintSupport-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Sql-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Test-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Xml-devel = %{version}

%description devel
You need this package, if you want to compile programs with Qt. It
contains the "Qt Crossplatform Development Kit". It does contain
include files and development applications like GUI designers,
translator tools and code generators.

%package common-devel
Summary:        Qt 5 Core Development Binaries
Group:          Development/Libraries/X11
Requires:       gcc-c++
Requires:       pkgconfig
# to get cmake(...) autoprovides
Requires:       cmake

%description common-devel
Qt 5 Core Development Binaries. It contains Qt5's moc, qmake,
rcc, uic and syncqt.pl binaries.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Core5
Summary:        Qt 5 Core Library
Group:          Development/Libraries/X11
Provides:       @PACKAGE_NAME_PREFIX@-libqt5-qtbase = %{version}
Obsoletes:      @PACKAGE_NAME_PREFIX@-libqt5-qtbase < %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Core5
The Qt 5 Core library.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Core-devel
Summary:        Qt 5 Core Library - development files
Group:          Development/Libraries/X11
Requires:       %{name}-common-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Core-devel
Qt 5 Core Library - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel
Summary:        Qt 5 Core Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel
Qt 5 Core Library - Non-ABI stable development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Concurrent5
Summary:        Qt 5 Concurrent Library
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Concurrent5
The Qt 5 Concurrent library.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Concurrent-devel
Summary:        Qt 5 Concurrent Library - development files
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Concurrent5 = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Concurrent-devel
The Qt 5 Concurrent library - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5DBus5
Summary:        Qt 5 DBus Library
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5DBus5
The Qt 5 DBus library.

%package -n @PACKAGE_NAME_PREFIX@-libQt5DBus-devel
Summary:        Qt 5 DBus Library - development files
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5DBus5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5DBus-devel
The Qt 5 DBus library - development files. Aditionally, it contains
Qt5's qdbusxml2cpp and qdbuscpp2xml binaries.

%package -n @PACKAGE_NAME_PREFIX@-libQt5DBus-private-headers-devel
Summary:        Qt 5 DBus Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5DBus-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5DBus-private-headers-devel
Qt 5 DBus Library - Non-ABI stable development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Network5
Summary:        Qt 5 Network Library
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core5 = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5DBus5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Network5
The Qt 5 Network library.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Network-devel
Summary:        Qt 5 Network Library - development files
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Network5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Network-devel
The Qt 5 Network library - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Network-private-headers-devel
Summary:        Qt 5 Network Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Network-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Network-private-headers-devel
Qt 5 Network Library - Non-ABI stable development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL5
Summary:        Qt 5 OpenGL Library
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL5
The Qt 5 OpenGL library.

%package -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL-devel
Summary:        Qt 5 OpenGL Library - development files
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5OpenGL5 = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets-devel = %{version}
Requires:       pkgconfig(gl)

%description -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL-devel
The Qt 5 OpenGL library - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL-private-headers-devel
Summary:        Qt 5 OpenGL Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5OpenGL-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets-private-headers-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL-private-headers-devel
Qt 5 OpenGL Library - Non-ABI stable development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport5
Summary:        Qt 5 Print Support Library
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport5
The Qt 5 Print Support library.

%package -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport-devel
Summary:        Qt 5 Print Support Library - development files
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5PrintSupport5 = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport-devel
The Qt 5 Print Support library - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport-private-headers-devel
Summary:        Qt 5 Print Support Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5PrintSupport-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets-private-headers-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport-private-headers-devel
Qt 5 Print Support Library - Non-ABI stable development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Xml5
Summary:        Qt 5 Xml Library
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Xml5
The Qt 5 Xml library.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Xml-devel
Summary:        Qt 5 Xml Library - development files
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Xml5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Xml-devel
The Qt 5 Xml library - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Test5
Summary:        Qt 5 Test Library
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Test5
The Qt 5 library for testing.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Test-devel
Summary:        Qt 5 Test Library - development files
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Test5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Test-devel
The Qt 5 library for testing - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Test-private-headers-devel
Summary:        Qt 5 Test Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Test-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Test-private-headers-devel
Qt 5 Test Library - Non-ABI stable development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Widgets5
Summary:        Qt 5 Widgets Library
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Widgets5
The Qt 5 library to display widgets.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Widgets-devel
Summary:        Qt 5 Widgets Library - development files
Group:          Development/Libraries/X11
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Widgets-devel
The Qt 5 library to display widgets - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Widgets-private-headers-devel
Summary:        Qt 5 Widgets Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Widgets-private-headers-devel
Qt 5 Widgets Library - Non-ABI stable development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-sqlite
Summary:        Qt 5 sqlite plugin
Group:          Development/Libraries/C and C++
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Sql5 = %{version}
Provides:       @PACKAGE_NAME_PREFIX@-libqt5-sql-sqlite = %{version}
Provides:       @PACKAGE_NAME_PREFIX@-libqt5_sql_backend = %{version}
Obsoletes:      @PACKAGE_NAME_PREFIX@-libqt5-sql-sqlite < %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-sqlite
Qt 5 sqlite plugin to be able to use database functionality with Qt
applications without the need to setup a SQL server.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-unixODBC
Summary:        Qt 5 unixODBC plugin
Group:          Development/Libraries/C and C++
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Sql5 = %{version}
Provides:       @PACKAGE_NAME_PREFIX@-libqt5-sql-unixODBC = %{version}
Provides:       @PACKAGE_NAME_PREFIX@-libqt5_sql_backend = %{version}
Obsoletes:      @PACKAGE_NAME_PREFIX@-libqt5-sql-unixODBC < %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-unixODBC
Qt unixODBC plugin to support databases via unixODBC within Qt
applications.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-postgresql
Summary:        Qt 5 PostgreSQL plugin
Group:          Development/Libraries/C and C++
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Sql5 = %{version}
Provides:       @PACKAGE_NAME_PREFIX@-libqt5-sql-postgresql = %{version}
Provides:       @PACKAGE_NAME_PREFIX@-libqt5_sql_backend = %{version}
Obsoletes:      @PACKAGE_NAME_PREFIX@-libqt5-sql-postgresql < %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-postgresql
Qt SQL plugin to support PostgreSQL servers in Qt applications.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-mysql
Summary:        Qt 5 MySQL support
Group:          Development/Libraries/C and C++
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Sql5 = %{version}
Provides:       @PACKAGE_NAME_PREFIX@-libqt5-sql-mysql = %{version}
Provides:       @PACKAGE_NAME_PREFIX@-libqt5_sql_backend = %{version}
Obsoletes:      @PACKAGE_NAME_PREFIX@-libqt5-sql-mysql < %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-mysql
A plugin to support MySQL server in Qt applications.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Gui5
Summary:        Qt 5 GUI related libraries
Group:          Development/Libraries/C and C++
%if ! 0%{?centos_version} && ! 0%{?rhel_version}
Recommends:     libqt5-qtimageformats = %{version}
%endif
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core5 = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5DBus5 = %{version}
Provides:       @PACKAGE_NAME_PREFIX@-libqt5-qtbase-platformtheme-gtk2 = %{version}
Obsoletes:      @PACKAGE_NAME_PREFIX@-libqt5-qtbase-platformtheme-gtk2 <= %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Gui5
Qt 5 libraries which are depending on X11.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Gui-devel
Summary:        Qt 5 GUI related libraries - development files
Group:          Development/Libraries/C and C++
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui5 = %{version}
Requires:       pkgconfig(gl)
%if %have_egl
Requires:       pkgconfig(egl)
%endif
Requires:       pkgconfig(libdrm)

%description -n @PACKAGE_NAME_PREFIX@-libQt5Gui-devel
Qt 5 libraries which are depending on X11 - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel
Summary:        Qt 5 Gui Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel
Qt 5 Gui Library - Non-ABI stable development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Sql5
Summary:        Qt 5 SQL related libraries
Group:          Development/Libraries/C and C++
%if ! 0%{?centos_version} && ! 0%{?rhel_version}
Recommends:     @PACKAGE_NAME_PREFIX@-libqt5_sql_backend = %{version}
Suggests:       @PACKAGE_NAME_PREFIX@-libqt5-sql-sqlite
%endif
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core5 = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Sql5
Qt 5 libraries which are used for connection with an SQL server. You
will need also a plugin package for a supported SQL server.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Sql-devel
Summary:        Qt 5 SQL related libraries - development files
Group:          Development/Libraries/C and C++
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Sql5 = %{version}
%if ! 0%{?centos_version} && ! 0%{?rhel_version}
Suggests:       @PACKAGE_NAME_PREFIX@-libQt5Sql5-mysql = %{version}
Suggests:       @PACKAGE_NAME_PREFIX@-libQt5Sql5-postgresql = %{version}
Suggests:       @PACKAGE_NAME_PREFIX@-libQt5Sql5-sqlite = %{version}
Suggests:       @PACKAGE_NAME_PREFIX@-libQt5Sql5-unixODBC = %{version}
%endif

%description -n @PACKAGE_NAME_PREFIX@-libQt5Sql-devel
Qt 5 libraries which are used for connection with an SQL server. You
will need also a plugin package for a supported SQL server - development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Sql-private-headers-devel
Summary:        Qt 5 SQL Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Sql-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Sql-private-headers-devel
Qt 5 SQL Library - Non-ABI stable development files.

%package private-headers-devel
Summary:        Non-ABI stable experimental API
Group:          Development/Libraries/C and C++
BuildArch:      noarch
Requires:       %{name}-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5DBus-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Network-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5OpenGL-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5PlatformSupport-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5PrintSupport-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Sql-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Test-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Widgets-private-headers-devel = %{version}

%description private-headers-devel
This package provides private headers of libqt5-qtbase-devel that are normally
not used by application development and that do not have any ABI or
API guarantees. The packages that build against these have to require
the exact Qt version.

%package -n @PACKAGE_NAME_PREFIX@-libQt5Bootstrap-devel-static
Summary:        Qt Bootstrap module
Group:          Development/Libraries/C and C++
Requires:       %{name}-common-devel = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5Bootstrap-devel-static
Qt Bootstrap module.

%package -n @PACKAGE_NAME_PREFIX@-libQt5OpenGLExtensions-devel-static
Summary:        Qt OpenGLExtensions module
Group:          Development/Libraries/C and C++
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-devel = %{version}
# List the below ones manually - they are private, but this is a static lib
Requires:       pkgconfig(gl)

%description -n @PACKAGE_NAME_PREFIX@-libQt5OpenGLExtensions-devel-static
Qt OpenGLExtensions module.

%package -n @PACKAGE_NAME_PREFIX@-libQt5PlatformSupport-devel-static
Summary:        Qt PlatformSupport module
Group:          Development/Libraries/C and C++
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5PlatformHeaders-devel = %{version}
# List the below ones manually - they are private, but this is a static lib
Requires:       tslib-devel
Requires:       pkgconfig(@PACKAGE_NAME_PREFIX@-Qt5DBus)
%if %have_egl
Requires:       pkgconfig(egl)
%endif
Requires:       pkgconfig(fontconfig)
Requires:       pkgconfig(freetype2)
Requires:       pkgconfig(gl)
Requires:       pkgconfig(glib-2.0)
Requires:       pkgconfig(libinput)
Requires:       pkgconfig(libudev)
Requires:       pkgconfig(mtdev)
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xext)
%if ! 0%{?centos_version} && ! 0%{?rhel_version}
Requires:       pkgconfig(xkbcommon) >= 0.4.1
Requires:       pkgconfig(xkbcommon-x11) >= 0.4.1
%endif
Requires:       pkgconfig(xrender)

%description -n @PACKAGE_NAME_PREFIX@-libQt5PlatformSupport-devel-static
Qt PlatformSupport module.

%package -n @PACKAGE_NAME_PREFIX@-libQt5PlatformSupport-private-headers-devel
Summary:        Qt 5 PlatformSupport Library - Non-ABI stable development files
Group:          Development/Libraries/X11
BuildArch:      noarch
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5PlatformSupport-devel-static = %{version}

%description -n @PACKAGE_NAME_PREFIX@-libQt5PlatformSupport-private-headers-devel
Qt 5 PlatformSupport Library - Non-ABI stable development files.

%package -n @PACKAGE_NAME_PREFIX@-libQt5PlatformHeaders-devel
Summary:        Qt 5 PlatformHeaders
Group:          Development/Libraries/X11
# NOTE this needs to be checked on every update - package provides only a low number of headers, so check which 3rd party, or other qtbase includes are used
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Core-devel = %{version}
Requires:       @PACKAGE_NAME_PREFIX@-libQt5Gui-devel = %{version}
%if %have_egl
Requires:       pkgconfig(egl)
%endif
Requires:       pkgconfig(x11)
Requires:       pkgconfig(gl)

%description -n @PACKAGE_NAME_PREFIX@-libQt5PlatformHeaders-devel
Qt 5 PlatformHeaders.

%package examples
Summary:        Qt5 base examples
Group:          Development/Libraries/X11
%if ! 0%{?centos_version} && ! 0%{?rhel_version}
Recommends:     libqt5-qtbase-devel
%endif

%description examples
Examples for libqt5-qtbase modules.

%build
%if 0%{?use_devtoolset}
source /opt/rh/devtoolset-4/enable
%endif

export QMAKESPEC=$PWD/mkspecs/linux-g++
%ifarch ppc64
  RPM_OPT_FLAGS="%{optflags} -mminimal-toc"
%endif
export CXXFLAGS="$CXXFLAGS %{optflags} -DOPENSSL_LOAD_CONF"
export CFLAGS="$CFLAGS %{optflags} -DOPENSSL_LOAD_CONF"
export MAKEFLAGS="%{?_smp_mflags}"
%ifarch sparc64
platform="-platform linux-g++-64"
%else
platform=""
%endif
%define xkbconfigroot %(pkg-config --variable=xkb_base xkeyboard-config)


#if %qt5_snapshot
#force the configure script to generate the forwarding headers (it checks whether .git directory exists)
mkdir -p .git
#endif
# Record mtime of changes file instead of build time
export CHANGES=`stat --format="%y" %{SOURCE1}|cut --characters=1-10`
sed -i 's|qt_instdate=`date +%Y-%m-%d`|qt_instdate=$CHANGES|g' configure
# so non-qt5 apps/libs don't get stripped
sed -i -e 's|^\(QMAKE_STRIP.*=\).*$|\1|g' mkspecs/common/linux.conf

echo yes | ./configure $platform \
	-prefix %{_prefix} \
	-L %{libqt5_libdir} \
	-libdir %{libqt5_libdir} \
	-archdatadir %{libqt5_archdatadir} \
	-bindir %{libqt5_bindir} \
	-datadir %{libqt5_datadir} \
	-docdir %{libqt5_docdir} \
	-examplesdir %{libqt5_examplesdir} \
	-headerdir %{libqt5_includedir} \
	-importdir %{libqt5_importdir} \
	-libexecdir %{libqt5_libexecdir} \
	-plugindir %{libqt5_plugindir} \
	-sysconfdir %{libqt5_sysconfdir} \
	-translationdir %{libqt5_translationdir} \
	-verbose \
%ifarch %ix86 x86_64
	-reduce-relocations \
%else
	-no-reduce-relocations \
%endif
%ifarch %ix86
	-no-sse2 -no-pch \
%endif
	-optimized-qmake \
	-accessibility \
	-no-strip \
	-opensource \
	-no-separate-debug-info \
	-shared \
	-xkb \
	%{xkbcommon} \
	-xrender \
	-xcursor \
	-dbus-linked \
	-xfixes \
	-xrandr \
	-xinerama \
	-sm \
	-no-rpath \
	-system-libjpeg \
	-openssl-linked \
	-system-libpng \
%if 0%{?is_opensuse}
	-system-harfbuzz \
%endif
	-fontconfig \
	-system-freetype \
	-cups \
	-system-zlib \
	-iconv \
	-no-pch \
	-glib \
	%{sqlite} \
	-no-sql-mysql \
	-no-strip \
%if %journald
	-journald \
%endif
	-xsync \
	-xinput \
	-gtkstyle \
	%{?xcb} \
%if %have_egl
	-egl \
	-eglfs \
%endif
	-opengl desktop \
    -release \
	-plugin-sql-sqlite -nomake tests \
	-plugin-sql-psql -I/usr/include/pgsql/ -I/usr/include/pgsql/server \
	-plugin-sql-odbc \
	-plugin-sql-mysql -I/usr/include/mysql/ -v

make %{?_smp_mflags} || make -j1

%install
%if 0%{?use_devtoolset}
source /opt/rh/devtoolset-4/enable
%endif

make INSTALL_ROOT=%{buildroot} install

%ifarch %ix86
install -d %{buildroot}%{libqt5_libdir}/sse2/

pushd src/corelib; make clean ; ../../bin/qmake -config sse2; make %{?_smp_mflags}
cp -av ../../lib/libQt5Core.so.* %{buildroot}%{libqt5_libdir}/sse2/
popd

pushd src/gui; ../../bin/qmake -config sse2; make %{?_smp_mflags}
cp -av ../../lib/libQt5Gui.so.* %{buildroot}%{libqt5_libdir}/sse2/
popd
%endif

install -D -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/macros.@PACKAGE_NAME_PREFIX@-qt5
# argggh, qmake is such a piece of <censored>
find %{buildroot}/%{libqt5_libdir} -type f -name '*prl' -exec perl -pi -e "s, -L$RPM_BUILD_DIR/\S+,,g" {} \;
find %{buildroot}/%{libqt5_libdir} -type f -name '*prl' -exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" {} \;
find %{buildroot}/%{libqt5_libdir} -type f -name '*la' -print -exec perl -pi -e "s, -L$RPM_BUILD_DIR/?\S+,,g" {} \;
# insanity ...
find %{buildroot}/%{libqt5_libdir} -type f -name '*pc' -print -exec perl -pi -e "s, -L$RPM_BUILD_DIR/?\S+,,g" {} \; -exec sed -i -e "s,^moc_location=.*,moc_location=%libqt5_bindir/moc," -e "s,uic_location=.*,uic_location=%libqt5_bindir/uic," {} \;
find %{buildroot}/%{libqt5_libdir}/ -name 'lib*.a' -exec chmod -x -- {} \;
# kill .la files
rm -f %{buildroot}%{libqt5_libdir}/lib*.la

#
rm -fv %{buildroot}%{libqt5_libdir}/cmake/Qt5*/Q*Plugin.cmake

mkdir -p %{buildroot}/%{libqt5_plugindir}/sqldrivers

# put all the binaries to ${libqt5_prefix}/bin and symlink them back to %_qt5_bindir
mkdir %{buildroot}%{libqt5_prefix}/bin
pushd %{buildroot}%{libqt5_bindir}
for i in * ; do
    mv $i ../../../bin/
    ln -s ../../../bin/$i .
done
popd

pushd %{buildroot}%{libqt5_docdir}/global/template/images
chmod -R 644 *.png
popd

%post -n @PACKAGE_NAME_PREFIX@-libQt5Core5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5Concurrent5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5DBus5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5Network5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5Xml5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5Gui5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5Sql5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5Test5 -p /sbin/ldconfig

%post -n @PACKAGE_NAME_PREFIX@-libQt5Widgets5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5Core5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5Concurrent5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5DBus5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5Network5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5Xml5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5Gui5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5Sql5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5Test5 -p /sbin/ldconfig

%postun -n @PACKAGE_NAME_PREFIX@-libQt5Widgets5 -p /sbin/ldconfig

%files common-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*

%{_sysconfdir}/rpm/macros.@PACKAGE_NAME_PREFIX@-qt5
%{libqt5_prefix}/bin/moc*
%{libqt5_bindir}/moc*
%{libqt5_prefix}/bin/qmake*
%{libqt5_bindir}/qmake*
%{libqt5_prefix}/bin/rcc*
%{libqt5_bindir}/rcc*
%{libqt5_prefix}/bin/uic*
%{libqt5_bindir}/uic*
%{libqt5_prefix}/bin/syncqt.pl*
%{libqt5_prefix}/bin/fixqt4headers.pl*
%{libqt5_bindir}/syncqt.pl*
%{libqt5_bindir}/fixqt4headers.pl*
%{libqt5_prefix}/bin/qlalr*
%{libqt5_bindir}/qlalr*
%{libqt5_archdatadir}/mkspecs/
%dir %{libqt5_libdir}/cmake
%dir %{libqt5_includedir}
%dir %{libqt5_archdatadir}
%dir %{libqt5_bindir}

%files -n @PACKAGE_NAME_PREFIX@-libQt5Core5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Core.so.*
%ifarch %ix86
%dir %{libqt5_libdir}/sse2
%{libqt5_libdir}/sse2/libQt5Core.so.*
%endif

%files -n @PACKAGE_NAME_PREFIX@-libQt5Core-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Core.so
%{libqt5_libdir}/libQt5Core.prl
%{libqt5_libdir}/cmake/Qt5Core/
%{libqt5_libdir}/cmake/Qt5/
%{libqt5_libdir}/pkgconfig/Qt5Core.pc
%{libqt5_includedir}/QtCore/
%exclude %{libqt5_includedir}/QtCore/%{so_version}
%{libqt5_docdir}

%files -n @PACKAGE_NAME_PREFIX@-libQt5Concurrent5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Concurrent.so.*

%files -n @PACKAGE_NAME_PREFIX@-libQt5Concurrent-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Concurrent.so
%{libqt5_libdir}/libQt5Concurrent.prl
%{libqt5_libdir}/cmake/Qt5Concurrent/
%{libqt5_libdir}/pkgconfig/Qt5Concurrent.pc
%{libqt5_includedir}/QtConcurrent/

%files -n @PACKAGE_NAME_PREFIX@-libQt5DBus5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5DBus.so.*

%files -n @PACKAGE_NAME_PREFIX@-libQt5DBus-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5DBus.so
%{libqt5_libdir}/libQt5DBus.prl
%{libqt5_libdir}/cmake/Qt5DBus/
%{libqt5_libdir}/pkgconfig/Qt5DBus.pc
%{libqt5_includedir}/QtDBus/
%exclude %{libqt5_includedir}/QtDBus/%{so_version}
%{libqt5_bindir}/qdbusxml2cpp*
%{libqt5_prefix}/bin/qdbusxml2cpp*
%{libqt5_bindir}/qdbuscpp2xml*
%{libqt5_prefix}/bin/qdbuscpp2xml*

%files -n @PACKAGE_NAME_PREFIX@-libQt5Network5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Network.so.*
%dir %{libqt5_libdir}/qt5
%dir %{libqt5_plugindir}
%{libqt5_plugindir}/bearer

%files -n @PACKAGE_NAME_PREFIX@-libQt5Network-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Network.so
%{libqt5_libdir}/libQt5Network.prl
%{libqt5_libdir}/cmake/Qt5Network/
%{libqt5_libdir}/pkgconfig/Qt5Network.pc
%{libqt5_includedir}/QtNetwork/
%exclude %{libqt5_includedir}/QtNetwork/%{so_version}

%files -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5OpenGL.so.*

%files -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5OpenGL.so
%{libqt5_libdir}/libQt5OpenGL.prl
%{libqt5_libdir}/cmake/Qt5OpenGL/
%{libqt5_libdir}/pkgconfig/Qt5OpenGL.pc
%{libqt5_includedir}/QtOpenGL/
%exclude %{libqt5_includedir}/QtOpenGL/%{so_version}

%files -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5PrintSupport.so.*
%{libqt5_plugindir}/printsupport

%files -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5PrintSupport.so
%{libqt5_libdir}/libQt5PrintSupport.prl
%{libqt5_libdir}/cmake/Qt5PrintSupport/
%{libqt5_libdir}/pkgconfig/Qt5PrintSupport.pc
%{libqt5_includedir}/QtPrintSupport/
%exclude %{libqt5_includedir}/QtPrintSupport/%{so_version}

%files -n @PACKAGE_NAME_PREFIX@-libQt5Xml5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Xml.so.*

%files -n @PACKAGE_NAME_PREFIX@-libQt5Xml-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Xml.so
%{libqt5_libdir}/libQt5Xml.prl
%{libqt5_libdir}/cmake/Qt5Xml/
%{libqt5_libdir}/pkgconfig/Qt5Xml.pc
%{libqt5_includedir}/QtXml/

%files -n @PACKAGE_NAME_PREFIX@-libQt5Test5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Test.so.*

%files -n @PACKAGE_NAME_PREFIX@-libQt5Test-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Test.so
%{libqt5_libdir}/libQt5Test.prl
%{libqt5_libdir}/cmake/Qt5Test/
%{libqt5_libdir}/pkgconfig/Qt5Test.pc
%{libqt5_includedir}/QtTest/
%exclude %{libqt5_includedir}/QtTest/%{so_version}

%files -n @PACKAGE_NAME_PREFIX@-libQt5Widgets5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Widgets.so.*

%files -n @PACKAGE_NAME_PREFIX@-libQt5Widgets-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Widgets.so
%{libqt5_libdir}/libQt5Widgets.prl
%{libqt5_libdir}/cmake/Qt5Widgets/
%{libqt5_libdir}/pkgconfig/Qt5Widgets.pc
%{libqt5_includedir}/QtWidgets/
%exclude %{libqt5_includedir}/QtWidgets/%{so_version}

%files -n @PACKAGE_NAME_PREFIX@-libQt5Gui5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Gui.so.*
%ifarch %ix86
%{libqt5_libdir}/sse2/libQt5Gui.so.*
%endif
%if %have_egl
%{libqt5_libdir}/libQt5EglDeviceIntegration.so.*
%endif
%{libqt5_libdir}/libQt5XcbQpa.so.*
%{libqt5_plugindir}/generic
%{libqt5_plugindir}/imageformats
%{libqt5_plugindir}/platforminputcontexts
%{libqt5_plugindir}/platforms
%if %have_egl
%{libqt5_plugindir}/egldeviceintegrations
%endif
%{libqt5_plugindir}/xcbglintegrations
%{libqt5_plugindir}/platformthemes/

%files -n @PACKAGE_NAME_PREFIX@-libQt5Gui-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Gui.so
%{libqt5_libdir}/libQt5Gui.prl
%{libqt5_libdir}/cmake/Qt5Gui/
%{libqt5_libdir}/pkgconfig/Qt5Gui.pc
%{libqt5_includedir}/QtGui/
%exclude %{libqt5_includedir}/QtGui/%{so_version}

%files devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*

%files private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*

%files -n @PACKAGE_NAME_PREFIX@-libQt5Sql5
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Sql.so.*
%dir %{libqt5_plugindir}/sqldrivers

%files -n @PACKAGE_NAME_PREFIX@-libQt5Sql-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Sql.so
%{libqt5_libdir}/libQt5Sql.prl
%{libqt5_libdir}/cmake/Qt5Sql/
%{libqt5_libdir}/pkgconfig/Qt5Sql.pc
%{libqt5_includedir}/QtSql/
%exclude %{libqt5_includedir}/QtSql/%{so_version}

%files -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-sqlite
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_plugindir}/sqldrivers/libqsqlite*.so

%files -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-unixODBC
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_plugindir}/sqldrivers/libqsqlodbc*.so

%files -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-postgresql
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_plugindir}/sqldrivers/libqsqlpsql*.so

%files -n @PACKAGE_NAME_PREFIX@-libQt5Sql5-mysql
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_plugindir}/sqldrivers/libqsqlmysql*.so

%files -n @PACKAGE_NAME_PREFIX@-libQt5Bootstrap-devel-static
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5Bootstrap.a
%{libqt5_libdir}/libQt5Bootstrap.prl
#{libqt5_libdir}/pkgconfig/Qt5Bootstrap.pc

%files -n @PACKAGE_NAME_PREFIX@-libQt5OpenGLExtensions-devel-static
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_libdir}/libQt5OpenGLExtensions.a
%{libqt5_libdir}/libQt5OpenGLExtensions.prl
%{libqt5_libdir}/cmake/Qt5OpenGLExtensions/
%{libqt5_libdir}/pkgconfig/Qt5OpenGLExtensions.pc
%{libqt5_includedir}/QtOpenGLExtensions/

%files -n @PACKAGE_NAME_PREFIX@-libQt5PlatformSupport-devel-static
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%if %have_egl
%{libqt5_libdir}/libQt5EglDeviceIntegration.so
%{libqt5_libdir}/libQt5EglDeviceIntegration.prl
%endif
%{libqt5_libdir}/libQt5XcbQpa.so
%{libqt5_libdir}/libQt5PlatformSupport.a
%{libqt5_libdir}/libQt5PlatformSupport.prl
%{libqt5_libdir}/libQt5XcbQpa.prl
#{libqt5_libdir}/pkgconfig/Qt5PlatformSupport.pc
#{libqt5_libdir}/pkgconfig/Qt5EglDeviceIntegration.pc
#{libqt5_libdir}/pkgconfig/Qt5XcbQpa.pc
%{libqt5_includedir}/QtPlatformSupport/
%exclude %{libqt5_includedir}/QtPlatformSupport/%{so_version}

%files -n @PACKAGE_NAME_PREFIX@-libQt5Core-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtCore/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5DBus-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtDBus/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtGui/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5Network-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtNetwork/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5OpenGL-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtOpenGL/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5PlatformSupport-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtPlatformSupport/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5PrintSupport-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtPrintSupport/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5Sql-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtSql/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5Test-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtTest/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5Widgets-private-headers-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtWidgets/%{so_version}/

%files -n @PACKAGE_NAME_PREFIX@-libQt5PlatformHeaders-devel
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_includedir}/QtPlatformHeaders/

%files examples
%defattr(-,root,root,755)
%doc *.txt LICENSE.*
%{libqt5_examplesdir}/

%changelog
