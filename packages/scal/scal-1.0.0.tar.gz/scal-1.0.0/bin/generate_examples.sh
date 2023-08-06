#!/bin/bash
#
# Compile examples located in the /example directory (where / is the root of
# the repository).

ROOTDIR="$(dirname $0)/.."
EXAMPLEDIR=doc/examples
cd "$ROOTDIR/$EXAMPLEDIR"
make -B
