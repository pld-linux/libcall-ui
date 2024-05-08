# NOTE: don't build yet, it's meant to be used as submodule currently
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Common user interface parts for call handling
Summary(pl.UTF-8):	Wspólne elementy interfejsu użytkownika do obsługi połączeń głosowych
Name:		libcall-ui
Version:	0.2.0
Release:	0.1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://gitlab.gnome.org/World/Phosh/libcall-ui/-/releases
Source0:	https://gitlab.gnome.org/World/Phosh/libcall-ui/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	57111039be1bcc33a68c610e6e9c7dd6
URL:		https://gitlab.gnome.org/World/Phosh/libcall-ui
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.62
BuildRequires:	gtk4-devel >= 4.0
BuildRequires:	libadwaita-devel >= 1.2
BuildRequires:	libcallaudio-devel >= 0.1
BuildRequires:	meson >= 0.56.2
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
Requires:	glib2 >= 1:2.62
Requires:	libadwaita >= 1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libcall-ui carries common user interface parts for call handling.

%description -l pl.UTF-8
Libcall-ui gromadzi wspólne elementy interfejsu użytkownika do obsługi
połączeń głosowych.

%package devel
Summary:	Header files for call-ui library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki call-ui
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.62
Requires:	gtk4-devel >= 4.0
Requires:	libadwaita-devel >= 1.2
Requires:	libcallaudio-devel >= 0.1

%description devel
Header files for call-ui library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki call-ui.

%package static
Summary:	Static call-ui library
Summary(pl.UTF-8):	Statyczna biblioteka call-ui
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static call-ui library.

%description static -l pl.UTF-8
Statyczna biblioteka call-ui.

%package apidocs
Summary:	API documentation for call-ui library
Summary(pl.UTF-8):	Dokumentacja API biblioteki call-ui
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for call-ui library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki call-ui.

%prep
%setup -q -n libcall-ui-v%{version}

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libcall-ui-0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%find_lang call-ui

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f call-ui.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libcall-ui.so.*.*.*
%{_libdir}/girepository-1.0/Cui-0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcall-ui.so
%{_includedir}/libcall-ui
%{_datadir}/gir-1.0/Cui-0.gir
%{_pkgconfigdir}/libcall-ui.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcall-ui.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libcall-ui-0
%endif
