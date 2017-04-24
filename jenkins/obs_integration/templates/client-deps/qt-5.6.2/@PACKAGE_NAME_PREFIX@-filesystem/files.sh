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

dirparts '%dir ' @OC_QT_ROOT@/fancy > $fileslist
dirparts '%dir ' /usr/share/inkscape >> $fileslist

cat $fileslist
echo $fileslist
