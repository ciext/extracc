#!/bin/sh

#
dir=`echo "$0" | sed 's,[^/]*$,,'`
test "x${dir}" = "x" && dir='.'

#
if test "x`cd "${dir}" 2>/dev/null && pwd`" != "x`pwd`"
then
    echo "This script must be executed directly from the source directory."
    exit 1
fi

#
rm -f config.cache acconfig.h

#
echo "- autoreconf."            && \
autoreconf -fvi                 && \
echo "" && \
echo "Now, the configuration script has to be run. For instance:" && \
echo "mkdir -p tmp && cd tmp && \\" && \
echo " ../configure --prefix=/home/user/dev/deliveries/extracc-99.99.99 \\ " && \
echo "  --srcdir=.." && \
echo "" && \
echo "Then:" && \
echo "make && make doc && make install" && \
echo "" && \
exit 0

#echo "- configure."     && ./configure "$@" && exit 0
