Name:           acs-hyprland
Version:        0.57.2
Release:        1%{?dist}
Summary:        Hyprland Wayland compositor with the AscendantOS patch series
License:        BSD-3-Clause AND BSD-2-Clause AND MIT
URL:            https://github.com/design-nexus/asc-hyprland
Source0:        https://github.com/hyprwm/Hyprland/releases/download/v%{version}/source-v%{version}.tar.gz
Source1:        https://codeload.github.com/stephenberry/glaze/tar.gz/refs/tags/v7.2.0#/glaze-7.2.0.tar.gz
Patch0001:      0001-gestures-add-workspace_swipe_wrap.patch
Patch0002:      0002-output-add-virtual-region-partitioning.patch
Patch0003:      0003-output-add-virtual-monitors.patch
Patch0004:      0004-render-composite-virtual-regions-on-their-host.patch
Patch0005:      0005-workspaces-per-region-workspace-selector-and-pointer.patch
Patch0006:      0006-virtual-monitors-add-merge-restore-physical-fullscre.patch
Patch0007:      0007-ipc-expose-virtual-monitors.patch
Patch0008:      0008-hyprtester-add-virtual-monitor-tests.patch
Patch0009:      0009-virtual-monitors-workspaces-0-leaves-numbering-to-th.patch
Patch0010:      0010-virtual-monitors-fixes-from-the-first-run-on-a-NyxOS.patch
Patch0011:      0011-hyprtester-workspace_swipe_wrap-checks-the-0.57-acti.patch
Patch0012:      0012-fullscreen-misc-fullscreen_own_workspace.patch
Patch0013:      0013-layers-top-layers-slide-with-the-workspace-when-it-m.patch
Patch0014:      0014-layers-work-the-slide-offset-out-once-per-monitor-pe.patch

BuildRequires:  cmake >= 3.30
BuildRequires:  gcc-c++
BuildRequires:  glslang-devel
BuildRequires:  hyprwayland-scanner-devel
BuildRequires:  ninja-build
BuildRequires:  patch
BuildRequires:  pkgconfig(aquamarine) >= 0.15.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprcursor) >= 0.1.7
BuildRequires:  pkgconfig(hyprgraphics) >= 0.5.1
BuildRequires:  pkgconfig(hyprland-protocols) >= 0.8.0
BuildRequires:  pkgconfig(hyprlang) >= 0.6.7
BuildRequires:  pkgconfig(hyprutils) >= 0.14.3
BuildRequires:  pkgconfig(hyprwire)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libeis-1.0)
BuildRequires:  pkgconfig(libinput) >= 1.29
BuildRequires:  pkgconfig(lua) >= 5.5
BuildRequires:  pkgconfig(muparser)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.49
BuildRequires:  pkgconfig(wayland-server) >= 1.22.91
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon) >= 1.11.0
BuildRequires:  python3-devel
BuildRequires:  systemd-rpm-macros

Provides:       hyprland = %{version}-%{release}
Provides:       bundled(glaze) = 7.2.0
Provides:       bundled(udis86)
Conflicts:      hyprland
Recommends:     xorg-x11-server-Xwayland

%description
Hyprland with AscendantOS workspace wrapping, experimental virtual monitors,
fullscreen workspaces, and workspace layer transitions.

%package devel
Summary:        Headers for the AscendantOS edition of Hyprland
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       hyprland-devel = %{version}-%{release}
Conflicts:      hyprland-devel

%description devel
Headers and pkg-config metadata for building plugins against acs-hyprland.

%prep
%setup -q -n hyprland-source
%global _default_patch_fuzz 0
%autopatch -p1
tar -xf %{SOURCE1} -C subprojects
cp subprojects/glaze-7.2.0/LICENSE LICENSE.glaze
cp subprojects/udis86/LICENSE LICENSE.udis86

%build
export GIT_COMMIT_HASH=11cbc6c577b84ffb1edf4df3fc5b6128c3ae6947
export GIT_TAG=v%{version}
%cmake -G Ninja \
    -DBUILD_TESTING=OFF \
    -DNO_UWSM=ON \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DFETCHCONTENT_SOURCE_DIR_GLAZE="$PWD/subprojects/glaze-7.2.0" \
    -DCMAKE_DISABLE_FIND_PACKAGE_glaze=ON
%cmake_build

%install
%cmake_install
install -d %{buildroot}%{_userunitdir}
mv %{buildroot}%{_libdir}/systemd/user/hyprland-session.target %{buildroot}%{_userunitdir}/
install -d %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{_datadir}/pkgconfig/hyprland.pc %{buildroot}%{_libdir}/pkgconfig/

%files
%license LICENSE LICENSE.glaze LICENSE.udis86
%{_bindir}/Hyprland
%{_bindir}/hyprland
%{_bindir}/start-hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_datadir}/hypr/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_datadir}/bash-completion/completions/hyprpm
%{_datadir}/fish/vendor_completions.d/hyprpm.fish
%{_datadir}/zsh/site-functions/_hyprpm
%{_mandir}/man1/*.1*
%{_userunitdir}/hyprland-session.target

%files devel
%{_includedir}/hyprland/
%{_libdir}/pkgconfig/hyprland.pc

%changelog
* Tue Nov 24 2026 AscendantOS contributors - 0.57.2-1
- Package the complete AscendantOS patch series against Hyprland 0.57.2.
