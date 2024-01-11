%if 0%{?fedora} >= 22 || 0%{?rhel} > 7
%define luaver 5.3
%else
%if 0%{?fedora} >= 20
%define luaver 5.2
%else
%define luaver 5.1
%endif
%endif

%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}

%define luacompatver 5.1
%define luacompatlibdir %{_libdir}/lua/%{luacompatver}
%define luacompatpkgdir %{_datadir}/lua/%{luacompatver}
%define lua51dir %{_builddir}/lua51-%{name}-%{version}-%{release}

Name:           lua-expat
Version:        1.3.0
Release:        12%{?dist}.1
Summary:        SAX XML parser based on the Expat library

Group:          Development/Libraries
License:        MIT
URL:            http://www.keplerproject.org/luaexpat/
Source0:        http://matthewwild.co.uk/projects/luaexpat/luaexpat-%{version}.tar.gz

BuildRequires:  lua >= %{luaver}, lua-devel >= %{luaver}
BuildRequires:  expat-devel
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
Requires:       lua(abi) = %{luaver}
%else
Requires:       lua >= %{luaver}
%endif

%description
LuaExpat is a SAX XML parser based on the Expat library.

%if 0%{?fedora} >= 20
%package compat
Summary:        SAX XML parser based on the Expat library for Lua 5.1
Group:          Development/Libraries
BuildRequires:  compat-lua >= %{luacompatver}, compat-lua-devel >= %{luacompatver}

%description compat
LuaExpat is a SAX XML parser based on the Expat library for Lua 5.1.
%endif

%prep
%setup -q -n luaexpat-%{version}

%if 0%{?fedora} >= 20
rm -rf %{lua51dir}
cp -a . %{lua51dir}
%endif

%build
make %{?_smp_mflags} LUA_V=%{luaver} LUA_CDIR=%{lualibdir} LUA_LDIR=%{luapkgdir} LUA_INC=-I%{_includedir} EXPAT_INC=-I%{_includedir} CFLAGS="%{optflags} -fPIC -std=c99" LDFLAGS="%{?__global_ldflags}"

%if 0%{?fedora} >= 20
pushd %{lua51dir}
make %{?_smp_mflags} LUA_V=%{luacompatver} LUA_CDIR=%{luacompatlibdir} LUA_LDIR=%{luacompatpkgdir} LUA_INC=-I%{_includedir}/lua-%{luacompatver} EXPAT_INC=-I%{_includedir} CFLAGS="%{optflags} -fPIC" LDFLAGS="%{?__global_ldflags}"
popd
%endif

%install
make install DESTDIR=%{buildroot} LUA_CDIR=%{lualibdir} LUA_LDIR=%{luapkgdir} INSTALL='install -p'

%if 0%{?fedora} >= 20
pushd %{lua51dir}
make install DESTDIR=%{buildroot} LUA_CDIR=%{luacompatlibdir} LUA_LDIR=%{luacompatpkgdir} INSTALL='install -p'
popd
%endif

%check
lua -e 'package.cpath="./src/?.so;"..package.cpath; dofile("tests/test.lua");'
lua -e 'package.cpath="./src/?.so;" .. package.cpath; package.path="./src/?.lua;" .. package.path; dofile("tests/test-lom.lua");'


%files
%doc README doc/us/*
%{lualibdir}/*
%{luapkgdir}/*

%if 0%{?fedora} >= 20
%files compat
%doc README doc/us/*
%{luacompatlibdir}/*
%{luacompatpkgdir}/*
%endif

%changelog
* Thu Jun 28 2018 Troy Dawson <tdawson@redhat.com> - 1.3.0-12.1
- Update lua conditionals (#1595834)

* Wed Apr 11 2018 Robert Scheck <robert@fedoraproject.org> - 1.3.0-12
- Build flags injection is only partially successful (#1565997)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Robert Scheck <robert@fedoraproject.org> - 1.3.0-5
- Rebuilt for lua 5.3 (#1225902)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Matěj Cepl <mcepl@redhat.com> - 1.3.0-2
- Apply patch by jkaluza (fix RHBZ# 1100238) to build -compat subpackage
  against compat-lua

* Wed Apr 23 2014 Robert Scheck <robert@fedoraproject.org> - 1.3.0-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Tom Callaway <spot@fedoraproject.org> - 1.2.0-5
- fix for lua 5.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 03 2011 Matěj Cepl <mcepl@redhat.com> - 1.2-1
- New upstream release, fixing "The Billion Laughs Attack" for XMPP servers.
- Fix tests so that we actually pass them.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 05 2008 Tim Niemueller <tim@niemueller.de> - 1.1-2
- Minor spec fixes for guideline compliance
- Added %%check macro to execute tests

* Wed Jun 04 2008 Tim Niemueller <tim@niemueller.de> - 1.1-1
- Initial package

