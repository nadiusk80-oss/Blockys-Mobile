# Blockys Mobile

Minecraft: Java Edition launcher for Android, with the Blockys visual identity.

Blockys Mobile is an unofficial fork of [Amethyst-Android](https://github.com/AngelAuraMC/Amethyst-Android)
(LGPL-3.0), which is itself a fork of
[PojavLauncher](https://github.com/PojavLauncherTeam/PojavLauncher) and Boardwalk.

## Download

APK: the **Releases** section of this repository (`Blockys-Mobile-<version>.apk`).

The APK is signed with the project debug key, so you need to allow installation from unknown
sources. The package is `com.blockys.movil`, different from PojavLauncher and Amethyst, so it can
run alongside them.

## Java

- **Java 8** is bundled inside the APK.
- **Java 17, 21 and 25** install from *Settings > Java* (runtime manager), or download
  automatically when launching a Minecraft version that requires them.
- Minecraft **26.3** and **26.4-snapshot** require Java 25; the launcher reads the version
  required by the game JSON and downloads the matching JRE from
  [angelauramc-openjdk-build](https://github.com/AngelAuraMC/angelauramc-openjdk-build).

## What changes compared to Amethyst

Only branding and packaging; the game engine is Amethyst's:

- Blockys name and icons, accent color `#3F6B32` and icon background `#F4EFE2`.
- Own `applicationId`: `com.blockys.movil`.
- Own build workflow (`.github/workflows/android.yml` + `blockys/brand.py`).
- README/NOTICE and the "About" screen carry the corresponding attribution.

There are no changes to launcher code or runtime selection beyond branding.

## Building

The `Blockys Mobile CI` workflow builds on GitHub Actions:

1. Downloads the Java 8 binpack (public artifact from `angelauramc-openjdk-build`).
2. Applies `blockys/brand.py` (Gradle, strings, colors, icons).
3. Runs `gradle :app_pojavlauncher:assembleDebug`.
4. Verifies the APK and publishes the release.

Locally, with JDK 21, NDK 27.3.13750724 and cloned submodules:

```
git clone --recursive -b v3_openjdk https://github.com/nadiusk80-oss/Blockys-Movil
python3 blockys/brand.py
gradle :app_pojavlauncher:assembleDebug
```

## License and attribution

Blockys Mobile is distributed under the **GNU Lesser General Public License v3.0**, the same as
Amethyst-Android and PojavLauncher. The modified source code is in this repository.

This project is **not affiliated** with AngelAuraMC, PojavLauncherTeam, Mojang Studios or
Microsoft, and is not endorsed or sponsored by them. Minecraft is a trademark of Mojang Studios.

## Desktop project

The Blockys launcher for Windows is at
[Blockys-Launcher](https://github.com/nadiusk80-oss/Blockys-Launcher).
