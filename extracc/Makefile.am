## top directory
@SET_MAKE@

AM_CPPFLAGS = -I$(top_builddir) -I$(top_srcdir)

ACLOCAL_AMFLAGS = -I config

AUTOMAKE_OPTIONS = dist-bzip2

# Maintainance files
MAINTAINERCLEANFILES = Makefile.in aclocal.m4 configure \
			config-h.in autogen.sh

EXTRA_DIST = @PACKAGE@.m4 $(install_sources)

# Build in these directories:
SUBDIRS = extracppunit man


# Configuration helpers
bin_SCRIPTS = @PACKAGE@-config

#pkgconfigdir = $(libdir)/pkgconfig
#pkgconfig_DATA = @PACKAGE@.pc

datadir = @datadir@
pkgdatadir = $(datadir)/@PACKAGE@

m4datadir = $(datadir)/aclocal
m4data_DATA = @PACKAGE@.m4

install_sources = \
	extracppunit/Makefile.common \
	build/ant/build.xml \
	build/ant/cppunit-to-junit.xsl \
	build/ant/text2ccxml/src/com/gb/bci/ant/taskdefs/TextToCCXml.java \
	tools/cc-open-trac-ticket.py

# Targets
install-data-local: $(addprefix $(DESTDIR)$(pkgdatadir)/,$(install_sources))
$(DESTDIR)$(pkgdatadir)/%: %
	$(mkinstalldirs) `dirname $@`
	$(INSTALL_DATA) $^ $@

uninstall-local:
	rm -rf $(DESTDIR)$(pkgdatadir)/*
