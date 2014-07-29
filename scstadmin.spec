%define perlver 5.8.8

Name: scstadmin
Summary: Configuartion scripts for Generic SCSI target mid-level (SCST)
Version: 2.2.1
Release: 0
License: GPL
Group: Applications/File
%define tarball %{name}-%{version}.tar.bz2
Source: http://sourceforge.net/projects/scst/files/%{name}/%{tarball}
Patch0: scstadmin-2.2.1.no-lsb.patch
Patch1: scstadmin-2.2.1.perl-build.patch
Patch2: scstadmin-2.2.1.iscsi-scst-path.patch
BuildArch: noarch
URL: http://scst.sourceforge.net/

BuildRequires: perl >= %{perlver}
Requires: perl >= %{perlver}


%description
SCST Configuration/Administration scripts. With scstadmin you can 
manually or automatically configure every aspect of SCST incuding 
enabling/disabling target mode on your target SCSI controller.

Detail description of SCST's features and internals
could be found in "Generic SCSI Target Middle Level for Linux" document
SCST's Internet page http://scst.sourceforge.net.


%prep
%setup -q
%patch0 -p1 -z .no-lsb
%patch1 -p1 -z .perl-build
%patch2 -p1 -z .iscsi-scst-path


%build
make DESTDIR=%{buildroot}


%install
make install \
     DESTDIR=%{buildroot} \
     SBINDIR=%{_sbindir} \
     INITDIR=%{_initrddir} \
     MANDIR=%{buildroot}%{_mandir}
mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}

# Sample config
sed 's/^/\# /' examples/scst.conf.sysfs > %{buildroot}%{_sysconfdir}/scst.conf

# clean perl cruft
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;


%clean
rm -rf %{buildroot}


%post
/sbin/chkconfig --add scst || :


%preun
if [ $1 = 0 ]; then
        /sbin/service scst stop > /dev/null 2>&1 || :
        /sbin/chkconfig --del scst || :
fi


%files 
%config(noreplace) %{_sysconfdir}/scst.conf
%config(noreplace) %{_sysconfdir}/default/scst
%{_sbindir}/scstadmin
%{_initrddir}/scst
%{perl_vendorlib}/SCST
%{_mandir}/man[135]/*
%doc ChangeLog LICENSE README README.procfs
%doc 


%changelog
* Tue Jul 29 2014 John Morris <john@zultron.com> - 2.2.1-0
- Update to 2.2.1
- Fix install locations; patches to fix build
- Package modernizations
- Remove package cruft
- Remove perl install artifacts
- Remove qla2x00t stuff (in separate sources)
- Update %%files
- Fix macros
- Switch to upstream example conf and scst init script

* Mon Nov 23 2009  Jaroslaw Polok <jaroslaw.polok@cern.ch> 1.0.6-1.cern
- initial packaging
