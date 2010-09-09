%define svnsnapshot 0
%define cupsbasename cups
%if %{svnsnapshot}
%define cupsnameext %nil
%define cupssvnrevision 8703
%define cupsversion 1.4
%define cupsminorversion .0
%define cupsextraversion svn-r%{cupssvnrevision}
%define cupsrelease %mkrel 0.%{cupssvnrevision}.1
%else
%define cupsnameext %nil
%define cupssvnrevision %nil
%define cupsversion 1.4.4
%define cupsminorversion %nil
%define cupsextraversion %nil
%define cupsrelease %mkrel 1
%endif
%define cupstarballname %{cupsbasename}-%{cupsversion}%{cupsextraversion}

%define major	2
%define libname	%mklibname %{cupsbasename} %{major}%{cupsnameext}

# Turning this on lets CUPS to be built in debug mode (with debugger
# symbols)
%define debug 0

# Links in the man page directories get deleted due to a bug in Mandriva's
# RPM helper script. So we copy the man pages for now
%define manpagelinks 0

%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}


##### GENERAL STUFF #####

Summary:	Common Unix Printing System - Server package
Name:		%{cupsbasename}%{cupsnameext}
Version:	%{cupsversion}%{cupsminorversion}
Release:	%{cupsrelease}
License:	GPLv2 and LGPLv2
Group:		System/Printing
%define real_version %{version}

##### SOURCE FILES #####

Source: ftp://ftp.easysw.com/pub/cups/%{cupsversion}/%{cupstarballname}-source.tar.bz2

# Small C program to get list of all installed PPD files
Source1: poll_ppd_base.c
# Small C program to list the printer-specific options of a particular printer
Source2: lphelp.c
# Complete replacement for startup script to have it the
# Mandriva Linux way
Source5: cups.startup
# Script for cleaning up the PPD files
Source6: cleanppd.pl
# Perl script for automatic configuration of CUPS, especially access
# restrictions and broadcasting
Source7: correctcupsconfig
Source9: cups.logrotate
# Backend filter for nprint (Novell client) from Mark Horn
# (mark@hornclan.com)
Source11: http://www.hornclan.com/~mark/cups/nprint.2002011801
# AppleTalk/netatalk backend for CUPS
Source12: http://www.oeh.uni-linz.ac.at/~rupi/pap/pap-backend.tar.bz2
Source13: http://www.oeh.uni-linz.ac.at/~rupi/pap/pap-docu.pdf.bz2
Source14: http://www.linuxprinting.org/download/printing/photo_print
Source15: http://printing.kde.org/downloads/pdfdistiller
Source16: cjktexttops
# Nice level for now. bug #16387
Source18: cups.sysconfig
Patch10: cups-1.4.0-recommended.patch

# fhimpe: taken from Fedora to compile with gcc 4.3
# Without this patch, build fails with:
# auth.c:485: error: storage size of 'peercred' isn't known
Patch30: cups-1.3.7-peercred.patch
# fhimpe: make installed binary files writeable as root
Patch32: cups-1.4-permissions.patch
# Debian/Ubuntu patch: make the USB
# backend supporting both printer access via libusb and via the usblp kernel
# module. Make it also printing via libusb if the URI for the queue was
# generated via usblp and vice versa. This should solve most USB printing
# problems which occured on the transition to CUPS 1.4.x (Launchpad #420015,
# #436495; bugs.debian.org: #546558, #545288, #545453)
Patch34: cups-1.4.3-both-usblp-and-libusb.patch
# Ubuntu patch, Launchpad #449586: Do not use host
# names for broadcasting print queues and managing print queues broadcasted
# from other servers by default. Many networks do not have valid host names
# for all machines
Patch35: cups-1.4.4-no-hostname-broadcast.patch

# Fedora patches:
# don't gzip man pages
Patch1001: cups-no-gzip-man.patch
# use correct libdir
Patch1003: cups-multilib.patch
# Ignore .rpmnew and .rpmsave banner files.
Patch1006: cups-banners.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=194005
# disabled: breaks build on x86_64
Patch1007: cups-serverbin-compat.patch
# Don't export in SSLLIBS to cups-config.
Patch1008: cups-no-export-ssllibs.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=197214
# disabled for now because there is no pstoaps yet in mdv
Patch1009: cups-paps.patch
# Add '--help' option to lpr command (RH bug #206380, STR #1989).
Patch1012: cups-lpr-help.patch
# Write a pid file (RH bug #132987).
Patch1014: cups-pid.patch
# Fixed orientation of page labels when printing text in landscape
# mode (RH bug #520141, STR #3334).
Patch1015: cups-1.4.4-page-label.patch
# Send QueueChanged D-Bus signal on all job state changes.
Patch1016: cups-eggcups.patch
# Don't use getpass() (RH bug #125133).
Patch1017: cups-1.4.4-getpass.patch
# Increased PPD timeout in copy_model() (RH bug #216065)
Patch1018: cups-driverd-timeout.patch
# Don't do logrotation in cups, so that logrotate can take care of it
Patch1020: cups-logrotate.patch
# cups-polld: reinit the resolver if we haven't yet resolved the
# hostname (RH bug #354071).
Patch1023: cups-res_init.patch
# Cheaply restore compatibility with 1.1.x by having cups_get_sdests()
# perform a CUPS_GET_CLASSES request if it is not sure it is talking
# to CUPS 1.2 or later (RH bug #512866).
Patch1035: cups-cups-get-classes.patch
# build against avahi (RH bug #245824).
Patch1037: cups-avahi.patch

##### ADDITIONAL DEFINITIONS #####

Url: http://www.cups.org
Requires: %{libname} >= %{version}-%{release} %{name}-common >= %{version}-%{release} openssl net-tools
Requires: printer-testpages
# Take care that device files are created with correct permissions
Requires: udev 
# For desktop menus
Requires: xdg-utils
Suggests: avahi
%if !%bootstrap
Requires:	poppler
%endif
BuildRequires:	autoconf2.5
BuildRequires:	openssl-devel
BuildRequires:	libpam-devel
BuildRequires:	libopenslp-devel, libldap-devel
%if %mdkver >= 200700
BuildRequires:	libdbus-devel >= 0.50
%endif
BuildRequires:	glibc
BuildRequires:	htmldoc
#BuildRequires:  libdbus-1-devel
BuildRequires:	libgnutls-devel
BuildRequires:	php-devel >= 5.1.0 php-cli
BuildRequires:	libjpeg-devel, libpng-devel, libtiff-devel, libz-devel
%if !%bootstrap
buildRequires:	poppler
%endif
BuildRequires:	acl-devel
Buildrequires:  xinetd
BuildRequires:	avahi-compat-libdns_sd-devel
BuildRequires:	libusb-devel
BuildRequires:	krb-devel
Requires: 	portreserve
Provides:	cupsddk-drivers
Obsoletes:	cupsddk-drivers < 1.2.3-5
Obsoletes:	cupsddk < 1.4.0

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot



##### SUB-PACKAGES #####

%description
The Common Unix Printing System provides a portable printing layer for 
UNIX(TM) operating systems. It has been developed by Easy Software Products 
to promote a standard printing solution for all UNIX vendors and users. 
CUPS provides the System V and Berkeley command-line interfaces.
This is the main package needed for CUPS servers (machines where a
printer is connected to or which host a queue for a network
printer). It can also be used on CUPS clients so that they simply pick
up broadcasted printer information from other CUPS servers and do not
need to be assigned to a specific CUPS server by an
%{_sysconfdir}/cups/client.conf file.

%package common
Summary: Common Unix Printing System - Common stuff
License: GPLv2
Group: System/Printing
Requires: %{libname} >= %{version}-%{release} rpm >= 3.0.4-6mdk update-alternatives openssl net-tools
# To satisfy LSB/FHS
Provides: lpddaemon

%description common
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. It contains the command line utilities for
printing and administration (lpr, lpq, lprm, lpadmin, lpc, ...), man
pages, locales, and a sample configuration file for daemon-less CUPS
clients (%{_sysconfdir}/cups/client.conf).

This package you need for both CUPS clients and servers. 

%package -n %{libname}
Summary: Common Unix Printing System - CUPS library
License: LGPLv2
Group: System/Libraries
Requires: openssl net-tools
Obsoletes: libcups1
Provides: libcups1 = %{version}

%description -n %{libname}
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%package -n %{libname}-devel
Summary: Common Unix Printing System - Development environment "libcups"
License: LGPLv2
Group: Development/C
Requires: cups-common = %{version}-%{release}
Requires: %{libname} >= %{version}-%{release} openssl openssl-devel
Provides: libcups-devel = %{version}-%{release}
Provides: libcups2_1-devel = %{version}-%{release}
Obsoletes: cups-devel, libcups1-devel
Provides: cups-devel = %{version}, libcups1-devel = %{version}
Conflicts: cupsddk < 1.4.0

%description -n %{libname}-devel
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This is the development package for
creating additional printer drivers, printing software, and other CUPS
services using the main CUPS library "libcups".

%package serial
Summary: Common Unix Printing System - Backend for serial port printers
License: GPLv2
Group: System/Printing
Requires: %{name} >= %{version}-%{release}

%description serial
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the backend filter
for printers on the serial ports. The auto-detection on the serial
ports takes several seconds (and so the startup time of the CUPS
daemon with this backend present) and therefore it is not recommended
to install this package when one has no serial port printer.

%package -n php-cups
Summary: PHP bindings for the libcups library
License: GPLv2
Group: Development/PHP
Obsoletes: php4-cups
Provides: php4-cups

%description -n php-cups
Provides bindings to the functions of libcups, to give direct access
to the CUPS printing environment from PHP programs.

##### PREP #####

%prep


%if %{svnsnapshot}
# SVN version
rm -rf $RPM_BUILD_DIR/%{cupstarballname}
%setup -q -n %{cupstarballname}
%else
# Released version
rm -rf $RPM_BUILD_DIR/%{cupsbasename}-%{version}
%setup -q -n %{cupsbasename}-%{real_version}
%endif

# Downdated pstops filter due to problems with multiple page documents
#bzcat %{SOURCE9} > $RPM_BUILD_DIR/%{cupsbasename}-%{real_version}/filter/pstops.c

# Do NEVER use cups.suse (this package is for Mandriva)
#cp -f data/cups.pam data/cups.suse

# Patch away ugly "(Recommended)" tag removal
%patch10 -p1 -b .recommended
%patch30 -p1 -b .peercred
%patch32 -p1 -b .permissions
%patch34 -p1 -b .usb
%patch35 -p1 -b .broadcast

# fedora patches
%patch1001 -p1 -b .no-gzip-man
%patch1003 -p1 -b .multilib
%patch1006 -p1 -b .banners
#%patch1007 -p1 -b .serverbin-compat
%patch1008 -p1 -b .no-export-ssllibs
#%patch1009 -p1 -b .paps
%patch1012 -p1 -b .lpr-help
%patch1014 -p1 -b .pid
%patch1015 -p1 -b .page-label
%patch1016 -p1 -b .eggcups
%patch1017 -p1 -b .getpass
%patch1018 -p1 -b .driverd-timeout
%patch1020 -p1 -b .logrotate
%patch1023 -p1 -b .res_init
%patch1035 -p1 -b .cups-get-classes
%patch1037 -p1 -b .avahi

%if 0
# Fix libdir for 64-bit architectures
mv config-scripts/cups-directories.m4 config-scripts/cups-directories.m4.orig
cat << EOF > config-scripts/cups-directories.m4
libdir=%{_libdir}
EOF
cat config-scripts/cups-directories.m4.orig >> \
	config-scripts/cups-directories.m4
# Need to regenerate configure script
WANT_AUTOCONF_2_5=1 autoconf
%endif

#if 0
# Set CUPS users and groups
perl -p -i -e 's:(SystemGroup\s+.*)$:$1\nGroup sys\nUser lp:' conf/cupsd.conf.in

# Let local printers be broadcasted in the local network(s)
perl -p -i -e 's:(Listen\s+)localhost:$1*:' conf/cupsd.conf.in
perl -p -i -e 's:(Browsing\s+On):$1\nBrowseAddress \@LOCAL:' conf/cupsd.conf.in
perl -p -i -e 's:(<Location\s+/\s*>):$1\n  Allow \@LOCAL:' conf/cupsd.conf.in

# Allow remote administration in local network (connections are encrypted,
# so no security problem)
perl -p -i -e 's:(<Location\s+/admin(|/conf)\s*>):$1\n  Allow \@LOCAL:' conf/cupsd.conf.in

%if %mdkver >= 200700
# Replace the PAM configuration file
cat << EOF > scheduler/cups.pam
auth	include	system-auth
account	include	system-auth
EOF
cp -f scheduler/cups.pam conf/pam.std.in
%else
# Adapt PAM configuration to Mandriva Linux (former patch #6)
perl -p -i -e 's:(auth\s+required\s+?).*$:${1}pam_stack.so service=system-auth:' scheduler/cups.pam conf/pam.std.in
perl -p -i -e 's:(account\s+required\s+?).*$:${1}pam_stack.so service=system-auth:' scheduler/cups.pam conf/pam.std.in
%endif

# Let the Makefiles not trying to set file ownerships
perl -p -i -e "s/ -o \\$.CUPS_USER.//" scheduler/Makefile
perl -p -i -e "s/ -g \\$.CUPS_GROUP.//" scheduler/Makefile
perl -p -i -e "s/ -o \\$.CUPS_USER.//" systemv/Makefile
perl -p -i -e "s/ -g \\$.CUPS_GROUP.//" systemv/Makefile

# Correct hard-coded path for pam_appl.h
#perl -p -i -e 's:pam/pam_appl.h:security/pam_appl.h:' config-scripts/cups-pam.m4 */*.[ch]*

# Work around bug on Mandriva compilation cluster (32-bit machine has
# /usr/lib64 directory)
perl -p -i -e 's:(libdir=")\$exec_prefix/lib64("):$1%{_libdir}$2:' config-scripts/cups-directories.m4 configure

# Let's look at the compilation command lines.
perl -p -i -e "s,^.SILENT:,," Makedefs.in

%if 0
# Recode all translations to UTF 8
for l in `ls -1 locale/*/cups_* | cut -d '/' -f 2`; do 
	enc=`head -1 locale/$l/cups_$l`
	iconv -f $enc -t utf-8 -o locale/$l/cups_$l.new locale/$l/cups_$l && \
		mv -f locale/$l/cups_$l.new locale/$l/cups_$l && \
		perl -p -i -e "s/$enc/utf-8/" locale/$l/cups_$l
done
for f in doc/fr/*.*html; do 
	iconv -f iso-8859-15 -t utf-8 -o $f.new $f && mv -f $f.new $f
done
for f in templates/fr/*.tmpl; do 
	iconv -f iso-8859-15 -t utf-8 -o $f.new $f && mv -f $f.new $f
done
%endif

# Load additional tools
cp %{SOURCE1} poll_ppd_base.c
cp %{SOURCE2} lphelp.c
# Load nprint backend
cp %{SOURCE11} nprint
# Load AppleTalk "pap" backend
%setup -q -T -D -a 12 -n %{cupstarballname}
# Load the "pap" documentation
bzcat %{SOURCE13} > pap-docu.pdf
# Load the "photo_print" utility
cp %{SOURCE14} photo_print
# Load the "pdfdistiller" utility
cp %{SOURCE15} pdf
# Load the "cjktexttops" filter
cp %{SOURCE16} cjktexttops



##### BUILD #####

%build
%serverbuild
# For 'configure' the macro is not used, because otherwise one does not get the
# /etc and /var directories correctly hardcoded into the executables (they
# would get /usr/etc and /usr/var. In addition, the "--with-docdir" option
# has to be given because the default setting is broken. "aclocal" and 
# "autoconf" are needed if we have a Subversion snapshot or patched the
# files of the build system.
%if %{svnsnapshot}
aclocal
WANT_AUTOCONF_2_5=1 autoconf
%endif
aclocal
autoconf
# Debug mode
%if %debug
export DONT_STRIP=1
export CFLAGS="-g"
export CXXFLAGS="-g"
./configure \
    --enable-avahi \
    --enable-debug=yes \
    --disable-libpaper \
    --enable-raw-printing \
    --enable-ssl \
    --enable-static \
    --with-cups-group=sys \
    --with-cups-user=lp \
    --with-docdir=%{_datadir}/cups/doc \
    --with-icondir=%{_datadir}/icons \
    --with-system-groups="lpadmin root" \
%if !%bootstrap
    --with-pdftops=pdftops
%endif

# Let Makefiles not execute the /usr/bin/strip command
export STRIP=":"
# Remove "-s" (stripping) option from "install" command used for binaries
# by "make install"
perl -p -i -e 's:^(\s*INSTALL_BIN\s*=.*)-s:$1:' Makedefs
%else
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -fPIC"
./configure \
    --enable-avahi \
    --disable-libpaper \
    --enable-raw-printing \
    --enable-ssl \
    --enable-static \
    --with-cups-group=sys \
    --with-cups-user=lp \
    --with-docdir=%{_datadir}/cups/doc \
    --with-icondir=%{_datadir}/icons \
    --with-system-groups="lpadmin root" \
%if !%bootstrap
    --with-pdftops=pdftops
%endif

#configure2_5x --enable-ssl --with-docdir=%{_datadir}/cups/doc
export STRIP="/usr/bin/strip"
%endif
# Remove hardcoded "chgrp" from Makefiles
perl -p -i -e 's/chgrp/:/' Makefile */Makefile
%ifnarch %{ix86}
export REAL_CFLAGS="$CFLAGS -fPIC"
%else
export REAL_CFLAGS="$CFLAGS"
%endif
make CHOWN=":" STRIP="$STRIP" OPTIM="$REAL_CFLAGS" \
             REQUESTS=%{buildroot}%{_var}/spool/cups \
             LOGDIR=%{buildroot}%{_var}/log/cups \
             STATEDIR=%{buildroot}%{_var}/run/cups

%if 0
%make LOGDIR=%{buildroot}%{_var}/log/cups \
             REQUESTS=%{buildroot}%{_var}/spool/cups \
             SERVERROOT=%{buildroot}%{_sysconfdir}/cups \
             MANDIR=%{buildroot}%{_mandir} \
             PAMDIR=%{buildroot}%{_sysconfdir}/pam.d \
             BINDIR=%{buildroot}%{_bindir} \
             SBINDIR=%{buildroot}%{_sbindir} \
             INITDIR=%{buildroot}%{_sysconfdir}/rc.d \
             DOCDIR=%{buildroot}%{_datadir}/cups/doc \
             CHOWN=":" STRIP="$STRIP" OPTIM="$REAL_CFLAGS"
%endif

# Compile additional tools
gcc -opoll_ppd_base -I. -I./cups -L./cups -lcups poll_ppd_base.c
gcc -olphelp -I. -I./cups -L./cups -lcups lphelp.c

%check
export LC_ALL=C
export LC_MESSAGES=C
export LANG=C
export LANGUAGE=C
make test << EOF

EOF


##### INSTALL #####

%install
rm -rf %{buildroot}
# Debug mode
%if %debug
export DONT_STRIP=1
%endif

make install BUILDROOT=%{buildroot} \
             DOCDIR=%{buildroot}%{_datadir}/cups/doc \
             CHOWN=":" CHGRP=":" STRIP="$STRIP" \
             LOGDIR=%{buildroot}%{_var}/log/cups \
             REQUESTS=%{buildroot}%{_var}/spool/cups \
             STATEDIR=%{buildroot}%{_var}/run/cups

%if 0
make install BUILDROOT=%{buildroot} \
	     LOGDIR=%{buildroot}%{_var}/log/cups \
             SERVERROOT=%{buildroot}%{_sysconfdir}/cups \
             AMANDIR=%{buildroot}%{_mandir} \
             PMANDIR=%{buildroot}%{_mandir} \
             MANDIR=%{buildroot}%{_mandir} \
             PAMDIR=%{buildroot}%{_sysconfdir}/pam.d \
             BINDIR=%{buildroot}%{_bindir} \
             SBINDIR=%{buildroot}%{_sbindir} \
             INITDIR=%{buildroot}%{_sysconfdir}/rc.d \
             DOCDIR=%{buildroot}%{_datadir}/cups/doc \
             CHOWN=":" CHGRP=":" STRIP="$STRIP"

#             DOCDIR=%{buildroot}%{_defaultdocdir}/cups \
%endif

# Make a directory for PPD generators
mkdir -p %{buildroot}%{_prefix}/lib/cups/driver

# Make a directory for the SSL files
mkdir -p %{buildroot}%{_sysconfdir}/cups/ssl

# Make a directory for authentication certificates
mkdir -p %{buildroot}%{_var}/run/cups/certs

# Make a directory for logrotate configuration
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d

# Install additional tools
install -m 755 poll_ppd_base %{buildroot}%{_bindir}
install -m 755 lphelp %{buildroot}%{_bindir}

# Install nprint backend
install -m 755 nprint %{buildroot}%{_prefix}/lib/cups/backend/

# Install AppleTalk backend
install -m 755 pap-backend/pap %{buildroot}%{_prefix}/lib/cups/backend/
install -m 644 pap-docu.pdf %{buildroot}%{_datadir}/%{cupsbasename}/doc

# Install "photo_print"
install -m 755 photo_print %{buildroot}%{_bindir}

# Install "pdfdistiller"
install -m 755 pdf %{buildroot}%{_prefix}/lib/cups/backend/

# Install "cjktexttops"
install -m 755 cjktexttops %{buildroot}%{_prefix}/lib/cups/filter/

# Install logrotate configuration
install -c -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/logrotate.d/cups

# Set link to test page in /usr/share/printer-testpages
#rm -f %{buildroot}%{_datadir}/cups/data/testprint.ps
ln -s %{_datadir}/printer-testpages/testprint.ps %{buildroot}%{_datadir}/cups/data/testprint-mdv.ps

# Install startup script
install -d %{buildroot}%{_initrddir}
install -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/cups
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE18} %{buildroot}%{_sysconfdir}/sysconfig/cups
rm -f %{buildroot}%{_sysconfdir}/init.d/cups

# https://qa.mandriva.com/show_bug.cgi?id=23846
install -d %{buildroot}%{_sysconfdir}/portreserve
echo "ipp" > %{buildroot}%{_sysconfdir}/portreserve/cups

# Install script for automatic CUPS configuration
cp %{SOURCE7} %{buildroot}%{_sbindir}/correctcupsconfig
chmod a+rx %{buildroot}%{_sbindir}/correctcupsconfig

# Install PPDs
mkdir -p %{buildroot}%{_datadir}/cups/model
#install -m 755 ppd/*.ppd %{buildroot}%{_datadir}/cups/model

# Uncompress Perl script for cleaning up manufacturer entries in PPD files
cp %{SOURCE6} ./cleanppd.pl
chmod a+rx ./cleanppd.pl
# Do the clean-up
find %{buildroot}%{_datadir}/cups/model -name "*.ppd" -exec ./cleanppd.pl '{}' \;

# bzip2 all man pages already now, so that we can link man pages without
# RPM breaking it. Links need to be deleted and afterwards regenerated
rm -f %{buildroot}%{_mandir}/man8/cupsdisable.8
rm -f %{buildroot}%{_mandir}/man8/reject.8
#bzme -F %{buildroot}%{_mandir}/man*/*.[0-9n].gz

# Set compatibility links for the man pages and executables
ln -s %{_sbindir}/cupsenable %{buildroot}%{_bindir}/enable
ln -s %{_sbindir}/cupsdisable %{buildroot}%{_bindir}/disable
ln -s %{_sbindir}/cupsenable %{buildroot}%{_sbindir}/enable
ln -s %{_sbindir}/cupsdisable %{buildroot}%{_sbindir}/disable
%if %manpagelinks
ln -s %{_mandir}/man8/cupsenable.8 %{buildroot}%{_mandir}/man8/cupsdisable.8
ln -s %{_mandir}/man8/cupsdisable.8 %{buildroot}%{_mandir}/man8/disable.8
ln -s %{_mandir}/man8/cupsenable.8 %{buildroot}%{_mandir}/man8/enable.8
ln -s %{_mandir}/man8/accept.8 %{buildroot}%{_mandir}/man8/reject.8
%else
cp %{buildroot}%{_mandir}/man8/cupsenable.8 %{buildroot}%{_mandir}/man8/cupsdisable.8
cp %{buildroot}%{_mandir}/man8/cupsdisable.8 %{buildroot}%{_mandir}/man8/disable.8
cp %{buildroot}%{_mandir}/man8/cupsenable.8 %{buildroot}%{_mandir}/man8/enable.8
cp %{buildroot}%{_mandir}/man8/accept.8 %{buildroot}%{_mandir}/man8/reject.8
%endif

%ifarch x86_64
# This one will be removed soon, when all other packages are
# modified appropriately
ln -s %{_prefix}/lib/cups %{buildroot}%{_libdir}/cups
%endif

# prepare the commands conflicting with LPD for the update-alternatives
# treatment
( cd %{buildroot}%{_bindir}
  mv lpr lpr-cups
  mv lpq lpq-cups
  mv lprm lprm-cups
  mv lp lp-cups
  mv cancel cancel-cups
  mv lpstat lpstat-cups
)
( cd %{buildroot}%{_sbindir}
  mv accept accept-cups
  mv disable disable-cups
  mv enable enable-cups
  mv lpc lpc-cups
  mv lpmove lpmove-cups
  mv reject reject-cups
)
( cd %{buildroot}%{_mandir}/man1
  mv lpr.1 lpr-cups.1
  mv lpq.1 lpq-cups.1
  mv lprm.1 lprm-cups.1
  mv lp.1 lp-cups.1
  mv cancel.1 cancel-cups.1
  mv lpstat.1 lpstat-cups.1
)
( cd %{buildroot}%{_mandir}/man8
  mv accept.8 accept-cups.8
  mv disable.8 disable-cups.8
  mv enable.8 enable-cups.8
  mv lpc.8 lpc-cups.8
  mv lpmove.8 lpmove-cups.8
  mv reject.8 reject-cups.8
)
ln -sf %{_sbindir}/accept-cups %{buildroot}%{_sbindir}/reject-cups
ln -sf %{_sbindir}/accept-cups %{buildroot}%{_sbindir}/cupsdisable
ln -sf %{_sbindir}/accept-cups %{buildroot}%{_sbindir}/cupsenable

# Remove links to the startup script, we make our own ones with chkconfig
rm -rf %{buildroot}%{_sysconfdir}/rc?.d/[SK]*
# Remove superflouus man page stuff
rm -rf %{buildroot}%{_mandir}/cat
rm -rf %{buildroot}%{_mandir}/cat?
rm -rf %{buildroot}%{_mandir}/*/cat
rm -rf %{buildroot}%{_mandir}/*/cat?

# Install missing headers (Thanks to Oden Eriksson)
install -m644 cups/debug.h  %{buildroot}%{_includedir}/cups/
install -m644 cups/string.h %{buildroot}%{_includedir}/cups/
install -m644 config.h %{buildroot}%{_includedir}/cups/

# Multiarch fixes
%multiarch_includes %{buildroot}%{_includedir}/cups/config.h

# Create dummy config files /etc/cups/printers.conf,
# /etc/cups/classes.conf, and /etc/cups/client.conf
touch %{buildroot}%{_sysconfdir}/cups/printers.conf
touch %{buildroot}%{_sysconfdir}/cups/classes.conf
touch %{buildroot}%{_sysconfdir}/cups/client.conf

# Create .ini file for the PHP bindings
install -d %{buildroot}%{_sysconfdir}/php.d
cat > %{buildroot}%{_sysconfdir}/php.d/A20_cups.ini << EOF
extension = phpcups.so
EOF

# Prefer xdg-utils than htmlview (kde one)
sed -i s/htmlview/xdg-open/ %{buildroot}%{_datadir}/applications/*.desktop

#find_lang %{name}

# http://qa.mandriva.com/show_bug.cgi?id=28383
# Common PPD dirs
mkdir -p %{buildroot}%{_datadir}/ppd

# Make CUPS know them
ln -s /usr/local/share/ppd %{buildroot}%{_datadir}/cups/model/1-local-admin
ln -s /opt/share/ppd %{buildroot}%{_datadir}/cups/model/2-third-party
ln -s %{_datadir}/ppd %{buildroot}%{_datadir}/cups/model/3-distribution

# Common printer driver dirs
mkdir -p %{buildroot}%{_libdir}/printdriver
# Other dirs can't be handled here, but on %post instead.

##### PRE/POST INSTALL SCRIPTS #####

%pre
%ifarch x86_64
# Fix /usr/lib/cups directory, so that updates can be done
if [ -d %{_libdir}/cups ] && ! [ -h %{_libdir}/cups ]; then
    if [ -h %{_prefix}/lib/cups ]; then
        rm -f %{_prefix}/lib/cups
	mv %{_libdir}/cups %{_prefix}/lib/cups
    else
	mv %{_libdir}/cups %{_libdir}/cups.rpmsave
	#echo 'Moved %{_libdir}/cups to %{_libdir}/cups.rpmsave' 1>&2
    fi
fi
%endif
%_pre_groupadd lpadmin

%post
# Make sure group ownerships are correct
chgrp -R sys %{_sysconfdir}/cups %{_var}/*/cups

# We can't enforce this. Bug #35993
for d in /opt/share/ppd /opt/lib/printdriver /usr/local/share/ppd /usr/local/lib/printdriver
do
  [ ! -e $d ] && mkdir -p $d || :
done
# End of 28383

# Let CUPS daemon be automatically started at boot time
%_post_service cups

%post common
# The lpc updates-alternative links were not correctly set in older CUPS
# packages, therefore remove the entry before making a new one when updating
%{_sbindir}/update-alternatives --remove lpc %{_sbindir}/lpc-cups || :
# Set up update-alternatives entries
%{_sbindir}/update-alternatives --install %{_bindir}/lpr lpr %{_bindir}/lpr-cups 10 --slave %{_mandir}/man1/lpr.1%{_extension} lpr.1%{_extension} %{_mandir}/man1/lpr-cups.1%{_extension}
%{_sbindir}/update-alternatives --install %{_bindir}/lpq lpq %{_bindir}/lpq-cups 10 --slave %{_mandir}/man1/lpq.1%{_extension} lpq.1%{_extension} %{_mandir}/man1/lpq-cups.1%{_extension}
%{_sbindir}/update-alternatives --install %{_bindir}/lprm lprm %{_bindir}/lprm-cups 10 --slave %{_mandir}/man1/lprm.1%{_extension} lprm.1%{_extension} %{_mandir}/man1/lprm-cups.1%{_extension}
%{_sbindir}/update-alternatives --install %{_bindir}/lp lp %{_bindir}/lp-cups 10 --slave %{_mandir}/man1/lp.1%{_extension} lp.1%{_extension} %{_mandir}/man1/lp-cups.1%{_extension}
%{_sbindir}/update-alternatives --install %{_bindir}/cancel cancel %{_bindir}/cancel-cups 10 --slave %{_mandir}/man1/cancel.1%{_extension} cancel.1%{_extension} %{_mandir}/man1/cancel-cups.1%{_extension}
%{_sbindir}/update-alternatives --install %{_bindir}/lpstat lpstat %{_bindir}/lpstat-cups 10 --slave %{_mandir}/man1/lpstat.1%{_extension} lpstat.1%{_extension} %{_mandir}/man1/lpstat-cups.1%{_extension}
%{_sbindir}/update-alternatives --install %{_sbindir}/accept accept %{_sbindir}/accept-cups 10 --slave %{_mandir}/man8/accept.8%{_extension} accept.8%{_extension} %{_mandir}/man8/accept-cups.8%{_extension}
%{_sbindir}/update-alternatives --install %{_sbindir}/disable disable %{_sbindir}/disable-cups 10 --slave %{_mandir}/man8/disable.8%{_extension} disable.8%{_extension} %{_mandir}/man8/disable-cups.8%{_extension}
%{_sbindir}/update-alternatives --install %{_sbindir}/enable enable %{_sbindir}/enable-cups 10 --slave %{_mandir}/man8/enable.8%{_extension} enable.8%{_extension} %{_mandir}/man8/enable-cups.8%{_extension}
%{_sbindir}/update-alternatives --install %{_sbindir}/lpc lpc %{_sbindir}/lpc-cups 10 --slave %{_mandir}/man8/lpc.8%{_extension} lpc.8%{_extension} %{_mandir}/man8/lpc-cups.8%{_extension}
%{_sbindir}/update-alternatives --install %{_sbindir}/lpmove lpmove %{_sbindir}/lpmove-cups 10 --slave %{_mandir}/man8/lpmove.8%{_extension} lpmove.8%{_extension} %{_mandir}/man8/lpmove-cups.8%{_extension}
%{_sbindir}/update-alternatives --install %{_sbindir}/reject reject %{_sbindir}/reject-cups 10 --slave %{_mandir}/man8/reject.8%{_extension} reject.8%{_extension} %{_mandir}/man8/reject-cups.8%{_extension}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%preun
# Let CUPS daemon not be automatically started at boot time any more
%_preun_service cups

%preun common
if [ "$1" = 0 ]; then
  # Remove update-alternatives entries
  %{_sbindir}/update-alternatives --remove lpr %{_bindir}/lpr-cups
  %{_sbindir}/update-alternatives --remove lpq %{_bindir}/lpq-cups
  %{_sbindir}/update-alternatives --remove lprm %{_bindir}/lprm-cups
  %{_sbindir}/update-alternatives --remove lp %{_bindir}/lp-cups
  %{_sbindir}/update-alternatives --remove cancel %{_bindir}/cancel-cups
  %{_sbindir}/update-alternatives --remove lpstat %{_bindir}/lpstat-cups
  %{_sbindir}/update-alternatives --remove accept %{_sbindir}/accept-cups
  %{_sbindir}/update-alternatives --remove disable %{_sbindir}/disable-cups
  %{_sbindir}/update-alternatives --remove enable %{_sbindir}/enable-cups
  %{_sbindir}/update-alternatives --remove lpc %{_sbindir}/lpc-cups
  %{_sbindir}/update-alternatives --remove lpmove %{_sbindir}/lpmove-cups
  %{_sbindir}/update-alternatives --remove reject %{_sbindir}/reject-cups
fi

%postun
%_postun_groupdel lpadmin

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif



%clean
##### CLEAN UP #####
rm -rf %{buildroot}



##### FILE LISTS FOR ALL BINARY PACKAGES #####

#####cups
%files
%defattr(-,root,root)
%doc *.txt
%attr(511,lp,lpadmin) %{_var}/run/cups/certs
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/cups/cupsd.conf
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/sysconfig/cups
%ghost %config(noreplace) %{_sysconfdir}/cups/printers.conf
%ghost %config(noreplace) %{_sysconfdir}/cups/classes.conf
%attr(-,root,sys) %{_sysconfdir}/cups/cupsd.conf.default
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/cups/interfaces
#%config(noreplace) %attr(644,root,sys) %{_sysconfdir}/cups/mime.convs
#%config(noreplace) %attr(644,root,sys) %{_sysconfdir}/cups/mime.types
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/cups/ppd
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/cups/ssl
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/cups/snmp.conf
%if %mdkver >= 200700
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/dbus*/system.d/cups.conf
%endif
%{_initrddir}/cups
%config(noreplace) %{_sysconfdir}/pam.d/cups
%config(noreplace) %{_sysconfdir}/logrotate.d/cups
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/xinetd.d/cups-lpd
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/portreserve/cups
%dir %{_prefix}/lib/cups
%{_prefix}/lib/cups/cgi-bin
%{_prefix}/lib/cups/daemon
%{_prefix}/lib/cups/notifier
%{_prefix}/lib/cups/filter
%{_prefix}/lib/cups/monitor
%dir %{_prefix}/lib/cups/backend
%{_prefix}/lib/cups/backend/dnssd
%{_prefix}/lib/cups/backend/http
%{_prefix}/lib/cups/backend/ipp
%{_prefix}/lib/cups/backend/lpd
%{_prefix}/lib/cups/backend/mdns
%{_prefix}/lib/cups/backend/nprint
%{_prefix}/lib/cups/backend/pap
%{_prefix}/lib/cups/backend/parallel
%{_prefix}/lib/cups/backend/scsi
%{_prefix}/lib/cups/backend/snmp
%{_prefix}/lib/cups/backend/socket
%{_prefix}/lib/cups/backend/usb
%{_prefix}/lib/cups/backend/pdf
%dir %{_prefix}/lib/cups/driver
%{_datadir}/cups
%attr(0755,root,sys) %{_var}/log/cups
# Set ownerships of spool directory which is normally done by 'make install'
# Because RPM does 'make install' as normal user, this has to be done here
%dir %attr(0710,root,sys) %{_var}/spool/cups
%dir %attr(01770,root,sys) %{_var}/spool/cups/tmp
%dir %attr(775,root,sys) %{_var}/cache/cups
# Bug #28383 dirs
%dir %{_datadir}/ppd
%dir %{_libdir}/printdriver
# Desktop icons
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/cups.png
%ifarch x86_64
# Compatibility link, will be removed soon
%{_libdir}/cups
%endif

#####cups-common
%files common
#-f %{name}.lang
%defattr(-,root,root)
%dir %config(noreplace) %attr(-,lp,sys) %{_sysconfdir}/cups
%ghost %config(noreplace) %attr(-,lp,sys) %{_sysconfdir}/cups/client.conf
%{_sbindir}/*
%{_bindir}/*cups
%{_bindir}/lphelp
%{_bindir}/lpoptions
%attr(6755,root,sys) %{_bindir}/lppasswd
%{_bindir}/photo_print
%{_bindir}/poll_ppd_base
%{_bindir}/ppdc
%{_bindir}/ppdhtml
%{_bindir}/ppdi
%{_bindir}/ppdmerge
%{_bindir}/ppdpo
%{_bindir}/cupstestppd
%{_bindir}/cupstestdsc
%{_bindir}/enable
%{_bindir}/disable
%lang(da) %{_datadir}/locale/da/cups_da.po
%lang(de) %{_datadir}/locale/de/cups_de.po
%lang(es) %{_datadir}/locale/es/cups_es.po
#%lang(et) %{_datadir}/locale/et/cups_et.po
%lang(eu) %{_datadir}/locale/eu/cups_eu.po
%lang(fi) %{_datadir}/locale/fi/cups_fi.po
%lang(fr) %{_datadir}/locale/fr/cups_fr.po
#%lang(he) %{_datadir}/locale/he/cups_he.po
%lang(id) %{_datadir}/locale/id/cups_id.po
%lang(it) %{_datadir}/locale/it/cups_it.po
%lang(ja) %{_datadir}/locale/ja/cups_ja.po
%lang(ko) %{_datadir}/locale/ko/cups_ko.po
%lang(nl) %{_datadir}/locale/nl/cups_nl.po
%lang(no) %{_datadir}/locale/no/cups_no.po
%lang(pl) %{_datadir}/locale/pl/cups_pl.po
%lang(pt) %{_datadir}/locale/pt/cups_pt.po
%lang(pt_BR) %{_datadir}/locale/pt_BR/cups_pt_BR.po
%lang(ru) %{_datadir}/locale/ru/cups_ru.po
%lang(sv) %{_datadir}/locale/sv/cups_sv.po
%lang(zh) %{_datadir}/locale/zh/cups_zh.po
%lang(zh_TW) %{_datadir}/locale/zh_TW/cups_zh_TW.po
%{_mandir}/man?/*

#####%{libname}
%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcups.so.*
%{_libdir}/libcupsimage.so.*
%{_libdir}/libcupscgi.so.1
%{_libdir}/libcupsdriver.so.1
%{_libdir}/libcupsmime.so.1
%{_libdir}/libcupsppdc.so.1

#####%{libname}-devel
%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/cups/*
%multiarch %{multiarch_includedir}/cups/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_bindir}/cups-config

%files serial
%defattr(-,root,root)
%{_prefix}/lib/cups/backend/serial

%files -n php-cups
%defattr(-,root,root)
%doc scripting/php/README
%attr(0755,root,root) %{_libdir}/php/extensions/*
%config(noreplace) %{_sysconfdir}/php.d/*
