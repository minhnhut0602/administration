%_oc_package_header
%_use_oc_qt5_as_default
%define use_devtoolset 0
%if 0%{?el6} || 0%{?el7}
%if ! 0%{?rhel_version}
%define use_devtoolset 1
%endif
%endif

%global qt_module qtwebkit

%global _hardened_build 1

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
# only primary archs (for now), allow secondary to bootstrap
%define docs 0

Summary: Qt5 - QtWebKit components
Name:    @PACKAGE_NAME_PREFIX@-libqt5-qtwebkit
Version: 5.6.2
Release: 2%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

# Search /usr/lib{,64}/mozilla/plugins-wrapped for browser plugins too
Patch1: qtwebkit-opensource-src-5.2.0-pluginpath.patch

# smaller debuginfo s/-g/-g1/ (debian uses -gstabs) to avoid 4gb size limit
Patch3: qtwebkit-opensource-src-5.0.1-debuginfo.patch

# tweak linker flags to minimize memory usage on "small" platforms
Patch4: qtwebkit-opensource-src-5.2.0-save_memory.patch

# use unbundled system angleproject library
#define system_angle 1
# NEEDS REBASE -- rex
Patch5: qtwebkit-opensource-src-5.0.2-system_angle.patch
# Fix compilation against latest ANGLE
# https://bugs.webkit.org/show_bug.cgi?id=109127
Patch6: webkit-commit-142567.patch

# truly madly deeply no rpath please, kthxbye
Patch8: qtwebkit-opensource-src-5.2.1-no_rpath.patch

Patch130:       no-Werror-rpath.diff

BuildRequires: @PACKAGE_NAME_PREFIX@-filesystem

%if 0%{?use_devtoolset}
BuildRequires: devtoolset-4-gcc-c++
%else
BuildRequires: gcc-c++
%endif


%if 0%{?system_angle}
BuildRequires: angleproject-devel angleproject-static
%endif

BuildRequires: @PACKAGE_NAME_PREFIX@-libqt5-qtbase-devel >= %{version}
BuildRequires: @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel >= %{version}

# BuildRequires: qt5-qtdeclarative-devel >= %{version}
# BuildRequires: qt5-qtlocation-devel
# BuildRequires: qt5-qtsensors-devel

BuildRequires: bison
BuildRequires: flex
BuildRequires: gperf
BuildRequires: libicu-devel
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig(gio-2.0) pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gl)
# gstreamer media support
%if 0%{?fedora} > 20 || 0%{?rhel} >= 7
BuildRequires: pkgconfig(gstreamer-1.0) pkgconfig(gstreamer-app-1.0)
%else
BuildRequires: pkgconfig(gstreamer-0.10) pkgconfig(gstreamer-app-0.10)
%endif
BuildRequires: libpng-devel
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(libudev)
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires: pkgconfig(libwebp)
BuildRequires: ruby-devel
%endif
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(xcomposite) pkgconfig(xrender)
BuildRequires: perl perl(version) perl(Digest::MD5) perl(Text::ParseWords)
BuildRequires: ruby
BuildRequires: zlib-devel
BuildRequires: python

# %{?_qt5_version:Requires: @PACKAGE_NAME_PREFIX@-libqt5-qtbase%{?_isa} >= %{_qt5_version}}

##upstream patches


%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: @PACKAGE_NAME_PREFIX@-libqt5-qtbase-devel%{?_isa}
# Requires: qt5-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
# for qhelpgenerator
BuildRequires: @PACKAGE_NAME_PREFIX@-libqt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif


%prep
%setup -q -n qtwebkit-opensource-src-%{version}%{?pre:-%{pre}}

%patch1 -p1 -b .pluginpath
%patch3 -p1 -b .debuginfo
%patch4 -p1 -b .save_memory
%if 0%{?system_angle}
#patch5 -p1 -b .system_angle
%patch6 -p1 -b .svn142567
%endif
%patch8 -p1 -b .no_rpath
%patch130 -p1 -b .no_rpath_2

echo "nuke bundled code..."
# nuke bundled code
mkdir Source/ThirdParty/orig
mv Source/ThirdParty/{gtest/,qunit/} \
   Source/ThirdParty/orig/

%if 0%{?system_angle}
mv Source/ThirdParty/ANGLE/ \
   Source/ThirdParty/orig/
%endif


%build
%if 0%{?use_devtoolset}
source /opt/rh/devtoolset-4/enable
%endif

export QTDIR=%{_prefix}
export PATH=$PATH:%{_prefix}/bin

mkdir %{_target_platform}
pushd %{_target_platform}

%{qmake5} .. \
	%{?system_angle:DEFINES+=USE_SYSTEM_ANGLE=1}

make %{?_smp_mflags}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif
popd


%install
%if 0%{?use_devtoolset}
source /opt/rh/devtoolset-4/enable
%endif

make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

find %{buildroot}/%{_libqt5_libdir} -type f -name '*la' -print -exec perl -pi -e 's,-L%{_builddir}/\S+,,g' {} \;
find %{buildroot}/%{_libqt5_libdir} -type f -name '*pc' -print -exec perl -pi -e "s, -L$RPM_BUILD_DIR/?\S+,,g" {} \; -exec sed -i -e "s,^moc_location=.*,moc_location=%{_lib}qt5_bindir/moc," -e "s,uic_location=.*,uic_location=%{_lib}qt5_bindir/uic," {} \;
find %{buildroot}/%{_libqt5_libdir} -type f -name '*prl' -exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" {} \;

# kill .la files
rm -f %{buildroot}%{_libqt5_libdir}/lib*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc Source/WebCore/LICENSE*
%doc ChangeLog* VERSION
%{_libqt5_libdir}/libQt5WebKit.so.5*
%{_libqt5_libdir}/libQt5WebKitWidgets.so.5*

%dir %{_libqt5_libexecdir}
%{_libqt5_libexecdir}/QtWebPluginProcess
%{_libqt5_libexecdir}/QtWebProcess

%files -n %{name}-devel
%{_libqt5_includedir}/Qt*/
%{_libqt5_libdir}/libQt5*.so
%{_libqt5_libdir}/libQt5*.prl
%{_libqt5_libdir}/cmake/Qt5*/
%{_libqt5_libdir}/pkgconfig/Qt5*.pc
%{_libqt5_libdir}/qt5/mkspecs/modules/*.pri


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-6
- Rebuilt for GCC 5 C++11 ABI change

* Fri Apr 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-5
- -doc: drop dep on main pkg, not strictly required

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-4
- QtWebKit logs visited URLs to WebpageIcons.db in private browsing mode (#1204795,#1204798)

* Wed Mar 18 2015 Than Ngo <than@redhat.com> - 5.4.1-3
- fix build failure with new gcc5

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Tue Feb 17 2015 Than Ngo <than@redhat.com> 5.4.0-4
- fix GMutexLocker build problem

* Tue Feb 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-3
- rebuild (gcc5)

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 5.4.0-2
- rebuild for ICU 54.1

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.5.rc
- 5.4.0-rc

* Tue Nov 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.4.beta
- use gst1 only fc21+ (and el8+) only

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.beta
- fix hardening, use new %%qmake_qt5 macro

* Sat Nov 01 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- enable hardened build, out-of-src tree build

* Sat Oct 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 5.3.1-3
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-4
- use standard (same as qtbase) .prl sanitation

* Fri May 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- no rpath, drop chrpath hacks
- BR: qt5-qtlocation qt5-qtsensors

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- rebuild (libicu)

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Sun Feb 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- Add AArch64 support to qtwebkit (#1056160)

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- rebuild (libwebp)

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Thu Nov 28 2013 Dan Horák <dan[at]danny.cz> 5.2.0-0.6.beta1
- disable JIT on secondary arches, fix build with JIT disabled (#1034940)

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1
- enable -doc only on primary archs (allow secondary bootstrap)

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg
- use gstreamer1 (where available)

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Tue Aug 20 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-8
- qt5-qtjsbackend only supports ix86, x86_64 and arm

* Fri Aug 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-7
- use bundled angleproject (until system version passes review)

* Fri Jun 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-6
- %%doc ChangeLog VERSION
- %%doc Source/WebCore/LICENSE*
- squash more rpaths

* Fri May 17 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-5
- unbundle angleproject code

* Wed May 15 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- BR: perl(version) perl(Digest::MD5) pkgconfig(xslt)
- deal with bundled code
- add (commented) upstream link http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
  to clarify licensing

* Thu May 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- -devel: Requires: qt5-qtdeclarative-devel

* Fri Apr 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- BR: qt5-qtdeclarative-devel

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-2
- .prl love
- BR: pkgconfig(gl)

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

