%define perlver 5.8.8

Summary: Configuartion scripts for Generic SCSI target mid-level (SCST)
Name: scstadmin
Version: 1.0.6
Release: 1.cern
License: GPL
Buildroot: %{_tmppath}/%{name}-buildroot
Group: Applications/File
Source: %{name}-%{version}.tar.gz
Patch1: %{name}-%{version}-Makefile.patch 
Source1: scst.init.d
Source2: qla2x00t.init.d
Source3: scst.conf.example

BuildArch: noarch

Packager: Jaroslw.Polok@cern.ch
URL: http://scst.sourceforge.net/

BuildRequires: perl >= %{perlver}
Requires: perl >= %{perlver}
# Hmm... maybe not
# Requires: kernel-module-scst

%description
SCST Configuration/Administration scripts. With scstadmin you can 
manually or automatically configure every aspect of SCST incuding 
enabling/disabling target mode on your target SCSI controller.

Detail description of SCST's features and internals
could be found in "Generic SCSI Target Middle Level for Linux" document
SCST's Internet page http://scst.sourceforge.net.

%prep

%setup
%patch1 -p1

%build

make DESTDIR=%{buildroot}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/usr/share/man/man3
make install DESTDIR=%{buildroot} 
mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}
cp -r README ChangeLog LICENSE examples/scst.conf %{buildroot}/usr/share/doc/%{name}-%{version}

rm -rf %{buildroot}/usr/lib/perl5/site_perl/%{perlver}/*linux-thread-multi*
rm -rf %{buildroot}/usr/lib/perl5/%{perlver}/*linux-thread-multi*

cp -f %{SOURCE1} %{buildroot}/etc/init.d/scst
cp -f %{SOURCE2} %{buildroot}/etc/init.d/qla2x00t
cp -f %{SOURCE3} %{buildroot}/etc/scst.conf

%clean
rm -rf %{buildroot}


%post
/sbin/chkconfig --add scst || :
/sbin/chkconfig --add qla2x00t || :

%preun
if [ $1 = 0 ]; then
        /sbin/service scst stop > /dev/null 2>&1 || :
	/sbin/service qla2x00t stop > /dev/null 2>&1 || :
        /sbin/chkconfig --del scst || :
	/sbin/chkconfig --del qla2x00t || :
fi



%files 
%defattr(-,root,root)
%config(noreplace) /etc/scst.conf
/usr/sbin/scstadmin
/etc/init.d/scst
/etc/init.d/qla2x00t
/usr/lib/perl5/site_perl/%{perlver}/SCST/SCST.pm
/usr/share/man/man3/SCST::SCST.3pm.gz
%doc /usr/share/doc/%{name}-%{version}/*

%changelog
* Mon Nov 23 2009  Jaroslaw Polok <jaroslaw.polok@cern.ch> 1.0.6-1.cern
- initial packaging
