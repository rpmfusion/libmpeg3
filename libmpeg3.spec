Summary: Decoder of various derivatives of MPEG standards
Name: libmpeg3
Version: 1.8
Release: 5%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://heroinewarrior.com/libmpeg3.php3
Source: http://dl.sf.net/heroines/libmpeg3-%{version}-src.tar.bz2
Patch1: libmpeg3-1.8-cinelerra_autotools.patch
Patch2: libmpeg3-1.7-cinelerra_hacking.patch
Patch3: libmpeg3-1.7-fix_commented.patch
Patch4: libmpeg3-1.7-spec_in.patch
Patch5: libmpeg3-1.7-pkgconfig.in.patch
Patch6: libmpeg3-1.7-boostrap.patch
# Patches 7/8 from gentoo
#http://sources.gentoo.org/viewcvs.py/gentoo-x86/media-libs/libmpeg3/files/
Patch7: libmpeg3-1.5.2-gnustack.patch
Patch9: libmpeg3-1.7-mpeg2qt-args.patch
Patch10: libmpeg3-1.8-mmx.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires: nasm
BuildRequires: a52dec-devel
BuildRequires: libquicktime-devel
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
# Removed unneeded files
rm -rf a52dec-* depend.a52

# Patch autotools
%patch1 -p1

# Thoses patches was taken from cinepaint cvs
# Which have special libmpeg3
%patch2 -p1 -b .cine_hack

# Fix comments
%patch3 -p1 -b .commented

# Add spec.in
%patch4 -p1

# Add pkgconfig.in
%patch5 -p1

# Add ./bootstrap
%patch6 -p1

# gentoo patches
%patch7 -p1 -b .gnustack

# Patch the number of arguments of mpeg2qt
%patch9 -p1 -b .args

# Patch to add mmx possibility via nasm/yasm
%patch10 -p1 -b .mmx

# Touch docs files:
touch INSTALL README NEWS AUTHORS ChangeLog

# Build autotools
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

make %{?_smp_mflags}



%install
%{__rm} -rf %{buildroot}

%{__make} install \
    LIBDIR=%{_libdir} \
    DESTDIR=%{buildroot} \
    INSTALL="install -c -p"

%{__rm} -rf %{buildroot}%{_libdir}/*.la


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc COPYING
%{_libdir}/*.so.*

%files utils
%defattr(-, root, root, -)
%{_bindir}/mpeg3cat
%{_bindir}/mpeg3dump
%{_bindir}/mpeg3peek
%{_bindir}/mpeg3toc
%{_bindir}/mpeg2qt

%files devel
%doc docs/*
%defattr(-, root, root,-)
%{_libdir}/*.so
%{_includedir}/mpeg3/
%{_libdir}/pkgconfig/%{name}.pc


%changelog
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

* Sat Jan 10 2008 kwizart < kwizart at gmail.com > - 1.7-6
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
