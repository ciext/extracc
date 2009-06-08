## command sub-directory
include $(srcdir)/sources.mk

AM_CPPFLAGS = -I$(top_srcdir)

MAINTAINERCLEANFILES = Makefile.in

lib_LTLIBRARIES= lib@PACKAGE@-extracppunit.la
if ENABLE_DEBUG
lib_LTLIBRARIES += lib@PACKAGE@-extracppunit_debug.la
endif

lib@PACKAGE@_extracppunit_la_SOURCES = $(test_com_h_sources) $(test_com_cc_sources)
lib@PACKAGE@_extracppunit_la_CXXFLAGS = $(CXXFLAGS_OPT) $(CPPUNIT_CFLAGS)

lib@PACKAGE@_extracppunit_debug_la_SOURCES = $(lib@PACKAGE@_extracppunit_la_SOURCES)
lib@PACKAGE@_extracppunit_debug_la_CXXFLAGS = $(CXXFLAGS_DEBUG) $(CPPUNIT_CFLAGS)

extracc_extracppunit_LDFLAGS = lib@PACKAGE@-extracppunit.la
extracc_extracppunit_debug_LDFLAGS = lib@PACKAGE@-extracppunit_debug.la