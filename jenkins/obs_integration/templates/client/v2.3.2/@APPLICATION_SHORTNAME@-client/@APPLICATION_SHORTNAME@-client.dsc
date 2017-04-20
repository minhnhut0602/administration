Format: 1.0
# CAUTION: Keep in sync with genbranding.pl:addDebChangelog(...)
Source: @APPLICATION_SHORTNAME@-client
Version: 2.3.1-1
Binary: @APPLICATION_SHORTNAME@-client
# According to debian lintian, maintainer must include a <email@example.com>
Maintainer: Jürgen Weigert <jw@owncloud.com>
Architecture: any
Standards-Version: 3.9.6
# we need qt5 >= 5.5.1 https://github.com/owncloud/client/issues/5432
# Reverted according to https://github.com/owncloud/client/issues/5470#issuecomment-275680311
Build-Depends: debhelper (>= 9), cmake, sed, doxygen, unzip | bash,
	libsqlite3-dev, python-sphinx | python3-sphinx, libssl-dev,
	@PACKAGE_NAME_PREFIX@-qt5-qmake,
	@PACKAGE_NAME_PREFIX@-qtbase5-dev,
	@PACKAGE_NAME_PREFIX@-qt5keychain-dev (>= 0.7.0),
    @PACKAGE_NAME_PREFIX@-libqt5webkit5-dev (>= 2.2.0)

Package-List:
 @PACKAGE_NAME_PREFIX@-lib@APPLICATION_EXECUTABLE@sync0 deb libs optional
 @APPLICATION_SHORTNAME@-client deb net optional
 @APPLICATION_SHORTNAME@-client-doc deb doc optional
 @APPLICATION_SHORTNAME@-client-l10n deb localization optional
# https://github.com/openSUSE/obs-build/pull/147
DEBTRANSFORM-RELEASE: 1
