%define oname Sigil

Summary:	A free, open source WYSIWYG ebook editor
Name:		sigil
Version:	2.5.1
Release:	1
Url:		https://sigil-ebook.com/
Source0:	https://github.com/Sigil-Ebook/Sigil/archive/%{version}/%{oname}-%{version}.tar.gz
License:	GPLv3
Group:		Office/Utilities

Patch0:		sigil-1.9.30-compile.patch

BuildRequires:	cmake(Qt6)
BuildRequires:	cmake ninja
BuildRequires:	boost-devel
BuildRequires:	zlib-devel bzip2-devel
BuildRequires:	libxerces-c-devel
BuildRequires:	hunspell-devel
BuildRequires:	pcre-devel
BuildRequires:  qt6-qttools
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Core5Compat)
BuildRequires:	pkgconfig(Qt6Linguist)
BuildRequires:	pkgconfig(Qt6Concurrent) 
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Help)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6PrintSupport)
BuildRequires:	pkgconfig(Qt6Qml)
BuildRequires:	pkgconfig(Qt6Quick)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6WebEngineCore)
BuildRequires:	pkgconfig(Qt6WebEngineWidgets)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6Xml)
BuildRequires:	pkgconfig(hunspell) >= 1.3.2
BuildRequires:	pkgconfig(libpcre) >= 8.31
BuildRequires:	pkgconfig(zlib) >= 1.2.7
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(python)

Requires:	python3dist(lxml)

Recommends:	%mklibname qt5gui5-x11

%description
Sigil is a free, open source WYSIWYG e-book editor.
It is designed to edit books in ePub format.

%prep
%autosetup -p1 -n %{oname}-%{version}
# there are only internal helper libs, and they need to be static as build
# fails otherwise (they contain undefined symbols), and making them shared
# libs wouldn't make sense anyway (they are not shared by anything else)
# - Anssi 06/2010
%cmake \
	-DSHARE_INSTALL_PREFIX=%{_prefix} \
	-DUSE_SYSTEM_LIBS:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

find %{buildroot} -name 'opf_newparser.py' -exec sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/env python3|g' {} \;
find %{buildroot} -name 'sanitycheck.py' -exec sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/env python3|g' {} \;

# install icons for the .desktop file
install -m644 -D src/Resource_Files/icon/app_icons_orig/app_icon_16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 -D src/Resource_Files/icon/app_icons_orig/app_icon_32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 -D src/Resource_Files/icon/app_icons_orig/app_icon_48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m644 -D src/Resource_Files/icon/app_icons_orig/app_icon_128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
install -m644 -D src/Resource_Files/icon/app_icons_orig/app_icon_256.png %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png

%files
%doc ChangeLog.txt README.md
%license COPYING.txt
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/pixmaps/*.png

