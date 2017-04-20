%include %{_sourcedir}/common.inc

%if 0%{?centos_version} == 600 || 0%{?rhel_version} == 600 || 0%{?fedora_version} || "%{prerelease}" == ""
# For beta and rc versions we use the ~ notation, as documented in
# http://en.opensuse.org/openSUSE:Package_naming_guidelines
# Some distro's (centos_6) don't allow ~ characters. There we follow the Fedora guidelines,
# which suggests massaging the buildrelease number.
# Otoh: for openSUSE, this technique is discouraged by the package naming guidelines.
Version:       	%{base_version}
%if "%{prerelease}" == ""
Release:        0
%else
Release:       	0.<CI_CNT>.<B_CNT>.%{prerelease}
%endif
%else
Version:       	%{base_version}~%{prerelease}
Release:        0
%endif

%define build_dolphin_overlays 0
%if 0%{?suse_version} || 0%{?fedora_version} > 20 || 0%{?rhel_version} >= 700 || 0%{?centos_version} >= 700
  # On top of the Qt5 requirement, Dolphin plugin interface can only work on distros with KDE Applications >= 15.12
  # This we make sure to allow building not for OpenSUSE Leap 42.1 GA, not for 13.2
  # Leap_Updates would allow a dolphin overlay to work, this is not handled below.
  %if 0%{?suse_version} == 1315 || 0%{?suse_version} > 1320 || 0%{?fedora_version} > 23
    # 1315 is 42.x, 120100 is 42.1
    %if 0%{?sle_version} != 120100 && (!0%{?suse_version} || 0%{?is_opensuse})
      %define build_dolphin_overlays 1
    %endif
  %endif
  %if "%_repository" == "openSUSE_Leap_42.1_Update"
    # It builds the overlay, despite this warning: Dolphin plugin disabled: KDE Frameworks 5.16 not found
    %define build_dolphin_overlays 1
  %endif
%endif


%define cmake_args %nil

Name:           @APPLICATION_SHORTNAME@-client-overlays
License:        GPL-2.0+
Summary:        @SUMMARY@ - overlay icons
Url:            @PROJECTURL@
Group:          Productivity/Networking/Other
Source0:        @TARNAME@

BuildRequires:  cmake >= 2.8.11
BuildRequires:  gcc gcc-c++

%if %build_dolphin_overlays
BuildRequires:  extra-cmake-modules
%if 0%{?suse_version}
BuildRequires:  kio-devel
%else
BuildRequires:  kf5-kio-devel
%endif
%else
%global debug_package %{nil}
%endif

%description
@PKGDESCRIPTION@ - overlay icons. Meta-package.

%package -n @APPLICATION_SHORTNAME@-client-overlays-icons
Summary:        Dolphin overlay icons
Group:          Productivity/Networking/Other
# TODO:
# Requires:       %%{name}%{?_isa} = %{version}-%{release}

%description -n @APPLICATION_SHORTNAME@-client-overlays-icons
This package provides the icons for the file manager display overlays.

%if %build_dolphin_overlays
%package -n @APPLICATION_SHORTNAME@-client-dolphin
Summary:        Dolphin overlay icons
Group:          Productivity/Networking/Other
Requires:       @APPLICATION_SHORTNAME@-client-overlays-icons
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
Requires:       dolphin
%else
Requires:       dolphin
%endif
# TODO:
# Requires:       %%{name}%{?_isa} = %{version}-%{release}

%description -n @APPLICATION_SHORTNAME@-client-dolphin
This package provides the neccessary plugin libraries for the KDE
Framework 5 based Dolphin filemanager to display overlay icons.
%endif

%package -n @APPLICATION_SHORTNAME@-client-nautilus
Summary:        Nautilus overlay icons
Group:          Productivity/Networking/Other
Requires:       @APPLICATION_SHORTNAME@-client-overlays-icons
Requires:       nautilus
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
Requires:       nautilus-python
%else
Requires:       python-nautilus
%endif
# Requires:       %%{name}%{?_isa} = %{version}-%{release}
Obsoletes:      opt-@APPLICATION_SHORTNAME@-client-nautilus

%description -n @APPLICATION_SHORTNAME@-client-nautilus
This package provides overlay icons to visualize the synchronization state
in the Nautilus file manager.

%package -n @APPLICATION_SHORTNAME@-client-nemo
Summary:        Nemo overlay icons
Group:          Productivity/Networking/Other
Requires:       @APPLICATION_SHORTNAME@-client-overlays-icons
Requires:       nemo
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
Requires:       nemo-python
%else
Requires:       python-nemo
%endif
# Requires:       %%{name}%{?_isa} = %{version}-%{release}
Obsoletes:      opt-@APPLICATION_SHORTNAME@-client-nemo

%description -n @APPLICATION_SHORTNAME@-client-nemo
This package provides overlay icons to visualize the synchronization state
in the Nemo file manager.

%package -n @APPLICATION_SHORTNAME@-client-caja
Summary:        Caja overlay icons
Group:          Productivity/Networking/Other
Requires:       @APPLICATION_SHORTNAME@-client-overlays-icons
Requires:       caja
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
Requires:       caja-python
%else
Requires:       python-caja
%endif
# Requires:       %%{name}%{?_isa} = %{version}-%{release}
Obsoletes:      opt-@APPLICATION_SHORTNAME@-client-caja

%description -n @APPLICATION_SHORTNAME@-client-caja
This package provides overlay icons to visualize the synchronization state
in the Caja file manager.

%prep
%setup -q -n @TARTOPDIR@

%_oc_client_apply_common_patches

%build
echo centos_version 0%{?centos_version}
echo rhel_version   0%{?rhel_version}
echo fedora_version 0%{?fedora_version}
echo suse_version   0%{?suse_version}
echo have_doc       0%{?have_doc}


mkdir build
pushd build
# http://www.cmake.org/Wiki/CMake_RPATH_handling#Default_RPATH_settings
cmake .. \
%if "%{prerelease}" != ""
  -DMIRALL_VERSION_SUFFIX="%{prerelease}" \
  -DMIRALL_VERSION_BUILD="@BUILD_NUMBER@" \
%endif
  -DKDE_INSTALL_USE_QT_SYS_PATHS=1 \
  -DCMAKE_C_FLAGS:STRING="%{optflags}" \
  -DCMAKE_CXX_FLAGS:STRING="%{optflags}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if %{_lib} == lib64
  -DLIB_SUFFIX=64 \
%endif
%if ! %{is_owncloud_client}
  -DOEM_THEME_DIR=$PWD/../@THEME@/@OEM_SUB_DIR@ \
%endif
  -DGIT_SHA1="HACK FIXME" \
  -DBUILD_CLIENT=OFF \
  %cmake_args


%install
pushd build
%make_install

%files -n @APPLICATION_SHORTNAME@-client-overlays-icons
%defattr(-,root,root,-)
%{_datadir}/icons/hicolor

%files -n @APPLICATION_SHORTNAME@-client-nautilus
%defattr(-,root,root,-)
# Fedora also has *.pyc and *.pyo files here.
%{_datadir}/nautilus-python/extensions/syncstate*.py*
%dir %{_datadir}/nautilus-python
%dir %{_datadir}/nautilus-python/extensions/

%files -n @APPLICATION_SHORTNAME@-client-nemo
%defattr(-,root,root,-)
# # # Fedora also has *.pyc and *.pyo files here.
%{_datadir}/nemo-python/extensions/syncstate*.py*
%dir %{_datadir}/nemo-python
%dir %{_datadir}/nemo-python/extensions/

%files -n @APPLICATION_SHORTNAME@-client-caja
%defattr(-,root,root,-)
# # # Fedora also has *.pyc and *.pyo files here.
%{_datadir}/caja-python/extensions/syncstate*.py*
%dir %{_datadir}/caja-python
%dir %{_datadir}/caja-python/extensions/

%if %build_dolphin_overlays
%files -n @APPLICATION_SHORTNAME@-client-dolphin
%defattr(-,root,root,-)
%{_libdir}/*dolphinpluginhelper.so
%{_libdir}/qt5/plugins/kf5/overlayicon/*dolphinoverlayplugin.so
%{_libdir}/qt5/plugins/*dolphinactionplugin.so

%{_datadir}/kservices5/*dolphinactionplugin.desktop
%dir %{_libdir}/qt5/plugins/kf5/overlayicon
%endif
