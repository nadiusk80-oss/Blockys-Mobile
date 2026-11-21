# Blockys Móvil

Launcher de Minecraft: Java Edition para Android, con la identidad visual de Blockys.

Blockys Móvil es un fork no oficial de [Amethyst-Android](https://github.com/AngelAuraMC/Amethyst-Android)
(LGPL-3.0), que a su vez es un fork de
[PojavLauncher](https://github.com/PojavLauncherTeam/PojavLauncher) y de Boardwalk.

## Descarga

APK: sección **Releases** de este repositorio (`Blockys-Movil-<versión>.apk`).

La APK está firmada con la clave de depuración del proyecto, así que hay que permitir la
instalación desde orígenes desconocidos. El paquete es `com.blockys.movil`, distinto del de
PojavLauncher y del de Amethyst, por lo que puede convivir con ellos.

## Java

- **Java 8** viene incluido dentro de la APK.
- **Java 17, 21 y 25** se instalan desde *Ajustes > Java* (gestor de runtimes), o se descargan
  automáticamente al iniciar una versión de Minecraft que las necesite.
- Minecraft **26.3** y **26.4-snapshot** requieren Java 25; el launcher detecta la versión
  requerida por el JSON del juego y descarga el JRE correspondiente desde
  [angelauramc-openjdk-build](https://github.com/AngelAuraMC/angelauramc-openjdk-build).

## Qué cambia respecto a Amethyst

Solo el branding y el empaquetado; el motor del juego es el de Amethyst:

- Nombre e iconos de Blockys, color de acento `#3F6B32` y fondo de icono `#F4EFE2`.
- `applicationId` propio: `com.blockys.movil`.
- Workflow de compilación propio (`.github/workflows/android.yml` + `blockys/brand.py`).
- README/NOTICE y pantalla "Acerca de" con la atribución correspondiente.

No hay cambios en el código del launcher ni en la selección de runtimes, más allá del branding.

## Compilar

El workflow `Blockys Móvil CI` compila en GitHub Actions:

1. Descarga el binpack de Java 8 (artefacto público de `angelauramc-openjdk-build`).
2. Aplica `blockys/brand.py` (Gradle, strings, colores, iconos).
3. Ejecuta `gradle :app_pojavlauncher:assembleDebug`.
4. Verifica la APK y publica el release.

Localmente, con JDK 21, NDK 27.3.13750724 y los submódulos clonados:

```
git clone --recursive -b v3_openjdk https://github.com/nadiusk80-oss/Blockys-Movil
python3 blockys/brand.py
gradle :app_pojavlauncher:assembleDebug
```

## Licencia y atribución

Blockys Móvil se distribuye bajo **GNU Lesser General Public License v3.0**, igual que
Amethyst-Android y PojavLauncher. El código fuente modificado está en este repositorio.

Este proyecto **no está afiliado** a AngelAuraMC, PojavLauncherTeam, Mojang Studios ni
Microsoft, y no está aprobado ni patrocinado por ellos. Minecraft es una marca de Mojang
Studios.

## Proyecto de escritorio

El launcher para Windows de Blockys está en
[Blockys-Launcher](https://github.com/nadiusk80-oss/Blockys-Launcher).
