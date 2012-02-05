#
# Conditional build:
%bcond_without	sasl		# build with sasl support
#
%define		_ver_major	3.0
%define		_ver_minor	0
%define		_rc		rc.43
%define		_rel	0.1
Summary:	Real time network flow monitor - client applications
Summary(pl.UTF-8):	Monitor obciążenia sieci czasu rzeczywistego - programy klienckie
Name:		argus-clients
Version:	%{_ver_major}.%{_ver_minor}
Release:	0.%{_rc}.%{_rel}
License:	GPL v2
Group:		Applications/Networking
Source0:	ftp://qosient.com/dev/argus-%{_ver_major}/%{name}-%{version}.%{_rc}.tar.gz
# Source0-md5:	d85d5546cdf527f096c367afffd8f334
Source1:	%{name}-excel.rc
Source2:	%{name}-racluster.conf
Source3:	%{name}-radium.conf
Source4:	%{name}-radium.init
Source5:	%{name}-radium.sysconfig
Source6:	%{name}-radium.logrotate
Source7:	%{name}-ranonymize.conf
Source8:	%{name}-ra.print.all.conf
Source9:	%{name}-rarc
Patch0:		%{name}-ragraph-rabins-paths.patch
Patch1:		%{name}-ratop-ncurses.patch
Patch2:		%{name}-configure-ncurses.patch
URL:		http://www.qosient.com/argus/
BuildRequires:	bison
%{?with_sasl:BuildRequires:	cyrus-sasl-devel}
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	perl-rrdtool
Requires:	rc-scripts
Provides:	group(argus)
Provides:	user(argus)
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Argus is a Real Time Flow Monitor designed to track and report on the
status and performance of all network transactions seen in a data
network traffic stream. It is similiar to Cisco NetFlow, however more
powerful and with different data format.

This package provides variuos methods to process and present the data.

%description -l pl.UTF-8
Argus jest monitorem sieci czasu rzeczywistego zaprojektowanym do
śledzenia i raportowania stanu sieci oraz wszelkiego typu transakcji
sieciowych widzianych w strumieniu danych. Jest bardzo podobny do
NetFlow z Cisco, jednak bardziej rozbudowany i posiada inny format
danych.

Ta paczka dostarcza różne metody do przetwarzania i prezentowania
danych.

%prep
%setup -q -n %{name}-%{version}.%{_rc}
%patch0
%patch1
%patch2

%build
%configure \
	--with%{!?with_sasl:out}-sasl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT%{_var}/log/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/excel.rc
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/racluster.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/radium.conf
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/randomize.conf
install %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ra.print.all.conf
install %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/rarc

install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/radium
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/radium
install %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/radium

touch $RPM_BUILD_ROOT%{_var}/log/%{name}/radium.log

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# same file is in argus.spec
mv $RPM_BUILD_ROOT%{_bindir}/argusbug $RPM_BUILD_ROOT%{_bindir}/argusbug-clients

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 214 argus
%useradd -u 214 -d /usr/share/empty -s /bin/sh -g argus -c "argus daemon" argus

%post
/sbin/chkconfig --add radium
%service radium restart

%preun
if [ "$1" = "0" ]; then
	%service -q radium stop
	/sbin/chkconfig --del radium
fi

%files
%defattr(644,root,root,755)
%doc CREDITS ChangeLog README doc/{CHANGES,FAQ,HOW-TO}
%attr(755,root,root) %{_bindir}/argusbug-clients
%attr(755,root,root) %{_bindir}/ra
%attr(755,root,root) %{_bindir}/rabins
%attr(755,root,root) %{_bindir}/racluster
%attr(755,root,root) %{_bindir}/racount
%attr(755,root,root) %{_bindir}/radump
%attr(755,root,root) %{_bindir}/ragraph
%attr(755,root,root) %{_bindir}/ragrep
%attr(755,root,root) %{_bindir}/rahisto
%attr(755,root,root) %{_bindir}/ramatrix
%attr(755,root,root) %{_bindir}/ranonymize
%attr(755,root,root) %{_bindir}/rapath
%attr(755,root,root) %{_bindir}/rapolicy
%attr(755,root,root) %{_bindir}/rasort
%attr(755,root,root) %{_bindir}/rasplit
%attr(755,root,root) %{_bindir}/rastrip
%attr(755,root,root) %{_bindir}/ratemplate
%attr(755,root,root) %{_bindir}/ratop
%attr(755,root,root) %{_sbindir}/radium
%attr(754,root,root) /etc/rc.d/init.d/radium
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/excel.rc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/racluster.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/radium.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/randomize.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/ra.print.all.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/rarc
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/radium
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/radium
%{_mandir}/man1/ra.1*
%{_mandir}/man1/rabins.1*
%{_mandir}/man1/racluster.1*
%{_mandir}/man1/racount.1*
%{_mandir}/man1/ragraph.1*
%{_mandir}/man1/ragrep.1*
%{_mandir}/man1/rahisto.1*
%{_mandir}/man1/rasort.1*
%{_mandir}/man1/rasplit.1*
%{_mandir}/man1/rastrip.1*
%{_mandir}/man5/racluster.5*
%{_mandir}/man5/radium.conf.5*
%{_mandir}/man5/rarc.5*
%{_mandir}/man8/radium.8*
%attr(770,root,argus) %dir %{_var}/log/%{name}
%attr(660,root,argus) %ghost %{_var}/log/%{name}/radium.log
