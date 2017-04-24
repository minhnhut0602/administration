#
# obsoleted by setup_client_obs.sh

themetar=testpilotcloud.tar.xz
# themetar=jwfablabnbg.tar.xz
# themetar=ownCloud.tar.xz

sh prepare_tarball.sh testdata/owncloudclient-2.3.2git.tar.bz2 testdata/customer-themes/$themetar testdata/tp_tmplvars.sh
# Please deprecate use of prjconf variables
sh fetch_prjconf_vars.sh isv:ownCloud:devel:Qt562 >> testdata/tp_tmplvars.sh

test -z "${BUILD_NUMBER}" && BUILD_NUMBER=$(date +%y%m%d)	# default when not running in jenkins

. testdata/tp_tmplvars.sh
# Escape the $-interpolation expansions here. We could expand some of the variables here, 
# but not all. Later expansion is safer.
cat <<EOF >> testdata/tp_tmplvars.sh
BUILD_NUMBER="${BUILD_NUMBER}"
VENDOR="ownCloud"
PACKAGE_NAME_PREFIX="ocqt562"
OC_QT_VERSION="5.6.2"
OC_QT_ROOT="/opt/\${VENDOR}/qt-\${OC_QT_VERSION}"
CLIENT_ROOT="/opt/\${VENDOR}/\${APPLICATION_SHORTNAME}"
EOF

sh prepare_package.sh ../templates/client/v$BASEVERSION out testdata/tp_tmplvars.sh

