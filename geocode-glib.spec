#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	GLib geocoding library that uses the Yahoo! Place Finder service
Name:		geocode-glib
Version:	0.99.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://download.gnome.org/sources/geocode-glib/0.99/%{name}-%{version}.tar.bz2
# Source0-md5:	73ac778225f35ad996ea0345c5abe4b9
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.8
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.35.0
BuildRequires:	json-glib-devel >= 0.13.1
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
geocode-glib allows you to do geocoding (going from a place name, to a
longitude/latitude pair) and reverse geocoding (finding a place name
from coordinates).

%package devel
Summary:	Header files for geocode-glib library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki geocode-glib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

%description apidocs
API documentation for geocode-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki geocode-glib.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable static_libs static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgeocode-glib.so
%{_libdir}/libgeocode-glib.la
%{_includedir}/geocode-glib
%{_datadir}/gir-1.0/GeocodeGlib-1.0.gir
%{_pkgconfigdir}/geocode-glib.pc

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
