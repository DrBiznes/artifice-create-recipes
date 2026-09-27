# Artifice Create Recipes

NeoForge **Minecraft 1.21.1** addon for Create manufacturing recipes for **Iron's Arms 'n Artifice**.

Replaces 44 Artifice crafting recipes with **23 sequenced assemblies, 11 basin compacting recipes, and 10 mixing recipes**. Both hat recipes remain unchanged. All guns, both ammunition routes, and all three mechanical component tiers now require assembly lines. Includes 23 inert incomplete items with original, code-generated 16 x 16 textures and a creative workpiece tab.

## Recipes and artwork

- [Implemented recipe specification](docs/final-recipe-proposal.md): complete replacement set, wood and material costs, assembly loops, and all 29 modifiers.
- [Workpiece texture contact sheet](docs/workpiece-textures.png): enlarged nearest-neighbor previews of the 23 original sprites.
- [Earlier alternatives and Create machine capabilities](docs/recipe-design.md): retained as research context; superseded by the final proposal.
- [Existing recipe inventory](docs/existing-recipes.md): all 46 recipes and their exact ingredient counts from the local Artifice checkout.

Iron ammunition consumes one sheet and **24 blackpowder** over six passes, producing 24 bullets. Copper consumes one sheet and six blackpowder over two passes, producing six. Wood is consumed by every gun, including a second log for long guns. Assembly products are guaranteed; unfinished products have no gun/modifier functionality. Processing recipes use the original Artifice IDs, so they replace the crafting routes. Their obsolete crafting-recipe unlock advancements are suppressed; hats and gameplay advancements remain intact.

Install the built jar alongside Create, Artifice, and their normal required dependencies on Minecraft 1.21.1 NeoForge. Because the addon registers new items, install it on both client and server. Existing finished equipment is not changed.

## Development

Requires a **JDK 21**. Open this directory as a Gradle project in IntelliJ IDEA or another Java IDE.

```powershell
.\gradlew.bat build
.\gradlew.bat runClient
.\gradlew.bat runData
.\gradlew.bat runServer
.\gradlew.bat runGameTestServer
```

On Linux/macOS use `bash ./gradlew` in place of `.\gradlew.bat`. The server's Minecraft EULA must be handled by the operator before running a normal server.

The build produces `build/libs/artifice_create_recipes-0.1.0-SNAPSHOT.jar`. Generated recipes/assets are checked in, so Java 21 and Gradle are sufficient to build. `runData` is an optional mod-loading check; this project generates its resources using the Python tools below instead of Java data providers.

`runGameTestServer` loads a separate development-only test mod in an isolated `run-gametest` directory. It verifies the actual server recipe manager, tag resolution, removal of all original crafting bypasses, all 23 native Create assembly progressions, unambiguous starter selection, key material budgets, workpiece registration, and old advancement suppression. The tests and their structure are not packaged in the release jar. `build` alone does not launch the game tests.

## Regenerating resources

```powershell
python tools/generate_recipes.py
python tools/generate_textures.py
python tools/verify_resources.py
```

Only texture generation requires Pillow (10.1 or later). Recipe generation and resource verification use Python's standard library. The texture generator draws original pixel geometry; it does not require or copy upstream texture files. Regeneration is deterministic. Edit the recipe generator and regenerate rather than manually editing its JSON, item-name manifest, models, or translations. Edit the texture generator for sprite changes.

The generators write resources to `src/main/resources` and the item-name manifest to `src/main/java`. The resource verifier compares replacement coverage to the audited original recipe inventory and checks unique starter signatures, models, translations, and distinct 16 x 16 RGBA textures. Review the contact sheet after changing sprite geometry.

The Gradle setup pins:

| Component | Version |
| --- | --- |
| Java | 21 |
| Minecraft | 1.21.1 |
| NeoForge | 21.1.228, matching the local Artifice project |
| ModDevGradle | 2.0.147 |
| Gradle wrapper | 9.2.1 |
| Create | 6.0.11-312 |
| Iron's Arms 'n Artifice | 1.21.1-1.0.1.1 |
| GeckoLib | 4.9.3 |
| Iron's Library | 1.21.1-2.2.0 |
| Registrate (bundled by Create) | MC1.21-1.3.0+67 |
| Ponder (bundled by Create) | 1.0.85+mc1.21.1 |
| Flywheel (bundled by Create) | 1.0.6 |

Verified implementation: `build runGameTestServer --no-daemon` completed successfully on JDK 21; **all four required server tests passed**, including native progression through all 23 assemblies. Resource verification passed for all 44 replacements and 23 sprites. The jar was inspected to confirm recipes/textures are packaged and development tests are excluded. The test server's first run logged a missing `server.properties` before generating its defaults; upstream development refmap/annotation warnings were non-fatal. No recipe decode errors occurred.

The assembly checks exercise Create's selection and advancement APIs against a live server registry; they do not simulate a complete moving belt factory. Graphical client rendering, JEI presentation, belt throughput, and survival balance still need playtesting.

Runtime dependencies resolve from their upstream Maven repositories. Artifice's published dependency metadata also lists its development integrations (Aeronautics and Sable); this addon selects its required runtime libraries explicitly instead. Bundled dependencies inside upstream jars still load through NeoForge. No upstream jars are redistributed inside the addon.

The local `../irons-artifice` repository was inspected as a read-only source of recipes. The dev runtime uses the published matching version, not the sibling checkout's Java sources. Changing that checkout will not change this addon's run configuration automatically.

If Gradle on Windows reports `Unable to establish loopback connection` with `UnixDomainSockets.connect` in the stack trace, a long temporary-directory path can be the cause. A project-local temporary path worked in the setup environment:

```powershell
New-Item -ItemType Directory -Force .gradle/tmp | Out-Null
$tempForGradle = (Resolve-Path .gradle/tmp).Path.Replace('\', '/')
$env:JAVA_TOOL_OPTIONS = "-Djava.io.tmpdir=$tempForGradle -Djdk.net.unixdomain.tmpdir=$tempForGradle"
.\gradlew.bat build runData --no-daemon
```

Use this in a dedicated terminal if `JAVA_TOOL_OPTIONS` already contains settings you need to retain. It changes only that terminal's environment.

## Layout and provenance

- `src/main/java`: NeoForge registration, inert workpiece item class, and generated item-name manifest.
- `src/main/resources`: generated recipes, advancement overrides, models, translations, and textures. Minecraft 1.21.1 uses singular `recipe` directories.
- `src/gametest`: development-only server tests and their empty structure.
- `tools`: deterministic generators and resource verification.
- `src/main/templates/META-INF/neoforge.mods.toml`: expanded mod metadata and required dependencies.
- `src/generated/resources`: reserved for generated resources.
- `docs`: design and source audit.
- `.research`: ignored local source downloads; never packaged.

Based on the [official NeoForge 1.21.1 ModDevGradle MDK](https://github.com/NeoForgeMDKs/MDK-1.21.1-ModDevGradle/tree/4e1be6e906e1b32a753e3580af4ea1bcc3dbc79e). The upstream wrapper, scripts, attributes, and `TEMPLATE_LICENSE.txt` are retained. Build and entry-point files are tailored to this addon. The addon retains the MDK's default All Rights Reserved setting until a project license is selected; upstream projects retain their own licenses.
