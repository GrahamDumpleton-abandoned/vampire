#!/bin/sh

if [ "$#" == "0" ]
then
  COMMAND="$0"
  find . -name ".svn" -prune -o \
   -type f -name "*.txt" -print -exec $COMMAND {} \;
else
  for file in $*
  do
    INPUT=$file
    OUTPUT=`echo $1 | sed -e "s/\\.txt$/.html/"`

    TMPFILE=`dirname $OUTPUT`/.`basename $OUTPUT`

    trap 'rm -f $TMPFILE; exit' 1 2 3 13 15

    python `dirname $0`/convert.py $INPUT $TMPFILE

    if [ "$?" = 0 ]
    then
      mv $TMPFILE $OUTPUT
    else
      rm -f $TMPFILE
    fi
  done
fi
