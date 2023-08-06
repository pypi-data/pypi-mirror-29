#!/bin/bash
set -e

TOP=$(readlink -e $(dirname $0))
cd $TOP

if [ -e /root/dist ]; then
    # we are probably running within a docker container
    docker="yes"
else
    docker="no"
fi

if [ $docker = "yes" ]; then
    cd ../..
    echo "copying pyexpander dir into container..."
    # do not stop the script here if e.g. an editor swap file couldn't be
    # copied:
    cp -dR --preserve=mode,timestamps pyexpander mypyexpander || true
    cd mypyexpander
    rm -rf dist
else
    cd ..
fi

echo "creating python2 and python3 debian packages..."
python3 setup.py --command-packages=stdeb.command sdist_dsc --with-python2=True --with-python3=True bdist_deb
if [ $docker = "yes" ]; then
    cp deb_dist/*.deb /root/dist 
    chmod 644 /root/dist/*.deb
fi
