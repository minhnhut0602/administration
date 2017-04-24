Format: 1.0
Source: @PACKAGE_NAME_PREFIX@-qt5keychain
Version: 0.7.0-1
Binary: @PACKAGE_NAME_PREFIX@-libqt5keychain1
Maintainer: Klaas Freitag <freitag@owncloud.com> 
Architecture: any
Build-Depends: debhelper (>= 4.2.21),
    cmake,
    @PACKAGE_NAME_PREFIX@-qtbase5-dev,
    @PACKAGE_NAME_PREFIX@-qttools5-dev,
    @PACKAGE_NAME_PREFIX@-qttools5-dev-tools,
    lintian-obs-permissive
Package-List:
 @PACKAGE_NAME_PREFIX@-libqt5keychain1 deb libs optional arch=any
 @PACKAGE_NAME_PREFIX@-qt5keychain-dbg deb debug extra arch=any
 @PACKAGE_NAME_PREFIX@-qt5keychain-dev deb libdevel optional arch=any
    
# https://github.com/openSUSE/obs-build/pull/147
DEBTRANSFORM-RELEASE: 1
