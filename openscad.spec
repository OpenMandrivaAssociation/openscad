%define uversion 2015.03-2
%define _disable_lto 1
%define debug_package %nil

Name:           openscad
Version:        2021.01
Release:        1
Summary:        The Programmers Solid 3D CAD Modeller
# COPYING contains a linking exception for CGAL
# AppData is CC0
License:        GPLv2 with exceptions and CC0
Group:          Graphics
URL:            http://www.openscad.org/
Source0:        https://github.com/openscad/openscad/releases/download/%{name}-%{version}/%{name}-%{version}.src.tar.gz
Patch1:         openscad-polyclipping.patch

BuildRequires:  bison
BuildRequires:  boost-devel
BuildRequires:  cgal-devel
BuildRequires:  cmake
BuildRequires:  qmake5
BuildRequires:  flex
BuildRequires:  pkgconfig(gmp)
BuildRequires:  imagemagick
BuildRequires:  pkgconfig(mpfr)
BuildRequires:  opencsg-devel
BuildRequires:  cmake(double-conversion)
BuildRequires:  pkgconfig(eigen3)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(polyclipping)
BuildRequires:  pkgconfig(egl)
#BuildRequires:  pkgconfig(lib3mf)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  qscintilla-qt5-devel
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gamepad)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5PrintSupport)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  x11-server-xvfb

%description
OpenSCAD is a software for creating solid 3D CAD objects.
Unlike most free software for creating 3D models (such as the famous
application Blender) it does not focus on the artistic aspects of 3D
modeling but instead on the CAD aspects. Thus it might be the application
you are looking for when you are planning to create 3D models of machine
parts but pretty sure is not what you are looking for when you are more
interested in creating computer-animated movies.

%prep
%autosetup -p1

# Unbundle polyclipping
rm -rf src/ext/polyclipping

%build
# respect cflags
sed -i "s/QMAKE_CXXFLAGS_RELEASE = .*//g" %{name}.pro
# don't force /usr/local
sed -i "s/\/usr\/local/\/usr/g" %{name}.pro

%qmake_qt5 VERSION=%{uversion} \
           PREFIX=%{_prefix} \
           CONFIG-=debug
# Work around bug
# https://github.com/openscad/openscad/issues/1546
sed -i -e 's!/usr/bin/flex!/usr/bin/flex --prefix=lexer!' Makefile
%make

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%doc COPYING README.md RELEASE_NOTES.md
%dir %{_datadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/%{name}/*
%doc %{_mandir}/man1/%{name}.1*
