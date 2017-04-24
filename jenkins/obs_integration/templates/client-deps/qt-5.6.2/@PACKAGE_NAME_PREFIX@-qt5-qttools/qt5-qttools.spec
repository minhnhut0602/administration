%_oc_package_header
%_use_oc_qt5_as_default
%define use_devtoolset 0
%if 0%{?el6} || 0%{?el7}
%if ! 0%{?rhel_version}
%define use_devtoolset 1
%endif
%endif

#global bootstrap 1

%global qt_module qttools
%if 0%{?centos_version} > 700
%global system_clucene 0
%endif

%_use_oc_qt5_as_default

Summary: Qt5 - QtTool components
Name:    @PACKAGE_NAME_PREFIX@-libqt5-qttools
Version: 5.6.2
Release: 2%{?dist}

License: LGPLv3 or LGPLv2
Url:     http://www.qt.io
Source0: http://download.qt.io/official_releases/qt/5.6/%{version}%{?prerelease:-%{prerelease}}/submodules/%{qt_module}-opensource-src-%{version}%{?prerelease:-%{prerelease}}.tar.xz

Patch1: qttools-opensource-src-5.3.2-system-clucene.patch

# help lrelease/lupdate use/prefer qmake-qt5
# https://bugzilla.redhat.com/show_bug.cgi?id=1009893
Patch2: qttools-opensource-src-5.5.0-qmake-qt5.patch

## upstream patches

Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qdbusviewer.desktop

# %%check needs cmake (and don't want to mess with cmake28)
BuildRequires: cmake
%if 0%{?use_devtoolset}
BuildRequires: devtoolset-4-gcc-c++
%else
BuildRequires: gcc-c++
%endif

BuildRequires: desktop-file-utils
BuildRequires: @PACKAGE_NAME_PREFIX@-filesystem
BuildRequires: @PACKAGE_NAME_PREFIX@-libqt5-qtbase-devel >= %{version}
BuildRequires: @PACKAGE_NAME_PREFIX@-libQt5Gui-private-headers-devel >= %{version}
BuildRequires: @PACKAGE_NAME_PREFIX@-libQt5Widgets-private-headers-devel
BuildRequires: @PACKAGE_NAME_PREFIX@-libQt5DBus-private-headers-devel
%if ! 0%{?rhel_version}
## CAUTION: dependency from tools to webkit? should not this be the other way round?
BuildRequires:  @PACKAGE_NAME_PREFIX@-libqt5-qtwebkit-devel
%endif

%if 0%{?system_clucene}
BuildRequires: clucene09-core-devel >= 0.9.21b-12
%endif

Requires: %{name}-common = %{version}-%{release}

%{?_qt5:Requires: %{_libqt5}%{?_isa} >= %{_libqt5_version}}

# when -libs were split out, for multilib upgrade path
Obsoletes: qt5-tools < 5.4.0-0.2

%description
%{summary}.

%package common
Summary: Common files for %{name}
BuildArch: noarch
%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs-clucene%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-help%{?_isa} = %{version}-%{release}
Requires: @PACKAGE_NAME_PREFIX@-libqt5-qtbase-devel%{?_isa}
Requires: @PACKAGE_NAME_PREFIX@-libqt5-qhelpgenerator = %{version}-%{release}
Requires: @PACKAGE_NAME_PREFIX@-libqt5-designer = %{version}-%{release}
Requires: @PACKAGE_NAME_PREFIX@-libqt5-linguist = %{version}-%{release}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%package libs-clucene
Summary: Qt5 CLucene runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-clucene
%{summary}.

%package libs-designer
Summary: Qt5 Designer runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-designer
%{summary}.

%package libs-designercomponents
Summary: Qt5 Designer Components runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-designercomponents
%{summary}.

%package libs-help
Summary: Qt5 Help runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-help
%{summary}.

%package -n @PACKAGE_NAME_PREFIX@-libqt5-assistant
Summary: Documentation browser for Qt5
Requires: %{name}-common = %{version}-%{release}
%description -n @PACKAGE_NAME_PREFIX@-libqt5-assistant
%{summary}.

%package -n @PACKAGE_NAME_PREFIX@-libqt5-designer
Summary: Design GUIs for Qt5 applications
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
%description -n @PACKAGE_NAME_PREFIX@-libqt5-designer
%{summary}.

%package -n @PACKAGE_NAME_PREFIX@-libqt5-designer-plugin-webkit
Summary: Qt5 designer plugin for WebKit
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
%description -n @PACKAGE_NAME_PREFIX@-libqt5-designer-plugin-webkit
%{summary}.

%package -n @PACKAGE_NAME_PREFIX@-libqt5-linguist
Summary: Qt5 Linguist Tools
Requires: %{name}-common = %{version}-%{release}
%description -n @PACKAGE_NAME_PREFIX@-libqt5-linguist
Tools to add translations to Qt5 applications.

%package -n @PACKAGE_NAME_PREFIX@-libqt5-qdbusviewer
Summary: D-Bus debugger and viewer
Requires: %{name}-common = %{version}-%{release}
%{?_qt5:Requires: %{_libqt5}%{?_isa} >= %{_libqt5_version}}
%description -n @PACKAGE_NAME_PREFIX@-libqt5-qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.

%package -n @PACKAGE_NAME_PREFIX@-libqt5-qhelpgenerator
Summary: Qt5 Help generator tool
Requires: %{name}-libs-help%{?_isa} = %{version}-%{release}
%{?_qt5:Requires: %{_libqt5}%{?_isa} >= %{_libqt5_version}}
%description -n @PACKAGE_NAME_PREFIX@-libqt5-qhelpgenerator

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
BuildRequires: @PACKAGE_NAME_PREFIX@-libqt5-qhelpgenerator
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}-common = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?prerelease:-%{prerelease}}

%if 0%{?system_clucene}
%patch1 -p1 -b .system_clucene
# bundled libs
rm -rf src/assistant/3rdparty/clucene
%endif
%patch2 -p1 -b .qmake-qt5


%build
%if 0%{?use_devtoolset}
source /opt/rh/devtoolset-4/enable
%endif

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{_oc_libqt5_libdir}
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags} || make

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif
popd


%install
%if 0%{?use_devtoolset}
source /opt/rh/devtoolset-4/enable
%endif

make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

# Add desktop files, --vendor=qt4 helps avoid possible conflicts with qt3/qt4
desktop-file-install \
  --dir=%{buildroot}%{_libqt5_datadir}/applications \
  --vendor="qt5" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}

# icons
install -m644 -p -D src/assistant/assistant/images/assistant.png %{buildroot}%{_libqt5_datadir}/icons/hicolor/32x32/apps/assistant-qt5.png
install -m644 -p -D src/assistant/assistant/images/assistant-128.png %{buildroot}%{_libqt5_datadir}/icons/hicolor/128x128/apps/assistant-qt5.png
install -m644 -p -D src/designer/src/designer/images/designer.png %{buildroot}%{_libqt5_datadir}/icons/hicolor/32x32/apps/designer-qt5.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_libqt5_datadir}/icons/hicolor/32x32/apps/qdbusviewer-qt5.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_libqt5_datadir}/icons/hicolor/128x128/apps/qdbusviewer-qt5.png
# linguist icons
for icon in src/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_libqt5_datadir}/icons/hicolor/${size}x${size}/apps/linguist-qt5.png
done

# hardlink files to %{_oc_bindir}
mkdir -p %{buildroot}%{_oc_bindir}
pushd %{buildroot}%{_libqt5_bindir}
for i in * ; do
  case "${i}" in
   assistant|designer|lconvert|linguist|lrelease|lupdate|pixeltool|qcollectiongenerator|qdbus|qdbusviewer|qdoc|qhelpconverter|qhelpgenerator|qtdiag|qtplugininfo|qtpaths)
      ln -v  ${i} %{buildroot}%{_oc_bindir}/${i}
      ;;
    *)
      ;;
  esac
done
popd

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_libqt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%files
# qdbus* matches qdbusviewer which is in a different package
%{_oc_bindir}/qdbus
%{_libqt5_bindir}/qdbus
%{_oc_bindir}/qdoc*
%{_libqt5_bindir}/qdoc
%{_oc_bindir}/qtpaths*
%{_libqt5_bindir}/qtpaths

%files common
%doc LICENSE.LGPL*

%post   libs-clucene -p /sbin/ldconfig
%postun libs-clucene -p /sbin/ldconfig
%files  libs-clucene
%{_libqt5_libdir}/libQt5CLucene.so.5*

%post   libs-designer -p /sbin/ldconfig
%postun libs-designer -p /sbin/ldconfig
%files  libs-designer
%{_libqt5_libdir}/libQt5Designer.so.5*
%dir %{_libqt5_libdir}/cmake/Qt5Designer/

%post   libs-designercomponents -p /sbin/ldconfig
%postun libs-designercomponents -p /sbin/ldconfig
%files  libs-designercomponents
%{_libqt5_libdir}/libQt5DesignerComponents.so.5*

%post   libs-help -p /sbin/ldconfig
%postun libs-help -p /sbin/ldconfig
%files  libs-help
%{_libqt5_libdir}/libQt5Help.so.5*

%post -n @PACKAGE_NAME_PREFIX@-libqt5-assistant
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n @PACKAGE_NAME_PREFIX@-libqt5-assistant
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n @PACKAGE_NAME_PREFIX@-libqt5-assistant
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -n @PACKAGE_NAME_PREFIX@-libqt5-assistant
%{_oc_bindir}/assistant*
%{_libqt5_bindir}/assistant
%dir %{_oc_datadir}
%dir %{_libqt5_datadir}
%dir %{_libqt5_datadir}/applications
%dir %{_libqt5_datadir}/icons/
%dir %{_libqt5_datadir}/icons/hicolor/
%dir %{_libqt5_datadir}/icons/hicolor/128x128
%dir %{_libqt5_datadir}/icons/hicolor/128x128/apps
%dir %{_libqt5_datadir}/icons/hicolor/32x32
%dir %{_libqt5_datadir}/icons/hicolor/32x32/apps

%{_libqt5_datadir}/applications/*assistant.desktop
%{_libqt5_datadir}/icons/hicolor/*/apps/assistant*.*


%post -n @PACKAGE_NAME_PREFIX@-libqt5-designer
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n @PACKAGE_NAME_PREFIX@-libqt5-designer
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun -n @PACKAGE_NAME_PREFIX@-libqt5-designer
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -n @PACKAGE_NAME_PREFIX@-libqt5-designer
%{_oc_bindir}/designer*
%{_libqt5_bindir}/designer
%dir %{_oc_datadir}
%dir %{_libqt5_datadir}
%dir %{_libqt5_datadir}/applications
%dir %{_libqt5_datadir}/icons/
%dir %{_libqt5_datadir}/icons/hicolor/
%dir %{_libqt5_datadir}/icons/hicolor/32x32
%dir %{_libqt5_datadir}/icons/hicolor/32x32/apps
%{_libqt5_datadir}/applications/*designer.desktop
%{_libqt5_datadir}/icons/hicolor/*/apps/designer*.*
%dir %{_libqt5_libdir}/cmake/Qt5Designer/

%dir %{_libqt5_libdir}/qt5/plugins/designer
%{_libqt5_libdir}/qt5/plugins/designer/libcontainerextension.so
%{_libqt5_libdir}/qt5/plugins/designer/libcustomwidgetplugin.so
%{_libqt5_libdir}/qt5/plugins/designer/libtaskmenuextension.so
%{_libqt5_libdir}/qt5/plugins/designer/libworldtimeclockplugin.so
%if ! 0%{?rhel_version}
## CAUTION: dependency from tools to webkit? should not this be the other way round?
## this is why.... sigh.
%{_libqt5_libdir}/qt5/plugins/designer/libqwebview.so
%endif
%{_libqt5_libdir}/cmake/Qt5Designer/Qt5Designer_AnalogClockPlugin.cmake
%{_libqt5_libdir}/cmake/Qt5Designer/Qt5Designer_MultiPageWidgetPlugin.cmake
%{_libqt5_libdir}/cmake/Qt5Designer/Qt5Designer_TicTacToePlugin.cmake
%{_libqt5_libdir}/cmake/Qt5Designer/Qt5Designer_WorldTimeClockPlugin.cmake

%if ! 0%{?rhel_version}
## CAUTION: dependency from tools to webkit? should not this be the other way round?
## this is why.... sigh.
%files -n @PACKAGE_NAME_PREFIX@-libqt5-designer-plugin-webkit
%{_libqt5_libdir}/cmake/Qt5Designer/Qt5Designer_QWebViewPlugin.cmake

%post -n @PACKAGE_NAME_PREFIX@-libqt5-linguist
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n @PACKAGE_NAME_PREFIX@-libqt5-linguist
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun -n @PACKAGE_NAME_PREFIX@-libqt5-linguist
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi
%endif

%files -n @PACKAGE_NAME_PREFIX@-libqt5-linguist
%{_oc_bindir}/linguist*
%{_libqt5_bindir}/linguist
# phrasebooks used by linguist
%{_libqt5_datadir}/phrasebooks/
%dir %{_oc_datadir}
%dir %{_libqt5_datadir}/
%dir %{_libqt5_datadir}/applications
%dir %{_libqt5_datadir}/icons/
%dir %{_libqt5_datadir}/icons/hicolor/
%dir %{_libqt5_datadir}/icons/hicolor/128x128
%dir %{_libqt5_datadir}/icons/hicolor/128x128/apps
%dir %{_libqt5_datadir}/icons/hicolor/16x16
%dir %{_libqt5_datadir}/icons/hicolor/16x16/apps
%dir %{_libqt5_datadir}/icons/hicolor/32x32
%dir %{_libqt5_datadir}/icons/hicolor/32x32/apps
%dir %{_libqt5_datadir}/icons/hicolor/48x48
%dir %{_libqt5_datadir}/icons/hicolor/48x48/apps
%dir %{_libqt5_datadir}/icons/hicolor/64x64
%dir %{_libqt5_datadir}/icons/hicolor/64x64/apps
%{_libqt5_datadir}/applications/*linguist.desktop
%{_libqt5_datadir}/icons/hicolor/*/apps/linguist*.*
# linguist friends
%{_oc_bindir}/lconvert*
%{_libqt5_bindir}/lconvert
%{_oc_bindir}/lrelease*
%{_libqt5_bindir}/lrelease
%{_oc_bindir}/lupdate*
%{_libqt5_bindir}/lupdate
# cmake config
%dir %{_libqt5_libdir}/cmake/Qt5LinguistTools/
%{_libqt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsConfig*.cmake
%{_libqt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsMacros.cmake

%post -n @PACKAGE_NAME_PREFIX@-libqt5-qdbusviewer
touch --no-create %{_libqt5_datadir}/icons/hicolor ||:

%posttrans -n @PACKAGE_NAME_PREFIX@-libqt5-qdbusviewer
gtk-update-icon-cache -q %{_libqt5_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n @PACKAGE_NAME_PREFIX@-libqt5-qdbusviewer
if [ $1 -eq 0 ] ; then
touch --no-create %{_libqt5_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_libqt5_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -n @PACKAGE_NAME_PREFIX@-libqt5-qdbusviewer
%{_oc_bindir}/qdbusviewer*
%{_libqt5_bindir}/qdbusviewer
%dir %{_oc_datadir}
%dir %{_libqt5_datadir}
%dir %{_libqt5_datadir}/applications
%dir %{_libqt5_datadir}/icons/
%dir %{_libqt5_datadir}/icons/hicolor/
%dir %{_libqt5_datadir}/icons/hicolor/128x128
%dir %{_libqt5_datadir}/icons/hicolor/128x128/apps
%dir %{_libqt5_datadir}/icons/hicolor/32x32
%dir %{_libqt5_datadir}/icons/hicolor/32x32/apps
%{_libqt5_datadir}/applications/*qdbusviewer.desktop
%{_libqt5_datadir}/icons/hicolor/*/apps/qdbusviewer*.*

%files -n @PACKAGE_NAME_PREFIX@-libqt5-qhelpgenerator
%{_oc_bindir}/qhelpgenerator*
%{_libqt5_bindir}/qhelpgenerator

%files devel
%{_oc_bindir}/pixeltool*
%{_libqt5_bindir}/pixeltool
%{_oc_bindir}/qcollectiongenerator*
%{_libqt5_bindir}/qcollectiongenerator
%{_oc_bindir}/qhelpconverter*
%{_libqt5_bindir}/qhelpconverter
%{_oc_bindir}/qtdiag*
%{_libqt5_bindir}/qtdiag
%{_oc_bindir}/qtplugininfo*
%{_libqt5_bindir}/qtplugininfo
%{_libqt5_includedir}/QtCLucene/
%{_libqt5_includedir}/QtDesigner/
%{_libqt5_includedir}/QtDesignerComponents/
%{_libqt5_includedir}/QtHelp/
%{_libqt5_includedir}/QtUiPlugin/
%{_libqt5_libdir}/libQt5CLucene.prl
%{_libqt5_libdir}/libQt5CLucene.so
%{_libqt5_libdir}/libQt5Designer*.prl
%{_libqt5_libdir}/libQt5Designer*.so
%{_libqt5_libdir}/libQt5Help.prl
%{_libqt5_libdir}/libQt5Help.so
%{_libqt5_libdir}/cmake/Qt5Designer/Qt5DesignerConfig*.cmake
%dir %{_libqt5_libdir}/cmake/Qt5Help/
%{_libqt5_libdir}/cmake/Qt5Help/Qt5HelpConfig*.cmake
%dir %{_libqt5_libdir}/cmake/Qt5UiPlugin/
%{_libqt5_libdir}/cmake/Qt5UiPlugin/Qt5UiPlugin*.cmake
# %{_libqt5_libdir}/pkgconfig/Qt5CLucene.pc
%{_libqt5_libdir}/pkgconfig/Qt5Designer.pc
# %{_libqt5_libdir}/pkgconfig/Qt5DesignerComponents.pc
%{_libqt5_libdir}/pkgconfig/Qt5Help.pc
%{_libqt5_libdir}/qt5/mkspecs/modules/*.pri

%files static
%{_libqt5_includedir}/QtUiTools/
%{_libqt5_libdir}/libQt5UiTools.*a
%{_libqt5_libdir}/libQt5UiTools.prl
%{_libqt5_libdir}/cmake/Qt5UiTools/
%{_libqt5_libdir}/pkgconfig/Qt5UiTools.pc

%if 0%{?docs}
%files doc
%doc LICENSE.FDL
%{_libqt5_docdir}/qtassistant.qch
%{_libqt5_docdir}/qtassistant/
%{_libqt5_docdir}/qtdesigner.qch
%{_libqt5_docdir}/qtdesigner/
%{_libqt5_docdir}/qthelp.qch
%{_libqt5_docdir}/qthelp/
%{_libqt5_docdir}/qtlinguist.qch
%{_libqt5_docdir}/qtlinguist/
%{_libqt5_docdir}/qtuitools.qch
%{_libqt5_docdir}/qtuitools/
%endif

# %if 0%{?_qt5_examplesdir:1}
%files examples
%{_libqt5_examplesdir}/
# %endif


%changelog
* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Sat Aug 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-4
- qt5-linguist: move lconvert,lrelease,lupdate, cmake Qt5LinguistTools  here

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- de-bootstrap

* Thu Jul 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- qt5-designer, qt5-linguist, qt5-qhelpgenerator subpkgs

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> 5.5.0-1
- New final upstream release Qt 5.5.0

* Mon Jun 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.4.rc
- Second round of builds now with bootstrap enabled due new qttools

* Sat Jun 27 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.3.rc
- Disable bootstrap

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Mon Jun 15 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-3
- rebuild (gcc5)

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.0-2
- rebuild (gcc5)

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Tue Dec 09 2014 Daniel Vrátil <dvratil@redhat.com> 5.4.0-0.10.rc
- fix icon name in qdbusviewer-qt5.desktop

* Sun Nov 30 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.9.rc
- install Linguist icon as linguist-qt5.png, fixes file conflict (#1169127)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.8.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.7.beta
- out-of-tree build, use %%qmake_qt5

* Fri Oct 31 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.6.beta
- respin system-clucene.patch

* Sun Oct 26 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.5.beta
- system-clucene patch: create path recursively in QtCLucene, CLucene can't

* Sun Oct 26 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.4.beta
- disable bootstrap (reenable -doc)
- system-clucene patch: drop -fpermissive flag
- system-clucene patch: use toLocal8Bit instead of toStdString
- system_clucene: BR clucene09-core-devel >= 0.9.21b-12 (-11 was broken)

* Sat Oct 25 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.4.0-0.3.beta
- libQt5Designer should be in a subpackage (#1156685)
- -doc: disable(boostrap for new clucene), drop dep on main pkg

* Sat Oct 25 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.2.beta
- BR and rebuild against reference-counting-enabled clucene09 (#1128293)

* Sat Oct 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Fri Oct 17 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-2
- -devel: Requires: qt5-designer-plugin-webkit

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.3.0-2
- restore system-clucene patch, rm the bundled copy

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- -examples subpkg

* Tue Jan 14 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- epel7 bootstrapped

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1
- enable -doc only on primary archs (allow secondary bootstrap)

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Tue Oct 01 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-6
- lupdate can't find qmake configuration file default (#1009893)

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-4
- use upstream cmake fix(es) (QTBUG-32570, #1006254)

* Wed Sep 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-3
- wrong path to lrelease (#1006254)
- %%check: first try

* Tue Sep 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- ExclusiveArch: %{ix86} x86_64 %{arm}
- epel-6 love

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- qttools-5.1.1
- qt5-assistant, qt5-qdbusviewer, qt5-designer-plugin-webkit subpkgs (to match qt4)

* Mon Aug 19 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- use system clucene09-core

* Mon Apr 29 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- drop deprecated Encoding= key from .desktop files
- add justification for desktop vendor usage

* Fri Apr 19 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- add .desktop/icons for assistant, designer, linguist, qdbusviewer

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-2
- BR: pkgconfig(zlib)
- -static subpkg

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

