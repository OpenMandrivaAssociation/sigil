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


%changelog
* Thu Jun 28 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 0.5.3-1
+ Revision: 807382
- update to 0.5.3

* Tue Jan 24 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 0.5.0-1
+ Revision: 767807
- add Russian dictionaries
- new version 0.5.0

* Wed Jan 11 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 0.4.2-1
+ Revision: 759787
- fixed linking to boost
- new version 0.4.2

* Thu Mar 17 2011 Funda Wang <fwang@mandriva.org> 0.3.4-2
+ Revision: 645796
- rebuild for new boost

* Thu Feb 03 2011 Ahmad Samir <ahmadsamir@mandriva.org> 0.3.4-1
+ Revision: 635702
- update to 0.3.4

* Wed Nov 24 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.3.2-1mdv2011.0
+ Revision: 600474
- update to 0.3.2

* Mon Nov 08 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.3.1-1mdv2011.0
+ Revision: 595009
- update to 0.3.1

* Fri Nov 05 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.3.0-1mdv2011.0
+ Revision: 593775
- update to 0.3.0

* Sun Oct 10 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.3.0-0.RC2.1mdv2011.0
+ Revision: 584546
- update to 0.3.0RC2

* Sat Oct 09 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.3.0-0.RC1.1mdv2011.0
+ Revision: 584293
- update to 0.3.0RC1
- bump qt BR to 4.7.0
- add BR, libxerces-c-devel
- rediff patch1 and make the package build with system libxerces-c (thanks to Anssi \o/)
- modify spec to make packaging rc's easier

* Fri Aug 13 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.2.4-1mdv2011.0
+ Revision: 569342
- update to 0.2.4
- rediff patch1

* Wed Jun 23 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.2.3-1mdv2011.0
+ Revision: 548731
- what do you know? new upstream release 0.2.3
- add more BR (they're pulled by qt-devel, but I prefer an explicit BR in this case)
- import sigil


