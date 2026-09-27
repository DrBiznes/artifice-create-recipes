# Final proposed recipe set — factory assembly

Status: implemented. Resource checks and four server GameTests passed, including all 23 native Create assembly progressions. Graphical client and survival factory playtesting remain outstanding. This is the accepted recipe specification and supersedes the earlier alternatives in `recipe-design.md`.

## Rules

- Replace all 44 existing crafting-table recipes for blackpowder, bullets, components, guns, and modifiers. Preserve the two hat recipes. The replacement set also has 44 recipes: 23 sequenced assemblies, 11 compacting recipes, and 10 mixing recipes.
- All three component tiers, both bullet routes, and all seven guns use sequenced assembly. Eleven mechanical/attachment modifiers also use sequences.
- Add only dedicated incomplete versions of products, with our own programmatically drawn 16 x 16 textures. No separate stocks, barrels, carbon dust, or other new crafting materials.
- All addon outputs are guaranteed; no failure/scrap pool. Every recipe yields one finished item unless a powder/bullet batch quantity is given.
- All sequences run once unless their loop count is explicitly given. `D(item x N)` means N individual deployer applications, each consuming one item; it is not a stack-sized ingredient in one standard deploying operation. P = pressing; C = cutting; F = filling.
- Costs below are total direct inputs including the starting item. Nested component costs are additional through the component recipes; do not add the same starting item twice.
- Prefer existing iron, copper, gold, and brass sheets. Use common sheet/ingot/log tags where appropriate. More iron and andesite alloy provide recurring demand for the user's automated materials; copper/redstone/brass costs remain deliberate rather than appearing at every station.
- Every gun explicitly consumes wood. Longer guns use two logs, compact guns one. All guns start with one log; their second log, when required, is deployed later.
- Every proposed incomplete item is a plain workpiece, never an operational gun or usable modifier. Never use a finished gun as a transitional item.

## Blackpowder: mixing only

All three are unheated mixer recipes. Replace each corresponding original recipe rather than retaining automatic shapeless conversion alongside it.

| Original recipe ID | Inputs | Output |
| --- | --- | --- |
| `blackpowder_from_charcoal` | 2 charcoal | 1 blackpowder |
| `blackpowder` | 1 charcoal + 1 redstone | 3 blackpowder |
| `blackpowder_from_gunpowder` | 1 charcoal + 1 redstone + 1 gunpowder | 8 blackpowder |

The charcoal-only route is intentionally inefficient but does not require redstone. With one blackpowder per bullet, it prevents recurring ammunition production from depending entirely on redstone supplies. Leave all existing Create milling/crushing recipes untouched. No new milling/crushing conversion is proposed.

## Bullets: one powder per bullet

| Original recipe ID | Start | Repeated sequence | Loops | Total direct cost | Output |
| --- | --- | --- | --- | --- | --- |
| `bullet_from_iron` | Iron sheet | D(blackpowder x 4), P | 6 | 1 iron sheet + 24 blackpowder | 24 bullets |
| `bullet_from_copper` | Copper sheet | D(blackpowder x 3), P | 2 | 1 copper sheet + 6 blackpowder | 6 bullets |

Iron takes 24 powder applications and 6 press operations (30 processing operations). Copper takes 6 applications and 2 presses (8 operations). Recirculation lets the same stations handle successive passes; 24 separate deployers are not required. Each sheet enters only once. This retains the 4:1 metal-efficiency distinction while charging the same powder per finished bullet.

This is a substantial intentional ammunition-cost increase, not merely an efficiency bonus. A 24-bullet iron batch can be supplied by 3 rich mixes (3 charcoal + 3 redstone + 3 gunpowder), 8 basic mixes, or 24 charcoal-only mixes.

Use distinct `incomplete_iron_bullet_batch` and `incomplete_copper_bullet_batch` items. A batch icon depicts a small cluster/tray, not a new reusable cartridge item.

## Components: all sequenced assembly

| Original recipe ID | Starting item | Sequence | Loops | Total direct ingredients |
| --- | --- | --- | --- | --- |
| `simple_mechanical_components` | 1 copper sheet | D(andesite alloy), D(cogwheel), D(iron sheet), D(blackpowder), P | 2 | Copper sheet x1; andesite alloy x2; cogwheel x2; iron sheet x2; blackpowder x2 |
| `mechanical_components` | 1 simple mechanical component | D(brass sheet), D(large cogwheel), D(iron sheet x2), D(andesite alloy), D(redstone), P | 2 | Simple component x1; brass sheet x2; large cogwheel x2; iron sheet x4; andesite alloy x2; redstone x2 |
| `clockwork_components` | 1 mechanical component | D(precision mechanism), D(mechanical component), D(brass sheet x4), D(golden sheet x2), P | 1 | Mechanical component x2; precision mechanism x1; brass sheet x4; golden sheet x2 |

All output one component. No extra copper sheets or starting components are consumed on each loop. Clockwork indirectly includes 4 redstone through its two mechanical components; do not add another redstone cost on top. Create's existing precision-mechanism recipe retains its own behavior; our downstream sequences introduce no additional failure chance.

## Guns: explicit wood and complete costs

Each gun starts with **one log**. Perform its unique opening deployment, then a cutting step to shape the wooden workpiece. Deploy the remaining listed ingredients in a fixed order and finish by pressing. Long guns receive their second log before cutting, so both logs are present for that step. One loop; one gun.

The opening ingredient is included in the totals below, not an extra cost. Choose different opening ingredients for the shared log starter, rather than adding separate kits or starting every line with a saw.

| Original recipe ID | Total wood | Opening deployment | Other total ingredients (including opener) |
| --- | --- | --- | --- |
| `flintlock` | 1 log | Flint | Iron sheets x4; andesite alloy x2; flint x1; blackpowder x1 |
| `musket` | 2 logs | Simple mechanical component | Simple component x1; iron sheets x6; andesite alloy x2; flint x1; blackpowder x1 |
| `blunderbuss` | 2 logs | Copper sheet | Simple components x2; iron sheets x8; copper sheet x1; andesite alloy x2 |
| `blackpowder_revolver` | 1 log | Mechanical component | Mechanical component x1; hopper x1; iron sheets x4; brass sheet x1; andesite alloy x2; blackpowder x1 |
| `six_shooter` | 1 log | Brass sheet | Mechanical component x1; hopper x1; iron sheets x4; brass sheets x2; andesite alloy x2 |
| `arquebus` | 2 logs | Clockwork component | Clockwork component x1; iron sheets x6; brass sheets x2; andesite alloy x2; blackpowder x1 |
| `clockwork_rifle` | 2 logs | Netherite ingot | Clockwork component x1; netherite ingot x1; hopper x1; repeater x1; iron sheets x4; brass sheets x2; andesite alloy x2 |

Use flint rather than flint and steel for the flintlock/musket assembly ingredient: native deployers damage damageable held tools instead of consuming the entire item. Flint behaves as a normal consumed part. The rifle's netherite is consumed once, never once per loop. The powder in a gun recipe is only a crafting cost; it does not imply the finished gun is preloaded.

Example musket order: log -> D(simple component) -> D(second log) -> C -> D(iron sheet x6) -> D(andesite alloy x2) -> D(flint) -> D(blackpowder) -> P -> musket.

All seven sequences use separate `incomplete_<gun_id>` items. Different opening deployer ingredients plus sequence progress distinguish the routes. Verify actual recipe selection with both loaded mods in game.

## Mechanical and attachment modifiers: 11 assemblies

All sequences below run once and output one modifier. All sequences have their own `incomplete_<modifier_id>` item. Start is consumed once; the deployed items are additional.

| Original recipe ID | Start | Additional ingredients and operations |
| --- | --- | --- |
| `hair_trigger_modifier` | Simple component | D(copper sheet), D(iron sheet x2), C, P |
| `buffer_spring_modifier` | Simple component | D(iron sheet x6), D(andesite alloy x2), C, P |
| `gas_vent_modifier` | Simple component | D(hopper), D(second simple component), D(iron sheet x2), P |
| `mechanical_accelerator_modifier` | Mechanical component | D(chain x2), D(copper sheet x2), D(shaft x2), P |
| `mechanical_repeater_modifier` | Clockwork component | D(chain x2), D(brass sheet x2), D(golden sheet x2), P |
| `scope_attachment_modifier` | Simple component | D(spyglass), D(iron sheet), P |
| `bayonet_attachment_modifier` | Iron sword | D(simple component), D(andesite alloy), P |
| `suppressor_attachment_modifier` | Clockwork component | D(leather x2), D(golden sheet), D(iron sheet x2), P |
| `gun_oil_modifier` | Simple component | D(redstone), F(250 mB honey) |
| `chain_shot_modifier` | Bullet | D(chain x5), D(second bullet), D(andesite alloy), P |
| `hook_shot_modifier` | Bullet | D(iron sheet x4), D(chain x2), D(andesite alloy x2), P |

The bayonet starts on an iron sword so the sword is actually consumed as the workpiece, not merely damaged in a deployer's hand. Gun oil uses existing honey fluid; no new oil fluid is required. Mechanical accelerator is deliberately raised from the original simple tier to mechanical. All other component requirements are visible in the table.

Assembly start signatures are distinct across this whole proposal. For example, simple components plus brass begin mechanical components, plus copper begin hair triggers, plus iron begin springs, plus hopper begin vents, plus spyglass begin scopes, and plus redstone begin gun oil. Mechanical components plus precision mechanism begin clockwork; plus chain begin accelerators. Do not reorder these opening operations arbitrarily during implementation.

## Packed and metal modifiers: 11 compacting recipes

All are unheated basin compacting and output one modifier. These recipes produce the finished item directly and do not need incomplete variants.

| Original recipe ID | Total ingredients |
| --- | --- |
| `blackpowder_charge_modifier` | 8 blackpowder + 2 string |
| `scattershot_modifier` | 4 bullets + 4 blackpowder + 2 string |
| `breaching_shell_modifier` | 2 copper sheets + 2 iron sheets + 4 blackpowder + 3 flint |
| `incendiary_tip_modifier` | 3 iron sheets + 4 blackpowder + 3 blaze powder |
| `frozen_jacket_modifier` | 3 iron sheets + 4 blackpowder + 3 blue ice |
| `voltaic_core_modifier` | 2 copper sheets + 1 brass sheet + 4 blackpowder + 3 lightning rods |
| `steel_core_modifier` | 1 iron block + 3 iron sheets + 4 blackpowder |
| `lead_core_modifier` | 1 deepslate bricks + 3 iron sheets + 2 andesite alloy + 4 blackpowder |
| `trick_bullet_modifier` | 1 gold block + 2 golden sheets + 1 brass sheet + 4 blackpowder |
| `spiral_tip_modifier` | 2 iron sheets + 1 brass sheet + 1 nautilus shell + 4 blackpowder |
| `wind_chamber_modifier` | 1 copper sheet + 1 brass sheet + 1 wind charge + 4 blackpowder |

Preserve the original special-material gates: blue ice, lightning rods, iron/gold blocks, nautilus shells, and wind charges. Steel core and lead core are Artifice item names, not requests for new steel or lead resources.

## Powder and magical modifiers: 7 mixing recipes

These output one finished modifier, not stacks of ammunition. Only overcharged powder requires heat. The others are unheated. No separate haunting/polishing intermediates in this first implementation.

| Original recipe ID | Total ingredients | Heat |
| --- | --- | --- |
| `antigravity_powder_modifier` | 4 blackpowder + 1 ender pearl | None |
| `seeking_powder_modifier` | 4 blackpowder + 1 amethyst cluster | None |
| `overcharged_powder_modifier` | 8 blackpowder + 1 redstone block + 2 blaze powder | Heated |
| `enchanted_bullet_modifier` | 1 bullet + 4 blackpowder + 3 lapis | None |
| `singularity_charge_modifier` | 4 blackpowder + 4 amethyst shards + 1 ender eye + 1 brass sheet | None |
| `venom_capsule_modifier` | 1 bullet + 1 glass bottle + 3 spider eyes | None |
| `bloodletting_tip_modifier` | 4 blackpowder + 3 quartz + 1 ghast tear + 1 redstone | None |

## Hats: retain both original recipes

- Cowboy hat: leather helmet + 3 leather + 2 bullets.
- Tricorne: leather helmet + 3 leather + blackpowder + feather.

No new recycling recipes, fluids, or alternative manual production routes are included. All 46 existing recipe IDs are accounted for by replacements or explicit retention.

## Texture and incomplete-item scope

23 distinct incomplete items: 7 guns, 3 component tiers, 2 ammunition batches, and 11 assembly modifiers. Mixing/compacting outputs do not get unnecessary incomplete variants.

Implemented by `tools/generate_textures.py` with Python/Pillow: individual **16 x 16 RGBA PNGs** and an enlarged nearest-neighbor [contact sheet](workpiece-textures.png). Models/translations are generated by `tools/generate_recipes.py`. The user explicitly requested programmatic art; no image generation was used.

Use the local Artifice textures as visual references. The inspected simple/clockwork component and six-shooter icons suggest compact angular silhouettes, dark outlines/shadows, warm copper/gold highlights, and gray metal. Draw original incomplete silhouettes: exposed mechanisms for components, unfinished wooden/metal outlines for guns, partially assembled attachments, and small unfinished ammunition clusters. Incomplete variants need visibly different silhouettes and not just recolors. Preserve wood in the gun icons. Avoid smooth gradients, antialiasing, and rescaling finished upstream icons into the new assets.

There is one fixed texture per incomplete item, not a sprite for every station/progress percentage. Source pixels are authored on the 16 x 16 grid; scaled images are for review only. All 23 distinct textures were visually reviewed in the contact sheet.

## Implementation checks and evidence

- Pin the recipe behavior to the configured Create 6.0.11 build. [Deployer processing](https://github.com/Creators-of-Create/Create/blob/fc9535d82a29419164a1e9dc9c678bdcddeab30d/src/main/java/com/simibubi/create/content/kinetics/deployer/BeltDeployerCallbacks.java) consumes one ordinary held ingredient per application, but damages damageable held items instead. This is why powder counts are repeated operations and the bayonet uses the sword as its base.
- [Sequenced assembly](https://github.com/Creators-of-Create/Create/blob/fc9535d82a29419164a1e9dc9c678bdcddeab30d/src/main/java/com/simibubi/create/content/processing/sequenced/SequencedAssemblyRecipe.java) tracks recipe and progress per stack, consumes the starting item only once, and repeats the full sequence for its loop count.
- Native steps are deploying, pressing, cutting, and filling. Mixer/compactor recipes are separate processes.
- Match every old recipe ID against the [inventory](existing-recipes.md), replacing the three powder recipes, two ammunition recipes, three components, seven guns, and 29 modifiers. Keep both hats.
- Use singular `recipe` paths and current 1.21.1 codecs; repeated item ingredients in basins must encode the full counts. Add advancement/recipe-ID handling as needed.
- Test each starting pair for ambiguity, loop consumption, guaranteed output count, proper sword consumption, wood consumption, fluid use, and removal of the original crafting route. Check that only finished products can be used as components/modifiers.
- Runtime tests verified replacement types, loaded ingredients/tags, every native sequence from start to finished output, unique recipe selection, key material costs, workpiece registration, and old unlock suppression. Graphical client/JEI inspection and physical belt-factory checks remain outstanding. Costs need survival playtesting, especially ammunition throughput and nested clockwork costs.
