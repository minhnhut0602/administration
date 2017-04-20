#!/bin/sh

set -x

if [ -x /usr/lib/rpm/redhat/find-provides ] ; then
FINDPROV=/usr/lib/rpm/redhat/find-provides
else
FINDPROV=/usr/lib/rpm/find-provides
fi

$FINDPROV $* | sed -e 's/libQt5/@PACKAGE_NAME_PREFIX@-libQt5/g' | sed -e 's/libqt5/@PACKAGE_NAME_PREFIX@-libqt5/g' | sed -e "s/pkgconfig(Qt5/pkgconfig(@PACKAGE_NAME_PREFIX@-Qt5/g"
