TARNAME="testpilotcloudclient-2.3.2git.tar.bz2"
TARTOPDIR="testpilotcloudclient-2.3.2git"
VERSION="2.3.2git"
BASEVERSION="2.3.2"
PRERELEASE="git"
THEME="testpilotcloud"
SUMMARY="The ownCloud TestPilot client"
PKGDESCRIPTION="The ownCloud TestPilot client is for testing only.\nIt does not conflict with your production ownCloud client.\n\nThe testpilot client can be installed in parallel to a stable production sync client."
PKGDESCRIPTION_DEBIAN="The ownCloud TestPilot client is for testing only. It does not conflict with your production ownCloud client."
SYSCONFDIR="etc/testpilotcloud"
MAINTAINER="ownCloud Inc."
MAINTAINER_PERSON="Jürgen Weigert <jw@owncloud.com>"
DESKTOPDESCRIPTION="ownCloud TestPilot client"
APPLICATION_SHORTNAME="testpilotcloud"
APPLICATION_NAME="ownCloud Testpilot Edition"
APPLICATION_EXECUTABLE=${APPLICATION_SHORTNAME}
APPLICATION_DOMAIN="owncloud.org"
APPLICATION_VENDOR="ownCloud GmbH"
APPLICATION_REV_DOMAIN="owncloud.desktop.testpilotclient"
THEME_CLASS="TestpilotCloudTheme"
THEME_INCLUDE="${OEM_THEME_DIR}/testpilotcloudtheme.h"
WIN_SETUP_BITMAP_PATH="${OEM_THEME_DIR}/installer/nsi"
APPLICATION_UPDATE_URL="https://updates.owncloud.com/client/"
MAC_INSTALLER_BACKGROUND_FILE="${OEM_THEME_DIR}/installer/osx/background.png"
COMPILE_HINT="cd src; cmake -DOEM_THEME_DIR=\/home/src/github/owncloud/administration/jenkins/obs_integration/genbranding/../testpilotcloud/syncclient"
_oc_pkg_name_client="owncloud-client"
_oc_client_executable="owncloud"
_oc_pkg_prefix="oc"
_oc_vendordir="ownCloud"
_oc_rootdir="Qt-5.6.2"
_oc_prefix="/opt/ownCloud/Qt-5.6.2"
BUILD_NUMBER="666"
PACKAGE_NAME_PREFIX="oc"
