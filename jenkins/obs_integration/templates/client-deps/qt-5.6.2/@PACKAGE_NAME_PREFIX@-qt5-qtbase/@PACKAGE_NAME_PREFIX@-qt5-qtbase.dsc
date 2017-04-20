Format: 1.0
Source: qt5-qtbase
# CAUTION: Keep the list below in sync with the pkgs_oc_prefix list in debian.rules.in
Binary: @PACKAGE_NAME_PREFIX@-libqt5core5a,
	@PACKAGE_NAME_PREFIX@-libqt5gui5,
	@PACKAGE_NAME_PREFIX@-libqt5libqgtk2,
	@PACKAGE_NAME_PREFIX@-libqt5network5,
	@PACKAGE_NAME_PREFIX@-libqt5opengl5,
	@PACKAGE_NAME_PREFIX@-libqt5sql5,
	@PACKAGE_NAME_PREFIX@-libqt5sql5-mysql,
	@PACKAGE_NAME_PREFIX@-libqt5sql5-odbc,
	@PACKAGE_NAME_PREFIX@-libqt5sql5-psql,
	@PACKAGE_NAME_PREFIX@-libqt5sql5-sqlite,
	@PACKAGE_NAME_PREFIX@-libqt5sql5-tds,
	@PACKAGE_NAME_PREFIX@-libqt5xml5,
	@PACKAGE_NAME_PREFIX@-libqt5dbus5,
	@PACKAGE_NAME_PREFIX@-libqt5test5,
	@PACKAGE_NAME_PREFIX@-libqt5concurrent5,
	@PACKAGE_NAME_PREFIX@-libqt5widgets5,
	@PACKAGE_NAME_PREFIX@-libqt5printsupport5,
	@PACKAGE_NAME_PREFIX@-qtbase5-dev,
	@PACKAGE_NAME_PREFIX@-qtbase5-private-dev,
	@PACKAGE_NAME_PREFIX@-libqt5opengl5-dev,
	@PACKAGE_NAME_PREFIX@-qtbase5-dev-tools,
	@PACKAGE_NAME_PREFIX@-qt5-qmake,
	@PACKAGE_NAME_PREFIX@-qtbase5-examples,
	@PACKAGE_NAME_PREFIX@-qtbase5-dbg,
	@PACKAGE_NAME_PREFIX@-qtbase5-dev-tools-dbg,
	@PACKAGE_NAME_PREFIX@-qtbase5-examples-dbg,
	@PACKAGE_NAME_PREFIX@-qt5-default
Architecture: any all
Version: 5.6.2-1
Maintainer: Juergen Weigert <jw@owncloud.com>
Homepage: http://qt-project.org/
Standards-Version: 3.9.5
Vcs-Browser: https://anonscm.debian.org/cgit/pkg-kde/qt/qtbase.git
Vcs-Git: https://anonscm.debian.org/git/pkg-kde/qt/qtbase.git
Build-Depends: debhelper (>= 9), dpkg-dev (>= 1.16.1), freetds-dev, gdb,
  libasound2-dev [linux-any], libatspi2.0-dev, libcups2-dev, libdbus-1-dev,
  libfontconfig1-dev, libfreetype6-dev, libgbm-dev [linux-any kfreebsd-any],
  libgl1-mesa-dev | libgl-dev, libgles2-mesa-dev | libgles2-dev, libglib2.0-dev,
  libglu1-mesa-dev | libglu-dev, libjpeg-dev, libgtk2.0-dev, libicu-dev, libmtdev-dev [linux-any],
  default-libmysqlclient-dev | libmysqlclient-dev, libpcre3-dev, libpng-dev, libpq-dev, libproxy-dev,
  libpulse-dev, libsqlite3-dev, libssl-dev, libudev-dev [linux-any], libx11-dev,
  libx11-xcb-dev, libxcb-icccm4-dev, libxcb-image0-dev, libxcb-keysyms1-dev,
  libxcb-randr0-dev, libxcb-render-util0-dev, libxcb-render0-dev,
  libxcb-shape0-dev, libxcb-shm0-dev, libxcb-xfixes0-dev, libxcb-xinerama0-dev,
  libxcb1-dev, libxext-dev, libxi-dev, libxrender-dev, unixodbc-dev, xvfb, xauth,
  zlib1g-dev, publicsuffix, lintian-obs-permissive,
  libgstreamer-plugins-base1.0-dev | libgstreamer-plugins-base0.10-dev,
  libgstreamer1.0-dev | libgstreamer0.10-dev,
  libxcb-sync-dev | libxcb-sync0-dev,
  libxcb-xkb-dev | bash,
  libxkbcommon-dev | bash,
  libxkbcommon-x11-dev | bash,
  pkg-kde-tools (>= 0.15.12) | pkg-kde-tools (>= 0.15.3)
# Build-Conflicts: libmariadbclient-dev
Package-List:
 @PACKAGE_NAME_PREFIX@-libqt5concurrent5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5core5a deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5dbus5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5gui5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5libqgtk2 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5network5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5opengl5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5opengl5-dev deb libdevel optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5printsupport5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5sql5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5sql5-mysql deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5sql5-odbc deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5sql5-psql deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5sql5-sqlite deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5sql5-tds deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5test5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5widgets5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5xml5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-qt5-default deb libdevel optional arch=any
 @PACKAGE_NAME_PREFIX@-qt5-qmake deb devel optional arch=any
 @PACKAGE_NAME_PREFIX@-qtbase5-dbg deb debug extra arch=any
 @PACKAGE_NAME_PREFIX@-qtbase5-dev deb libdevel optional arch=any
 @PACKAGE_NAME_PREFIX@-qtbase5-dev-tools deb devel optional arch=any
 @PACKAGE_NAME_PREFIX@-qtbase5-dev-tools-dbg deb debug extra arch=any
 @PACKAGE_NAME_PREFIX@-qtbase5-examples deb x11 optional arch=any
 @PACKAGE_NAME_PREFIX@-qtbase5-examples-dbg deb debug extra arch=any
 @PACKAGE_NAME_PREFIX@-qtbase5-private-dev deb libdevel optional arch=any
# https://github.com/openSUSE/obs-build/pull/147
DEBTRANSFORM-RELEASE: 1

