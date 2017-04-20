#!/bin/sh

# spit out all the subdirs one after another.
dirparts () {
	prefix=$1 
	path=$2
	while [ "$path" != '/' -a "$path" != '.' ]; do
		echo $prefix$path
		path=$(dirname $path)
	done | tac
}

fileslist=files.list
:> $fileslist

dirparts '%dir ' /opt/ownCloud/qt-5.6.2/fancy > $fileslist
dirparts '%dir ' /usr/share/inkscape >> $fileslist

cat $fileslist
echo $fileslist
