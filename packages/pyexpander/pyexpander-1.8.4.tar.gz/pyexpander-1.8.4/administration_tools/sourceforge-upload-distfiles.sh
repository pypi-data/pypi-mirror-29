cd ..
DESTHOST=goetzpf@frs.sourceforge.net
#DESTPATH=/home/frs/project/p/py/pyexpander
DESTPATH=/home/frs/project/pyexpander
#scp dist/*.tar.gz $DESTHOST:$DESTPATH
#scp dist/*.zip $DESTHOST:$DESTPATH
scp -r dist/* $DESTHOST:$DESTPATH
scp README $DESTHOST:$DESTPATH
