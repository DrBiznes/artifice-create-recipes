# Create recipe proposals

Superseded by the [final factory assembly proposal](final-recipe-proposal.md). This file retains the earlier alternatives for reference; it is not the current proposed recipe set.

These are Minecraft gameplay proposals, not active recipes. Quantities are initial balance suggestions and have not been playtested. The addon scaffold deliberately contains no replacements yet.

## Recommendation and alternatives

| Direction | Behavior | Tradeoff |
| --- | --- | --- |
| A. Automation companion | Keep crafting recipes; add selected processing recipes with modest efficiency improvements. | Easiest to add to an existing world, but players can bypass the factory. |
| **B. Integrated workshop (recommended)** | Keep starter supplies and flintlock accessible; replace component progression, advanced guns, and modifiers with appropriate Create processes. | A meaningful factory without making every item a long assembly loop. |
| C. Full factory | Replace all relevant crafting routes; add stocks, unfinished gun kits, projectile blanks, and treatment stages. | Most visual and involved; more items, assets, balancing, and machine infrastructure. |

Start with B's recipe designs as additive prototypes, test cost/throughput, then enable replacements as a deliberate pack mode. Additive prototypes are not an enforced progression overhaul. No configuration modes have been implemented yet.

## What the existing recipes establish

The [complete inventory](existing-recipes.md) covers 46 recipes: 7 guns, 3 component tiers, 3 blackpowder routes, 2 bullet routes, 2 hats, and 29 modifiers. These are crafting-table recipes supplied by Iron's mod, not vanilla Minecraft items.

- Blackpowder: 2 charcoal -> 1; charcoal + redstone -> 2; gunpowder + charcoal + redstone -> 6.
- Bullets: iron ingot + blackpowder -> 16; copper ingot + blackpowder -> 4. A blanket equal-yield conversion would remove an existing distinction.
- Simple components: 8 copper ingots + blackpowder.
- Mechanical components: simple components + iron block + iron nugget + 4 chains + 2 redstone.
- Clockwork components: 2 mechanical components + 4 gold ingots + redstone.
- Flintlock uses no component tier; musket/blunderbuss use simple; revolvers use mechanical; arquebus/rifle use clockwork. The rifle additionally requires netherite.
- Modifier items are registered with stack size 1. Produce one per craft; these are equipment upgrades, not bulk ammunition outputs.

## Create's actual processing options

Verified against Create's `mc1.21.1/dev` revision `fc9535d82a29419164a1e9dc9c678bdcddeab30d` (6.0.11 source). The build pins Maven artifact `6.0.11-312`; its successful data-run startup reported the same commit hash. Future development-branch revisions may differ.

| Process / recipe type | Capabilities and limits relevant here | Best use |
| --- | --- | --- |
| Milling / `create:milling` | One input item, possible multiple/chance outputs; early machine. | Optional charcoal preparation. |
| Crushing / `create:crushing` | One input item, up to 7 output entries; processing duration and chance outputs. | Higher-throughput raw-material prep or carefully limited scrap recovery. Cannot combine charcoal and redstone in one crushing recipe. |
| Pressing / `create:pressing` | One input item, up to 2 outputs; works on belt/depot. | Existing metal sheets, or custom stamped blanks. Cannot combine metal and blackpowder directly. |
| Compacting / `create:compacting` | Press above a basin; multiple ingredients, fluids, optional heat. | Bullets, simple components, packed charges. |
| Mixing / `create:mixing` | Mixer above a basin; multiple ingredients, fluids, optional heat (`none`, `heated`, `superheated`). | Powder blends, coatings, fictional modifier treatments. |
| Cutting / `create:cutting` | One input, up to 4 output entries, duration; saw processing. | Optional stocks/wood parts; machining assembly intermediates. |
| Deploying / `create:deploying` | Workpiece + one held ingredient; optional `keep_held_item` for a reusable tool. | Attaching scope/bayonet; adding parts during assembly. |
| Filling / `create:filling` | One item + one fluid ingredient -> one item output. | Honey treatment, or a potion-fluid coating route with properly matched potion components. |
| Emptying / `create:emptying` | One item -> item and fluid output. | Existing honey-bottle emptying supplies 250 mB honey and returns the bottle. |
| Sandpaper / `create:sandpaper_polishing` | One input -> one output; manual or automated with a deployer holding sandpaper. | Optional polished lens/tip intermediate. Not itself a sequenced-assembly step. |
| Washing / `create:splashing` | Fan through water; one input, possible chance outputs. | Optional cleanup of a dedicated dirty blank. No ingredient additions. |
| Haunting / `create:haunting` | Fan through soul fire; one input. | Optional finishing stage on a pre-combined magical intermediate. |
| Fan smelting/blasting/smoking | Uses vanilla cooking recipe types, not imaginary `create:smelting` recipes. | Optional heat treatment of a dedicated intermediate; furnace recipes would also work. |
| Mechanical crafting / `create:mechanical_crafting` | Shaped machine-only assembly; larger layouts available. | Final guns or intricate component layouts. Existing ordinary crafting recipes can also be automated by mechanical crafters. |
| Sequenced assembly / `create:sequenced_assembly` | Ordered deploying, pressing, cutting, and filling steps; transitional item; loops; weighted final output pool. | Component tiers and optional gun production lines. |

Mixing, crushing, washing, haunting, polishing, and compacting are **separate factory stages**, not native steps inside one sequenced-assembly recipe. A belt can connect them to assembly, but assembly progress should be completed into a distinct intermediate before starting an unrelated treatment.

Create already admits eligible shapeless crafting recipes into mixers when `allowShapelessInMixer` is enabled. Both existing multi-ingredient blackpowder recipes qualify under those rules. Merely duplicating them as mixing recipes adds little. Define different inputs/yields or actually replace the original recipe when enforcing a new progression.

## Bulk supplies

| Product | Conservative conversion | More industrial alternative |
| --- | --- | --- |
| Charcoal-only blackpowder | Keep 2 charcoal -> 1 as the survival fallback. | Mill 1 charcoal -> 1 blackpowder as an intentional 2x efficiency bonus; crushing may use the same yield. Avoid two outputs that make a single machine randomly choose a route. |
| Basic blackpowder | Mixer: 1 charcoal + 1 redstone -> 2, preserving cost. | Mixer -> 3 (+50%); stronger bonus needs throughput/playtesting. |
| Rich blackpowder | Mixer: 1 gunpowder + 1 charcoal + 1 redstone -> 6. | Mixer -> 8 (+33%); keep unheated for the early supply chain. |
| Iron bullets | Basin press: 1 iron ingot + 1 blackpowder -> 16. | Existing press: iron ingot -> iron sheet; sequence starts with sheet, deploys 1 blackpowder, presses -> 24 bullets, once, guaranteed. |
| Copper bullets | Basin press: 1 copper ingot + 1 blackpowder -> 4. | Copper sheet -> deploy 1 blackpowder -> press -> 6 bullets. Preserve the 4:1 iron/copper output ratio. |

The 24/6 bullet proposal adds one new `incomplete_ammunition` item, not a separate casing item per bullet. The input sheet's full value pays for the batch. Do not accidentally consume 24 blackpowder by looping 24 times. The proposed outputs are distinct recipe designs, not a request to register every variant concurrently.

## Components: the main assembly progression

| Tier | Option 1: preserve material cost | Option 2: Create-native workshop |
| --- | --- | --- |
| Simple | Basin compact 8 copper ingots + 1 blackpowder -> 1 simple component. | Compact 4 copper sheets + 2 andesite alloy + 1 cogwheel + 1 blackpowder -> 1. Reduces raw copper, adds existing Create parts. No brass/deployer gate yet. |
| Mechanical | Mechanical-crafter pattern using the existing ingredients and amounts. | Start with 1 simple component; deploy iron sheet -> deploy cogwheel -> deploy redstone -> press; repeat **2 times**, output 1 mechanical component. Total additions: 2 sheets, 2 cogwheels, 2 redstone. |
| Clockwork | Mechanical-crafter pattern retaining 2 mechanical components + 4 gold + redstone. | Start with 1 mechanical component; deploy another mechanical component, 4 golden sheets (4 stations), and 1 precision mechanism; press -> 1 clockwork component. **One pass**, guaranteed output. |

Option 2 is a rebalance, not material parity: mechanical components become cheaper in raw iron/chains but require a brass-era deployer setup. Clockwork keeps the two-mechanical-component dependency and replaces its redstone ingredient with a precision mechanism. Create's own precision-mechanism production has a failure pool; the proposed downstream assembly does not introduce another failure roll.

Use `incomplete_mechanical_components` and `incomplete_clockwork_components` as new addon items with models/translations. For a version emphasizing sequenced assembly on *every* tier, simple components can also be assembled from copper sheets with deployers and pressing, but that would move even muskets behind brass. I recommend the early basin route instead.

## Guns: preserve identity and offer two assembly styles

| Gun | Current ingredients (one output) | Recommended workshop route | Full-factory alternative |
| --- | --- | --- | --- |
| Flintlock | 2 iron, log, flint and steel, blackpowder | Keep its table recipe as the entry gun; optional mechanical-crafter equivalent. | Cut a stock, make a flintlock kit, then deploy the remaining ignition/material ingredients and press. |
| Musket | Iron, log, flint and steel, simple component, blackpowder | Mechanical crafting; retain simple tier, replace iron ingot with sheet if desired. | Musket kit -> fit simple component -> apply remaining parts -> press. |
| Blunderbuss | 4 iron, log, 2 simple components | Mechanical crafting using 4 iron sheets + stock/log + 2 simple components. | Dedicated kit -> fit both simple components and metal parts -> press. |
| Blackpowder revolver | Iron, log, hopper, mechanical component, blackpowder | Mechanical crafting retaining hopper and blackpowder; iron may become a sheet. | Dedicated kit -> fit mechanical component/hopper -> add remaining ingredients -> press. |
| Six shooter | 2 iron, log, hopper, mechanical component | Mechanical crafting retaining this distinct input set; no added blackpowder requirement. | Dedicated kit -> fit mechanical component/hopper -> add remaining iron -> press. |
| Arquebus | 2 iron, log, clockwork component, blackpowder | Mechanical crafting retaining its surprisingly high clockwork tier. | Dedicated kit -> fit clockwork component -> add remaining materials -> press. |
| Clockwork rifle | Netherite ingot, log, hopper, repeater, clockwork component | Mechanical crafting retaining **netherite**, hopper, repeater, and clockwork tier. | Dedicated kit -> fit clockwork component/hopper/repeater -> deploy netherite if not already paid by kit -> press. |

Mechanical crafting is the low-overhead choice: existing shapes can be reused, with sheets standing in for ingots. Optional sawing can introduce `gun_stock`: one log -> one stock, preserving the original one-log-per-gun cost. Existing log cutting recipes require output filtering; do not globally replace Create's plank recipes.

The full-factory column describes the route, not additional costs. Each kit must consume a documented subset of that gun's listed ingredients; deployers consume the remainder exactly once. Register distinct starting kits for the seven gun routes so a shared stock and identical first step cannot silently choose the wrong gun. Use one loop and deterministic one-gun output. Distinct `incomplete_*` workpieces make the line readable. Never use finished guns as intermediates: guns carry ammo/modifier state that generic recipe outputs need not preserve.

## All 29 modifiers

These baseline proposals preserve the ingredient counts from the inventory unless an alternative is explicitly stated. Every result count is 1. A sequence requiring several ingredients uses one deployer operation per ingredient item; it is not a multi-slot deployer.

| Modifier IDs (suffix `_modifier`) | Baseline machine replacement | Optional elaboration |
| --- | --- | --- |
| `blackpowder_charge`, `scattershot` | Basin compact their existing blackpowder/bullet/string inputs. | Dedicated wrapped-charge intermediate, then belt pressing. |
| `antigravity_powder`, `seeking_powder` | Unheated mixing using the existing pearl/cluster and powder amounts. | Mix into separate unstable intermediates, then haunt to finish. Preserve the pearl/cluster cost. |
| `overcharged_powder` | Heated mixing: 6 blackpowder + redstone block + 2 blaze powder. | Superheated version only for a deliberately later progression; it adds a blaze-cake gate. |
| `singularity_charge` | Mix 2 blackpowder + 4 amethyst shards + ender eye. | Output unstable singularity charge, then haunt. Do not replace the ender eye with a cheap haunting-only input. |
| `enchanted_bullet` | Mix 1 bullet + 2 blackpowder + 3 lapis. | Same ingredients -> arcane blank -> haunting. This creates a modifier item, not an enchanted ammo stack. |
| `gun_oil` | Mix simple component + redstone + 250 mB honey -> gun-oil modifier. | First deploy redstone onto a simple component to make a dry mechanism, then fill with 250 mB honey. No new oil fluid required. |
| `venom_capsule` | Mix 1 bullet + glass bottle + 3 spider eyes -> modifier. | Prepared capsule + poison potion fluid in a spout; requires a new capsule intermediate and potion-component matching. This alternative changes the brewing/cost gate. |
| `incendiary_tip`, `frozen_jacket`, `voltaic_core` | Basin compact the existing metal, blackpowder, and respectively 3 blaze powder / 3 blue ice / 3 lightning rods. | Prepare separate coated blanks, then press. Preserve blue ice/lightning-rod costs; generic water does not replace blue ice for free. |
| `breaching_shell`, `steel_core`, `lead_core`, `trick_bullet`, `spiral_tip` | Basin compact the exact original ingredient multiset. | Short assembly with a distinct blank and final pressing/cutting; retain iron/gold blocks, deepslate, and nautilus-shell gates. No new steel/lead material required despite the item names. |
| `wind_chamber` | Compact 2 copper + blackpowder + wind charge. | Short sequence fitting the charge; preserve the Trial Chamber-related ingredient. |
| `bloodletting_tip` | Mix 2 blackpowder + 3 quartz + ghast tear + redstone. | Make a pre-combined rough tip, then sandpaper polish. The ghast tear remains required. |
| `chain_shot`, `hook_shot` | Mechanical crafting with their existing bullets/chains/iron. | Dedicated unfinished linkage with each chain/bullet fitted by deployer, then press. |
| `hair_trigger`, `buffer_spring` | Mechanical crafting with simple component + 2 copper / 6 iron. | One-pass sequence attaching copper/iron sheets one at a time, then cutting/pressing. |
| `gas_vent` | Mechanical crafting: 2 simple components + hopper. | Start with simple component, deploy second simple component and hopper, press. |
| `mechanical_accelerator`, `mechanical_repeater` | Mechanical crafting preserving simple/clockwork tier + 3 copper/gold + 2 chains. | One-pass sequence fitting the same parts, then pressing. |
| `scope_attachment`, `bayonet_attachment` | Single deploying recipe: simple component + spyglass / iron sword. | These already express the attachment operation well; no extra chain needed. |
| `suppressor_attachment` | Mechanical crafting: clockwork component + gold + leather. | Start with clockwork component, deploy gold sheet, deploy leather, press. |

Keep both hat recipes unchanged in the workshop mode. They are apparel and add little to the mechanical progression; mechanical crafters can already automate their ordinary shaped recipes. Full-factory mode can give them explicit mechanical-crafting replacements using the same ingredients.

## Implementation and balance rules

1. Use `data/<namespace>/recipe/` (singular) for Minecraft 1.21.1. New additive recipes get addon IDs. Actual replacements override the original `irons_artifice:<recipe>` IDs, or disable those IDs and add new ones. Adding an addon recipe alone does not remove the crafting recipe.
2. For an override, supply the Create recipe under the original ID when there is one replacement route. For deliberate removal, a resource with `neoforge:conditions` and `neoforge:false` can suppress that entry. Validate pack priority and recipe reload in game; existing advancement recipe references also need reviewing when changing IDs/types.
3. Prefer a datapack/built-in-pack mode switch for optional wholesale replacements, or a real registered NeoForge condition if configuration must control it. Do not assume a generic config JSON key changes recipe loading. Switching recipes requires reload/restart.
4. Create 1.21.1 processing result stacks use `id` and optional `count`, not old 1.20 `item` output syntax. Inputs remain `item`/`tag`. Fluid ingredients use the NeoForge typed format; see the linked honey example.
5. Normal processing chances describe output rolls. Sequenced-assembly result chances are **relative weights for one selected final result**, not simultaneous byproducts. Use one result for guaranteed output. Loops repeat all added ingredients, not just the motion of machines.
6. Do not register competing sequences starting from the same item and indistinguishable first operation. Distinct starting kits are safer for gun families. Use dedicated unfinished items so partial work cannot be spent as complete components elsewhere.
7. Avoid new gun/ammo recycling recipes initially. Equipment comes from loot and may carry state; unconditional crushing refunds can create resource farms or erase attached upgrades. Scrap recovery should be limited to addon intermediates with a proven loss, never full ingredient refunds.
8. No actual replacement is considered verified until a client recipe reload, JEI view (if installed), successful factory run, and survival progression check confirm ingredients, counts, loop consumption, and original-recipe removal.

## Source references

- [Official NeoForge 1.21.1 ModDevGradle MDK](https://github.com/NeoForgeMDKs/MDK-1.21.1-ModDevGradle/tree/4e1be6e906e1b32a753e3580af4ea1bcc3dbc79e).
- [Create recipe registry](https://github.com/Creators-of-Create/Create/blob/fc9535d82a29419164a1e9dc9c678bdcddeab30d/src/main/java/com/simibubi/create/AllRecipeTypes.java).
- [Sequenced assembly implementation and weighted outputs](https://github.com/Creators-of-Create/Create/blob/fc9535d82a29419164a1e9dc9c678bdcddeab30d/src/main/java/com/simibubi/create/content/processing/sequenced/SequencedAssemblyRecipe.java).
- [Create's precision-mechanism recipe](https://github.com/Creators-of-Create/Create/blob/fc9535d82a29419164a1e9dc9c678bdcddeab30d/src/generated/resources/data/create/recipe/sequenced_assembly/precision_mechanism.json).
- [Mixer's automatic crafting eligibility](https://github.com/Creators-of-Create/Create/blob/fc9535d82a29419164a1e9dc9c678bdcddeab30d/src/main/java/com/simibubi/create/content/kinetics/mixer/MechanicalMixerBlockEntity.java#L262).
- [Processing recipe codec](https://github.com/Creators-of-Create/Create/blob/fc9535d82a29419164a1e9dc9c678bdcddeab30d/src/main/java/com/simibubi/create/content/processing/recipe/ProcessingRecipeParams.java).
- [Modern honey filling JSON](https://github.com/Creators-of-Create/Create/blob/fc9535d82a29419164a1e9dc9c678bdcddeab30d/src/generated/resources/data/create/recipe/filling/honeyed_apple.json).
- [NeoForge 1.21.1 data load conditions](https://docs.neoforged.net/docs/1.21.1/resources/server/conditions/).
