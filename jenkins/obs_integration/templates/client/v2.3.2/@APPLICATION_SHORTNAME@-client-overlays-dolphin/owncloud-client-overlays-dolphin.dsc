Format: 1.0
# CAUTION: Keep in sync with genbranding.pl:addDebChangelog(...)
Source: owncloud-client-overlays-dolphin
Version: 2.3.0~beta1-1
Binary: owncloud-client-overlays-dolphin
# According to debian lintian, maintainer must include a <email@example.com>
Maintainer: Jürgen Weigert <jw@owncloud.com>
Architecture: any
Standards-Version: 3.9.6
Build-Depends: debhelper (>= 9), cmake,
    extra-cmake-modules,
    kio-dev,
    libfam0,
    qtbase5-dev

Package-List:
 owncloud-client-dolphin deb net optional

# https://github.com/openSUSE/obs-build/pull/147
DEBTRANSFORM-RELEASE: 1
