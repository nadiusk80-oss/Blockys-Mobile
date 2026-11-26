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
    ("versionCode 10000000", "versionCode 20000008"),
    ("versionName getVersionName()", 'versionName "2.0.8"'),
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
        "            // Minecraft 26.3+ prefers the Vulkan-backed renderer, so a profile\n"
        "            // without one gets Kopper Zink. If Zink cannot start on this device,\n"
        "            // RendererFallback moves the profile to MobileGlues (see JREUtils).\n"
        "            if (mVersionInfo.javaVersion != null\n"
        "                    && mVersionInfo.javaVersion.majorVersion >= 25\n"
        "                    && Tools.LOCAL_RENDERER == null) {\n"
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

patch("src/main/java/net/kdt/pojavlaunch/utils/JREUtils.java", [
    (
        "        final int exitCode = VMLauncher.launchJVM(userArgs.toArray(new String[0]));\n"
        "        Logger.appendToLog(\"Java Exit code: \" + exitCode);\n"
        "        if (exitCode != 0) {\n"
        "            LifecycleAwareAlertDialog.DialogCreator dialogCreator = (dialog, builder)->\n"
        "                    builder.setMessage(activity.getString(R.string.mcn_exit_title, exitCode))\n",
        "        final int exitCode = VMLauncher.launchJVM(userArgs.toArray(new String[0]));\n"
        "        Logger.appendToLog(\"Java Exit code: \" + exitCode);\n"
        "        // If Zink cannot start here, move the profile to MobileGlues so the next\n"
        "        // Play does not repeat the same crash.\n"
        "        final boolean rendererSwitched = exitCode != 0\n"
        "                && RendererFallback.switchToMobileGlues();\n"
        "        if (exitCode != 0) {\n"
        "            LifecycleAwareAlertDialog.DialogCreator dialogCreator = (dialog, builder)->\n"
        "                    builder.setMessage(activity.getString(rendererSwitched\n"
        "                                    ? R.string.mcn_exit_renderer_switch\n"
        "                                    : R.string.mcn_exit_title, exitCode))\n",
    ),
])

patch("src/main/res/values/strings.xml", [
    (
        '<string name="mcn_exit_title">Application/Game exited with code %d, check '
        'latestlog.txt for more details.</string>\n',
        '<string name="mcn_exit_title">Application/Game exited with code %d, check '
        'latestlog.txt for more details.</string>\n'
        '    <string name="mcn_exit_renderer_switch">The game exited with code %d. Zink '
        'could not start on this device, so this profile now uses the MobileGlues '
        'renderer. Press Play to try again.</string>\n',
    ),
])

patch("src/main/res/values-es/strings.xml", [
    (
        '<string name="mcn_exit_title">La aplicación/juego ha finalizado con el código %d, '
        'mira el archivo latestlog.txt para más detalles.</string>\n',
        '<string name="mcn_exit_title">La aplicación/juego ha finalizado con el código %d, '
        'mira el archivo latestlog.txt para más detalles.</string>\n'
        '    <string name="mcn_exit_renderer_switch">El juego terminó con el código %d. '
        'Zink no pudo iniciarse en este dispositivo, así que este perfil usa ahora el '
        'renderer MobileGlues. Pulsa Jugar para intentarlo de nuevo.</string>\n',
    ),
])

(APP / "src/main/java/net/kdt/pojavlaunch/utils/RendererFallback.java").write_text("""package net.kdt.pojavlaunch.utils;

import android.util.Log;

import net.kdt.pojavlaunch.Logger;
import net.kdt.pojavlaunch.Tools;
import net.kdt.pojavlaunch.value.launcherprofiles.LauncherProfiles;
import net.kdt.pojavlaunch.value.launcherprofiles.MinecraftProfile;

import java.io.File;
import java.io.RandomAccessFile;

/**
 * Moves the current profile from Zink to MobileGlues after Zink failed to start.
 */
public final class RendererFallback {
    private static final String MOBILEGLUES = "opengles_mobileglues";
    private static final String LOG_FILE = "latestlog.txt";
    private static final String EGL_FAILURE = "Could not initialize EGL";
    private static final int TAIL_BYTES = 256 * 1024;

    private RendererFallback() {}

    /** @return whether the profile was switched to MobileGlues */
    public static boolean switchToMobileGlues() {
        String renderer = Tools.LOCAL_RENDERER;
        if (renderer == null || !renderer.toLowerCase().contains("zink")) return false;
        if (!logShowsEglFailure()) return false;
        try {
            MinecraftProfile profile = LauncherProfiles.getCurrentProfile();
            profile.pojavRendererName = MOBILEGLUES;
            LauncherProfiles.write();
            Tools.LOCAL_RENDERER = MOBILEGLUES;
            Logger.appendToLog("Renderer fallback: Zink could not initialize EGL, "
                    + "this profile now uses MobileGlues");
            return true;
        } catch (Throwable throwable) {
            Log.w("RendererFallback", "Could not switch the renderer", throwable);
            return false;
        }
    }

    private static boolean logShowsEglFailure() {
        File logFile = new File(Tools.DIR_GAME_HOME, LOG_FILE);
        if (!logFile.isFile()) return false;
        try (RandomAccessFile file = new RandomAccessFile(logFile, "r")) {
            long length = file.length();
            int tailLength = (int) Math.min(length, TAIL_BYTES);
            byte[] tail = new byte[tailLength];
            file.seek(length - tailLength);
            file.readFully(tail);
            return new String(tail, "UTF-8").contains(EGL_FAILURE);
        } catch (Throwable throwable) {
            Log.w("RendererFallback", "Could not read the log tail", throwable);
            return false;
        }
    }
}
""", encoding="utf-8")

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
