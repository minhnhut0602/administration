#!/bin/sh

# Wrapper to start the correct owncloud binary with proper preinitializations.
export LD_LIBRARY_PATH=@CLIENT_ROOT@/lib64:@CLIENT_ROOT@/lib:@OC_QT_ROOT@/lib64:@OC_QT_ROOT@/lib:$LD_LIBRARY_PATH

exec @CLIENT_ROOT@/bin/@APPLICATION_SHORTNAME@ "$@"
