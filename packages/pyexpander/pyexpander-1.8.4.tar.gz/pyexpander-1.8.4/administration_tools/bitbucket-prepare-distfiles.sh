#!/bin/bash

set -e

SCRIPT_FULL_NAME=$(readlink -e $0)
MYDIR=$(dirname $SCRIPT_FULL_NAME)
MYNAME=$(basename $SCRIPT_FULL_NAME)

cd $MYDIR/..

rm -rf dist-bitbucket
mkdir -p dist-bitbucket

for f in dist/*; do
    if [ ! -d "$f" ]; then
        cp -a "$f" dist-bitbucket;
    else
        for ff in $f/*; do
            subdir=$(basename $f)
            cp "$ff" dist-bitbucket/$subdir-$(basename $ff)
        done;
    fi
done

rm -f dist-bitbucket/pyexpander.tar.gz dist-bitbucket/pyexpander.zip

echo "Now go to https://bitbucket.org/goetzpf/pyexpander/downloads"
echo "Select 'Add files'."
echo "Go to [local-repo}/dist-bitbucket"
echo "select all files (mark with shift) and upload"


