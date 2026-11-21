# NOTICE — Blockys Mobile

Blockys Mobile is an unofficial fork of
[Amethyst-Android](https://github.com/AngelAuraMC/Amethyst-Android) (branch `v3_openjdk`),
published by AngelAuraMC under the GNU Lesser General Public License v3.0 (LGPL-3.0).

Amethyst-Android is itself a fork of
[PojavLauncher](https://github.com/PojavLauncherTeam/PojavLauncher) (LGPL-3.0), originally based
on Boardwalk by Zhuowei Zhang.

## Changes made by this fork (2026-11-20)

- Rebranding applied at build time by `blockys/brand.py`:
  - Visible name: `Blockys Mobile` (instead of `Amethyst`).
  - Launcher and default profile icons regenerated from the Blockys artwork.
  - `minebutton_color` accent changed to `#3F6B32` and adaptive icon background to
    `#F4EFE2`.
  - "About" screen (`about_en.txt`) with the corresponding attribution.
- Own package identifier: `com.blockys.movil` (no `.debug` suffix), so it does not conflict
  with PojavLauncher or Amethyst.
- Own build workflow (`.github/workflows/android.yml`) that downloads the public Java 8
  binpack, applies branding, builds and publishes the APK.
- README and this NOTICE rewritten.

The execution engine, runtime selection and native modules are unchanged.

## Source code and license

- This repository contains the full fork source, including the branding binary
  (`blockys/icon.png`) and the `blockys/brand.py` script.
- License: LGPL-3.0 (see `LICENSE`). The LGPL-3.0 terms apply to this derivative work the same
  as they do to the original project.
- Bundled Java Runtime: OpenJDK 8, built by AngelAuraMC for Android, under GPLv2 with
  Classpath Exception. The Java 17/21/25 JREs download from
  `AngelAuraMC/angelauramc-openjdk-build`.

## Non-affiliation

Blockys Mobile is not affiliated with AngelAuraMC, PojavLauncherTeam, Mojang Studios or
Microsoft, and is not endorsed or sponsored by them. "Minecraft" is a registered trademark of
Mojang Studios.
