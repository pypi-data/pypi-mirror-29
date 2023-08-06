#!/bin/sh

# abort on errors:
set -e

if [ -z "$1" ]; then
    echo "usage: $0 <version-string>"
    echo "patches the version strings in all parts of the project"
    exit 0
fi

VERSION="$1"

FILES="`ls ../python2/bin/[A-Za-z]*.py` `ls ../python2/pyexpander/[A-Za-z]*.py` `ls ../python3/bin/[A-Za-z]*.py` `ls ../python3/pyexpander/[A-Za-z]*.py` ../doc/conf.py ../setup.py"

for f in $FILES; do
    sed -i -e "s/\"[^\"]\+\" \+\(#VERSION#\)/\"$VERSION\" \1/" $f
done

sed -i -e "s/^\(\<Version:\).*/\1 $VERSION/" ../PKG-INFO.ok

hg qnew new-version-$VERSION -m "The version was changed to $VERSION."

