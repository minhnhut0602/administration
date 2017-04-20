cat <<EOF > testdata/deps_tmplvars.sh
VENDOR="ownCloud"
PACKAGE_NAME_PREFIX="ocqt562"
OC_QT_VERSION="5.6.2"
OC_QT_ROOT="/opt/\${VENDOR}/qt-\${OC_QT_VERSION}"
EOF

. testdata/deps_tmplvars.sh
sh prepare_package.sh ../templates/client-deps/qt-${OC_QT_VERSION} out testdata/deps_tmplvars.sh
