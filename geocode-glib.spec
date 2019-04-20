#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	GLib geocoding library that uses the Yahoo! Place Finder service
Summary(pl.UTF-8):	Biblioteka GLib do geokodowania wykorzystująca serwis Yahoo! Place Finder
Name:		geocode-glib
Version:	3.26.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/geocode-glib/3.26/%{name}-%{version}.tar.xz
# Source0-md5:	21094494e66c86368add6a55bf480049
URL:		https://developer.gnome.org/geocode-glib/
BuildRequires:	gettext-tools >= 0.19.6
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	gtk-doc >= 1.13
BuildRequires:	json-glib-devel >= 0.99.2
BuildRequires:	libsoup-devel >= 2.42
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.44
Requires:	json-glib >= 0.99.2
Requires:	libsoup >= 2.42
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
geocode-glib allows you to do geocoding (going from a place name, to a
longitude/latitude pair) and reverse geocoding (finding a place name
from coordinates).

%description -l pl.UTF-8
Ten pakiet umożliwia geokodowanie (kodowanie geograficzne - zamianę
nazwy miejsca na parę długość/szerokość geograficzna) oraz odwrotne
geokodowanie (odnajdywanie nazwy miejsca na podstawie współrzędnych).

%package devel
Summary:	Header files for geocode-glib library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki geocode-glib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44

%description devel
Header files for geocode-glib library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki geocode-glib.

%package static
Summary:	Static geocode-glib library
Summary(pl.UTF-8):	Statyczna biblioteka geocode-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static geocode-glib library.

%description static -l pl.UTF-8
Statyczna biblioteka geocode-glib.

%package apidocs
Summary:	geocode-glib API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki geocode-glib
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for geocode-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki geocode-glib.

%prep
%setup -q

%if %{with static_libs}
%{__sed} -i -e 's/shared_library/library/' geocode-glib/meson.build
%endif

%build
%meson build \
	%{!?with_apidocs:-Denable-gtk-doc=false} \
	-Denable-installed-tests=false

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libgeocode-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgeocode-glib.so.0
%{_libdir}/girepository-1.0/GeocodeGlib-1.0.typelib
%{_iconsdir}/gnome/scalable/places/poi-*.svg

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgeocode-glib.so
%{_includedir}/geocode-glib-1.0
%{_datadir}/gir-1.0/GeocodeGlib-1.0.gir
%{_pkgconfigdir}/geocode-glib-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgeocode-glib.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/geocode-glib
%endif
