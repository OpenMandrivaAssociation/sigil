%define oname Sigil

%define version 0.5.3
%define prerel 0
%define rel 1

%if %prerel
%define release 0.%{prerel}.%{rel}
%define srcname %{oname}-%{version}%{prerel}
%else
%define release %{rel}
%define srcname %{oname}-%{version}
%endif

Summary:	A free, open source WYSIWYG ebook editor
Name:		sigil
Version:	%{version}
Release:	%{release}
Url:		http://code.google.com/p/sigil/
Source0:	http://sigil.googlecode.com/files/%{srcname}-Code.zip
Source1:	ru_RU.aff
Source2:	ru_RU.dic
# from Anssi: this makes it use system libs instead of bundled ones. Except for
# libtidy which has some local hacks not present in system-provided libtidy.
# code is GPlv3 and content is CC BY-SA
License:	GPLv3 and Creative Commons Attribution-ShareAlike
Group:		Office
BuildRequires:	cmake
BuildRequires:	qt4-devel >= 4:4.7.0
BuildRequires:	boost-devel >= 1.48.0
BuildRequires:	zlib-devel bzip2-devel
BuildRequires:	libxerces-c-devel
BuildRequires:	hunspell-devel
BuildRequires:	pcre-devel

%description
Sigil is a free, open source WYSIWYG e-book editor.
It is designed to edit books in ePub format.

%prep
%setup -q -c -n %{srcname}-Code

rm -fr src/BoostParts
# fix end of line encoding for the docs:
sed -i 's/\r//' ChangeLog.txt README.txt COPYING.txt

%build
# there are only internal helper libs, and they need to be static as build
# fails otherwise (they contain undefined symbols), and making them shared
# libs wouldn't make sense anyway (they are not shared by anything else)
# - Anssi 06/2010
%cmake -G "Unix Makefiles" -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_STATIC_LIBS:BOOL=ON
%make

%install
%makeinstall_std -C build

# install icons for the .desktop file
install -m644 -D src/Sigil/Resource_Files/icon/app_icon_16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/sigil.png
install -m644 -D src/Sigil/Resource_Files/icon/app_icon_32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/sigil.png
install -m644 -D src/Sigil/Resource_Files/icon/app_icon_48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/sigil.png
install -m644 -D src/Sigil/Resource_Files/icon/app_icon_128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/sigil.png
install -m644 -D src/Sigil/Resource_Files/icon/app_icon_256.png %{buildroot}%{_iconsdir}/hicolor/256x256/apps/sigil.png

# create a .desktop file:
mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Name=%{oname}
Comment=WYSIWYG ebook editor
Icon=%{name}
Exec=%{name} %u
MimeType=application/epub+zip;
Categories=Office;
EOF

# install additional dictionaries
install -m644 -D %{SOURCE1} %{SOURCE2} %{buildroot}%{_datadir}/%{name}/dictionaries/

%find_lang %{name} --with-qt

%files -f %{name}.lang
%doc ChangeLog.txt README.txt COPYING.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/pixmaps/*.png
%{_datadir}/%{name}/dictionaries
