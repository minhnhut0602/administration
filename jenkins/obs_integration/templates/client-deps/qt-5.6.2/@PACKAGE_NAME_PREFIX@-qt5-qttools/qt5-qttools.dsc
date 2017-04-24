Format: 1.0
Source: qt5-qttools
Binary: @PACKAGE_NAME_PREFIX@-libqt5clucene5, @PACKAGE_NAME_PREFIX@-libqt5designer5, @PACKAGE_NAME_PREFIX@-libqt5designercomponents5, @PACKAGE_NAME_PREFIX@-qdbus-qt5, @PACKAGE_NAME_PREFIX@-libqt5help5, @PACKAGE_NAME_PREFIX@-qttools5-dev, @PACKAGE_NAME_PREFIX@-qttools5-private-dev, @PACKAGE_NAME_PREFIX@-qttools5-dev-tools, @PACKAGE_NAME_PREFIX@-qttools5-examples, @PACKAGE_NAME_PREFIX@-qttools5-dbg, @PACKAGE_NAME_PREFIX@-qttools5-examples-dbg
Architecture: any all
Version: 5.6.2-1
Maintainer: Juergen Weigert <jw@owncloud.com>
Homepage: http://qt-project.org/
Standards-Version: 3.9.8
Vcs-Browser: https://anonscm.debian.org/cgit/pkg-kde/qt/qttools.git
Vcs-Git: https://anonscm.debian.org/git/pkg-kde/qt/qttools.git
Build-Depends: debhelper (>= 9), lintian-obs-permissive,
	pkg-kde-tools,
	@PACKAGE_NAME_PREFIX@-qt5-qmake,
	@PACKAGE_NAME_PREFIX@-libqt5core5a,
	@PACKAGE_NAME_PREFIX@-libqt5sql5,
	@PACKAGE_NAME_PREFIX@-libqt5xml5,
	@PACKAGE_NAME_PREFIX@-libqt5concurrent5,
	@PACKAGE_NAME_PREFIX@-libqt5dbus5,
	@PACKAGE_NAME_PREFIX@-libqt5test5,
	@PACKAGE_NAME_PREFIX@-qtbase5-private-dev, 
	@PACKAGE_NAME_PREFIX@-libqt5network5,
	@PACKAGE_NAME_PREFIX@-libqt5gui5,
	@PACKAGE_NAME_PREFIX@-libqt5widgets5,
	@PACKAGE_NAME_PREFIX@-libqt5printsupport5,
	@PACKAGE_NAME_PREFIX@-qtbase5-examples,
    zlib1g-dev
#	libdouble-conversion-dev,
Package-List:
 @PACKAGE_NAME_PREFIX@-libqt5clucene5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5designer5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5designercomponents5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5help5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-qdbus-qt5 deb utils optional arch=any
 @PACKAGE_NAME_PREFIX@-qttools5-dbg deb debug extra arch=any
 @PACKAGE_NAME_PREFIX@-qttools5-dev deb libdevel optional arch=any
 @PACKAGE_NAME_PREFIX@-qttools5-dev-tools deb devel optional arch=any
 @PACKAGE_NAME_PREFIX@-qttools5-examples deb x11 optional arch=any
 @PACKAGE_NAME_PREFIX@-qttools5-examples-dbg deb debug extra arch=any
 @PACKAGE_NAME_PREFIX@-qttools5-private-dev deb libdevel optional arch=any
