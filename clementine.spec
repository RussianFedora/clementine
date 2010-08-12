Name:           clementine
Version:        0.4.2
Release:        9%{?dist}
Summary:        A music player and library organizer

Group:          Applications/Multimedia
License:        GPLv3+ and GPLv2+
URL:            http://code.google.com/p/clementine-player
Source0:        http://clementine-player.googlecode.com/files/%{name}-%{version}.tar.gz
# The following patches 0-4 are from the upstream trunk
# Fix trailing semicolon
# http://code.google.com/p/clementine-player/source/detail?r=1486
Patch0:         clementine-desktop-fix.patch
# The next 3 are to split out the bundled libraries
# http://code.google.com/p/clementine-player/source/detail?r=1443
Patch1:         clementine-system-projectM.patch
# http://code.google.com/p/clementine-player/source/detail?r=1444
Patch2:         clementine-system-qtsingleapplication.patch
# http://code.google.com/p/clementine-player/source/detail?r=1445
Patch3:         clementine-system-qtiocompressor.patch
# Also split qxt. Patch accepted by upstream
#http://code.google.com/p/clementine-player/source/detail?r=1512
Patch4:         clementine-system-qxt.patch
# We need to pass the font paths to the Renderer constructor of libprojectM.
# Otherwise ftgl library segfaults. Note that this is not a problem if projectM
# is not compiled with ftgl support. However, the Fedora package is. More
# details on this at
# http://code.google.com/p/clementine-player/issues/detail?id=291#c22
Patch5:         clementine-font-paths.patch
# Fix lastFM crash RHBZ#618474
# http://code.google.com/p/clementine-player/issues/detail?id=463
# From upstream trunk
Patch6:         clementine-fix-lastfm-crash.patch
# Enforce Fedora specific optimization flags. Accepted by upstream.
# http://code.google.com/p/clementine-player/source/detail?r=1639
Patch7:         clementine-fix-buildfags.patch
# Only create the OpenGL graphics context when you first open the visualisations
# window. Fixes RHBZ#621913. From upstream trunk:
# http://code.google.com/p/clementine-player/source/detail?spec=svn1661&r=1431
Patch8:         clementine-visualization-init.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gstreamer-devel
BuildRequires:  gtest-devel
BuildRequires:  liblastfm-devel
BuildRequires:  libnotify-devel
BuildRequires:  libprojectM-devel >= 2.0.1-7
BuildRequires:  libqxt-devel
BuildRequires:  notification-daemon
BuildRequires:  qt4-devel
BuildRequires:  qtiocompressor-devel
BuildRequires:  qtsingleapplication-devel >= 2.6.1-2
BuildRequires:  sqlite-devel
BuildRequires:  taglib-devel

Requires:       hicolor-icon-theme
Requires:       libprojectM >= 2.0.1-7
Requires:       qtsingleapplication >= 2.6.1-2

%description
Clementine is a modern music player and library organizer.
It is largely a port of Amarok 1.4, with some features rewritten to take
advantage of Qt4.

%prep
%setup -q
%patch0 -p1 -b .desktopfix
%patch1 -p1 -b .projectM
%patch2 -p1 -b .qtsingleapplication
%patch3 -p1 -b .qtiocompressor
%patch4 -p1 -b .qxt
%patch5 -p1 -b .fontpaths
%patch6 -p1 -b .fix.lastfm.crash
%patch7 -p1 -b .build.flags
%patch8 -p1 -b .visual.init

# We already don't use these but just to make sure
rm -fr 3rdparty/gmock
rm -fr 3rdparty/libprojectm
rm -fr 3rdparty/qxt
rm -fr 3rdparty/qsqlite
rm -fr 3rdparty/qtiocompressor
rm -fr 3rdparty/qtsingleapplication


# Don't build tests. They require gmock which is not yet available on Fedora
# RHBZ #527402
sed -i '/tests/d' CMakeLists.txt


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
   -DUSE_SYSTEM_QTSINGLEAPPLICATION=1 \
   -DUSE_SYSTEM_PROJECTM=1 \
   -DUSE_SYSTEM_QXT=1 \
   .. 


# Parallel build fails sometimes
make VERBOSE=1
popd

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}


%check
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%doc Changelog COPYING TODO
%{_bindir}/clementine
%{_datadir}/applications/clementine.desktop
%{_datadir}/icons/hicolor/64x64/apps/application-x-clementine.png


%changelog
* Sun Aug 08 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-9
- Only create the OpenGL graphics context when you first open the visualisations
  window. Fixes RHBZ#621913

* Fri Aug 06 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-8
- Enforce Fedora compilation flags

* Thu Aug 05 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-7
- Fix crash on lastfm tree RHBZ#618474

* Tue Jul 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-6
- Rebuild against new boost on F-14

* Fri Jul 23 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-5
- Add missing scriptlets

* Wed Jul 21 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-4
- Use: make VERBOSE=1
- License is GPLv3+ and GPLv2+
- Put BRs in alphabetical order
- Remove redundant BRs: glew-devel, xine-lib-devel, and
  the extra libprojectM-devel
- Add R: hicolor-icon-theme

* Sun Jul 18 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-3
- Better qxt split patch

* Sat Jul 17 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-2
- Fix font paths issue, which caused a segfault on visualizations

* Sat Jul 17 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-1
- Version 0.4.2

* Fri May 07 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.3-1
- Version 0.3

* Sat Apr 17 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.2-2
- Patch out the external libraries
- Build the libclementine_lib into the final executable

* Sat Mar 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.2-1
- Fedorized the upstream specfile

* Mon Mar 22 2010 David Sansome <me@davidsansome.com> - 0.2
- Version 0.2

* Sun Feb 21 2010 David Sansome <me@davidsansome.com> - 0.1-5
- Various last-minute bugfixes

* Sun Jan 17 2010 David Sansome <me@davidsansome.com> - 0.1-1
- Initial package
