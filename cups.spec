# {_exec_prefix}/lib/cups is correct, even on x86_64.
# It is not used for shared objects but for executables.
# It's more of a libexec-style ({_libexecdir}) usage,
# but we use lib for compatibility with 3rd party drivers (at upstream request).
%global cups_serverbin %{_exec_prefix}/lib/cups

# Turning this on lets CUPS to be built in debug mode (with debugger symbols)
%define debug 0
%define enable_check 0

# Define to %nil for release builds
%define beta %{nil}

%define _disable_lto 1

%bcond_without	dnssd
%bcond_without	bootstrap

Summary:	Common Unix Printing System - Server package
Name:		cups
Version:	2.2.4
%if "%beta" != ""
Release:	0.%beta.1
%else
Release:	1
%endif
Source0:	https://github.com/apple/cups/releases/download/v%version%beta/cups-%version%beta-source.tar.gz
Source1000:	%{name}.rpmlintrc
License:	GPLv2 and LGPLv2
Group:		System/Printing
Url:		http://www.cups.org

# Small C program to get list of all installed PPD files
Source1:	poll_ppd_base.c
# Small C program to list the printer-specific options of a particular printer
# fails to build now
Source2:	lphelp.c
# Script for cleaning up the PPD files
Source6:	cleanppd.pl
# Perl script for automatic configuration of CUPS, especially access
# restrictions and broadcasting
Source7:	correctcupsconfig
Source9:	cups.logrotate
# Backend filter for nprint (Novell client) from Mark Horn
# (mark@hornclan.com)
Source11:	http://www.hornclan.com/~mark/cups/nprint.2002011801
# AppleTalk/netatalk backend for CUPS
Source12:	http://www.oeh.uni-linz.ac.at/~rupi/pap/pap-backend.tar.bz2
Source13:	http://www.oeh.uni-linz.ac.at/~rupi/pap/pap-docu.pdf.bz2
Source14:	http://www.linuxprinting.org/download/printing/photo_print
Source15:	http://download.kde.org/printing/pdfdistiller
Source16:	cjktexttops
# Nice level for now. bug #16387
Source18:	cups.sysconfig
# udev rules for setting symlinks needed if the usblp module is loaded
Source19:	10-cups_device_links.rules
# Udev rules for setting properly rights and groups
Source20:	10-cups_device_usb.rules

Patch1:		cups-dbus-utf8.patch
Patch10:	cups-1.4.0-recommended.patch

# Fedora patches
Patch1000:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-no-gzip-man.patch
Patch1001:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-system-auth.patch
Patch1002:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-multilib.patch
Patch1004:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-banners.patch
Patch1005:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-serverbin-compat.patch
Patch1006:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-no-export-ssllibs.patch
Patch1007:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-direct-usb.patch
Patch1008:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-lpr-help.patch
Patch1009:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-peercred.patch
Patch1010:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-pid.patch
Patch1011:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-eggcups.patch
Patch1012:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-driverd-timeout.patch
Patch1013:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-strict-ppd-line-length.patch
Patch1014:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-logrotate.patch
Patch1015:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-usb-paperout.patch
Patch1016:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-res_init.patch
Patch1017:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-filter-debug.patch
Patch1018:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-uri-compat.patch
Patch1019:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-str3382.patch
#same as mdv patch cups-1.4-permissions.patch
#Patch1020:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-0755.patch
Patch1021:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-hp-deviceid-oid.patch
Patch1022:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-dnssd-deviceid.patch
Patch1023:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-ricoh-deviceid-oid.patch
Patch1024:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-systemd-socket.patch
Patch1026:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-avahi-address.patch
Patch1028:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-dymo-deviceid.patch
Patch1029:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-freebind.patch
Patch1030:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-no-gcry.patch
Patch1031:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-libusb-quirks.patch
Patch1032:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-use-ipp1.1.patch
Patch1033:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-avahi-no-threaded.patch
Patch1034:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-ipp-multifile.patch
Patch1035:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-web-devices-timeout.patch
Patch1037:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-synconclose.patch
Patch1038:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-lspp.patch
# End fedora patches

# Fixes for breakages in Fedora patches
Patch1050:	cups-serverbin-compat-for-aarch64-too.patch

# Requires /etc/tmpfiles.d (bug #656566)
Requires:	systemd >= 208
Requires(post):	rpm-helper >= 0.24.1
Requires(preun):	rpm-helper >= 0.24.1
Requires(postun):	rpm-helper
BuildRequires:	htmldoc
BuildRequires:	php-cli
BuildRequires:	xdg-utils
BuildRequires:	acl-devel
BuildRequires:	jpeg-devel
BuildRequires:	krb5-devel
BuildRequires:	openldap-devel
BuildRequires:	openslp-devel
BuildRequires:	pam-devel
BuildRequires:	php-devel >= 5.1.0
BuildRequires:	tiff-devel
%if %{with dnssd}
BuildRequires:	pkgconfig(avahi-compat-libdns_sd)
%endif
BuildRequires:	pkgconfig(dbus-1) >= 0.50
BuildRequires:	pkgconfig(gnutls) >= 3.0
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libusb) < 1.0
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libsystemd)

Requires:	%{name}-common >= %{version}-%{release}
Requires:	net-tools
%if !%{with bootstrap}
Suggests:	avahi
%endif
Requires:	printer-testpages
# Take care that device files are created with correct permissions
Requires:	udev
Requires:	cups-filters
# For desktop menus
Requires:	xdg-utils
%rename		cupsddk-drivers

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

%package	common
Summary:	Common Unix Printing System - Common stuff
License:	GPLv2
Group:		System/Printing
Requires(post,preun): update-alternatives
Requires:	net-tools
# To satisfy LSB/FHS
Provides:	lpddaemon

%description	common
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. It contains the command line utilities for
printing and administration (lpr, lpq, lprm, lpadmin, lpc, ...), man
pages, locales, and a sample configuration file for daemon-less CUPS
clients (%{_sysconfdir}/cups/client.conf).

This package you need for both CUPS clients and servers. 

%define	cupsmajor	2
%define	libcups		%mklibname cups %{cupsmajor}

%package -n	%{libcups}
Summary:	Common Unix Printing System - CUPS library
License:	LGPLv2
Group:		System/Libraries
Obsoletes:	%{_lib}cups3 < 1.6.1-2

%description -n	%{libcups}
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%define	cupscgimajor	1
%define	libcupscgi	%mklibname cupscgi %{cupscgimajor}

%package -n	%{libcupscgi}
Summary:	Common Unix Printing System - CUPSCGI library
License:	LGPLv2
Group:		System/Libraries
Conflicts:	%{libcups} < 1.6.1-2

%description -n	%{libcupscgi}
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%define	cupsimagemajor	2
%define	libcupsimage	%mklibname cupsimage %{cupsimagemajor}

%package -n	%{libcupsimage}
Summary:	Common Unix Printing System - CUPSimage library
License:	LGPLv2
Group:		System/Libraries
Conflicts:	%{libcups} < 1.6.1-2

%description -n	%{libcupsimage}
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%define	cupsmimemajor	1
%define	libcupsmime	%mklibname cupsmime %{cupsmimemajor}

%package -n	%{libcupsmime}
Summary:	Common Unix Printing System - CUPS library
License:	LGPLv2
Group:		System/Libraries
Conflicts:	%{libcups} < 1.6.1-2

%description -n	%{libcupsmime}
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%define	cupsppdcmajor	1
%define	libcupsppdc	%mklibname cupsppdc %{cupsppdcmajor}

%package -n	%{libcupsppdc}
Summary:	Common Unix Printing System - CUPSPPDC library
License:	LGPLv2
Group:		System/Libraries
Conflicts:	%{libcups} < 1.6.1-2

%description -n	%{libcupsppdc}
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%define	devname	%mklibname %{name} -d
%package -n	%{devname}
Summary:	Common Unix Printing System - Development environment "libcups"
License:	LGPLv2
Group:		Development/C
Requires:	%{libcups} >= %{version}-%{release}
Requires:	%{libcupscgi} >= %{version}-%{release}
Requires:	%{libcupsimage} >= %{version}-%{release}
Requires:	%{libcupsmime} >= %{version}-%{release}
Requires:	%{libcupsppdc} >= %{version}-%{release}

Provides:	cups-devel
Obsoletes:	%mklibname %{name}2 -d

%description -n	%{devname}
CUPS 1.4 is fully compatible with CUPS-1.1 machines in the network and
with software built against CUPS-1.1 libraries.

The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This is the development package for
creating additional printer drivers, printing software, and other CUPS
services using the main CUPS library "libcups".

%package -n php-cups
Summary: PHP bindings for the libcups library
Group: Development/PHP

%description -n php-cups
Provides bindings to the functions of libcups, to give direct access

%prep
%setup -q -n %{name}-%{version}%{beta}
%apply_patches

# Let local printers be broadcasted in the local network(s)
perl -p -i -e 's:(Listen\s+)localhost:$1*:' conf/cupsd.conf.in
perl -p -i -e 's:(Browsing\s+On):$1:' conf/cupsd.conf.in
perl -p -i -e 's:(<Location\s+/\s*>):$1\n  Allow \@LOCAL:' conf/cupsd.conf.in

# Allow remote administration in local network (connections are encrypted,
# so no security problem)
perl -p -i -e 's:(<Location\s+/admin(|/conf)\s*>):$1\n  Allow \@LOCAL:' conf/cupsd.conf.in

# Log to the system journal by default (bug #1078781).
sed -i -e 's,^ErrorLog .*$,ErrorLog journal,' conf/cups-files.conf.in

# Let's look at the compilation command lines.
perl -pi -e "s,^.SILENT:,," Makedefs.in

# Set CUPS users and groups
perl -p -i -e 's:(LogLevel\s+.*)$:$1\nGroup lp\nUser lp:' conf/cupsd.conf.in


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


# Load additional tools
cp %{SOURCE1} poll_ppd_base.c
cp %{SOURCE2} lphelp.c
# Load nprint backend
cp %{SOURCE11} nprint
# Load AppleTalk "pap" backend
%setup -q -T -D -a 12 -n %{name}-%{version}%{beta}
# Load the "pap" documentation
bzcat %{SOURCE13} > pap-docu.pdf
# Load the "photo_print" utility
cp %{SOURCE14} photo_print
# Load the "pdfdistiller" utility
sed -i -e 's,/tmp/pdf.log,/dev/null,g' %{SOURCE15} >pdf
chmod +x pdf
# Load the "cjktexttops" filter
cp %{SOURCE16} cjktexttops

# needed by additional SOURCES
aclocal -I config-scripts
autoconf -I config-scripts

%build
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
%configure \
    --with-cupsd-file-perm=0755 \
    --with-log-file-perm=0600 \
%if !%{with dnsd}
    --enable-avahi \
%endif
%if %{debug}
    --enable-debug=yes \
%endif
    --with-dbusdir=%{_sysconfdir}/dbus-1 \
    --enable-threads \
    --enable-gnutls \
    --enable-webif \
    --disable-libpaper \
    --enable-raw-printing \
    --enable-ssl \
    --disable-static \
    --disable-lspp \
    --with-cups-group=lp \
    --with-cups-user=lp \
    --with-docdir=%{_datadir}/cups/doc \
    --with-icondir=%{_datadir}/icons \
    --with-system-groups="lpadmin root" \
    --with-php=%{_bindir}/php \
    --enable-relro \
    --without-xinetd \
    --without-rcdir

# Remove "-s" (stripping) option from "install" command used for binaries
# by "make install"
perl -p -i -e 's:^(\s*INSTALL_BIN\s*=.*)-s:$1:' Makedefs

# Remove hardcoded "chgrp" from Makefiles
perl -p -i -e 's/chgrp/:/' Makefile */Makefile
%make

# Compile additional tools
%{__cc} %{optflags} %{ldflags} -opoll_ppd_base -I. -I./cups poll_ppd_base.c -L./cups -lcups

%if !%{with bootstrap} && %{enable_check}
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
make BUILDROOT=%{buildroot} install


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

# Link dnssd backend as mdns backend
(cd %{buildroot}%{cups_serverbin}/backend && ln -s dnssd mdns)

# Install "photo_print"
install -m 755 photo_print %{buildroot}%{_bindir}

# Install "pdfdistiller"
install -m 755 pdf %{buildroot}%{_prefix}/lib/cups/backend/

# Install "cjktexttops"
install -m 755 cjktexttops %{buildroot}%{_prefix}/lib/cups/filter/

# Install logrotate configuration
install -c -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/logrotate.d/cups

mkdir -p %{buildroot}%{_unitdir}

# Set link to test page in /usr/share/printer-testpages
ln -s %{_datadir}/printer-testpages/testprint.ps %{buildroot}%{_datadir}/cups/data/testprint-mdv.ps
# replace no longer supported testprint banner format with our own
ln -sf testprint-mdv.ps %{buildroot}%{_datadir}/cups/data/testprint

# Install startup script
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE18} %{buildroot}%{_sysconfdir}/sysconfig/cups
rm -f %{buildroot}%{_sysconfdir}/init.d/cups

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
pushd %{buildroot}%{_bindir}
  mv lpr lpr-cups
  mv lpq lpq-cups
  mv lprm lprm-cups
  mv lp lp-cups
  mv cancel cancel-cups
  mv lpstat lpstat-cups
popd
pushd %{buildroot}%{_sbindir}
  mv accept accept-cups
  mv disable disable-cups
  mv enable enable-cups
  mv lpc lpc-cups
  mv lpmove lpmove-cups
  mv reject reject-cups
popd
pushd %{buildroot}%{_mandir}/man1
  mv lprm.1 lprm-cups.1
  mv lp.1 lp-cups.1
  mv cancel.1 cancel-cups.1
  mv lpstat.1 lpstat-cups.1
popd
pushd %{buildroot}%{_mandir}/man8
  mv accept.8 accept-cups.8
  mv disable.8 disable-cups.8
  mv enable.8 enable-cups.8
  mv lpc.8 lpc-cups.8
  mv lpmove.8 lpmove-cups.8
  mv reject.8 reject-cups.8
popd
ln -sf %{_sbindir}/accept-cups %{buildroot}%{_sbindir}/reject-cups
ln -sf %{_sbindir}/accept-cups %{buildroot}%{_sbindir}/cupsdisable
ln -sf %{_sbindir}/accept-cups %{buildroot}%{_sbindir}/cupsenable

# Install missing headers (Thanks to Oden Eriksson)
install -m644 cups/debug-private.h  %{buildroot}%{_includedir}/cups/
install -m644 cups/string-private.h %{buildroot}%{_includedir}/cups/
install -m644 config.h %{buildroot}%{_includedir}/cups/

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

# install /usr/lib/tmpfiles.d/cups.conf (bug #656566)
mkdir -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/cups.conf <<EOF
d %{_localstatedir}/run/cups 0755 root lp -
d %{_localstatedir}/run/cups/certs 0511 lp lp -
EOF

# /usr/lib/tmpfiles.d/cups-lp.conf (bug #812641)
cat > %{buildroot}%{_tmpfilesdir}/cups-lp.conf <<EOF
# This file is part of cups.
#
# Legacy parallel port character device nodes, to trigger the
# auto-loading of the kernel module on access.
#
# See tmpfiles.d(5) for details

c /dev/lp0 0660 root lp - 6:0
c /dev/lp1 0660 root lp - 6:1
c /dev/lp2 0660 root lp - 6:2
c /dev/lp3 0660 root lp - 6:3
EOF

# Prefer xdg-utils rather than htmlview (kde one)
sed -i s/htmlview/xdg-open/ %{buildroot}%{_datadir}/applications/*.desktop

## Hide desktop file
chmod 0755 %{buildroot}%{_datadir}/applications/cups.desktop
echo -e '\nHidden=true' >> %{buildroot}%{_datadir}/applications/cups.desktop

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

# Create /dev/lp* nodes to make usblp happy
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
install -c -m 644 %{SOURCE19} %{buildroot}%{_sysconfdir}/udev/rules.d/
# Fix USB printers permissions and groups
install -c -m 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/udev/rules.d/

# Remove stuff that's also in cups-filters
rm -f %{buildroot}%{_datadir}/cups/banners/{classified,confidential,secret,standard,topsecret,unclassified}
rm -f %{buildroot}%{_datadir}/cups/data/testprint

# (tpg) rename units to meet old name scheme
mv %{buildroot}%{_unitdir}/org.cups.cupsd.path %{buildroot}%{_unitdir}/cups.path
mv %{buildroot}%{_unitdir}/org.cups.cupsd.service %{buildroot}%{_unitdir}/cups.service
mv %{buildroot}%{_unitdir}/org.cups.cupsd.socket %{buildroot}%{_unitdir}/cups.socket
mv %{buildroot}%{_unitdir}/org.cups.cups-lpd.socket %{buildroot}%{_unitdir}/cups-lpd.socket
mv %{buildroot}%{_unitdir}/org.cups.cups-lpd@.service %{buildroot}%{_unitdir}/cups-lpd@.service
sed -i -e "s,org.cups.cupsd,cups,g" %{buildroot}%{_unitdir}/cups.service

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
chgrp -R lp %{_sysconfdir}/cups %{_var}/*/cups

# We can't enforce this. Bug #35993
for d in /opt/share/ppd /opt/lib/printdriver /usr/local/share/ppd /usr/local/lib/printdriver
do
  [ ! -e $d ] && mkdir -p $d || :
done
# End of 28383

%post common
# The lpc updates-alternative links were not correctly set in older CUPS
# packages, therefore remove the entry before making a new one when updating
%{_sbindir}/update-alternatives --remove lpc %{_sbindir}/lpc-cups || :
# Set up update-alternatives entries
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
%config(noreplace) %attr(-,root,lp) %{_sysconfdir}/cups/cupsd.conf
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/cups/cups-files.conf
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/cups/cups-files.conf.default
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/cups/snmp.conf.default
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/sysconfig/cups
%ghost %config(noreplace) %{_sysconfdir}/cups/printers.conf
%ghost %config(noreplace) %{_sysconfdir}/cups/classes.conf
%attr(-,root,sys) %{_sysconfdir}/cups/cupsd.conf.default
#%config(noreplace) %attr(644,root,lp) %{_sysconfdir}/cups/mime.convs
#%config(noreplace) %attr(644,root,lp) %{_sysconfdir}/cups/mime.types
%config(noreplace) %attr(-,root,lp) %{_sysconfdir}/cups/ppd
%config(noreplace) %attr(-,root,lp) %{_sysconfdir}/cups/ssl
%config(noreplace) %attr(-,root,lp) %{_sysconfdir}/cups/snmp.conf
%config(noreplace) %attr(-,root,lp) %{_sysconfdir}/dbus*/system.d/cups.conf
%{_tmpfilesdir}/*.conf
%{_unitdir}/cups*.path
%{_unitdir}/cups*.service
%{_unitdir}/cups*.socket
%config(noreplace) %{_sysconfdir}/pam.d/cups
%config(noreplace) %{_sysconfdir}/logrotate.d/cups
%{_sysconfdir}/udev/rules.d/*
%dir %{_prefix}/lib/cups
%{_prefix}/lib/cups/cgi-bin
%{_prefix}/lib/cups/daemon
%{_prefix}/lib/cups/notifier
%{_prefix}/lib/cups/filter
%{_prefix}/lib/cups/monitor
%dir %{_prefix}/lib/cups/backend
%if %{with dnssd}
%{_prefix}/lib/cups/backend/dnssd
%endif
%{_prefix}/lib/cups/backend/http
%{_prefix}/lib/cups/backend/https
%{_prefix}/lib/cups/backend/ipp
%{_prefix}/lib/cups/backend/ipps
%{_prefix}/lib/cups/backend/lpd
%{_prefix}/lib/cups/backend/mdns
%{_prefix}/lib/cups/backend/nprint
%{_prefix}/lib/cups/backend/pap
#{_prefix}/lib/cups/backend/parallel
#%{_prefix}/lib/cups/backend/scsi
%{_prefix}/lib/cups/backend/snmp
%{_prefix}/lib/cups/backend/socket
%{_prefix}/lib/cups/backend/usb
%{_prefix}/lib/cups/backend/pdf
%dir %{_prefix}/lib/cups/driver
%{_datadir}/cups
%attr(0755,root,lp) %{_var}/log/cups
# Set ownerships of spool directory which is normally done by 'make install'
# Because RPM does 'make install' as normal user, this has to be done here
%dir %attr(0710,root,lp) %{_var}/spool/cups
%dir %attr(01770,root,lp) %{_var}/spool/cups/tmp
%dir %attr(775,root,lp) %{_var}/cache/cups
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


%files common
%dir %config(noreplace) %attr(-,lp,lp) %{_sysconfdir}/cups
%ghost %config(noreplace) %attr(-,lp,lp) %{_sysconfdir}/cups/client.conf
%{_sbindir}/*
%{_bindir}/*cups
%if %{with dnssd}
%{_bindir}/ippfind
%endif
%{_bindir}/ipptool
#%{_bindir}/lphelp
%{_bindir}/lpoptions
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

%files -n %{libcups}
%{_libdir}/libcups.so.%{cupsmajor}*

%files -n %{libcupsimage}
%{_libdir}/libcupsimage.so.%{cupsimagemajor}*

%files -n %{libcupscgi}
%{_libdir}/libcupscgi.so.%{cupscgimajor}*

%files -n %{libcupsmime}
%{_libdir}/libcupsmime.so.%{cupsmimemajor}*

%files -n %{libcupsppdc}
%{_libdir}/libcupsppdc.so.%{cupsppdcmajor}*

%files -n %{devname}
%dir %{_includedir}/cups
%{_includedir}/cups/*
%{_libdir}/*.so
%{_bindir}/cups-config

%files -n php-cups
%{_sysconfdir}/php.d/A20_cups.ini
