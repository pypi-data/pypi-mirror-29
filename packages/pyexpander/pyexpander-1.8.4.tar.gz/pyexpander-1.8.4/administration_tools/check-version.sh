#!/bin/sh

cd ..

FILES="`ls python2/bin/[A-Za-z]*.py` `ls python2/pyexpander/[A-Za-z]*.py` `ls python3/bin/[A-Za-z]*.py` `ls python3/pyexpander/[A-Za-z]*.py` doc/conf.py setup.py"

grep "\"[^\"]\+\" \+\(#VERSION#\)" $FILES | column -t -s := | column -t

echo -n "PKG-INFO.ok:                     "; grep '^Version:' PKG-INFO.ok
