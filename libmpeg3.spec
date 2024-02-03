Summary: Decoder of various derivatives of MPEG standards
Name: libmpeg3
Version: 1.8
Release: 22%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://heroinewarrior.com/libmpeg3.php3
Source: http://dl.sf.net/heroines/libmpeg3-%{version}-src.tar.bz2

# patch from https://github.com/sergiomb2/libmpeg3
# date=$(date +%Y%m%d)
# git clone git@github.com:sergiomb2/libmpeg3.git
# tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
# git diff 1.8 . > "$date"_git"$tag".patch
Patch0: 20140922_git47a2f45.patch

#BuildRequires: nasm
BuildRequires: a52dec-devel
# libquicktime is FTBFS in F28
%if 0%{?fedora} <= 27
BuildRequires: libquicktime-devel >= 0.9.8
%endif
BuildRequires: libtool

%description
LibMPEG3 decodes the many many derivatives of MPEG standards into
uncompressed data suitable for editing and playback.

libmpeg3 currently decodes:
 - MPEG-1 Layer II/III Audio and program streams
 - MPEG-2 Layer III Audio, program streams and transport streams
 - MPEG-1 and MPEG-2 Video
 - AC3 Audio
 - IFO files
 - VOB files


%package utils
Summary: Utilities from libmpeg3
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description utils
LibMPEG3 decodes the many many derivatives of MPEG standards into
uncompressed data suitable for editing and playback.

This package contains utility programs based on libmpeg3.


%package devel
Summary: Development files for libmpeg3
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
LibMPEG3 decodes the many many derivatives of MPEG standards into
uncompressed data suitable for editing and playback.

This package contains files needed to build applications that will use
libmpeg3.


%prep
%setup -q
%patch0 -p1 -b .github

chmod 755 bootstrap
./bootstrap


%build
# Enable USE_MMX for archs that support it, not by default on i386
%configure --enable-shared --disable-static \
%if 0
  --enable-mmx \
%endif

# This seems not to work with x86_64 on AMD64
# Error: suffix or operands invalid for `push'
#sed -i -e 's|$(CCASFLAGS)|#$(CCASFLAGS)|g' video/Makefile

# Hack to have mmx compiled on i686
%if 0
pushd video
mkdir -p .libs
nasm -f elf reconmmx.s -o .libs/reconmmx.o
popd
%endif

%make_build


%install
%make_install LIBDIR=%{_libdir}

%{__rm} -rf %{buildroot}%{_libdir}/*.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license COPYING
%{_libdir}/*.so.*

%files utils
%{_bindir}/mpeg3cat
%{_bindir}/mpeg3dump
%{_bindir}/mpeg3peek
%{_bindir}/mpeg3toc
%if 0%{?fedora} <= 27
%{_bindir}/mpeg2qt
%endif

%files devel
%doc docs/*
%{_libdir}/*.so
%{_includedir}/mpeg3/
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.8-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.8-10
- Build without libquicktime for F28

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 22 2014 Sérgio Basto <sergio@serjux.com> - 1.8-7
- Use 20140922_git47a2f45.patch, repo sergiomb2/libmpeg3 has been refactored,
  almost just update git hash

* Tue Aug 26 2014 Sérgio Basto <sergio@serjux.com> - 1.8-6
- update to 20140830_git6c02a5e.patch (fixes when uses -Werror=format-security)
- add mpeg3protos.h to pkginclude_HEADERS 
- use https://github.com/sergiomb2/libmpeg3 with all patches
- spec clean up

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.8-5
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  4 2009 kwizart < kwizart at gmail.com > - 1.8-3
- Rebuild for F-12
- Disable mmx (broken)

* Fri Mar 27 2009 kwizart < kwizart at gmail.com > - 1.8-2
- Rebuild

* Mon Aug 11 2008 kwizart < kwizart at gmail.com > - 1.8-1
- Upate to 1.8
- Enable cinelerra-cv hacks

* Sat Jan 12 2008 kwizart < kwizart at gmail.com > - 1.7-6
- Fix mpeg2qt linked with libquicktime
- Disable mmx 

* Fri Sep 28 2007 kwizart < kwizart at gmail.com > - 1.7-5
- Add gentoo patches
  7: Remove executable stacks, thanks to Martin von Gagern in gentoo #131155.
  8: Fix missing include string.h for implicit declaration of memcpy.

* Thu Sep 13 2007 kwizart < kwizart at gmail.com > - 1.7-4
- Add autotools support (default is shared )
- Remove internal css
- Build with our cflags (-fPIC is no more necessary )
- TODO build mpeg2qt

* Fri Sep  7 2007 kwizart < kwizart at gmail.com > - 1.7-3
- Add dist tag
- modified patch for Makefile
- Add BR's

* Wed Sep 20 2006 Matthias Saou <http://freshrpms.net/> 1.7-2
- Run make twice since there is an EOF error that makes the first run abort.

* Mon Jul  3 2006 Matthias Saou <http://freshrpms.net/> 1.7-1
- Update to 1.7.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 1.6-2
- Add -fPIC to the CFLAGS to fix transcode build on x86_64.

* Thu Jan 19 2006 Matthias Saou <http://freshrpms.net/> 1.6-1
- Update to 1.6.
- Split "main" into "utils" (bin) and "devel" (the static lib).
- Add Makefile patch to ease install and get our CFLAGS used.
- Don't enable MMX on x86_64, the x86 asm fails.

* Mon Aug 15 2005 Matthias Saou <http://freshrpms.net/> 1.5.4-5
- Force __USE_LARGEFILE64 to fix FC4 ppc build.

* Fri Apr 22 2005 Matthias Saou <http://freshrpms.net/> 1.5.4-4
- Add gcc4 patch.

* Thu Nov  4 2004 Matthias Saou <http://freshrpms.net/> 1.5.4-3
- Remove unneeded /usr/bin fix, since we don't use "make install".
- Replace -O? with -O1 in optflags since build fails with O2 and gcc 3.4.
- Make nasm mandatory : The configure script won't run without it anyway.
- Use libdir/*.* in order to not catch all debuginfo files too.
- Added -devel provides for now.

* Sat Jun 26 2004 Dag Wieers <dag@wieers.com> - 1.5.4-2
- Fixes for x86_64.

* Wed Apr 07 2004 Dag Wieers <dag@wieers.com> - 1.5.4-1
- Updated to release 1.5.4.

* Mon Sep 08 2003 Dag Wieers <dag@wieers.com> - 1.5.2-0
- Updated to release 1.5.2.

* Wed Feb 12 2003 Dag Wieers <dag@wieers.com> - 1.4-0
- Initial package. (using DAR)
