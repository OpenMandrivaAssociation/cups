%define major	2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

# Turning this on lets CUPS to be built in debug mode (with debugger symbols)
%define debug 0
%define enable_check 0

%define bootstrap 0
%if !%{bootstrap}
%define _with_systemd 1
%endif

Summary:	Common Unix Printing System - Server package
Name:		cups
Version:	1.5.2
Release:	1
License:	GPLv2 and LGPLv2
Group:		System/Printing
Url:		http://www.cups.org
Source0:	ftp://ftp.easysw.com/pub/cups/%{version}/%{name}-%{version}-source.tar.bz2

# Small C program to get list of all installed PPD files
Source1: poll_ppd_base.c
# Small C program to list the printer-specific options of a particular printer
# fails to build now
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
Source17: cups.service

# Nice level for now. bug #16387
Source18: cups.sysconfig
Patch10: cups-1.4.0-recommended.patch
# fhimpe: make installed binary files writeable as root
Patch32: cups-1.4-permissions.patch
#RosaLabs - needs to be rediff'd
#Patch9999: cups-1.4.8-l10n-ru.patch

# Ubuntu patch, Launchpad #449586: Do not use host
# names for broadcasting print queues and managing print queues broadcasted
# from other servers by default. Many networks do not have valid host names
# for all machines
Patch35: do-not-broadcast-with-hostnames.patch

#fedora patches all shifted by 1000
Patch1001: cups-no-gzip-man.patch
Patch1002: cups-system-auth.patch
Patch1003: cups-multilib.patch
Patch1004: cups-serial.patch
Patch1005: cups-banners.patch
Patch1006: cups-serverbin-compat.patch
Patch1007: cups-no-export-ssllibs.patch
Patch1008: cups-direct-usb.patch
Patch1009: cups-lpr-help.patch
Patch1010: cups-peercred.patch
Patch1011: cups-pid.patch
Patch1012: cups-eggcups.patch
Patch1013: cups-getpass.patch
Patch1014: cups-driverd-timeout.patch
Patch1015: cups-strict-ppd-line-length.patch
Patch1016: cups-logrotate.patch
Patch1017: cups-usb-paperout.patch
Patch1018: cups-build.patch
Patch1019: cups-res_init.patch
Patch1020: cups-filter-debug.patch
Patch1021: cups-uri-compat.patch
Patch1022: cups-cups-get-classes.patch
Patch1023: cups-str3382.patch
#NOT_IN_FEDPatch1024: cups-str3947.patch
#same as mdv patch cups-1.4-permissions.patch
#Patch1025: cups-0755.patch
Patch1026: cups-snmp-quirks.patch
Patch1027: cups-hp-deviceid-oid.patch
Patch1028: cups-dnssd-deviceid.patch
Patch1029: cups-ricoh-deviceid-oid.patch

Patch1030: cups-avahi-1-config.patch
Patch1031: cups-avahi-2-backend.patch
Patch1032: cups-avahi-3-timeouts.patch
Patch1033: cups-avahi-4-poll.patch
Patch1034: cups-avahi-5-services.patch

Patch1035: cups-icc.patch
Patch1036: cups-systemd-socket.patch
Patch1037: cups-str4014.patch
Patch1038: cups-polld-reconnect.patch
Patch1039: cups-translation.patch
Patch1040: cups-str3985.patch
Patch1041: cups-revision10277.patch
# selinux
#Patch1100: cups-lspp.patch

BuildRequires:	htmldoc
BuildRequires:	php-cli
BuildRequires:	xdg-utils
Buildrequires:	xinetd
BuildRequires:	acl-devel
BuildRequires:	jpeg-devel
BuildRequires:	krb5-devel
BuildRequires:	libldap-devel
BuildRequires:	openslp-devel
BuildRequires:	pam-devel
BuildRequires:	php-devel >= 5.1.0
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(avahi-compat-libdns_sd)
BuildRequires:	pkgconfig(dbus-1) >= 0.50
BuildRequires:	pkgconfig(gnutls) >= 3.0
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libusb) < 1.0
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(zlib)
%if !%{bootstrap}
BuildRequires:	poppler
%if %{_with_systemd}
BuildRequires:	systemd-units
%endif
%endif

Requires: %{name}-common >= %{version}-%{release}
Requires: net-tools
%if !%{bootstrap}
Requires: poppler
Suggests: avahi
%endif
Requires: portreserve
Requires: printer-testpages
# Take care that device files are created with correct permissions
Requires: udev 
Requires: update-alternatives
# For desktop menus
Requires: xdg-utils
%rename cupsddk-drivers

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
Requires: update-alternatives
Requires: net-tools
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

%description -n %{libname}
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%package -n %{develname}
Summary: Common Unix Printing System - Development environment "libcups"
License: LGPLv2
Group: Development/C
Requires: %{libname} >= %{version}-%{release}
Provides: cups-devel
Obsoletes: %mklibname %{name}2 -d

%description -n %{develname}
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

%prep
%setup -q
%apply_patches

# Set CUPS users and groups
perl -p -i -e 's:(SystemGroup\s+.*)$:$1\nGroup sys\nUser lp:' conf/cupsd.conf.in

# Let local printers be broadcasted in the local network(s)
perl -p -i -e 's:(Listen\s+)localhost:$1*:' conf/cupsd.conf.in
perl -p -i -e 's:(Browsing\s+On):$1\nBrowseAddress \@LOCAL:' conf/cupsd.conf.in
perl -p -i -e 's:(<Location\s+/\s*>):$1\n  Allow \@LOCAL:' conf/cupsd.conf.in

# Allow remote administration in local network (connections are encrypted,
# so no security problem)
perl -p -i -e 's:(<Location\s+/admin(|/conf)\s*>):$1\n  Allow \@LOCAL:' conf/cupsd.conf.in

# Replace the PAM configuration file
cat << EOF > scheduler/cups.pam
auth	include	system-auth
account	include	system-auth
EOF
cp -f scheduler/cups.pam conf/pam.std.in

# Let the Makefiles not trying to set file ownerships
perl -p -i -e "s/ -o \\$.CUPS_USER.//" scheduler/Makefile
perl -p -i -e "s/ -g \\$.CUPS_GROUP.//" scheduler/Makefile
perl -p -i -e "s/ -o \\$.CUPS_USER.//" systemv/Makefile
perl -p -i -e "s/ -g \\$.CUPS_GROUP.//" systemv/Makefile

# Work around bug on Mandriva compilation cluster (32-bit machine has
# /usr/lib64 directory)
perl -p -i -e 's:(libdir=")\$exec_prefix/lib64("):$1%{_libdir}$2:' config-scripts/cups-directories.m4 configure

# Let's look at the compilation command lines.
perl -p -i -e "s,^.SILENT:,," Makedefs.in

# Load additional tools
cp %{SOURCE1} poll_ppd_base.c
cp %{SOURCE2} lphelp.c
# Load nprint backend
cp %{SOURCE11} nprint
# Load AppleTalk "pap" backend
%setup -q -T -D -a 12 -n %{name}-%{version}
# Load the "pap" documentation
bzcat %{SOURCE13} > pap-docu.pdf
# Load the "photo_print" utility
cp %{SOURCE14} photo_print
# Load the "pdfdistiller" utility
cp %{SOURCE15} pdf
# Load the "cjktexttops" filter
cp %{SOURCE16} cjktexttops
# systemd service
cp %{SOURCE17} cups.service

%build
# needed by additional SOURCES
aclocal
autoconf
# for the PHP module
%define _disable_ld_no_undefined 1
#setup_compile_flags
%if %{debug}
# Debug mode
export DONT_STRIP=1
export CFLAGS="-g"
export CXXFLAGS="-g"
%endif
# cups uses $DSOFLAGS instead of $LDFLAGS for shared libs
export DSOFLAGS="$LDFLAGS"
%configure2_5x \
    --enable-avahi \
%if %{debug}
    --enable-debug=yes \
%endif
    --disable-libpaper \
    --enable-raw-printing \
    --enable-ssl \
    --disable-static \
    --with-cups-group=sys \
    --with-cups-user=lp \
    --with-docdir=%{_datadir}/cups/doc \
    --with-icondir=%{_datadir}/icons \
    --with-system-groups="lpadmin root" \
    --enable-relro \
%if !%{bootstrap}
    --with-pdftops=pdftops
%endif

%if %{debug}
# Remove "-s" (stripping) option from "install" command used for binaries
# by "make install"
perl -p -i -e 's:^(\s*INSTALL_BIN\s*=.*)-s:$1:' Makedefs
%endif

# Remove hardcoded "chgrp" from Makefiles
perl -p -i -e 's/chgrp/:/' Makefile */Makefile
%make 

# Compile additional tools
gcc %optflags %ldflags -opoll_ppd_base -I. -I./cups poll_ppd_base.c -L./cups -lcups
#no longer compiles
#gcc %optflags %ldflags -olphelp -I. -I./cups lphelp.c -L./cups -lcups

%if !%{bootstrap} && %{enable_check}
%check
export LC_ALL=C
export LC_MESSAGES=C
export LANG=C
export LANGUAGE=C
make test << EOF

EOF
%endif

%install
# Debug mode
%if %{debug}
export DONT_STRIP=1
%endif
make install BUILDROOT=%{buildroot} \
             DOCDIR=%{buildroot}%{_datadir}/cups/doc \
             CHOWN=":" CHGRP=":" STRIP="$STRIP" \
             LOGDIR=%{buildroot}%{_var}/log/cups \
             REQUESTS=%{buildroot}%{_var}/spool/cups \
             STATEDIR=%{buildroot}%{_var}/run/cups

rm -f %{buildroot}%{_libdir}/lib*.la
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
#install -m 755 lphelp %{buildroot}%{_bindir}

# Install nprint backend
install -m 755 nprint %{buildroot}%{_prefix}/lib/cups/backend/

# Install AppleTalk backend
install -m 755 pap-backend/pap %{buildroot}%{_prefix}/lib/cups/backend/
install -m 644 pap-docu.pdf %{buildroot}%{_datadir}/%{name}/doc

# Install "photo_print"
install -m 755 photo_print %{buildroot}%{_bindir}

# Install "pdfdistiller"
install -m 755 pdf %{buildroot}%{_prefix}/lib/cups/backend/

# Install "cjktexttops"
install -m 755 cjktexttops %{buildroot}%{_prefix}/lib/cups/filter/

# Install logrotate configuration
install -c -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/logrotate.d/cups

%if %{_with_systemd}
# systemd
mkdir -p %{buildroot}/lib/systemd/system
install -m644 cups.service %{buildroot}/lib/systemd/system
%endif

# Set link to test page in /usr/share/printer-testpages
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

# RPM breaking it. Links need to be deleted and afterwards regenerated
rm -f %{buildroot}%{_mandir}/man8/cupsdisable.8
rm -f %{buildroot}%{_mandir}/man8/reject.8

# Set compatibility links for the man pages and executables
ln -s %{_sbindir}/cupsenable %{buildroot}%{_bindir}/enable
ln -s %{_sbindir}/cupsdisable %{buildroot}%{_bindir}/disable
ln -s %{_sbindir}/cupsenable %{buildroot}%{_sbindir}/enable
ln -s %{_sbindir}/cupsdisable %{buildroot}%{_sbindir}/disable
ln -s %{_mandir}/man8/cupsenable.8 %{buildroot}%{_mandir}/man8/cupsdisable.8
ln -s %{_mandir}/man8/cupsdisable.8 %{buildroot}%{_mandir}/man8/disable.8
ln -s %{_mandir}/man8/cupsenable.8 %{buildroot}%{_mandir}/man8/enable.8
ln -s %{_mandir}/man8/accept.8 %{buildroot}%{_mandir}/man8/reject.8

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
install -m644 cups/debug-private.h  %{buildroot}%{_includedir}/cups/
install -m644 cups/string-private.h %{buildroot}%{_includedir}/cups/
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

%files
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
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/dbus*/system.d/cups.conf
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
%{_prefix}/lib/cups/backend/https
%{_prefix}/lib/cups/backend/ipp
%{_prefix}/lib/cups/backend/ipps
%{_prefix}/lib/cups/backend/lpd
%{_prefix}/lib/cups/backend/mdns
%{_prefix}/lib/cups/backend/nprint
%{_prefix}/lib/cups/backend/pap
%{_prefix}/lib/cups/backend/parallel
#%{_prefix}/lib/cups/backend/scsi
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
%if %{_with_systemd}
/lib/systemd/system/cups.*
%endif

%files common
%dir %config(noreplace) %attr(-,lp,sys) %{_sysconfdir}/cups
%ghost %config(noreplace) %attr(-,lp,sys) %{_sysconfdir}/cups/client.conf
%{_sbindir}/*
%{_bindir}/*cups
%{_bindir}/ipptool
#%{_bindir}/lphelp
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
%{_datadir}/locale/*/*.po
%{_mandir}/man?/*

%files -n %{libname}
%{_libdir}/libcups.so.*
%{_libdir}/libcupsimage.so.*
%{_libdir}/libcupscgi.so.1
%{_libdir}/libcupsdriver.so.1
%{_libdir}/libcupsmime.so.1
%{_libdir}/libcupsppdc.so.1

%files -n %{develname}
%{_includedir}/cups/*
%{multiarch_includedir}/cups/*
%{_libdir}/*.so
%{_bindir}/cups-config

%files serial
%{_prefix}/lib/cups/backend/serial

%files -n php-cups
%doc scripting/php/README
%attr(0755,root,root) %{_libdir}/php/extensions/*
%config(noreplace) %{_sysconfdir}/php.d/*

