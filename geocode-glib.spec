#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	libsoup3	# libsoup3 variant (geocode-glib-2)
%bcond_without	static_libs	# static library (geocode-glib 1.0 only)

Summary:	GLib geocoding library that uses the Nominatim service
Summary(pl.UTF-8):	Biblioteka GLib do geokodowania wykorzystująca serwis Nominatim
Name:		geocode-glib
Version:	3.26.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/geocode-glib/3.26/%{name}-%{version}.tar.xz
# Source0-md5:	748921b2cfa8450ac6857c5da370e129
URL:		https://developer.gnome.org/geocode-glib/
BuildRequires:	gettext-tools >= 0.19.6
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	gtk-doc >= 1.13
BuildRequires:	json-glib-devel >= 0.99.2
BuildRequires:	libsoup-devel >= 2.42
%{?with_libsoup3:BuildRequires:	libsoup3-devel >= 3.0}
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
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
Requires:	json-glib-devel >= 0.99.2
Requires:	libsoup-devel >= 2.42

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
BuildArch:	noarch

%description apidocs
API documentation for geocode-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki geocode-glib.

%package -n geocode-glib2
Summary:	GLib geocoding library that uses the Nominatim service (soup3 version)
Summary(pl.UTF-8):	Biblioteka GLib do geokodowania wykorzystująca serwis Nominatim (wersja soup3)
Group:		Libraries
Requires:	glib2 >= 1:2.44
Requires:	json-glib >= 0.99.2
Requires:	libsoup3 >= 3.0

%description -n geocode-glib2
geocode-glib allows you to do geocoding (going from a place name, to a
longitude/latitude pair) and reverse geocoding (finding a place name
from coordinates).

This package uses libsoup 3 library.

%description -n geocode-glib2 -l pl.UTF-8
Ten pakiet umożliwia geokodowanie (kodowanie geograficzne - zamianę
nazwy miejsca na parę długość/szerokość geograficzna) oraz odwrotne
geokodowanie (odnajdywanie nazwy miejsca na podstawie współrzędnych).

Ten pakiet wykorzystuje bibliotekę libsoup 3.

%package -n geocode-glib2-devel
Summary:	Header files for geocode-glib-2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki geocode-glib-2
Group:		Development/Libraries
Requires:	geocode-glib2 = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44
Requires:	json-glib-devel >= 0.99.2
Requires:	libsoup3-devel >= 3.0

%description -n geocode-glib2-devel
Header files for geocode-glib-2 library.

%description -n geocode-glib2-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki geocode-glib-2.

%package -n geocode-glib2-apidocs
Summary:	geocode-glib-2 API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki geocode-glib-2
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description -n geocode-glib2-apidocs
API documentation for geocode-glib-2 library.

%description -n geocode-glib2-apidocs -l pl.UTF-8
Dokumentacja API biblioteki geocode-glib-2.

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

%if %{with libsoup3}
%meson build-soup3 \
	--default-library=shared \
	%{!?with_apidocs:-Denable-gtk-doc=false} \
	-Denable-installed-tests=false \
	-Dsoup2=false

%ninja_build -C build-soup3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with libsoup3}
%ninja_install -C build-soup3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n geocode-glib2 -p /sbin/ldconfig
%postun	-n geocode-glib2 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libgeocode-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgeocode-glib.so.0
%{_libdir}/girepository-1.0/GeocodeGlib-1.0.typelib
%{_iconsdir}/hicolor/scalable/places/poi-*.svg

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

%if %{with libsoup3}
%files -n geocode-glib2
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libgeocode-glib-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgeocode-glib-2.so.0
%{_libdir}/girepository-1.0/GeocodeGlib-2.0.typelib
%{_iconsdir}/hicolor/scalable/places/poi-*.svg

%files -n geocode-glib2-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgeocode-glib-2.so
%{_includedir}/geocode-glib-2.0
%{_datadir}/gir-1.0/GeocodeGlib-2.0.gir
%{_pkgconfigdir}/geocode-glib-2.0.pc

%if %{with apidocs}
%files -n geocode-glib2-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/geocode-glib-2
%endif
%endif
