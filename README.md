# AscendantOS Hyprland

AscendantOS packages Hyprland v0.57.2 as `acs-hyprland` for Fedora 45.
The 14 patches come from nyxos-project/nyx-hyprland at
`b603f3515f6685c6e7efebc16e250577b15e74ad`. They preserve workspace swipe
wrapping, experimental virtual monitors, fullscreen workspaces, and top-layer
transitions. Virtual monitors remain opt-in. The patch emails retain their
original authorship.

Run `./prepare-sources OUTPUT_DIRECTORY` to stage verified source archives and
the patch series. Use `rpmbuild -bs --define "_sourcedir OUTPUT_DIRECTORY"
acs-hyprland.spec` to generate the source RPM. Build that source RPM in a clean
Fedora 45 build environment with the AscendantOS-approved dependency source.

A Fedora installation should use the resulting `acs-hyprland` package as its
single Hyprland provider. The upstream command names and Wayland session entry
are preserved. The separate `acs-hyprland-devel` package contains plugin headers.
