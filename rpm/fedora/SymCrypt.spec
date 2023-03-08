Summary:        Cryptographic library 
Name:           SymCrypt
License:        MIT and BSD-2-Clause-Views

Version:        103.1.0
Release:        1%{?dist}

URL:            https://github.com/microsoft/SymCrypt
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  jitterentropy-devel
BuildRequires:  libasan
BuildRequires:  libatomic
BuildRequires:  libubsan
BuildRequires:  python3
BuildRequires:  python3-pyelftools
# Fedora specific patch to create shared library, use 
# packaged jitterentropy and use Fedora build flags
Patch0:  shared-library-and-distro-jitterentropy.patch

Group:   Development/Libraries
ExclusiveArch: x86_64 AArch64

%description
SymCrypt is the core cryptographic function library
currently used by Windows.

%package devel
Summary: Development headers for SymCrypt
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers for the core cryptographic
Windows library

%prep
%autosetup -p1 -n %{name}-%{version}
%build
mkdir bin
cd bin
cmake .. \
       -DSYMCRYPT_USE_ASM=OFF \
       -DCMAKE_BUILD_TYPE=Debug \
       -DSYMCRYPT_FIPS_BUILD=OFF
make

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}

install -m 755 bin/module/generic/libsymcrypt.so* %{buildroot}%{_libdir}
install -m 644 bin/inc/*.h %{buildroot}%{_includedir}
install -m 644 bin/symcrypt.pc %{buildroot}%{_libdir}/pkgconfig/

%check
./bin/exe/symcryptunittest


%files
%license LICENSE
%license NOTICE
%doc README.md
%doc SECURITY.md
%{_libdir}/libsymcrypt.so.103*

%files devel
%{_libdir}/libsymcrypt.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/symcrypt.pc

%changelog
* Sat Jan 21 2023 Benson Muite <benson_muite@emailplus.org> - 103.1.0-1
- Initial packaging
