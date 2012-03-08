# Use rpmbuild --without gcj to disable native bits
%define with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

Name: flute
Version: 1.3.0
Release: 3.OOo31%{?dist}
Summary: Java CSS parser using SAC
# The entire source code is W3C except ParseException.java which is LGPLv2+
License: W3C and LGPLv2+
Group: System Environment/Libraries
Source0: http://downloads.sourceforge.net/jfreereport/%{name}-%{version}-OOo31.zip
URL: http://www.w3.org/Style/CSS/SAC/
BuildRequires: ant, java-devel, jpackage-utils, sac
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: java, jpackage-utils sac
%if %{with_gcj}
BuildRequires: java-gcj-compat-devel >= 1.0.31
Requires(post): java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
BuildArch: noarch
%endif

%description
A Cascading Style Sheets parser using the Simple API for CSS, for Java.

%package javadoc
Group: Development/Documentation
Summary: Javadoc for %{name}
%if %{with_gcj}
BuildArch: noarch
%endif

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
find . -name "*.jar" -exec rm -f {} \;
mkdir -p lib
build-jar-repository -s -p lib sac

%build
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp build/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc COPYRIGHT.html
%{_javadir}/*.jar
%if %{with_gcj}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Thu Jan 07 2010 Caolan McNamara <caolanm@redhat.com> - 1.3.0-3.OOo31
- Resolves: rhbz#553327 ParseException.java is under LGPLv2+

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.3.0-2.OOo31.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Caolan McNamara <caolanm@redhat.com> - 1.3.0-2.OOo31
- make javadoc no-arch when building as arch-dependant aot

* Sun May 03 2009 Caolan McNamara <caolanm@redhat.com> - 1.3.0-1.OOo31
- post-release tuned for OpenOffice.org report-designer

* Mon Mar 09 2009 Caolan McNamara <caolanm@redhat.com> - 1.3-5.20061107jfree
- better adherence to versioning guidelines

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 07 2007 Caolan McNamara <caolanm@redhat.com> 1.3-4
- initial import from jpackage

* Mon Aug 23 2004 Ralph Apel <r.apel at r-apel.de> 1.3-3jpp
- update for JPackage 1.5

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 1.3-2jpp
- update for JPackage 1.5

* Thu Jul 11 2002 Ville Skyttä <ville.skytta at iki.fi> 1.3-1jpp
- Update to 1.3.
- Use sed instead of bash 2 extension when symlinking jars during build.
- Add Distribution tag, fix URL, tweak Summary and description.

* Wed Feb 06 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-1jpp
- first jpp release
