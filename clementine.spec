Name:           clementine
Version:        1.0.1
Release:        2%{?dist}.R
Summary:        A music player and library organizer

Group:          Applications/Multimedia
License:        GPLv3+ and GPLv2+
URL:            http://code.google.com/p/clementine-player
Source0:        http://clementine-player.googlecode.com/files/%{name}-%{version}.tar.gz

# Use system sha2. Patch accepted by upstream
# http://code.google.com/p/clementine-player/issues/detail?id=2623
Patch0:         clementine-system-sha2.patch
# Desktop file fixes. Sent upstream
# http://code.google.com/p/clementine-player/issues/detail?id=2690
Patch1:         clementine-desktop.patch
# Fixes startup on a fresh install. From upstream trunk
Patch2:         clementine-fresh-start.patch


BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gmock-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  gtest-devel
%if 0%{fedora} > 16
BuildRequires:  kdeplasma-addons-devel
%endif
BuildRequires:  libcdio-devel
BuildRequires:  libchromaprint-devel
BuildRequires:  libechonest-devel
%ifnarch s390 s390x
BuildRequires:  libgpod-devel
BuildRequires:  libimobiledevice-devel
%endif
BuildRequires:  liblastfm-devel
BuildRequires:  libmtp-devel 
BuildRequires:  libnotify-devel
BuildRequires:  libplist-devel 
BuildRequires:  libprojectM-devel >= 2.0.1-7
BuildRequires:  libqxt-devel
BuildRequires:  notification-daemon
BuildRequires:  protobuf-devel
BuildRequires:  qca2-devel
BuildRequires:  qt4-devel
BuildRequires:  qjson-devel
BuildRequires:  qtiocompressor-devel
BuildRequires:  qtsinglecoreapplication-devel
BuildRequires:  qtsingleapplication-devel >= 2.6.1-2
BuildRequires:  sha2-devel
BuildRequires:  sqlite-devel
BuildRequires:  taglib-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  xorg-x11-xauth

Requires:       hicolor-icon-theme
Requires:       libprojectM >= 2.0.1-7
Requires:       qtsingleapplication >= 2.6.1-2

%description
Clementine is a multi-platform music player. It is inspired by Amarok 1.4,
focusing on a fast and easy-to-use interface for searching and playing your
music.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Remove all 3rdparty libraries exceph universalchardet
# as it is not available as a separate library.
mv 3rdparty/universalchardet/ .
rm -fr 3rdparty/*
mv universalchardet/ 3rdparty/

# Can't run all the unit tests
#   songloader requires internet connection
#   mpris1 requires a dbus session
for test in mpris1 songloader; do
    sed -i -e "/${test}_test/d" tests/CMakeLists.txt
done

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
    %{cmake} \
        -DUSE_SYSTEM_QTSINGLEAPPLICATION=1 \
        -DUSE_SYSTEM_PROJECTM=1 \
        -DUSE_SYSTEM_QXT=1 \
        -DSTATIC_SQLITE=0 \
%if 0%{fedora} > 16
        -DENABLE_PLASMARUNNER=1 \
%endif
        .. 

    # Parallel build fails sometimes
    make VERBOSE=1
popd

%install
make install DESTDIR=%{buildroot} -C %{_target_platform}


%check
pushd %{_target_platform}
    # Run a fake X session since some tests check for X
    # Yet the tests still fail sometimes
    xvfb-run -a -n 10 make test ||:
popd

desktop-file-validate \
    %{buildroot}%{_datadir}/applications/%{name}.desktop


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
%doc Changelog COPYING
%{_bindir}/clementine
%{_datadir}/applications/clementine.desktop
%{_datadir}/icons/hicolor/64x64/apps/application-x-clementine.png
%{_datadir}/icons/hicolor/scalable/apps/application-x-clementine.svg
%if 0%{fedora} > 16
%{_libdir}/kde4/plasma_runner_clementine.so
%{_datadir}/kde4/services/plasma-runner-clementine.desktop
%endif

%changelog
* Thu Feb 07 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-2
- Re-add the fresh start patch. Looks like it didn't make it to 1.0.1
- Include plasma addon only in F-17+

* Thu Feb 02 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-1
- New upstream release RHBZ#772175

* Thu Jan 12 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-6
- Fix startup on a fresh install RHBZ#773547
- Some specfile clean-ups

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.1-4.1
- rebuild (libechonest)

* Tue Nov 29 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-4
- Lastfm login fix RHBZ#757280
- Patches for building against newer glibmm24 and glib2

* Mon Oct 10 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-3
- Rebuild for libechonest soname bump.

* Sat Jun 11 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-2
- Rebuild due to libmtp soname bump. Was this announced?

* Thu Mar 31 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-1
- New upstream release
- Drop upstreamed patch

* Thu Mar 31 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7-2
- gcc-4.6 fix

* Wed Mar 30 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7-1
- New upstream version
- Drop all upstreamed patches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6-2
- Rebuilt against new libimobiledevice on F-15

* Thu Dec 23 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6-1
- New upstream version

* Thu Oct 14 2010 Dan Horák <dan[at]danny.cz> - 0.5.3-2
- Update BRs for s390(x)

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
