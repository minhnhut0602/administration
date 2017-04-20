#!/bin/sh

set -x

if [ -x /usr/lib/rpm/redhat/find-requires ] ; then
FINDREQ=/usr/lib/rpm/redhat/find-requires
else
FINDREQ=/usr/lib/rpm/find-requires
fi

$FINDREQ $* | sed -e 's/libQt5/@PACKAGE_NAME_PREFIX@-libQt5/g' | sed -e 's/libqt5/@PACKAGE_NAME_PREFIX@-libqt5/g' | sed -e "s/pkgconfig(Qt5/pkgconfig(@PACKAGE_NAME_PREFIX@-Qt5/g"
