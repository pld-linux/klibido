Summary:	KLibido - KDE Linux Binaries Downloader
Summary(pl):	KLibido - narzêdzie do ¶ci±gania binariów dla KDE
Name:		klibido
Version:	0.2.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/klibido/%{name}-%{version}.tar.gz
# Source0-md5:	d4851385b333ddf8970ac24955ea4c48
Patch0:		%{name}-bugfix.patch
URL:		http://klibido.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	kdelibs-devel >= 9:3.2.0
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	uudeview-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KLibido is a KDE usenet news grabber for Linux.

%description -l pl
KLibido jest narzêdziem do ¶ci±gania za³±czników binarnych z grup
dyskusyjnych napisanym dla KDE.

%prep
%setup -q
%patch0 -p1

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

%find_lang %{name} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
#XXX: use desktopdir %{_datadir}/applnk/*/*
%{_datadir}/apps/%{name}
%{_iconsdir}/*/*/*/*
