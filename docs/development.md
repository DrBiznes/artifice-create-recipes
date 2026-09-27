# Development

Requires a **JDK 21**. Open this directory as a Gradle project in IntelliJ IDEA or another Java IDE.

```powershell
.\gradlew.bat build
.\gradlew.bat runClient
.\gradlew.bat runServer
.\gradlew.bat runGameTestServer
```

On Linux/macOS use `bash ./gradlew`. `build` produces `build/libs/artifice_create_recipes-<version>.jar`. `runGameTestServer` loads a development-only test mod in `run-gametest`. It checks the live recipe manager, tag resolution, removal of the original crafting recipes, all 23 Create assembly progressions, starter selection, material budgets, workpiece registration, and advancement suppression. These tests are not packaged in the release jar.

## Regenerating resources

```powershell
python tools/generate_recipes.py    # recipes, models, lang, WorkpieceNames.java
python tools/generate_textures.py   # 16x16 workpiece sprites + docs/workpiece-textures.png
python tools/generate_branding.py   # docs/banner.png, docs/icon.png, packaged mod logo
python tools/verify_resources.py
```

Texture and branding generation require Pillow 10.1+. The rest uses only the standard library. All output is deterministic and checked in. Edit the generators rather than the generated JSON or PNGs. The branding script downloads the Rye font (OFL) into the ignored `.research/` directory.

## Pinned versions

| Component | Version |
| --- | --- |
| Minecraft | 1.21.1 |
| NeoForge | 21.1.248 (supports 21.1.248 and later) |
| Create | 6.0.10-281 (supports 6.0.10 and later 6.0.x) |
| Iron's Arms 'n Artifice | 1.21.1-1.0.1.1 |
| GeckoLib | 4.9.3 |
| Iron's Library | 1.21.1-2.2.0 |
| ModDevGradle | 2.0.147 |
| Gradle wrapper | 9.2.1 |

Runtime dependencies come from their upstream Maven repositories with `transitive = false`. This avoids Artifice's development-only integrations. No upstream jars are redistributed.

## Windows loopback error

If Gradle reports `Unable to establish loopback connection` from `UnixDomainSockets.connect`, the temp path may be too long:

```powershell
New-Item -ItemType Directory -Force .gradle/tmp | Out-Null
$tempForGradle = (Resolve-Path .gradle/tmp).Path.Replace('\', '/')
$env:JAVA_TOOL_OPTIONS = "-Djava.io.tmpdir=$tempForGradle -Djdk.net.unixdomain.tmpdir=$tempForGradle"
```

## Layout

- `src/main/java`: registration, the inert workpiece item, and the generated item-name manifest.
- `src/main/resources`: generated recipes, advancement overrides, models, translations, textures, and the logo.
- `src/main/templates/META-INF/neoforge.mods.toml`: mod metadata, expanded from `gradle.properties`.
- `src/gametest`: development-only server tests.
- `tools`: deterministic generators and the resource verifier.
- `docs`: recipe specification, research, and artwork.

This project is based on the [NeoForge 1.21.1 ModDevGradle MDK](https://github.com/NeoForgeMDKs/MDK-1.21.1-ModDevGradle). `TEMPLATE_LICENSE.txt` is retained from it.
