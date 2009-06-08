#
AC_PREREQ(2.59)
AC_COPYRIGHT([Copyright (C) 2007  Christophe LACOMBE <clacombe@amadeus.com>])
AC_INIT([EXTRACC],[0.1.0],[clacombe@amadeus.com],[extracc])
AC_CONFIG_AUX_DIR([config])
AM_INIT_AUTOMAKE

AM_PATH_CPPUNIT(1.10)
AM_CONDITIONAL([HAVE_CPPUNIT], [test "x$CPPUNIT_LIBS" != x])

# Check for host and disable building a shared library in Windows
AC_CANONICAL_HOST
case $host in
  *-*-msdos* | *-*-go32* | *-*-mingw32* | *-*-cygwin* | *-*-windows*) 
    AC_DISABLE_SHARED
    AC_ENABLE_STATIC
    ;;
  *)  
    AC_ENABLE_SHARED
    AC_DISABLE_STATIC
    ;;
esac

# Check for debug switch
AC_ARG_ENABLE(debug,
              [AS_HELP_STRING([--enable-debug],
                              [build additional debugging library])])
test "x$enable_debug" != xyes && enable_debug=no
AM_CONDITIONAL([ENABLE_DEBUG], [test "x$enable_debug" = xyes])

# Checks for programs
AC_PROG_CXX
AC_PROG_CXXCPP
AC_PROG_INSTALL
AC_PROG_LIBTOOL
#AC_PROG_LN_S
#AC_PROG_MAKE_SET

# Set default language to C++
AC_LANG([C++])

# Checks for header files
AC_HEADER_STDC
AC_CHECK_HEADERS([ fstream ])

# Define configured files
AC_CONFIG_FILES(Makefile)
AC_CONFIG_FILES(extracc.m4)
AC_CONFIG_FILES(extracc-config)
AC_CONFIG_FILES(extracppunit/Makefile)
AC_OUTPUT

echo "
------------------------------------------------------------------------------
$PACKAGE-$VERSION library configuration:
------------------------------------------------------------------------------

Directories:
  - prefix ......... : ${prefix}
  - exec_prefix .... : ${exec_prefix}
  - includedir ..... : ${includedir}
  - libdir ......... : ${libdir}
  - docdir ......... : ${docdir}
  - mandir ......... : ${mandir}
  - infodir ........ : ${infodir}

Switches:
  - shared ......... : ${enable_shared}
  - static ......... : ${enable_static}

Compiler/linker flags/libs/defs:
  - CXX ............ : ${CXX}
  - CPPFLAGS ....... : ${CPPFLAGS}
  - LDFLAGS ........ : ${LDFLAGS}
  - LIBS ........... : ${LIBS}

CPPUNIT:
  - CPPUNIT_VERSION . : ${CPPUNIT_VERSION}
  - CPPUNIT_CFLAGS .. : ${CPPUNIT_CFLAGS}
  - CPPUNIT_LIBS .... : ${CPPUNIT_LIBS}

------------------------------------------------------------------------------
Now type 'make' to build and install $PACKAGE-$VERSION library
------------------------------------------------------------------------------
"
