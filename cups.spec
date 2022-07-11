# cups is used by wine as well as some of its dependencies
%ifarch %{x86_64}
%bcond_without compat32
%endif

# {_exec_prefix}/lib/cups is correct, even on x86_64.
# It is not used for shared objects but for executables.
# It's more of a libexec-style ({_libexecdir}) usage,
# but we use lib for compatibility with 3rd party drivers (at upstream request).
%global cups_serverbin %{_exec_prefix}/lib/cups

# Turning this on lets CUPS to be built in debug mode (with debugger symbols)
%define debug 0
%define enable_check 0

# Undefine for release builds
#define beta rc1

%define _disable_lto 1

%bcond_without	dnssd
%bcond_with	bootstrap

Summary:	Common Unix Printing System - Server package
Name:		cups
Version:	2.4.2
Release:	%{?beta:0.%{beta}.}1
Source0:	https://github.com/openprinting/cups/releases/download/v%version%{?beta:%{beta}}/cups-%version%{?beta:%{beta}}-source.tar.gz
Source1000:	%{name}.rpmlintrc
License:	GPLv2 and LGPLv2
Group:		System/Printing
Url:		https://openprinting.github.io/cups/

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
Patch2:		https://github.com/heftig/cups/commit/455c52a027ab3548953372a0b7bdb0008420e9ba.patch

# Fedora patches
Patch1002:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-multilib.patch
Patch1003:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-banners.patch
Patch1004:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-no-export-ssllibs.patch
Patch1005:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-direct-usb.patch
Patch1006:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-eggcups.patch
Patch1007:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-driverd-timeout.patch
Patch1009:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-usb-paperout.patch
Patch1010:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-uri-compat.patch
Patch1014:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-freebind.patch
Patch1015:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-ipp-multifile.patch
Patch1016:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-web-devices-timeout.patch
Patch1019:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-failover-backend.patch
Patch1020:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-filter-debug.patch
Patch1021:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-dymo-deviceid.patch
#Patch1100:	http://pkgs.fedoraproject.org/cgit/rpms/cups.git/plain/cups-lspp.patch
# End fedora patches

# Requires /etc/tmpfiles.d (bug #656566)
Requires:	systemd >= 208
Requires(post):	rpm-helper >= 0.24.1
Requires(preun):	rpm-helper >= 0.24.1
Requires(postun):	rpm-helper
BuildRequires:	htmldoc
BuildRequires:	php-cli
BuildRequires:	xdg-utils
BuildRequires:	pkgconfig(libacl)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	krb5-devel
BuildRequires:	openldap-devel
BuildRequires:	openslp-devel
BuildRequires:	pam-devel
BuildRequires:	php-devel >= 5.1.0
BuildRequires:	pkgconfig(libtiff-4)
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
BuildRequires:	pkgconfig(com_err)

Requires:	%{name}-common >= %{version}-%{release}
Requires:	net-tools
%if !%{with bootstrap}
Suggests:	avahi
%endif
Requires:	printer-testpages
# Take care that device files are created with correct permissions
Requires:	udev
%if ! %{with bootstrap}
Requires:	cups-filters
%endif
# For desktop menus
Requires:	xdg-utils
%rename		cupsddk-drivers
Obsoletes: php-cups < %{EVRD}
# No longer existing old libraries
%define	libcupscgi	%mklibname cupscgi 1
Obsoletes:	%{libcupscgi} < %{EVRD}
%define	libcupsmime	%mklibname cupsmime 1
Obsoletes:	%{libcupsmime} < %{EVRD}
%define	libcupsppdc	%mklibname cupsppdc 1
Obsoletes:	%{libcupsppdc} < %{EVRD}

%if %{with compat32}
BuildRequires:	devel(libz)
BuildRequires:	devel(libsystemd)
BuildRequires:	devel(libcom_err)
BuildRequires:	devel(libusb-1.0)
BuildRequires:	devel(libssl)
BuildRequires:	devel(libgnutls)
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libkrb5)
BuildRequires:	libcrypt-devel
%endif

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
Summary:	Common Unix Printing System - Common stuff
License:	GPLv2
Group:		System/Printing
Requires:	net-tools
# To satisfy LSB/FHS
Provides:	lpddaemon

%description common
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. It contains the command line utilities for
printing and administration (lpr, lpq, lprm, lpadmin, lpc, ...), man
pages, locales, and a sample configuration file for daemon-less CUPS
clients (%{_sysconfdir}/cups/client.conf).

This package you need for both CUPS clients and servers.

%define cupsmajor 2
%define libcups %mklibname cups %{cupsmajor}

%package -n %{libcups}
Summary:	Common Unix Printing System - CUPS library
License:	LGPLv2
Group:		System/Libraries
Obsoletes:	%{_lib}cups3 < 1.6.1-2

%description -n %{libcups}
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%define cupsimagemajor 2
%define libcupsimage %mklibname cupsimage %{cupsimagemajor}

%package -n %{libcupsimage}
Summary:	Common Unix Printing System - CUPSimage library
License:	LGPLv2
Group:		System/Libraries
Conflicts:	%{libcups} < 1.6.1-2

%description -n %{libcupsimage}
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%define devname %mklibname %{name} -d

%package -n %{devname}
Summary:	Common Unix Printing System - Development environment "libcups"
License:	LGPLv2
Group:		Development/C
Requires:	%{libcups} >= %{version}-%{release}
Requires:	%{libcupsimage} >= %{version}-%{release}
Requires:	pkgconfig(krb5)
Requires:	pkgconfig(com_err)

Provides:	cups-devel
Obsoletes:	%mklibname %{name}2 -d

%description -n %{devname}
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This is the development package for
creating additional printer drivers, printing software, and other CUPS
services using the main CUPS library "libcups".

%if %{with compat32}
%define lib32cups %mklib32name cups %{cupsmajor}

%package -n %{lib32cups}
Summary:	Common Unix Printing System - CUPS library (32-bit)
License:	LGPLv2
Group:		System/Libraries

%description -n %{lib32cups}
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%define lib32cupsimage %mklib32name cupsimage %{cupsimagemajor}

%package -n %{lib32cupsimage}
Summary:	Common Unix Printing System - CUPSimage library (32-bit)
License:	LGPLv2
Group:		System/Libraries
Conflicts:	%{libcups} < 1.6.1-2

%description -n %{lib32cupsimage}
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%define dev32name %mklib32name %{name} -d

%package -n %{dev32name}
Summary:	Common Unix Printing System - Development environment "libcups" (32-bit)
License:	LGPLv2
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32cups} = %{version}-%{release}
Requires:	%{lib32cupsimage} = %{version}-%{release}

%description -n %{dev32name}
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This is the development package for
creating additional printer drivers, printing software, and other CUPS
services using the main CUPS library "libcups".
%endif

%prep
%autosetup -p1 -n %{name}-%{version}%{?beta:%{beta}}

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
%setup -q -T -D -a 12 -n %{name}-%{version}%{?beta:%{beta}}
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

%if %{with compat32}
export DSOFLAGS="$(echo %{ldflags} |sed -e 's,-m64,,g;s,-mx32,,g;s,-flto,,g') -m32"
%configure32 \
	--with-pkgconfpath=%{_prefix}/lib/pkgconfig \
	--with-exe-file-perm=0755 \
	--with-cupsd-file-perm=0755 \
	--with-log-file-perm=0600 \
	--enable-relro \
	--with-dbusdir=%{_sysconfdir}/dbus-1 \
	--enable-threads \
	--enable-gnutls \
	--enable-webif \
	--without-xinetd \
	--with-access-log-level=actions \
	--enable-page-logging \
	--with-rundir=/run/cups \
%if %{debug}
	--enable-debug=yes \
%endif
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
	--without-rcdir \
	localedir=%{_datadir}/locale
%make_build
mkdir lib32
mv cups/*.so* lib32/
make distclean
%endif

%if %{debug}
# Debug mode
export DONT_STRIP=1
export CFLAGS="-g"
export CXXFLAGS="-g"
%endif
# cups uses $DSOFLAGS instead of $LDFLAGS for shared libs
export DSOFLAGS="$LDFLAGS"
%configure \
	--with-pkgconfpath=%{_libdir}/pkgconfig \
%if %{with lspp}
	--enable-lspp \
%else
	--disable-lspp \
%endif
	--with-exe-file-perm=0755 \
	--with-cupsd-file-perm=0755 \
	--with-log-file-perm=0600 \
	--enable-relro \
	--with-dbusdir=%{_sysconfdir}/dbus-1 \
	--with-php=%{_bindir}/php \
%if !%{with dnsd}
	--enable-avahi \
%endif
	--enable-threads \
	--enable-gnutls \
	--enable-webif \
	--without-xinetd \
	--with-access-log-level=actions \
	--enable-page-logging \
	--with-rundir=/run/cups \
%if %{debug}
	--enable-debug=yes \
%endif
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
	--without-rcdir \
	localedir=%{_datadir}/locale

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

%ifarch x86_64
# This one will be removed soon, when all other packages are
# modified appropriately
ln -s %{_prefix}/lib/cups %{buildroot}%{_libdir}/cups
%endif

# Install missing headers (Thanks to Oden Eriksson)
install -m644 cups/debug-private.h  %{buildroot}%{_includedir}/cups/
install -m644 cups/string-private.h %{buildroot}%{_includedir}/cups/
install -m644 config.h %{buildroot}%{_includedir}/cups/

# Create dummy config files /etc/cups/printers.conf,
# /etc/cups/classes.conf, and /etc/cups/client.conf
touch %{buildroot}%{_sysconfdir}/cups/printers.conf
touch %{buildroot}%{_sysconfdir}/cups/classes.conf
touch %{buildroot}%{_sysconfdir}/cups/client.conf

# install /usr/lib/tmpfiles.d/cups.conf (bug #656566)
mkdir -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/cups.conf <<EOF
d /run/cups 0755 root lp -
d /run/cups/certs 0511 lp lp -
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

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable cups.socket
enable cups.service
enable cups.path
EOF

%if %{with compat32}
cp -a lib32/* %{buildroot}%{_prefix}/lib/
%endif

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
%systemd_post %{name}.path %{name}.socket %{name}.service %{name}-lpd.socket

%preun
%systemd_preun %{name}.path %{name}.socket %{name}.service %{name}-lpd.socket

%postun
%_postun_groupdel lpadmin
%systemd_postun_with_restart %{name}.path %{name}.socket %{name}.service %{name}-lpd.socket

%files
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
%{_presetdir}/86-%{name}.preset
%{_unitdir}/*.path
%{_unitdir}/*.service
%{_unitdir}/*.socket
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
%{_prefix}/lib/cups/backend/failover
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
%dir %{_prefix}/lib/cups/command
%{_prefix}/lib/cups/command/ippevepcl
%{_prefix}/lib/cups/command/ippeveps
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
%{_sbindir}/correctcupsconfig
%{_sbindir}/cupsaccept
%{_sbindir}/cupsctl
%{_sbindir}/cupsd
%{_sbindir}/cupsdisable
%{_sbindir}/cupsenable
%{_sbindir}/cupsfilter
%{_sbindir}/cupsreject
%{_sbindir}/lpadmin
%{_sbindir}/lpc
%{_sbindir}/lpinfo
%{_sbindir}/lpmove
%{_bindir}/cancel
%{_bindir}/lp
%{_bindir}/lpq
%{_bindir}/lpr
%{_bindir}/lprm
%{_bindir}/lpstat
%if %{with dnssd}
%{_bindir}/ippfind
%endif
%{_bindir}/ippeveprinter
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
%{_datadir}/locale/*/*.po
%{_mandir}/man?/*

%files -n %{libcups}
%{_libdir}/libcups.so.%{cupsmajor}*

%files -n %{libcupsimage}
%{_libdir}/libcupsimage.so.%{cupsimagemajor}*

%files -n %{devname}
%dir %{_includedir}/cups
%{_includedir}/cups/*
%{_libdir}/*.so
%{_bindir}/cups-config
%{_libdir}/pkgconfig/cups.pc

%if %{with compat32}
%files -n %{lib32cups}
%{_prefix}/lib/libcups.so.%{cupsmajor}*

%files -n %{lib32cupsimage}
%{_prefix}/lib/libcupsimage.so.%{cupsimagemajor}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%endif
