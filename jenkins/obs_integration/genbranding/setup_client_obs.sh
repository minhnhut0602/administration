#! /bin/sh
#
# setup_client_obs.sh -- prepare an entire build project in obs for building (a branded) ownCloud client.
#
# Procedure:
# * combine a client tar and a branding tar producing the clientsourcetar and a tmplvars.sh list.
# * browse through the client-dep templates and either
#   a) create dependency source packages  or
#   b) aggregatepac depdencency source packages.
# * aggregatepac all client-deps packages.
# * co; addremove; ci
# * setup_build_targets.pl
#
# --------------------------
# 2017-04-24, jw@owncloud.com 
# v1.0 		fully functional, except argument parser and not calling setup_build_targets.pl
# --------------------------

_version_='1.0'

obs_api=https://api.opensuse.org
osc_cmd=osc

basename_av0=$(basename $0)
dirname_av0=$(dirname $0)
template_root=$dirname_av0/../templates/
tmpdir=tmp

## NONE (or empty) for rebuilding all client-deps packages from source
# aggregatepac_prj=NONE
##
aggregatepac_prj=isv:ownCloud:devel:Qt562:templatized

client_src_tar=owncloud-client/owncloudclient-2.3.2git.tar.bz2
branding_src_tar=customer-themes/testpilotcloud.tar.xz
client_dest_prj=home:jnweiger:octest
targets_64=ubuntu_16.10,ubuntu_16.04,ubuntu_14.04,debian_7.0,debian_8.0,centos_6,centos_7,fedora_24,fedora_25,opensuse_13.1,opensuse_13.2,opensuse_leap_42.1
targets_32=ubuntu_14.04,debian_7.0,centos_6
client_deps_list="cmake devtoolset-4-centos6-i386 devtoolset-4-centos6-x86-64 devtoolset-4-centos7-x86-64 devtoolset-4-rhel6-i386 devtoolset-4-rhel6-x86-64 devtoolset-4-rhel7-x86-64 gperf libdouble-conversion1 libicu lintian-obs-permissive ocqt562-filesystem ocqt562-qt5-qtbase ocqt562-qt5-qttools ocqt562-qt5-qtwebkit ocqt562-qt5keychain publicsuffix"

test -n "$1" && client_src_tar=$1
test -n "$2" && branding_src_tar=$2
test -n "$3" && client_dest_prj=$3
test -n "$4" && targets_64=$4
test -n "$5" && targets_32=$5

test -z "${BUILD_NUMBER}" && BUILD_NUMBER=$(date +%y%m%d)	# default when not running in jenkins
test -n "${OBS_API}" && obs_api=${OBS_API}
test -n "${OSC_CMD}" && osc_cmd=${OSC_CMD}
test -n "${AGGREGATEPAC_PRJ}" && aggregatepac_prj=${AGGREGATEPAC_PRJ}

osc="$osc_cmd -A$obs_api"

if [ "$aggregatepac_prj" = "NONE" -o "$aggregatepac_prj" = "" ]; then
	# some client-deps packages are in $template_root/client/qt-5.6.3/, some are not. 
	echo "$0: building client-deps from source not impl. Try setting AGGREGATEPAC_PRJ"
	exit 1
fi


rm -rf $tmpdir/co $tmpdir/new $tmpdir/tmplvars.sh
mkdir -p $tmpdir/new
mkdir -p $tmpdir/co
sh $dirname_av0/prepare_tarball.sh $client_src_tar $branding_src_tar $tmpdir/tmplvars.sh

. $tmpdir/tmplvars.sh

cat <<EOF >> $tmpdir/tmplvars.sh
BUILD_NUMBER="${BUILD_NUMBER}"
VENDOR="ownCloud"
PACKAGE_NAME_PREFIX="ocqt562"
OC_QT_VERSION="5.6.2"
OC_QT_ROOT="/opt/\${VENDOR}/qt-\${OC_QT_VERSION}"
CLIENT_ROOT="/opt/\${VENDOR}/\${APPLICATION_SHORTNAME}"
EOF

# Caution: only bash understands 'nullglob'
bash $dirname_av0/prepare_package.sh ${template_root}/client/v$BASEVERSION $tmpdir/new $tmpdir/tmplvars.sh
rm -f $tmpdir/${TARNAME}	# is now populated into $tmptdir/new/*/

## get list of existing packages
# Assert project $client_dest_prj exists.
# FIXME: we use the aggregatepac_prj as a template here. This does not work if aggregatepac_prj=NONE.
$osc meta prj $aggregatepac_prj | sed -e "s@project name=\"[^\"]*\"@project name=\"$client_dest_prj\"@" | $osc meta prj $client_dest_prj -F -
# both meta prj and meta prjconf are needed for a correct setup
$osc meta prjconf $aggregatepac_prj | $osc meta prjconf $client_dest_prj -F -
existing_pkg_list=$($osc ls $client_dest_prj)
# existing_pkg_list="foobar cmake ocqt562-filesystem blarf libicu"	# dummy for testing

## remove excessive packages
# build list of source packages. We also toss the aggregates $client_deps_list, to make sure 
# their _aggregate file is up to date. obs does not log this.
pkg_checklist=" $(ls $tmpdir/new | tr '\n' ' ') "
echo "pkg_checklist='$pkg_checklist'"
for pkg in $existing_pkg_list; do
	echo "$pkg_checklist" | grep -q " $pkg " && continue
	echo "  - $client_dest_prj $pkg"
	$osc rdelete $client_dest_prj $pkg -m "Gone in v$VERSION"
done

## aggregate the dependencies
# if it already existed: We get either a collision saying _aggregate already exists, 
# or we get strange merge of source files and _aggregate. Don't do that. Better have them removed (above)
for pkg in $client_deps_list; do
	echo "  r $client_dest_prj $pkg _aggregate ..."
	$osc aggregatepac $aggregatepac_prj $pkg $client_dest_prj
done

## fill in the source packages
for pkg in $(ls $tmpdir/new); do
	# make sure the package exists. CAUTION: this resets description and everything.
	echo "<package name=\"$pkg\"><title>$pkg</title><description/></package>" | $osc meta pkg $client_dest_prj $pkg  -F -
	# check out a working copy
	echo "checkout ..."
	(cd $tmpdir/co; $osc co $client_dest_prj $pkg)
	# refresh all files
	rm -f $tmpdir/co/$client_dest_prj/$pkg/*
	cp $tmpdir/new/$pkg/* $tmpdir/co/$client_dest_prj/$pkg/
	(cd $tmpdir/co/$client_dest_prj/$pkg; $osc addremove; $osc ci -m "New version $VERSION; - Created with $basename_av0 v$_version_")
done

## enable/disable the desired targets
echo "TODO: (configure build targets like this):"
echo OBS_API=$obs_api OSC_CMD=$osc_cmd $dirname_av0/../setup_build_targets.pl $client_dest_prj set32=$targets_64 set64=$targets_32
# TODO: replace setup_build_targets.pl with a shell script...
# targets_32_list=$(echo "$targets_32" | tr , ' ')
# targets_64_list=$(echo "$targets_64" | tr , ' ')

rm -rf $tmpdir/co $tmpdir/new 

