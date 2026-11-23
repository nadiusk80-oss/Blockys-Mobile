#!/usr/bin/env python3
"""Rebrand an Amethyst-Android checkout as Blockys Mobile (run from repo root copy)."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app_pojavlauncher"
NAME = "Blockys Mobile"
PKG = "com.blockys.movil"
ACCENT = "#3F6B32"
BG = "#F4EFE2"


def patch(rel, pairs):
    path = APP / rel
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in text:
            raise SystemExit(f"brand: pattern not found in {path}: {old!r}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


patch("build.gradle", [
    ('applicationId "org.angelauramc.amethyst"', f'applicationId "{PKG}"'),
    ("versionCode 10000000", "versionCode 20000006"),
    ("versionName getVersionName()", 'versionName "2.0.6"'),
    ("            applicationIdSuffix '.debug'\n", ""),
    ('resValue "string", "app_name", "Amethyst (Debug)"',
     f'resValue "string", "app_name", "{NAME}"'),
    ('resValue "string", "app_short_name", "Amethyst (Debug)"',
     f'resValue "string", "app_short_name", "{NAME}"'),
    ("resValue 'string', 'application_package', 'org.angelauramc.amethyst.debug'",
     f"resValue 'string', 'application_package', '{PKG}'"),
    ("resValue 'string', 'storageProviderAuthorities', 'org.angelauramc.amethyst.scoped.gamefolder.debug'",
     f"resValue 'string', 'storageProviderAuthorities', '{PKG}.scoped.gamefolder'"),
    ("resValue 'string', 'shareProviderAuthority', 'org.angelauramc.amethyst.scoped.controlfolder.debug'",
     f"resValue 'string', 'shareProviderAuthority', '{PKG}.scoped.controlfolder'"),
    ('resValue "string", "app_name", "Amethyst"',
     f'resValue "string", "app_name", "{NAME}"'),
    ('resValue "string", "app_short_name", "Amethyst"',
     f'resValue "string", "app_short_name", "{NAME}"'),
    ("resValue 'string', 'storageProviderAuthorities', 'org.angelauramc.amethyst.scoped.gamefolder'",
     f"resValue 'string', 'storageProviderAuthorities', '{PKG}.scoped.gamefolder'"),
    ("resValue 'string', 'application_package', 'org.angelauramc.amethyst'",
     f"resValue 'string', 'application_package', '{PKG}'"),
])

patch("src/main/res/values/strings.xml", [
    ('<string name="app_name" translatable="false">Amethyst</string>',
     f'<string name="app_name" translatable="false">{NAME}</string>'),
    ('<string name="app_short_name" translatable="false">Amethyst</string>',
     f'<string name="app_short_name" translatable="false">{NAME}</string>'),
    ('<string name="error_fatal">Amethyst has unexpectedly crashed</string>',
     f'<string name="error_fatal">{NAME} has unexpectedly crashed</string>'),
    ('<string name="lazy_service_default_title">Amethyst Foreground Service</string>',
     f'<string name="lazy_service_default_title">{NAME} Foreground Service</string>'),
])

patch("src/main/res/values/colors.xml", [
    ('<color name="minebutton_color">#9649b8</color>',
     f'<color name="minebutton_color">{ACCENT}</color>'),
])

patch("src/main/java/net/kdt/pojavlaunch/fragments/SelectAuthFragment.java", [
    (
        "mLocalButton.setOnClickListener(v -> hasNoOnlineProfileDialog(requireActivity(), "
        "() -> Tools.swapFragment(requireActivity(), LocalLoginFragment.class, "
        "LocalLoginFragment.TAG, null)));",
        "mLocalButton.setOnClickListener(v -> Tools.swapFragment(requireActivity(), "
        "LocalLoginFragment.class, LocalLoginFragment.TAG, null));",
    ),
])

patch("src/main/java/net/kdt/pojavlaunch/fragments/ProfileTypeSelectFragment.java", [
    (
        "private void tryInstall(Class<? extends Fragment> fragmentClass, String tag){\n"
        "        if(!hasOnlineProfile()){\n"
        "            hasNoOnlineProfileDialog(requireActivity());\n"
        "        } else {\n"
        "            Tools.swapFragment(requireActivity(), fragmentClass, tag, null);\n"
        "        }\n"
        "    }",
        "private void tryInstall(Class<? extends Fragment> fragmentClass, String tag){\n"
        "        Tools.swapFragment(requireActivity(), fragmentClass, tag, null);\n"
        "    }",
    ),
])

patch("src/main/java/net/kdt/pojavlaunch/fragments/LocalLoginFragment.java", [
    (
        "        // This is overkill but meh\n"
        "        if (!hasOnlineProfile()){\n"
        "            Tools.swapFragment(requireActivity(), MainMenuFragment.class, "
        "MainMenuFragment.TAG, null);\n"
        "        }\n",
        "",
    ),
])

patch("src/main/java/net/kdt/pojavlaunch/fragments/MainMenuFragment.java", [
    (
        "        if (hasOnlineProfile()) {\n"
        "            mInstallJarButton.setOnClickListener(v -> "
        "runInstallerWithConfirmation(false));\n"
        "            mInstallJarButton.setOnLongClickListener(v -> {\n"
        "                runInstallerWithConfirmation(true);\n"
        "                return true;\n"
        "            });\n"
        "        } else mInstallJarButton.setOnClickListener(v -> "
        "hasNoOnlineProfileDialog(requireActivity()));",
        "        mInstallJarButton.setOnClickListener(v -> "
        "runInstallerWithConfirmation(false));\n"
        "        mInstallJarButton.setOnLongClickListener(v -> {\n"
        "            runInstallerWithConfirmation(true);\n"
        "            return true;\n"
        "        });",
    ),
    (
        "            } else if (!hasOnlineProfile()) { "
        "// Otherwise display the generic pop-up to log in\n"
        "                hasNoOnlineProfileDialog(requireActivity());\n"
        "            } else openPath(v.getContext(), "
        "getCurrentProfileDirectory(), false);",
        "            } else openPath(v.getContext(), "
        "getCurrentProfileDirectory(), false);",
    ),
])

patch("src/main/java/net/kdt/pojavlaunch/tasks/MinecraftDownloader.java", [
    (
        "                if(isLocalProfile || !isOnline) {",
        "                if(!isOnline) {",
    ),
])

patch("src/main/java/net/kdt/pojavlaunch/MainActivity.java", [
    (
        "            JMinecraftVersionList.Version mVersionInfo = Tools.getVersionInfo(version);\n",
        "            JMinecraftVersionList.Version mVersionInfo = Tools.getVersionInfo(version);\n"
        "            // Minecraft 26.3+ needs the Vulkan-backed renderer; the OpenGL\n"
        "            // fallback aborts on Android because SDL allows a single window.\n"
        "            if (mVersionInfo.javaVersion != null\n"
        "                    && mVersionInfo.javaVersion.majorVersion >= 25\n"
        "                    && (Tools.LOCAL_RENDERER == null\n"
        "                        || !Tools.LOCAL_RENDERER.toLowerCase().contains(\"zink\"))) {\n"
        "                Log.i(\"RdrDebug\", \"Java 25+ version: switching renderer to Kopper Zink\");\n"
        "                Tools.LOCAL_RENDERER = \"opengles3_desktopgl_zink_kopper\";\n"
        "            }\n",
    ),
])

patch("src/main/java/net/kdt/pojavlaunch/MinecraftGLSurface.java", [
    (
        'MCOptionUtils.set("fullscreen", "off");',
        'MCOptionUtils.set("fullscreen", "false");',
    ),
])

patch("src/main/java/net/kdt/pojavlaunch/fragments/ModpackCreateFragment.java", [
    (
        "private void tryInstall(Class<? extends Fragment> fragmentClass, String tag){\n"
        "        if(!hasOnlineProfile()){\n"
        "            hasNoOnlineProfileDialog(requireActivity());\n"
        "        } else {\n"
        "            Tools.swapFragment(requireActivity(), fragmentClass, tag, null);\n"
        "        }\n"
        "    }",
        "private void tryInstall(Class<? extends Fragment> fragmentClass, String tag){\n"
        "        Tools.swapFragment(requireActivity(), fragmentClass, tag, null);\n"
        "    }",
    ),
])

src = Image.open(ROOT / "blockys" / "icon.png").convert("RGBA")
res = APP / "src/main/res"

for qual, d in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
    out = res / f"mipmap-{qual}"
    out.mkdir(parents=True, exist_ok=True)
    icon = src.resize((d, d), Image.LANCZOS)
    icon.convert("RGB").save(out / "ic_launcher.webp", "WEBP", quality=95, method=6)

    mask = Image.new("L", (d * 4, d * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, d * 4 - 1, d * 4 - 1), fill=255)
    rnd = icon.copy()
    rnd.putalpha(mask.resize((d, d), Image.LANCZOS))
    rnd.save(out / "ic_launcher_round.webp", "WEBP", quality=95, method=6)

    fg = int(d * 2.25)
    art_size = int(fg * 0.62)
    fgimg = Image.new("RGBA", (fg, fg), (0, 0, 0, 0))
    art = src.resize((art_size, art_size), Image.LANCZOS)
    offset = (fg - art_size) // 2
    fgimg.paste(art, (offset, offset), art)
    fgimg.save(out / "ic_launcher_foreground.webp", "WEBP", quality=95, method=6)
    Image.new("RGB", (fg, fg), BG).save(out / "ic_launcher_background.webp", "WEBP", quality=95, method=6)

mono = Image.new("RGBA", (432, 432), (0, 0, 0, 0))
ImageDraw.Draw(mono).rounded_rectangle((36, 36, 395, 395), radius=92, fill=(255, 255, 255, 255))
mono.save(res / "drawable" / "ic_launcher_monochrome.webp", "WEBP", quality=95, method=6)

src.resize((512, 512), Image.LANCZOS).save(res / "drawable" / "ic_pojav_full.webp", "WEBP", quality=95, method=6)

about = (APP / "src/main/assets/about_en.txt").read_text(encoding="utf-8")
head, _, rest = about.partition("* Credits / Third party components")
about = (
    "%s (Minecraft: Java Edition launcher for Android), version %s \u2014 "
    f"{NAME}, a branded fork of Amethyst-Android (LGPL-3.0) by AngelAuraMC, itself based on "
    "PojavLauncher and Boardwalk.<br>\n\n"
    "* License:<br>\n"
    " \u2022 This application is licensed under "
    '<a href="https://github.com/nadiusk80-oss/Blockys-Movil/blob/v3_openjdk/LICENSE">'
    "GNU Lesser General Public License v3.0</a>.<br>\n \n"
    "* Credits / Third party components" + rest
)
(APP / "src/main/assets/about_en.txt").write_text(about, encoding="utf-8")

print("brand: done")
