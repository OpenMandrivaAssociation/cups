# {_exec_prefix}/lib/cups is correct, even on x86_64.
# It is not used for shared objects but for executables.
# It's more of a libexec-style ({_libexecdir}) usage,
# but we use lib for compatibility with 3rd party drivers (at upstream request).
%global cups_serverbin %{_exec_prefix}/lib/cups

# Turning this on lets CUPS to be built in debug mode (with debugger symbols)
%define debug 0
%define enable_check 0

# Define to %nil for release builds
%define beta rc1

%bcond_with	bootstrap
%if !%{with bootstrap}
%bcond_without	systemd
%endif

Summary:	Common Unix Printing System - Server package
Name:		cups
Version:	1.7
%if "%beta" != ""
Release:	0.%beta.1
%else
Release:	2
%endif
Source0:	http://cups.org/software/%version%beta/cups-%version%beta-source.tar.bz2
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
Source15:	http://printing.kde.org/downloads/pdfdistiller
Source16:	cjktexttops
Source17:	cups.service
# Nice level for now. bug #16387
Source18:	cups.sysconfig
# udev rules for setting symlinks needed if the usblp module is loaded
Source19:	10-cups_device_links.rules

Patch1:		cups-dbus-utf8.patch
Patch2:		cups-systemd-socket.patch
Patch10:	cups-1.4.0-recommended.patch
# fhimpe: make installed binary files writeable as root
Patch32:	cups-1.5.3-permissions.patch

#fedora patches all shifted by 1000
Patch1001:	cups-no-gzip-man.patch
Patch1002:	cups-system-auth.patch
Patch1003:	cups-multilib.patch
Patch1005:	cups-banners.patch
Patch1006:	cups-serverbin-compat.patch
Patch1007:	cups-no-export-ssllibs.patch
Patch1008:	cups-direct-usb.patch
Patch1009:	cups-lpr-help.patch
Patch1010:	cups-peercred.patch
Patch1011:	cups-pid.patch
Patch1012:	cups-eggcups.patch
Patch1014:	cups-driverd-timeout.patch
Patch1015:	cups-strict-ppd-line-length.patch
Patch1016:	cups-logrotate.patch
Patch1017:	cups-usb-paperout.patch
Patch1019:	cups-res_init.patch
Patch1020:	cups-filter-debug.patch
Patch1021:	cups-uri-compat.patch
Patch1023:	cups-str3382.patch
#NOT_IN_FEDPatch1024: cups-str3947.patch
#same as mdv patch cups-1.4-permissions.patch
#Patch1025: cups-0755.patch
Patch1027:	cups-hp-deviceid-oid.patch
Patch1028:	cups-dnssd-deviceid.patch
Patch1029:	cups-ricoh-deviceid-oid.patch
Patch1032:	cups-lpd-manpage.patch

# selinux
#Patch1100:	cups-lspp.patch

# Requires /etc/tmpfiles.d (bug #656566)
Requires:	systemd-units >= 13
Requires(post):	systemd-units
Requires(preun):systemd-units
Requires(postun): systemd-units
Requires(post):	rpm-helper >= 0.24.1
Requires(preun):rpm-helper >= 0.24.1

BuildRequires:	htmldoc
BuildRequires:	php-cli
BuildRequires:	xdg-utils
BuildRequires:	xinetd
BuildRequires:	acl-devel
BuildRequires:	jpeg-devel
BuildRequires:	krb5-devel
BuildRequires:	openldap-devel
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
%if !%{with bootstrap}
BuildRequires:	poppler
%if %{with systemd}
BuildRequires:	systemd-units
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(systemd)
%endif
%endif

Requires:	%{name}-common >= %{version}-%{release}
Requires:	net-tools
%if !%{with bootstrap}
Requires:	poppler
Suggests:	avahi
%endif
Requires:	printer-testpages
# Take care that device files are created with correct permissions
Requires:	udev 
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
%setup -q -n %name-%version%beta
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
%setup -q -T -D -a 12 -n %{name}-%{version}%beta
# Load the "pap" documentation
bzcat %{SOURCE13} > pap-docu.pdf
# Load the "photo_print" utility
cp %{SOURCE14} photo_print
# Load the "pdfdistiller" utility
cp %{SOURCE15} pdf
# Load the "cjktexttops" filter
cp %{SOURCE16} cjktexttops
# systemd service
#cp %{SOURCE17} cups.service

# needed by additional SOURCES
aclocal
autoconf

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
    --with-php=%_bindir/php \
    --enable-relro \
%if !%{with bootstrap}
    --with-pdftops=%{_bindir}/pdftops
%endif

# Remove "-s" (stripping) option from "install" command used for binaries
# by "make install"
perl -p -i -e 's:^(\s*INSTALL_BIN\s*=.*)-s:$1:' Makedefs

# Remove hardcoded "chgrp" from Makefiles
perl -p -i -e 's/chgrp/:/' Makefile */Makefile
%make 

# Compile additional tools
gcc %{optflags} %{ldflags} -opoll_ppd_base -I. -I./cups poll_ppd_base.c -L./cups -lcups
#no longer compiles
#gcc %{optflags} %{ldflags} -olphelp -I. -I./cups lphelp.c -L./cups -lcups

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

%if %{with systemd}
# systemd
#mkdir -p %{buildroot}/lib/systemd/system
#install -m644 cups.service %{buildroot}/lib/systemd/system
%endif

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
  mv lpr.1 lpr-cups.1
  mv lpq.1 lpq-cups.1
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

# Remove links to the startup script, we make our own ones with chkconfig
rm -r %{buildroot}%{_sysconfdir}/rc?.d/[SK]*

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

# install /usr/lib/tmpfiles.d/cups.conf (bug #656566)
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
cat > %{buildroot}%{_prefix}/lib/tmpfiles.d/cups.conf <<EOF
d %{_localstatedir}/run/cups 0755 root lp -
d %{_localstatedir}/run/cups/certs 0511 lp sys -
EOF

# /usr/lib/tmpfiles.d/cups-lp.conf (bug #812641)
cat > %{buildroot}%{_prefix}/lib/tmpfiles.d/cups-lp.conf <<EOF
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
mkdir -p %buildroot%_sysconfdir/udev/rules.d
install -c -m 644 %SOURCE19 %buildroot%_sysconfdir/udev/rules.d/

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
%config(noreplace) %attr(-,root,root) %_sysconfdir/cups/cups-files.conf
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
%{_prefix}/lib/tmpfiles.d/cups.conf
%{_prefix}/lib/tmpfiles.d/cups-lp.conf
%config(noreplace) %{_sysconfdir}/pam.d/cups
%config(noreplace) %{_sysconfdir}/logrotate.d/cups
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/xinetd.d/cups-lpd
%_sysconfdir/udev/rules.d/*
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
#{_prefix}/lib/cups/backend/parallel
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
%if %{with systemd}
/lib/systemd/system/cups.*
%endif

%files common
%dir %config(noreplace) %attr(-,lp,sys) %{_sysconfdir}/cups
%ghost %config(noreplace) %attr(-,lp,sys) %{_sysconfdir}/cups/client.conf
%{_sbindir}/*
%{_bindir}/*cups
%{_bindir}/ippfind
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
%dir %{multiarch_includedir}/cups
%{multiarch_includedir}/cups/*
%{_libdir}/*.so
%{_bindir}/cups-config

%files -n php-cups
%_sysconfdir/php.d/A20_cups.ini

%changelog
* Fri Jan  4 2013 Per Øyvind Karlsen 1.5.4-3
- always remove '-s' argument for 'install' to prevent binaries getting
  stripped by other than find-debuginfo.sh
- cleanups
- change Requires on 'update-alternatives' to Requires(post,preun) for
  cups-common subpkg

* Wed Sep 26 2012 akdengi 1.5.4-1
- update to 1.5.4
- don't use portreserve
- ship tmpfiles to support legacy parallel printers
- drop sysinit support


* Tue May 15 2012 Matthew Dawkins <mattydaw@mandriva.org> 1.5.3-1
+ Revision: 799051
- rediff'd p32 from mdv
- sync'd patchset with fedora
- new version 1.5.3

* Sat May 12 2012 Matthew Dawkins <mattydaw@mandriva.org> 1.5.2-1
+ Revision: 798495
- new version 1.5.2
- sync'd patchset with fedora

* Mon Mar 19 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.5.0-4
+ Revision: 785746
- Build for gnutls 3.x
- Fix missing files when building with current systemd
- Fix BuildRequires: line, nothing provides krb-devel these days

* Wed Feb 01 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.5.0-3
+ Revision: 770462
- Adjust build requirements. cups needs libusb 0.x, not 1.x for now

* Thu Dec 22 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-2
+ Revision: 744391
- rebuilt against libtiff.so.5

* Thu Dec 01 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.5.0-1
+ Revision: 735848
- new version 1.5.0
- sync'd all patches to fedora
- sync'd ubuntu patch do-not-broadcast-with-hostnames.patch
- suse patch dropped by suse cups-1.4.4-str3461-1.4.reverted.patch
- ru lang patch still needs to be rediff'd
- ubuntu/debian patch dropped cups-1.4.3-both-usblp-and-libusb.patch
- Source2 lphelp no longer compiles
- check disabled for now
- more cleanup to spec
- use apply_patches
- converted BRs to pkgconfig provides
- rebuild
- major spec clean (hopefully easier to upgrade now)
- removed long commented out if 0 code
- removed defattr, mkrel, clean section, BuildRoot
- reimplemented find_lang for maintainability
- dropped major from devel pkg
- removed old ldconfig scriptlets
- removed long unused svnsnapshot build options
- simplified debug build, and disabled again
- bracketed systemd build with bootstrap
- disabled static build
- removed old conflicts, provides, & dup requires

* Wed Nov 09 2011 vsinitsyn <vsinitsyn> 1.4.8-6
+ Revision: 729306
- Updated Russian translation

* Mon Oct 10 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.8-5
+ Revision: 704068
- sync with MDVSA-2011:147

* Thu Sep 29 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.8-4
+ Revision: 701851
- disable bootstrap

* Mon Sep 12 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.8-3
+ Revision: 699575
- disable check when in boostrap build
- export Mdv's LDFLAGS
- enable relro
- enable bootstrap for poppler
- rebuild for new libpng-1.5

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Rebuild against new libpng

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.8-2
+ Revision: 696366
- rebuilt for php-5.3.8

* Tue Aug 23 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.8-1
+ Revision: 696273
- 1.4.8

* Mon Aug 22 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-6
+ Revision: 696094
- rebuilt for php-5.3.7

* Sat May 14 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.4.6-5
+ Revision: 674598
- Fix always failing message, thanks to J.A.Magall?\195?\179n message on cooker.

* Sat May 14 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.4.6-4
+ Revision: 674386
- Cups-devel requires gnutls-devel, otherwise cups-config fails

* Fri May 06 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.4.6-3
+ Revision: 670658
- Properly build systemd support

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-2
+ Revision: 661647
- multiarch fixes

  + Eugeni Dodonov <eugeni@mandriva.com>
    - Added initial draft of cups systemd unit.
    - Remove dead and prehistoric code.

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-1mdv2011.0
+ Revision: 630336
- 1.4.6

* Sat Nov 13 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.5-1mdv2011.0
+ Revision: 597089
- 1.4.5
- rediffed P1012 (the avahi patch)

* Tue Oct 26 2010 Claudio Matsuoka <claudio@mandriva.com> 1.4.4-4mdv2011.0
+ Revision: 589545
- Apply SUSE patch to revert CUPS STR #3461 (fixes bug #61009)

* Thu Oct 21 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.4-3mdv2011.0
+ Revision: 587086
- rebuild for latest openssl
- use standard macro to allow automatic update
- renumber the patches to match fedora, so as to make comparaison easier

* Fri Sep 10 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.4-2mdv2011.0
+ Revision: 577108
- ensure build with debug symbols by default

* Thu Sep 09 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.4-1mdv2011.0
+ Revision: 577003
- new version
- rediff patches 35, 1015, 1017
- drop patches 1038, 1039, 1040, 1041 (merged upstream)

* Fri Jun 18 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-3mdv2010.1
+ Revision: 548314
- added some upstream security patches

* Thu Jun 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.3-2mdv2010.1
+ Revision: 548231
- add krb5-devel build dependency

* Thu Apr 01 2010 Tiago Salem <salem@mandriva.com.br> 1.4.3-1mdv2010.1
+ Revision: 530727
- reenable the id po file

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - new version
    - rediff usb patch
    - fix some tests

* Fri Mar 26 2010 Tiago Salem <salem@mandriva.com.br> 1.4.2-6mdv2010.1
+ Revision: 527859
- oops, forgot to remove some lines concerning the last commit
- move udev patch to system-config-printer-dev package, as we need the right permission on devices even when cups is not installed yet
- bump release

* Fri Mar 26 2010 Tiago Salem <salem@mandriva.com.br> 1.4.2-5mdv2010.1
+ Revision: 527675
- fix udev rule number 69 to properly match usb printers (fix #56298)
- bump release

* Mon Jan 11 2010 Funda Wang <fwang@mandriva.org> 1.4.2-4mdv2010.1
+ Revision: 489461
- rebuild for new libjpegv8

* Wed Dec 09 2009 Tiago Salem <salem@mandriva.com.br> 1.4.2-3mdv2010.1
+ Revision: 475699
- re-add patch to keep compatibility with previously configured printers.
- bump relase

* Wed Dec 09 2009 Tiago Salem <salem@mandriva.com.br> 1.4.2-2mdv2010.1
+ Revision: 475605
- disable the usblp load in the initscript, as this modules does not exist aymore
- disable usblp + libusb patch
- bump release

* Tue Nov 10 2009 Tiago Salem <salem@mandriva.com.br> 1.4.2-1mdv2010.1
+ Revision: 464296
- cups 1.4.2

* Fri Oct 30 2009 Gustavo De Nardin <gustavodn@mandriva.com> 1.4.1-12mdv2010.0
+ Revision: 460224
- fixed "lp user fix" udev rules so they do not apply to every plugged device

* Tue Oct 27 2009 Gustavo De Nardin <gustavodn@mandriva.com> 1.4.1-11mdv2010.0
+ Revision: 459603
- only run setfacl when the device is added

* Mon Oct 26 2009 Gustavo De Nardin <gustavodn@mandriva.com> 1.4.1-10mdv2010.0
+ Revision: 459433
- Let printers have an ACL allowing rw for user lp, as our CUPS runs
  backends as lp:sys (bug 49407).

* Mon Oct 19 2009 Gustavo De Nardin <gustavodn@mandriva.com> 1.4.1-9mdv2010.0
+ Revision: 458294
- stop using libpaper, Fedora also doesn't use it, seems unneeded anymore

* Sat Oct 17 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.1-8mdv2010.0
+ Revision: 457996
- Add no-hostname-broadcast patch from Ubuntu, Launchpad #449586: Do not
  use hostnames for broadcasting print queues and managing print queues
  broadcasted from other servers by default. Many networks do not have
  valid host names for all machines
- Update usblp-libusp patch from Ubuntu: Fixed a bug of modifying the
  URI of the current print queue when comparing it with discovered
  URIs. Made the USB backend also compatible with URIS generated by old
  versions of CUPS, without serial number or with "serial=?"
  (Launchpad #450513)
- Enable avahi support; lower error to warning in avahi patch when avahi
  is not running, in order to make the test suite succeed without
  running avahi (from Debian/Ubuntu)

* Wed Oct 14 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.1-7mdv2010.0
+ Revision: 457453
- Sync with Fedora:
  * Fixed orientation of page labels when printing text in landscape
    mode (RH bug #520141, STR #3334).
  * Replace str3356 patch by new patch approved by upstream

* Mon Oct 05 2009 Frederic Crozat <fcrozat@mandriva.com> 1.4.1-6mdv2010.0
+ Revision: 454122
- No longer depends on dynamic

* Sun Oct 04 2009 Funda Wang <fwang@mandriva.org> 1.4.1-5mdv2010.0
+ Revision: 453332
- obsoletes cupsddk also

* Sun Oct 04 2009 Funda Wang <fwang@mandriva.org> 1.4.1-4mdv2010.0
+ Revision: 453318
- rebuild

* Sat Oct 03 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.1-3mdv2010.0
+ Revision: 452766
- Fix BuildRequires, fixing build with usblp compatibility patch
- Remove build fix patch: included in usblp compatibility patch
- Add Fedora patch: Don't use cached PPD for raw queue (RH bug #526405)
- Add Debian patch: Use both usblp and libusb, to prevent trouble if
  kernel usblp module is loaded. Disabled for now because of build
  problems on x86_64

* Thu Sep 24 2009 Olivier Blin <blino@mandriva.org> 1.4.1-2mdv2010.0
+ Revision: 448232
- allow to bootstrap build by breaking build dep loop
  gtk->cups->poppler->gtk (from Arnaud Patard)

* Mon Sep 14 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.1-1mdv2010.0
+ Revision: 440972
- Add patch to fix build on x86_64 due to conflicting declarations
- Dont't run cups with nice level 14 by default: makes no sense on
  servers, no proof that it helps interactivity on desktops, and should
  not be needed with recent kernels anyway
- Update avahi patch from Fedora: Fixes the dnssd backend so that it
  only reports devices once avahi resolution has completed.  This
  makes it report Device IDs
- Install logrotate configuration
- Update to new version 1.4.1
- Remove patches for issues fixed upstream
- Test-suite is now working again

* Wed Sep 02 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.0-2mdv2010.0
+ Revision: 426016
- Merge with cups from testing branch:
  * Update to cups 1.4
  * Add patch fixing permisions of installed files
  * Add Fedora patches
  * Rediff recommended patch
  * Remove old, unneeded patches

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.10-4mdv2010.0
+ Revision: 416592
- rebuilt against libjpeg v7

* Sat May 30 2009 Funda Wang <fwang@mandriva.org> 1.3.10-3mdv2010.0
+ Revision: 381443
- build with latest gnutls 2.8

* Wed Apr 22 2009 Gustavo De Nardin <gustavodn@mandriva.com> 1.3.10-2mdv2009.1
+ Revision: 368615
- Make cups run usb backend as root to workaround device permissions issues (bug #49407)

* Fri Apr 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.10-1mdv2009.1
+ Revision: 367896
- use poppler as the backend and fix deps
- enable acl support
- disable "make test" for now due to unknown problems in the test suite
- fix build deps (poppler + ghostscript)
- added P31 from debian in an attempt to make the tests pass
- 1.3.10

* Wed Jan 21 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.3.9-4mdv2009.1
+ Revision: 332230
- Patched pdfdistiller to prevent CVE-2008-5377 (arbitrary local file overwrite
  via symlinks).

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.9-3mdv2009.1
+ Revision: 318064
- drop the CVE-2008-1373 patch (P19), it's fixed since 1.3.7,
  spotted by fhimpe

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.9-2mdv2009.1
+ Revision: 318055
- rediffed one fuzzy patch

* Fri Oct 10 2008 Frederik Himpe <fhimpe@mandriva.org> 1.3.9-1mdv2009.0
+ Revision: 291529
- Update to new version 1.3.9 (fixes 3 integer overflow security
  bugs)

* Wed Jul 30 2008 Frederik Himpe <fhimpe@mandriva.org> 1.3.8-1mdv2009.0
+ Revision: 256478
- New upstream version 1.3.8
- Remove str2086, str2865 and CVE-2008-1722 patches: all of them
  were integrated upstream
- Add new Indonesian translation to file list

  + Tiago Salem <salem@mandriva.com.br>
    - fix bug #41073 by using an upstream patch.
    - bump release
    - fix for crash when enabling printers with missing backends. (#41073)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - drop useless ldconfig in %%preun (it is already correctly done in %%postun)

* Thu May 22 2008 Frederik Himpe <fhimpe@mandriva.org> 1.3.7-2mdv2009.0
+ Revision: 210108
- Add peercred.patch from Fedora to fix build with gcc 4.3
- Do the lib64 substitution also on the configure script, because the
  one done in the m4 file has no effect if configure is not regenerated
  (which is currently the case)

* Sun May 18 2008 Frederik Himpe <fhimpe@mandriva.org> 1.3.7-1mdv2009.0
+ Revision: 208559
- Add patch from Fedora to fix security problem CVE-2008-1722
- Try to get the licenses right
- Enable test suite, add upstream patch to fix test suite failure
  (http://www.cups.org/str.php?L2806)
- Remove CVE-2008-0047.patch, cups 1.3.7 already includes it
- Remove cups-1.3.6-disconnected-usb-increases-cpu-usage.patch, an
  equivalent fix was integrated in Cups 1.3.7
- Update to version 1.3.7

* Mon Apr 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.6-6mdv2009.0
+ Revision: 196241
- really attempt to fix #23846 (portmap randomly bind ports used by other application)

* Tue Apr 01 2008 Tiago Salem <salem@mandriva.com.br> 1.3.6-5mdv2008.1
+ Revision: 191434
- Patch for CVE-2008-1373.

* Wed Mar 26 2008 Frederik Himpe <fhimpe@mandriva.org> 1.3.6-4mdv2008.1
+ Revision: 190239
- Patch for CVE-2008-0047 (remotely exploitable buffer overflow),
  taken from Debian

* Tue Mar 25 2008 Tiago Salem <salem@mandriva.com.br> 1.3.6-3mdv2008.1
+ Revision: 190046
- fix for bug #38820
- bump release

* Sun Mar 16 2008 Funda Wang <fwang@mandriva.org> 1.3.6-2mdv2008.1
+ Revision: 188140
- locales should not be installed at every case

* Mon Feb 25 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.3.6-1mdv2008.1
+ Revision: 174766
- Remove unapplied patches and make rpmlint happy.
- New upstream: 1.3.6. Closes: #38032
- Added patch str2703.

* Wed Jan 30 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.3.5-5mdv2008.1
+ Revision: 160417
- Really don't put /usr/local dirs under %%files section.

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 1.3.5-4mdv2008.1
+ Revision: 157242
- rebuild with fixed %%serverbuild macro

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - Bunzip text sources.
    - Match owners according to cupsd. Closes: #32330

* Sun Jan 13 2008 Funda Wang <fwang@mandriva.org> 1.3.5-3mdv2008.1
+ Revision: 150450
- rebuild against latest gnutls

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3.5-2mdv2008.1
+ Revision: 137455
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 19 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.3.5-1mdv2008.1
+ Revision: 134898
- New upstream: 1.3.5
- Removed patch CVE-2007-4352-5392-5393: already applied.

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 10 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.3.4-4mdv2008.1
+ Revision: 116986
- Do not check for errors while creating /usr/local/lib/printdriver
  Closes: #35993

* Tue Nov 20 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.3.4-3mdv2008.1
+ Revision: 110713
- Added patch for cups-1.3.0-CVE-2007-{4352,5392,5393}

* Sat Nov 17 2007 Funda Wang <fwang@mandriva.org> 1.3.4-2mdv2008.1
+ Revision: 109291
- rebuild for new lzma

* Thu Nov 01 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.3.4-1mdv2008.1
+ Revision: 104391
- New upstream: 1.3.4
- Fix the enable of raw printing by default. Closes: #34614

* Wed Oct 10 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.3.3-1mdv2008.1
+ Revision: 96910
- Only rebuild autotools if we are using a snapshot.
- Removed patch str2472: It's already applied on this version.
- New upstream: 1.3.3

* Wed Sep 26 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.3.0-3mdv2008.0
+ Revision: 93180
- Fix icondir on configure.
- Replay svn_corrupted commit 150560:
  - Added support for LSB 3.2. Closes: #28383

* Thu Sep 13 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.3.0-2mdv2008.0
+ Revision: 85025
- Do not force requires on xinetd, as it's not used by default.

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 1.3.0-1mdv2008.0
+ Revision: 69816
- fix build
- kill file require on update-alternatives

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix RPM GROUPS

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - Added patch str2472: adds fallbacks in case browser-supplied languages are
      not found.
    - New upstream: 1.3.0
    - Rediffed recommended patch.

* Fri Aug 10 2007 David Walluck <walluck@mandriva.org> 1.2.12-6mdv2008.0
+ Revision: 61627
- remove newline from beginning of %%description tags (shows up in, e.g., `rpm -qi')

* Fri Aug 10 2007 Funda Wang <fwang@mandriva.org> 1.2.12-5mdv2008.0
+ Revision: 61565
- no hplip service any more
- use %%_extension for man pages
- man-pages are lzma-ed

* Wed Jul 25 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.2.12-4mdv2008.0
+ Revision: 55266
- Move cups-config back to the lib-devel package.
  http://bugzilla.gnome.org/show_bug.cgi?id=459732

* Tue Jul 24 2007 David Walluck <walluck@mandriva.org> 1.2.12-3mdv2008.0
+ Revision: 55055
- fix a few instances of /etc and /var that were not macros
- fix changing of perms in scriptlets which should be done in %%files (and causes rpm -V to fail)
- remove echo in %%post which should not be done

* Fri Jul 13 2007 Funda Wang <fwang@mandriva.org> 1.2.12-2mdv2008.0
+ Revision: 51851
- New version

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 1.2.11-2mdv2008.0
+ Revision: 45162
- using new serverbuild macro (-fstack-protector-all)

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - Do not overwrite snmp backend anymore: the new upstream one is newer than
      ours and also fixes the related bug.

* Tue May 15 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.2.11-1mdv2008.0
+ Revision: 26962
- New upstream: 1.2.11


* Tue Apr 03 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.2.10-2mdv2007.1
+ Revision: 150418
- Added patch recommended: patch away the removal of the Recommended tag.

* Wed Mar 21 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.2.10-1mdv2007.1
+ Revision: 147258
- New bugfixes upstream: 1.2.10

* Sat Mar 17 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.2.9-1mdv2007.1
+ Revision: 145647
- New upstream 1.2.9 which contains security fixes.

* Mon Mar 12 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.2.7-2mdv2007.1
+ Revision: 141961
- Release bump.
- Prefer xdg-open (xdg-utils) than html-view (kde only) for desktop menus.
  Closes: #29202
- Added /etc/sysconfig/cups to files section.
- Nice cups daemon. Closes: #16387
- Bunzip startup script.

* Fri Nov 24 2006 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.2.7-1mdv2007.1
+ Revision: 86921
- New upstream: 1.2.7
- Removed all unused and commented patches.
- Removed patch 'r5958-bugfixes': already applied.
- Import cups

* Thu Sep 14 2006 Till Kamppeter <till@mandriva.com> 1.2.3-5mdv2007.0
- Overtaken upstream bug fix patch from Debian (Patch 38: "All
  Documents" link in on-line help was missing a trailing slash, job
  history with Polish web interface, "Reprint job" button did not
  work, daemon did not always report printer or job events properly,
  daemon did not respect backend error codes, problems with UTF-8 in
  job names and on the command line, custom page size problem).
- Removed patch 36 and 37 (part of patch 38 now).

* Thu Sep 14 2006 Till Kamppeter <till@mandriva.com> 1.2.3-4mdv2007.0
- Added missing BuildRequires for image and directory service support.

* Thu Sep 14 2006 Till Kamppeter <till@mandriva.com> 1.2.3-3mdv2007.0
- It sometimes happens that lpstat lets the CUPS daemon fall into an 
  infinite loop. Patch 36 and 37, proposed by Mike Sweet on
  http://www.cups.org/str.php?L1968 should fix the problem (should fix bug
  25186).
- If there is a directory named /usr/lib64/cups, rename it to
  /usr/lib/cups and let /usr/lib64/cups be a symlink (bug 25517).

* Wed Sep 06 2006 Till Kamppeter <till@mandriva.com> 1.2.3-2mdv2007.0
- Added "Requires: cups-common" to the libcups-devel subpackage to
  assure that cups-config is present.

* Thu Aug 31 2006 Till Kamppeter <till@mandriva.com> 1.2.3-1mdv2007.0
- Updated to CUPS 1.2.3 (Tons of bug fixes, see
  http://www.cups.org/articles.php?L407).
- Simplified conditional build for MDV 2006/Corporate 4 and MDV 2007
  (Thanks to Olivier Thauvin).

* Wed Aug 09 2006 Till Kamppeter <till@mandriva.com> 1.2.2-4mdv2007.0
- Updated PAM configuration file (bug 24199).

* Sat Aug 05 2006 Till Kamppeter <till@mandriva.com> 1.2.2-3mdv2007.0
- Several fixes on the "snmp" network printer autodiscovery backend.

* Thu Aug 03 2006 Frederic Crozat <fcrozat@mandriva.com> 1.2.2-2mdv2007.0
- Rebuild with latest dbus

* Thu Jul 20 2006 Till Kamppeter <till@mandriva.com> 1.2.2-1mdv2007.0
- Updated to CUPS 1.2.2 (Tons of bug fixes, see
  http://www.cups.org/articles.php?L397).

* Wed Jul 05 2006 Till Kamppeter <till@mandriva.com> 1.2.1-4mdv2007.0
- Uncompressed patches.

* Wed Jul 05 2006 Till Kamppeter <till@mandriva.com> 1.2.1-3mdv2007.0
- Removed absolute paths from /etc/pam.d/cups (bug 22960).

* Thu Jun 22 2006 Laurent MONTEL <lmontel@mandriva.com> 1.2.1-2
- Rebuild

* Tue May 23 2006 Till Kamppeter <till@mandriva.com> 1.2.1-1mdk
- Updated to CUPS 1.2.1 (The most important "dot-zero" version
  bugs are fixed now).
- Removed patch 35 (merged upstream).
- Do not build in debug mode any more,

* Fri May 19 2006 Till Kamppeter <till@mandriva.com> 1.2.0-4mdk
- Delete broken update-alternatives links when updating to this
  version of CUPS (containing the correct links).

* Thu May 18 2006 Till Kamppeter <till@mandriva.com> 1.2.0-3mdk
- Expanded use of update-alternatives to not conflict with
  papi-commands package.
- Fixed update-alternatives mechanism for the man pages.
- Set some links to find man pages more easily.

* Wed May 17 2006 Till Kamppeter <till@mandriva.com> 1.2.0-2mdk
- Fixes raw data files not being accepted when
  "application/octet-stream ..." rules in /etc/cups/mime.* files are active
  (bug 21814, STR 1667).

* Thu May 11 2006 Till Kamppeter <till@mandriva.com> 1.2.0-1mdk
- Updated to CUPS 1.2.0 official release.
- Fixed alternatives setup for the man pages.

* Mon May 08 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5497.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5497.

* Fri Apr 28 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5470.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5470 (Fix in web
  interface: Once you are in SSL mode, you stay there when navigating
  through the web interface).
- Allow remote administration via web interface from the local network
  by default (admin connections are always SSL-encryoted, so no security
  problem).

* Thu Apr 27 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5464.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5464 (Shortly after
  CUPS 1.2rc3 release).

* Tue Apr 25 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5454.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5454 (Added "Encryption
  Required" to "/admin" location in /etc/cups/cupsd.conf, so that all
  administration transactions are done via SSL and input into the web
  interface cannot get lost when the web interface switches from http
  to https in the end of the add printer wizard).
- Added IEEE-1284 device ID support to "poll_ppd_base".

* Mon Apr 24 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5453.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5441 (SNMP
  auto-discovery not hanging any more on IPP device which requests a
  password, many other bug fixes, Polish translation).

* Fri Apr 21 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5441.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5441 (Fixes on SNMP
  auto-discovery).
- Moved cups-config from the libcups2-devel to the cups-common package,
  for easy checking of currently installed CUPS version.

* Thu Apr 20 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5431.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5431 (SNMP auto-discovery
  for network printers, as suggested on the OSDL Printing Summit in Atlanta).

* Thu Apr 13 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5390.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5390.
- Added "BuildRequires: libgnutls-devel", GNU TLS is needed for automatic
  certificate generation for SSL-encrypted access.
- Added /usr/lib/cups/driver directory for PPD file generators.

* Tue Apr 11 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5389.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5389.

* Tue Apr 11 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5388.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5388 (Somewhat after
  the 1.2rc2 release).

* Tue Apr 04 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5368.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5368.
- When building for the Mandriva Linux Corporate 4 products, do not
  require DBUS for building, as CUPS 1.2 uses a new DBUS generation
  which is not available in the Mandriva-2006-based Corporate products.

* Sat Apr 01 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5361.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5361.

* Fri Mar 31 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5357.3mdk
- Fixed 64-bit issue with /usr/lib/cups correctly. It must stay
  /usr/lib/cups to be compatible with third-party filter/backend
  installations (See http://www.cups.org/str.php?L1524).
- Added compatibility link from /usr/lib/cups to /usr/lib64/cups on x86_64
  systems (will be removed when all other Mandriva packages with CUPS
  backends/filters are updated).
- Worked around bug on Mandriva compilation cluster (32-bit machine has
  /usr/lib64 directory).

* Fri Mar 31 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5357.2mdk
- Corrected hard-coded /usr/lib/cups.

* Fri Mar 31 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5357.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5357.
- Added "Requires: udev dynamic" to assure that device files (like
  /dev/usb/lp0) are created and their ownerships/permissions are set 
  correctly (bug 21461).

* Wed Mar 29 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5344.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5344 (Somewhat after
  the 1.2rc1 release).

* Sun Mar 19 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5312.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5312 (Somewhat after
  the 1.2b2 release).

* Thu Mar 09 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5257.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5257 (SHOWSTOPPPER
  FIX! The original CUPS 1.2beta1 did not print at all!).

* Thu Mar 09 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5256.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5256 (This is the 
  CUPS 1.2beta1 release).

* Tue Mar 07 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5239.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5239.
- Made the no non-existing /etc/cups/client.conf a %%ghost.

* Tue Feb 28 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5205.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5205 (Fixed margins
  for N-up printing).

* Tue Feb 28 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5201.2mdk
- Added "BuildRequires: php-cli" so that "./configure" recognizes the
  presence of PHP.

* Tue Feb 28 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5201.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5201.
- Added non-existing files /etc/cups/printers.conf and
  /etc/cups/classes.conf as %%ghost and %%config(noreplace) so that the
  old files of CUPS 1.1 do not get renamed when updating to CUPS 1.2.

* Mon Feb 27 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5186.2mdk
- Obsoleted out old "php4-cups" package from contrib.
- Named file in /etc/php.d/ as in the old "php4-cups" package.

* Sun Feb 26 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5186.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5186.

* Sun Feb 26 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5183.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5183.
- Added new sub package "php-cups" with PHP bindings for the CUPS library.

* Fri Feb 24 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5168.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5168 (Do not accept
  invalid directories for temporary files).

* Fri Feb 24 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5165.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5165 (This is probably
  really the fix for bug 21094).

* Fri Feb 24 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5162.2mdk
- Added backward compatibility links for "enable" and "disable" commands.

* Fri Feb 24 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5162.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5162.

* Thu Feb 23 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5130.2mdk
- Added "--with-system-groups=lpadmin root" to the "./configure" command 
  line and added/removed the "lpadmin" in the pre-install/post-uninstall
  scripts. This way the group "sys" can stay the standard CUPS group. This
  is the way as it is also done in Debian GNU/Linux (see CUPS STR 1434).

* Fri Feb 17 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5130.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5130.

* Thu Feb 16 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5120.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5120.
- Removed hardcoded "chgrp" from Makefiles, set group ownerships in
  %%files section.
- Set permissions of /etc/cups/mime.convs and /etc/cups/mime.types to
  644 (world-readable) so that HP's hp-sendfax utility works for normal
  users.
- Added "unset TMPDIR" to the start-up script of CUPS (cups.startup).

* Mon Feb 06 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5083.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5083.

* Wed Feb 01 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.5046.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 5046 (Add system 
  management interface for power management/sleep, network changes, hostname
  changes, etc. to cupsd, updated man pages, added whitespace and line 
  ending checks to cupstestppd, fixed many file permission issues. tons 
  of bug fixes and polishing).

* Mon Jan 23 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.4964.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 4964 (mailto: notifier
  added).
- Removed patch 34 (merged upstream).

* Thu Jan 19 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.4951.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 4951 (Bug 20504:
  Fixed last missing problem, bad7.pdf from Chris Evans, updated all 
  command-line programs to support "-h" and "-U", small fixes).

* Wed Jan 18 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.4945.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 4945 (Bug 20504:
  Security update for CVE-2005-3191,3192,3193, overflows in goo/gmem.c,
  additional overflow issues discovered by Chris Evans, CVE-2005-3624,
  3625,3626,3627, fixed also print queue set up of auto-detected printers
  with the web interface).

* Wed Jan 18 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.4929.2mdk
- Added libpaper support.

* Sat Jan 14 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.4929.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 4929.
- Removed correction of path for pam_appl.h (fixed upstream).
- Rediffed patch 34.
- Re-introduced %%{_datadir}/locale in %%files section.

* Mon Jan 09 2006 Till Kamppeter <till@mandriva.com> 1.2.0-0.4892.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 4892.
- Added htmldoc to "BuildRequires:".
- Corrected path for pam_appl.h.
- Removed %%{_datadir}/locale from %%files section.
- Reverted the use of the %%configure2_5x macro back to the direct
  ./configure call, as the use of the macro broke CUPS totally (bug 20511).
- Added STATEDIR definition to "make" and "make install" calls
  (/var/run/cups/).

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 1.2.0-0.4876.5mdk
- convert parallel init to LSB

* Wed Jan 04 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.2.0-0.4876.3mdk
- fix build on x86_64
- patch 34: fix build on x86_64 (-fpie overided -fPIC)

* Sat Dec 31 2005 Couriousous <couriousous@mandriva.org> 1.2.0-0.4876.2mdk
- Add parallel init stuff

* Fri Dec 16 2005 Till Kamppeter <till@mandriva.com> 1.2.0-0.4876.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 4876.

* Wed Dec 07 2005 Till Kamppeter <till@mandriva.com> 1.2.0-0.4865.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 4865.

* Thu Nov 24 2005 Till Kamppeter <till@mandriva.com> 1.2.0-0.4843.1mdk
- Updated to CUPS 1.2 development snapshot SVN rev 4843.
- Temporarily deactivated patches 2, 3, 22, 27, 33.

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.23-19mdk
- rebuilt against openssl-0.9.8a

* Sat Oct 29 2005 Till Kamppeter <till@mandriva.com> 1.1.23-18mdk
- Introduced a timeout when waiting for CUPS daemon listening (bug
  19255).
- Replaced dbus patch by newer one from Red Hat (current one did not build
  any more).

* Fri Aug 19 2005 Till Kamppeter <till@mandriva.com> 1.1.23-17mdk
- Removed facility to automatically set up print queues when starting CUPS.
  This can cause problems during installation.

* Thu Aug 18 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.1.23-16mdk
- 64-bit fixes

* Thu Aug 18 2005 Till Kamppeter <till@mandriva.com> 1.1.23-15mdk
- Moved comment away from "%%postun".

* Wed Aug 17 2005 Till Kamppeter <till@mandriva.com> 1.1.23-14mdk
- Turned off automatic re-enabling of print queues on CUPS start-up
  because we have the new CUPS backend wrapper no which prevents queues
  from being disabled automatically.

* Sun Aug 14 2005 Till Kamppeter <till@mandriva.com> 1.1.23-13mdk
- SECURITY FIX: Fixes CAN-2005-2097: Vulnerability on PDF processing 
  (patch 35).
- Added "Requires: xinetd" to "cups" packages. It is needed for the
  "cups-lpd" mini daemon.

* Thu Jul 28 2005 Till Kamppeter <till@mandriva.com> 1.1.23-12mdk
- Added automatic re-enabling of print queues and automatic
  print queue setup (both configurable) to /etc/init.d/cups.

* Tue Apr 12 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-11mdk
- Fixed bug 15376: "!(" -> "! (" in /etc/init.d/cups.

* Tue Mar 22 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-10mdk
- Updated Pierre Jarillon's I18n patch, especially there are "Set as
  default" buttons in all languages now.

* Fri Mar 18 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-9mdk
- Revert change of lock file name to have /var/lock/subsys/cups again.
  Handling services with different service name and daemon name is a
  general problem (also with Samba and MySQL) which has to be addressed
  later. Renaming the service to "cupsd" would break other stuff
  (printerdrake, KDE Printing Manager, ...). The bugs 11715, 14727, and 
  14545 cannot be fixed all at once.

* Wed Mar 16 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-8mdk
- Fixed I18n of the CUPS web interface and online help (bug 10598, thanks
  to Pierre Jarillon, jarillon at abul dot org, for the big patch).
- Let online help go into /usr/share/cups/doc and not into /usr/share/doc,
  so that it gets also installed in a minimum installation without
  documentation, otherwise the web interface would be broken in this case
  (Thanks to Raul Dias, raul at dias dot com dot br, for reporting this).

* Wed Mar 02 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-7mdk
- Recode all translations to UTF-8 so that the web interface of CUPS is
  shown correctly, especially with Mozilla.

* Tue Mar 01 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-6mdk
- Removed menu entry for CUPS web interface.

* Fri Feb 18 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-5mdk
- Use /var/lock/subsys/cupsd instead of /var/lock/subsys/cups
  in startup script, to fix bug 11715.
- SECURITY FIX: Fixes CAN-2005-0064/MDKSA-2005:041/Bug 13751: See
  http://www.mandrakesoft.com/security/advisories?name=MDKSA-2005:041

* Fri Feb 11 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-4mdk
- SECURITY FIX: Fixes CAN-2005-0064/MDKSA-2005:018/Bug 13580: See
  http://www.mandrakesoft.com/security/advisories?name=MDKSA-2005:018

* Fri Feb 11 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-3mdk
- Updated CUPS startup script to also check HPLIP.

* Wed Feb 09 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.23-2mdk
- multiarch

* Tue Jan 04 2005 Till Kamppeter <till@mandrakesoft.com> 1.1.23-1mdk
- Updated to CUPS 1.1.23 final (Tons of bug fixes: "Media tray empty" on
  USB backend, possible DoS in CUPS daemon, buffer overflow on "hpgltops"
  filter, ...).
- Set "lppasswd" SUID root again, otherwise it does not work.
- Removed support for Mandrakelinux 7.2.
- Fixed icon stuff.

* Tue Nov 30 2004 Till Kamppeter <till@mandrakesoft.com> 1.1.22-2mdk
- Added Red Hat's DBUS support (Patch 27).

* Tue Nov 09 2004 Till Kamppeter <till@mandrakesoft.com> 1.1.22-1mdk
- Updated to CUPS 1.1.22 final.
- Removed Patch 26, it is already applied upstream.

* Tue Oct 12 2004 Till Kamppeter <till@mandrakesoft.com> 1.1.21-1mdk
- Updated to CUPS 1.1.21 final.
- Removed Patch 24 and Patch 25, they are already applied upstream.
- Improved debug mode, now the RPM built in debug mode has really
  unstripped executables.
- Fix the CUPS daemon dieing on "killall -HUP cupsd" (Patch 26, Thanks to
  Tim Waugh from Red Hat, CUPS STR 865 and 928).

* Sat Oct 09 2004 Vincent Danen <vdanen@mandrakesoft.com> 1.1.21-0.rc1.7mdk
- P25: security fix for CAN-2004-0558

* Tue Sep 21 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.1.21-0.rc1.6mdk
- start cups at level 15 to avoid conflicts with RPC programs like
  ypbind (bug #9951)

* Tue Aug 31 2004 Till Kamppeter <till@mandrakesoft.com> 1.1.21-0.rc1.5mdk
- Added switchable debug mode.
- Moved "Provides: lpddaemon" from "cups" to "cups-common" package as we
  support daemon-less CUPS client mode with printerdrake now.

* Sat Aug 21 2004 Till Kamppeter <till@mandrakesoft.com> 1.1.21-0.rc1.4mdk
- If there is no USB printer connected, let the "usb" backend put out
  /dev/usb/lpX as default device file names and not /dev/usblpX.

* Tue Aug 10 2004 Till Kamppeter <till@mandrakesoft.com> 1.1.21-0.rc1.3mdk
- Set temporary directory and other parameters in /etc/xinetd.d/cups-lpd,
  sp that cups-lpd uses the correct temporary directory and
  permissions/ownerships (Anthill bug 879).

* Fri Aug 06 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1.21-0.rc1.2mdk
- use -fPIC too on ix86

* Thu Jun 10 2004 Till Kamppeter <till@mandrakesoft.com> 1.1.21-0.rc1.1mdk
- Updated to CUPS 1.1.21rc1.
- Perlified patch 6.

* Sat Jun 05 2004 <lmontel@n2.mandrakesoft.com> 1.1.20-6mdk
- Rebuild

