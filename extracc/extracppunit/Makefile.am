## extracppunit sub-directory
include $(srcdir)/sources.mk

AM_CPPFLAGS = -I$(top_srcdir)

MAINTAINERCLEANFILES = Makefile.in

lib_LTLIBRARIES = libextracc-extracppunit.la

libextracc_extracppunit_la_SOURCES = \
	$(test_com_h_sources) $(test_com_cc_sources)
libextracc_extracppunit_la_CXXFLAGS = $(CXXFLAGS_OPT) $(CPPUNIT_CFLAGS)
libextracc_extracppunit_la_LDFLAGS = -version-info $(GENERIC_LIBRARY_VERSION)

#extracc_extracppunit_LDFLAGS = libextracc-extracppunit.la
