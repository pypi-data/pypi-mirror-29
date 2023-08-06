#!/bin/bash

TOP=$(readlink -e $(dirname $0)/..)
cd $TOP/doc
./mk-html.sh
