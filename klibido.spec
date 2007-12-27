Summary:	KLibido - KDE Linux Binaries Downloader
Summary(pl.UTF-8):	KLibido - narzędzie do ściągania binariów dla KDE
Name:		klibido
Version:	0.2.5
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/klibido/%{name}-%{version}.tar.gz
# Source0-md5:	e343338541a3ff3f2983023ccc922af0
Patch0:		%{name}-gcc4.patch
Patch1:		kde-ac260.patch
Patch2:		kde-am1.10.patch
URL:		http://klibido.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db-cxx-devel
BuildRequires:	kdelibs-devel >= 9:3.2.0
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	uudeview-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KLibido is a KDE usenet news grabber for Linux.

%description -l pl.UTF-8
KLibido jest narzędziem do ściągania załączników binarnych z grup
dyskusyjnych napisanym dla KDE.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.sub admin
%{__make} -f admin/Makefile.common cvs

%configure \
%if "%{_lib}" == "lib64"
	--enable-libsuffix=64 \
%endif
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--with-qt-libraries=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir}

install -d $RPM_BUILD_ROOT%{_desktopdir}/kde
mv $RPM_BUILD_ROOT/usr/share/applnk/Utilities/*.desktop \
    $RPM_BUILD_ROOT%{_desktopdir}/kde

%find_lang %{name} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:

%postun
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/kde/*.desktop
%{_datadir}/apps/%{name}
%{_iconsdir}/*/*/*/*
