Format: 1.0
Source: @PACKAGE_NAME_PREFIX@-qt5-qtwebkit
Binary: @PACKAGE_NAME_PREFIX@-libqt5webkit5 @PACKAGE_NAME_PREFIX@-libqt5webkit5-dev
Architecture: any all
Version: 5.6.2-1
Maintainer: Juergen Weigert <jw@owncloud.com>
Homepage: http://qt-project.org/
Standards-Version: 3.9.5
Build-Depends: debhelper (>= 9), lintian-obs-permissive,
	flex, libpng-dev,
    bison,
    gperf,
    python-minimal,
    python2.7,
    ruby,
    libicu-dev,
    libsqlite3-dev,
    libxml2-dev,
    mesa-common-dev,
    libgl1-mesa-dev [!armel !armhf] | libgl-dev [!armel !armhf],
    libgles2-mesa-dev [armel armhf] | libgles2-dev [armel armhf],
    libglib2.0-dev,
    libglu1-mesa-dev [!armel !armhf] | libglu-dev [!armel !armhf],
    libxrender-dev,
    libxslt1-dev,
    @PACKAGE_NAME_PREFIX@-qt5-default,
    @PACKAGE_NAME_PREFIX@-qtbase5-private-dev,
    @PACKAGE_NAME_PREFIX@-libqt5opengl5-dev,
    pkg-config,
    pkg-kde-tools (>= 0.6.4),
    chrpath,
    libjpeg-dev,
    libfontconfig1-dev

Package-List:
 @PACKAGE_NAME_PREFIX@-libqt5webkit5 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-libqt5webkit5-dev deb libdevel optional arch=any
