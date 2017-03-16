# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel

%global _scl_prefix %{ns_dir}
%global scl_name_base    %{ns_name}-php
%global scl_macro_base   %{ns_name}_php
%global scl_name_version 70
%global scl              %{scl_name_base}%{scl_name_version}
%scl_package %scl

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary:       Package that installs PHP 7.0
Name:          %scl_name
Version:       7.0.17
Vendor:        cPanel, Inc.
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
Group:         Development/Languages
License:       GPLv2+

Source0:       macros-build
Source1:       README
Source2:       LICENSE

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: scl-utils-build
BuildRequires: help2man
# Temporary work-around
BuildRequires: iso-codes

Requires:      %{?scl_prefix}php-common
Requires:      %{?scl_prefix}php-cli
Requires:      %{?scl_prefix}pear

%description
This is the main package for %scl Software Collection,
that install PHP 7.0 language.


%package runtime
Summary:   Package that handles %scl Software Collection.
Group:     Development/Languages
Requires:  scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.


%package build
Summary:   Package shipping basic build configuration
Group:     Development/Languages
Requires:  scl-utils-build

%description build
Package shipping essential configuration macros
to build %scl Software Collection.


%package scldevel
Summary:   Package shipping development files for %scl
Group:     Development/Languages

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.


%prep
%setup -c -T

cat <<EOF | tee enable
export PATH=%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF

# generate rpm macros file for depended collections
cat << EOF | tee scldev
%%scl_%{scl_macro_base}         %{scl}
%%scl_prefix_%{scl_macro_base}  %{scl_prefix}
EOF

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE1})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE2} .


%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -D -m 644 enable %{buildroot}%{_scl_scripts}/enable
install -D -m 644 scldev %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel
install -D -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7

%scl_install

tmp_version=$(echo %{scl_name_version} | sed -re 's/([0-9])([0-9])/\1\.\2/')
sed -e 's/@SCL@/%{scl_macro_base}%{scl_name_version}/g' -e "s/@VERSION@/${tmp_version}/g" %{SOURCE0} \
  | tee -a %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files


%files runtime
%defattr(-,root,root)
%doc README LICENSE
%scl_files
%{_mandir}/man7/%{scl_name}.*


%files build
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl}-config


%files scldevel
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel


%changelog
* Thu Mar 16 2017 Cory McIntire <cory@cpanel.net> - 7.0.17-1
- EA-6068: Release 7.0.17 to PHP 7.0 release of 7.0.17

* Thu Feb 16 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 7.0.16-1
- EA-5992: Release 7.0.16 to PHP 7.0 release of 7.0.16

* Thu Jan 19 2017 Dan Muey <dan@pcanel.net> - 7.0.15-1
- EA-5874: Release 7.0.15 to PHP 7.0 release of 7.0.15

* Thu Dec 9 2016 Cory McIntire <cory@cpanel.net> - 7.0.14-1
- EA-5754: Release 7.0.14 to match PHP 7.0 release of 7.0.14

* Thu Nov 10 2016 Jacob Perkins <jacob.perkins@cpanel.net> - 7.0.13-1
- EA-5627: Release 7.0.13 to match PHP 7.0 release of 7.0.13

* Fri Oct 14 2016 Jacob Perkins <jacob.perkins@cpanel.net> - 7.0.12-1
- EA-5414: Release 7.0.12 to match PHP 7.0 release of 7.0.12

* Thu Sep 15 2016 Jacob Perkins <jacob.perkins@cpanel.net> - 7.0.11-1
- EA-5249: Release 7.0.11 to match PHP 7.0 release of 7.0.11

* Fri Aug 19 2016 Jacob Perkins <jacob.perkins@cpanel.net> - 7.0.10-1
- EA-5086: Release 7.0.10 to match PHP 7.0 release of 7.0.10

* Mon Jun 27 2016 Dan Muey <dan@cpanel.net> - 7.0.9-1
- EA-4820: Release 7.0.9 to match PHP 7.0 release of 7.0.9

* Mon Jun 27 2016 Dan Muey <dan@cpanel.net> - 7.0.8-1
- EA-4739: Bumped version to match PHP version

* Mon Jun 20 2016 Dan Muey <dan@cpanel.net> - 7.0.7-2
- EA-4383: Update Release value to OBS-proof versioning

* Thu May 26 2016 S. Kurt Newman <kurt.newman@cpanel.net> - 7.0.7-1
- Bumped pacakge version (EA-4629)

* Thu Apr 28 2016 Jacob Perkins <jacob.perkins@cpanel.net> 7.0.6-1
- Bumped package version

* Thu Apr 1 2016 Jacob Perkins <jacob.perkins@cpanel.net> 7.0.5-1
- Bumped package version

* Thu Mar 3 2016 David Nielson <david.nielson@cpanel.net> 7.0.4-1
- Bumped package version

* Wed Feb 24 2016 Jacob Perkins <jacob.perkins@cpanel.net> 7.0.3-1
- Bumped package version

* Tue Dec 08 2015 <matt@cpanel.net> 1-1
- initial packaging
