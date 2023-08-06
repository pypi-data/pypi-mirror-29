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

echo "creating rpm package..."

python setup.py bdist_rpm
python3 setup.py bdist_rpm
if [ $docker = "yes" ]; then
    cp dist/*.rpm /root/dist 
    chmod 644 /root/dist/*.rpm
fi
