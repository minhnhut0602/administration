Format: 1.0
# CAUTION: Keep in sync with genbranding.pl:addDebChangelog(...)
Source: owncloud-client-overlays
Version: 2.3.0~beta1-1
Binary: owncloud-client
# According to debian lintian, maintainer must include a <email@example.com>
Maintainer: Jürgen Weigert <jw@owncloud.com>
Architecture: any
Standards-Version: 3.9.6
Build-Depends: debhelper (>= 9), cmake


Package-List:
 owncloud-client-overlays-icons deb net optional
 owncloud-client-caja deb net optional
 owncloud-client-nautilus deb net optional
 owncloud-client-nemo deb net optional

# https://github.com/openSUSE/obs-build/pull/147
DEBTRANSFORM-RELEASE: 1
