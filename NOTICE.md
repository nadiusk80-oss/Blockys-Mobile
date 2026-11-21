# NOTICE — Blockys Móvil

Blockys Móvil es un fork no oficial de
[Amethyst-Android](https://github.com/AngelAuraMC/Amethyst-Android) (rama `v3_openjdk`),
publicado por AngelAuraMC bajo la GNU Lesser General Public License v3.0 (LGPL-3.0).

Amethyst-Android es, a su vez, un fork de
[PojavLauncher](https://github.com/PojavLauncherTeam/PojavLauncher) (LGPL-3.0), basado
originalmente en Boardwalk de Zhuowei Zhang.

## Modificaciones realizadas por este fork (2026-11-20)

- Rebranding aplicado en tiempo de compilación por `blockys/brand.py`:
  - Nombre visible: `Blockys Móvil` (en lugar de `Amethyst`).
  - Iconos de lanzador y de perfil por defecto regenerados a partir del arte de Blockys.
  - Color de acento `minebutton_color` cambiado a `#3F6B32` y fondo de icono adaptativo
    `#F4EFE2`.
  - Pantalla "Acerca de" (`about_en.txt`) con la atribución correspondiente.
- Identificador de paquete propio: `com.blockys.movil` (sin sufijo `.debug`), para no
  entrar en conflicto con PojavLauncher ni con Amethyst.
- Workflow de compilación propio (`.github/workflows/android.yml`) que descarga el binpack
  público de Java 8, aplica el branding, compila y publica la APK.
- README y este NOTICE reescritos.

No se han modificado el motor de ejecución, la selección de runtimes ni los módulos nativos.

## Código fuente y licencia

- Este repositorio contiene el código fuente completo del fork, incluido el binario de
  branding (`blockys/icon.png`) y el script `blockys/brand.py`.
- Licencia: LGPL-3.0 (ver `LICENSE`). Los términos de la LGPL-3.0 se aplican a este trabajo
  derivado igual que al proyecto original.
- Java Runtime incluido: OpenJDK 8, construido por AngelAuraMC para Android, bajo GPLv2 con
  Classpath Exception. Los JRE de Java 17/21/25 se descargan desde
  `AngelAuraMC/angelauramc-openjdk-build`.

## No afiliación

Blockys Móvil no está afiliado a AngelAuraMC, PojavLauncherTeam, Mojang Studios ni Microsoft,
y no está aprobado ni patrocinado por ellos. "Minecraft" es una marca registrada de Mojang
Studios.
