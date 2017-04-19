#!/bin/sh

# Wrapper to start the correct owncloud binary with proper preinitializations.
export LD_LIBRARY_PATH=@PACKAGE_ROOT@/lib64:@PACKAGE_ROOT@/lib:$LD_LIBRARY_PATH

exec @PACKAGE_ROOT@/bin/@APPLICATION_SHORTNAME@ "$@"
