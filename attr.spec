Summary: Utilities for managing filesystem extended attributes.
Name: attr
Version: 2.2.0
Release: 1
Prereq: /sbin/ldconfig
Conflicts: xfsdump < 2.0.0
BuildRoot: %{_tmppath}/%{name}-root
Source: http://acl.bestbits.at/current/tar/attr-%{version}.src.tar.gz
Patch1: attr-2.0.8-docperms.patch
Patch2: attr-2.2.0-multilib.patch
License: GPL
URL: http://acl.bestbits.at/
Group: System Environment/Base
BuildRequires: autoconf

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n libattr
Summary: Dynamic library for extended attribute support.
Group: System Environment/Libraries
License: LGPL
Prereq: /sbin/ldconfig

%description -n libattr
This package contains the libattr.so dynamic library which contains
the extended attribute system calls and library functions.

%package -n libattr-devel
Summary: Extended attribute static libraries and headers.
Group: Development/Libraries
License: LGPL
Requires: libattr

%description -n libattr-devel
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

Currently only ext2, ext3 and XFS support extended attributes.
The SGI IRIX compatibility API built above the Linux system calls is
used by programs such as xfsdump(8), xfsrestore(8) and xfs_fsr(8).

You should install libattr-devel if you want to develop programs
which make use of extended attributes.  If you install libattr-devel,
you'll also want to install attr.

%prep
%setup -q
# We need to turn off executable permissions on the script in %doc
# because we don't want to drag perl into the base.  Users advanced
# enough to have used ACLs before they were added to the distro can
# figure out how to chmod and how to install perl.  :-)
%patch1 -p1 -b .perms
%patch2 -p1 -b .multilib
autoconf

%build
# attr abuses libexecdir
%configure --libdir=/%{_lib} --libexecdir=%{_libdir}
make

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
DIST_INSTALL_LIB=`pwd`/install-lib.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV DIST_INSTALL_LIB
make install DIST_MANIFEST="$DIST_INSTALL"
make install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"
make install-lib DIST_MANIFEST="$DIST_INSTALL_LIB"

chmod +x ${RPM_BUILD_ROOT}/%{_lib}/libattr.so.*

files()
{
	sort | uniq | awk ' 
$1 == "d" { 
	    if (match ($6, "/usr/include/attr"))
		printf ("%%%%dir %%%%attr(%s,%s,%s) %s\n", $2, $3, $4, $5); } 
$1 == "f" { if (match ($6, "/usr/share/man") || match ($6, "/usr/share/doc/attr"))
		printf ("%%%%doc ");
	    if (match ($6, "/usr/share/man"))
		printf ("%%%%attr(%s,%s,%s) %s*\n", $2, $3, $4, $6);
	    else
		printf ("%%%%attr(%s,%s,%s) %s\n", $2, $3, $4, $6); }
$1 == "l" { if (match ($3, "/usr/share/man") || match ($3, "/usr/share/doc/attr"))
		printf ("%%%%doc ");
	    if (match ($3, "/usr/share/man"))
		printf ("%attr(0777,root,root) %s*\n", $3);
	    else
		printf ("%attr(0777,root,root) %s\n", $3); }'
}
set +x
files < "$DIST_INSTALL" > files.rpm
files < "$DIST_INSTALL_DEV" > filesdevel.rpm
files < "$DIST_INSTALL_LIB" > fileslib.rpm
set -x

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libattr -p /sbin/ldconfig

%postun -n libattr -p /sbin/ldconfig

%files -f files.rpm

%files -n libattr-devel -f filesdevel.rpm

%files -n libattr -f fileslib.rpm

%changelog
* Tue Jan 28 2003 Michael K. Johnson <johnsonm@redhat.com> 2.2.0-1
- update/rebuild

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 2.0.8-6
- set execute bits on library so that requires are generated.

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 2.0.8-5
- Redo multilib patch to work everywhere

* Wed Sep 11 2002 Than Ngo <than@redhat.com> 2.0.8-4
- Added fix to install libs in correct directory on 64bit machine 

* Thu Aug 08 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.8-3
- Made the package only own the one directory that is unique to it:
  /usr/include/attr

* Wed Jun 26 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.8-2
- get perl out of base with attr-2.0.8-docperms.patch

* Mon Jun 24 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.8-1
- Initial Red Hat package
  Made as few changes as possible relative to upstream packaging to
  make it easier to maintain long-term.  This means that some of
  the techniques used here are definitely not standard Red Hat
  techniques.  If you are looking for an example package to fit
  into Red Hat Linux transparently, this would not be the one to
  pick.
- attr-devel -> libattr-devel
