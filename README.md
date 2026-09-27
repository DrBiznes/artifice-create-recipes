# Artifice Create Recipes

A NeoForge 1.21.1 addon that replaces [Iron's Arms 'n Artifice](https://modrinth.com/mod/irons-artifice) crafting recipes with [Create](https://modrinth.com/mod/create) assembly lines, mixing, and compacting. Guns, bullets, and components have to come out of a factory. It is required on both the client and the server. Hat recipes are unchanged.

Requires NeoForge 21.1.248+, Create 6.0.10+, and Iron's Arms 'n Artifice. Development notes are in [docs/development.md](docs/development.md), and the full design rationale is in [docs/final-recipe-proposal.md](docs/final-recipe-proposal.md).

## Recipes

Sequenced assembly steps are deployer steps unless marked **Saw** (cutting), **Press** (pressing), or **Fill** (spout).

| Output | Machine | Inputs |
| --- | --- | --- |
| Blackpowder | Mixing | 2× Charcoal |
| 3× Blackpowder | Mixing | Charcoal, Redstone |
| 8× Blackpowder | Mixing | Charcoal, Redstone, Gunpowder |
| 24× Bullet | Sequenced Assembly, 6 loops | Iron Sheet → Blackpowder ×4 → Press |
| 6× Bullet | Sequenced Assembly, 2 loops | Copper Sheet → Blackpowder ×3 → Press |
| Simple Mechanical Components | Sequenced Assembly, 2 loops | Copper Sheet → Andesite Alloy → Cogwheel → Iron Sheet → Blackpowder → Press |
| Mechanical Components | Sequenced Assembly, 2 loops | Simple Mechanical Components → Brass Sheet → Large Cogwheel → Iron Sheet ×2 → Andesite Alloy → Redstone → Press |
| Clockwork Components | Sequenced Assembly | Mechanical Components → Precision Mechanism → Mechanical Components → Brass Sheet ×4 → Golden Sheet ×2 → Press |
| Flintlock | Sequenced Assembly | Log → Flint → Saw → Iron Sheet ×4 → Andesite Alloy ×2 → Blackpowder → Press |
| Musket | Sequenced Assembly | Log → Simple Mechanical Components → Log → Saw → Iron Sheet ×6 → Andesite Alloy ×2 → Flint → Blackpowder → Press |
| Blunderbuss | Sequenced Assembly | Log → Copper Sheet → Log → Saw → Simple Mechanical Components ×2 → Iron Sheet ×8 → Andesite Alloy ×2 → Press |
| Blackpowder Revolver | Sequenced Assembly | Log → Mechanical Components → Saw → Hopper → Iron Sheet ×4 → Brass Sheet → Andesite Alloy ×2 → Blackpowder → Press |
| Six Shooter | Sequenced Assembly | Log → Brass Sheet → Saw → Mechanical Components → Hopper → Iron Sheet ×4 → Brass Sheet → Andesite Alloy ×2 → Press |
| Arquebus | Sequenced Assembly | Log → Clockwork Components → Log → Saw → Iron Sheet ×6 → Brass Sheet ×2 → Andesite Alloy ×2 → Blackpowder → Press |
| Clockwork Rifle | Sequenced Assembly | Log → Netherite Ingot → Log → Saw → Clockwork Components → Hopper → Repeater → Iron Sheet ×4 → Brass Sheet ×2 → Andesite Alloy ×2 → Press |
| Hair Trigger Modifier | Sequenced Assembly | Simple Mechanical Components → Copper Sheet → Iron Sheet ×2 → Saw → Press |
| Buffer Spring Modifier | Sequenced Assembly | Simple Mechanical Components → Iron Sheet ×6 → Andesite Alloy ×2 → Saw → Press |
| Gas Vent Modifier | Sequenced Assembly | Simple Mechanical Components → Hopper → Simple Mechanical Components → Iron Sheet ×2 → Press |
| Mechanical Accelerator Modifier | Sequenced Assembly | Mechanical Components → Chain ×2 → Copper Sheet ×2 → Shaft ×2 → Press |
| Mechanical Repeater Modifier | Sequenced Assembly | Clockwork Components → Chain ×2 → Brass Sheet ×2 → Golden Sheet ×2 → Press |
| Scope Attachment Modifier | Sequenced Assembly | Simple Mechanical Components → Spyglass → Iron Sheet → Press |
| Bayonet Attachment Modifier | Sequenced Assembly | Iron Sword → Simple Mechanical Components → Andesite Alloy → Press |
| Suppressor Attachment Modifier | Sequenced Assembly | Clockwork Components → Leather ×2 → Golden Sheet → Iron Sheet ×2 → Press |
| Gun Oil Modifier | Sequenced Assembly | Simple Mechanical Components → Redstone → Fill 250 mB Honey |
| Chain Shot Modifier | Sequenced Assembly | Bullet → Chain ×5 → Bullet → Andesite Alloy → Press |
| Hook Shot Modifier | Sequenced Assembly | Bullet → Iron Sheet ×4 → Chain ×2 → Andesite Alloy ×2 → Press |
| Blackpowder Charge Modifier | Compacting | 8× Blackpowder, 2× String |
| Scattershot Modifier | Compacting | 4× Bullet, 4× Blackpowder, 2× String |
| Breaching Shell Modifier | Compacting | 2× Copper Sheet, 2× Iron Sheet, 4× Blackpowder, 3× Flint |
| Incendiary Tip Modifier | Compacting | 3× Iron Sheet, 4× Blackpowder, 3× Blaze Powder |
| Frozen Jacket Modifier | Compacting | 3× Iron Sheet, 4× Blackpowder, 3× Blue Ice |
| Voltaic Core Modifier | Compacting | 2× Copper Sheet, Brass Sheet, 4× Blackpowder, 3× Lightning Rod |
| Steel Core Modifier | Compacting | Iron Block, 3× Iron Sheet, 4× Blackpowder |
| Lead Core Modifier | Compacting | Deepslate Bricks, 3× Iron Sheet, 2× Andesite Alloy, 4× Blackpowder |
| Trick Bullet Modifier | Compacting | Gold Block, 2× Golden Sheet, Brass Sheet, 4× Blackpowder |
| Spiral Tip Modifier | Compacting | 2× Iron Sheet, Brass Sheet, Nautilus Shell, 4× Blackpowder |
| Wind Chamber Modifier | Compacting | Copper Sheet, Brass Sheet, Wind Charge, 4× Blackpowder |
| Antigravity Powder Modifier | Mixing | 4× Blackpowder, Ender Pearl |
| Seeking Powder Modifier | Mixing | 4× Blackpowder, Amethyst Cluster |
| Overcharged Powder Modifier | Mixing (heated) | 8× Blackpowder, Redstone Block, 2× Blaze Powder |
| Enchanted Bullet Modifier | Mixing | Bullet, 4× Blackpowder, 3× Lapis Lazuli |
| Singularity Charge Modifier | Mixing | 4× Blackpowder, 4× Amethyst Shard, Ender Eye, Brass Sheet |
| Venom Capsule Modifier | Mixing | Bullet, Glass Bottle, 3× Spider Eye |
| Bloodletting Tip Modifier | Mixing | 4× Blackpowder, 3× Quartz, Ghast Tear, Redstone |

## Attribution

- [Create](https://modrinth.com/mod/create) by the Creators of Create: machines and processing recipes.
- [Iron's Arms 'n Artifice](https://modrinth.com/mod/irons-artifice) by iron431: the guns, ammo, and modifiers this addon rebalances.
