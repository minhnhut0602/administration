%global _oc_prefix @OC_QT_ROOT@
%global _oc_bindir %{_oc_prefix}/bin
%global _oc_libdir %{_oc_prefix}/%{_lib}
%global _oc_includedir %{_oc_prefix}/include


Name:           @PACKAGE_NAME_PREFIX@-filesystem
Version:        0
Release:        0
Summary:        oc filesystem and environment
License:        GPL-2.0+
Group:          Development/Libraries
Source1:        macros.oc
Source4:        oc-find-requires.sh
Source5:        oc-find-provides.sh
Requires:       rpm
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#!BuildIgnore: post-build-checks

%description
This package contains the base filesystem layout, RPM macros and
environment for all oc branded packages.

%prep

%build

%install
mkdir -p %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rpm
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.%{_oc_pkg_prefix}

mkdir -p %{buildroot}%{_libexecdir}/rpm
install -m 0755 %{SOURCE4} %{buildroot}%{_libexecdir}/rpm/%{_oc_pkg_prefix}-find-requires.sh
install -m 0755 %{SOURCE5} %{buildroot}%{_libexecdir}/rpm/%{_oc_pkg_prefix}-find-provides.sh

mkdir -p %{buildroot}%{_oc_prefix}
mkdir %{buildroot}%{_oc_bindir}
mkdir %{buildroot}%{_oc_includedir}
mkdir %{buildroot}%{_oc_libdir}
mkdir %{buildroot}%{_oc_libdir}/pkgconfig


# spit out all the subdirs one after another.
dirparts () {
	prefix=$1
	path=$2
	while [ "$path" != '/' -a "$path" != '.' ]; do
		echo $prefix$path
		path=$(dirname $path)
	done | tac
}

dirparts >  files.list '%dir ' /opt/@VENDOR@/@APPLICATION_SHORTNAME@
dirparts >> files.list '%dir ' %{_oc_prefix}


%files -f files.list
%defattr(-,root,root,-)
%config %{_sysconfdir}/rpm/macros.%{_oc_pkg_prefix}
# %config %{_sysconfdir}/rpmlint/oc-rpmlint.config
%{_libexecdir}/rpm/%{_oc_pkg_prefix}-*

%dir %{_oc_bindir}
%dir %{_oc_includedir}
%dir %{_oc_libdir}
%dir %{_oc_libdir}/pkgconfig

%changelog
