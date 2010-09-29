Name:           clementine
Version:        0.5.3
Release:        1%{?dist}
Summary:        A music player and library organizer

Group:          Applications/Multimedia
License:        GPLv3+ and GPLv2+
URL:            http://code.google.com/p/clementine-player
Source0:        http://clementine-player.googlecode.com/files/%{name}-%{version}.tar.gz
# This 3rd party library is not needed on Linux. Patch accepted by upstream
# http://code.google.com/p/clementine-player/issues/detail?id=798
Patch0:         clementine-no-qtwin.patch
# Safeguard against a null pipeline in GstEngine::Play. From upstream trunk
# Fixes RHBZ#636544
# http://code.google.com/p/clementine-player/source/detail?r=2063
Patch1:         clementine-gst-safeguard.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gstreamer-devel
BuildRequires:  gtest-devel
BuildRequires:  libgpod-devel
BuildRequires:  libimobiledevice-devel
BuildRequires:  liblastfm-devel
BuildRequires:  libmtp-devel 
BuildRequires:  libnotify-devel
BuildRequires:  libplist-devel 
BuildRequires:  libprojectM-devel >= 2.0.1-7
BuildRequires:  libqxt-devel
BuildRequires:  notification-daemon
BuildRequires:  qt4-devel
BuildRequires:  qtiocompressor-devel
BuildRequires:  qtsinglecoreapplication-devel
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
%patch0 -p1 -b .noqtwin
%patch1 -p1 -b .gstsafeguard

# Remove all 3rdparty libraries exceph universalchardet
# as it is not available as a separate library.
mv 3rdparty/universalchardet/ .
rm -fr 3rdparty/*
mv universalchardet/ 3rdparty/


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
   -DSTATIC_SQLITE=0 \
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
%{_datadir}/icons/hicolor/scalable/apps/application-x-clementine.svg


%changelog
* Wed Sep 29 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.5.3-1
- New upstream version

* Sun Sep 26 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.5.2-1
- New upstream version

* Wed Sep 22 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.5.1-1
- New upstream version
- Drop all upstreamed patches

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
