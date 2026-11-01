"""Generate the agreed recipes, item registration, models, and localization.

Uses only Python's standard library. Run from any directory; outputs are tracked.
Recipe IDs intentionally occupy the upstream namespace to replace table recipes.
"""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'src/main/resources'
MOD = 'artifice_create_recipes'
IA = 'irons_artifice:'
# Optional Hazen's Archaic Hexerei Armaments (1.21.1) support. Its recipes are
# overridden by id and only load when it and the mods its recipes use are present.
HEX = 'hazens_archaic_hexerei_armaments'
HEX_CONDITIONS = [{'type': 'neoforge:mod_loaded', 'modid': m} for m in (HEX, 'irons_spellbooks', 'hazentouvelib')]

ALIASES = {
    'iron': '#c:plates/iron', 'copper': '#c:plates/copper',
    'brass': '#c:plates/brass', 'gold': '#c:plates/gold',
    'log': '#minecraft:logs', 'leather': '#c:leathers',
    'netherite': '#c:ingots/netherite',
    'alloy': 'create:andesite_alloy', 'cog': 'create:cogwheel',
    'large_cog': 'create:large_cogwheel', 'shaft': 'create:shaft',
    'precision': 'create:precision_mechanism',
    'simple': IA + 'simple_mechanical_components',
    'mechanical': IA + 'mechanical_components',
    'clockwork': IA + 'clockwork_components',
    'powder': IA + 'blackpowder', 'bullet': IA + 'bullet',
    'blunderbuss_gun': IA + 'blunderbuss', 'rifle': IA + 'clockwork_rifle',
    'overcharged': IA + 'overcharged_powder_modifier',
    'steel_block': 'hazentouvelib:steel_block', 'cog': 'create:cogwheel',
    'warhog_cog': HEX + ':warhog_cog', 'star_cannon_gun': HEX + ':star_cannon',
    'mithril_ingot': 'irons_spellbooks:mithril_ingot', 'mithril_scrap': 'irons_spellbooks:mithril_scrap',
    'cinder_essence': 'irons_spellbooks:cinder_essence',
}


def ingredient(name):
    name = ALIASES.get(name, name if ':' in name else 'minecraft:' + name)
    return {'tag': name[1:]} if name.startswith('#') else {'item': name}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def D(name, count=1):
    return [('deploying', name)] * count


P = [('pressing', None)]
C = [('cutting', None)]
HONEY = [('filling', {'type': 'neoforge:tag', 'tag': 'c:honey', 'amount': 250})]
RECIPES = {}
ITEMS = {}
# Hexerei overrides, keyed by recipe path under data/<HEX>/recipe.
HEX_RECIPES = {}
HEX_ITEMS = {}
# Additive pre-brass routes. They live under this mod's namespace because they
# replace nothing upstream; RECIPES stays one-to-one with upstream recipe IDs.
EARLY_RECIPES = {}
# Upstream files these unlocks outside recipes/misc.
UNLOCK_CATEGORY = {'bullet_box': 'tools'}


def assembly(recipe_id, start, steps, loops=1, output=None, count=1, incomplete=None, addon=None):
    assert len(steps) <= 6, recipe_id + ' exceeds the six steps Create can display'
    name = recipe_id.rsplit('/', 1)[-1]
    item = incomplete or 'incomplete_' + name
    transitional = MOD + ':' + item
    (HEX_ITEMS if addon else ITEMS)[item] = {'recipe': recipe_id, 'output': output or name}
    sequence = []
    for kind, value in steps:
        step = {'type': 'create:' + kind, 'ingredients': [{'item': transitional}],
                'results': [{'id': transitional}]}
        if kind == 'deploying':
            step['ingredients'].append(ingredient(value))
        elif kind == 'filling':
            step['ingredients'].append(value)
        elif kind == 'cutting':
            step['processing_time'] = 50
        sequence.append(step)
    recipe = {
        'type': 'create:sequenced_assembly', 'ingredient': ingredient(start),
        'transitional_item': {'id': transitional}, 'loops': loops,
        'sequence': sequence,
        'results': [{'id': (addon + ':' + name) if addon else IA + (output or recipe_id), 'count': count}],
    }
    if addon:
        HEX_RECIPES[recipe_id] = {'neoforge:conditions': HEX_CONDITIONS, **recipe}
    else:
        RECIPES[recipe_id] = recipe


def handloaded(recipe_id, metal, powder, powder_count, count):
    EARLY_RECIPES[recipe_id] = {
        'type': 'minecraft:crafting_shapeless', 'category': 'equipment',
        'ingredients': [ingredient(metal)] + [ingredient(powder)] * powder_count,
        'result': {'id': IA + 'bullet', 'count': count}}


def basin(recipe_id, kind, inputs, output=None, count=1, heat=None, target=RECIPES):
    recipe = {'type': 'create:' + kind,
              'ingredients': [ingredient(name) for name, quantity in inputs for _ in range(quantity)],
              'results': [{'id': IA + (output or recipe_id), 'count': count}]}
    if kind == 'mixing':
        recipe['processing_time'] = 100
    if heat:
        recipe['heat_requirement'] = heat
    target[recipe_id] = recipe


basin('blackpowder_from_charcoal', 'mixing', [('charcoal', 2)], 'blackpowder')
basin('blackpowder', 'mixing', [('charcoal', 1), ('redstone', 1)], count=3)
basin('blackpowder_from_gunpowder', 'mixing', [('charcoal', 1), ('redstone', 1), ('gunpowder', 1)], 'blackpowder', 8)
assembly('bullet_from_iron', 'iron', D('powder', 4) + P, 6, 'bullet', 24, 'incomplete_iron_bullet_batch')
assembly('bullet_from_copper', 'copper', D('powder', 3) + P, 2, 'bullet', 6, 'incomplete_copper_bullet_batch')
assembly('simple_mechanical_components', 'copper', D('alloy') + D('cog') + D('iron') + D('powder') + P, 2)
assembly('mechanical_components', 'simple', D('brass') + D('large_cog') + D('iron', 2) + D('redstone') + P, 2)
assembly('clockwork_components', 'precision', D('mechanical') + D('brass', 2) + D('gold') + P, 2)
assembly('bullet_box', 'bullet', D('bullet') + D('gold', 3) + P, 2)

# Deployers need brass, so everything an early gunsmith needs stays on andesite
# age machines: press, basin, and mixer. These routes must not need a deployer.
# Handloading always loses to the assembly lines: gunpowder gives half of what
# a rich mix would, and blackpowder keeps its cost but burns 12x the metal.
handloaded('bullet_handloaded_iron_from_gunpowder', 'iron', 'gunpowder', 1, 4)
handloaded('bullet_handloaded_copper_from_gunpowder', 'copper', 'gunpowder', 1, 2)
handloaded('bullet_handloaded_iron', 'iron', 'powder', 2, 2)
handloaded('bullet_handloaded_copper', 'copper', 'powder', 2, 1)
basin('simple_mechanical_components_compacted', 'compacting', [('copper', 8), ('alloy', 2), ('powder', 1)],
      'simple_mechanical_components', target=EARLY_RECIPES)
basin('flintlock', 'compacting', [('flint', 1), ('log', 2), ('iron', 4), ('alloy', 2)])
basin('musket', 'compacting', [('simple', 1), ('log', 3), ('iron', 6), ('alloy', 3)])

# Create's viewer fits six steps, so costs repeat through loops and one-off
# parts become the starting item. Short guns loop twice, long guns three times;
# each loop deploys one log. Start + first deployment stay unique per recipe.
WOOD = D('log') + D('iron', 2)
assembly('blunderbuss', 'simple', D('alloy') + D('log') + D('copper') + D('iron') + C + P, 3)
assembly('blackpowder_revolver', 'mechanical', WOOD + D('powder') + C + P, 2)
assembly('six_shooter', 'mechanical', D('brass') + WOOD + C + P, 2)
assembly('arquebus', 'clockwork', WOOD + D('brass') + C + P, 3)
assembly('clockwork_rifle', 'clockwork', D('netherite_scrap') + D('log') + D('iron') + D('brass') + C + P, 3)

ASSEMBLY_MODIFIERS = {
    'hair_trigger': ('simple', D('copper') + D('iron', 2) + C + P),
    'buffer_spring': ('simple', D('iron', 3) + D('alloy') + C + P, 2),
    'gas_vent': ('simple', D('hopper') + D('simple') + D('iron', 2) + P),
    'mechanical_accelerator': ('mechanical', D('chain') + D('copper') + D('shaft') + P, 2),
    'mechanical_repeater': ('clockwork', D('chain') + D('brass') + D('gold') + P, 2),
    'scope_attachment': ('simple', D('spyglass') + D('iron') + P),
    'bayonet_attachment': ('iron_sword', D('simple') + D('alloy') + P),
    'suppressor_attachment': ('clockwork', D('leather', 2) + D('gold') + D('iron', 2) + P),
    'gun_oil': ('simple', D('redstone') + HONEY),
    'chain_shot': ('bullet', D('chain', 4) + D('bullet') + P),
    'hook_shot': ('bullet', D('iron', 2) + D('chain') + D('alloy') + P, 2),
    'soulfire_coin': ('soul_lantern', D('netherite_scrap', 2) + D('gold', 2) + P),
}
for name, (start, steps, *loops) in ASSEMBLY_MODIFIERS.items():
    assembly(name + '_modifier', start, steps, *loops)

# Hexerei's guns upgrade a finished Artifice gun. Six steps is the viewer limit,
# so there is no closing press; every sequence starts from a different item.
assembly('crafting/materials/warhog_cog', 'netherite',
         D('clockwork') + D('steel_block') + D('netherite_scrap') + D('redstone') + P, 2, count=2, addon=HEX)
assembly('crafting/guns/royaltys_barrel', 'blunderbuss_gun',
         D('clockwork') + D('mechanical') + D('cinder_essence') + D('netherite_scrap') + D('quartz', 2), addon=HEX)
assembly('crafting/guns/star_cannon', 'rifle',
         D('warhog_cog', 2) + D('mithril_scrap', 2) + D('nether_star') + D('powder'), addon=HEX)
assembly('crafting/guns/super_star_shooter', 'star_cannon_gun',
         D('warhog_cog', 2) + D('clockwork') + D('mithril_ingot') + D('netherite') + D('netherite_scrap'), addon=HEX)
assembly('crafting/guns/tactical_crossgun', 'warhog_cog',
         D('mithril_ingot') + D('mithril_scrap', 2) + D('cinder_essence') + D('steel_block') + D('overcharged'), addon=HEX)

COMPACTING = {
    'blackpowder_charge': [('powder', 8), ('string', 2)],
    'scattershot': [('bullet', 4), ('powder', 4), ('string', 2)],
    'breaching_shell': [('copper', 2), ('iron', 2), ('powder', 4), ('flint', 3)],
    'incendiary_tip': [('iron', 3), ('powder', 4), ('blaze_powder', 3)],
    'frozen_jacket': [('iron', 3), ('powder', 4), ('blue_ice', 3)],
    'voltaic_core': [('copper', 2), ('brass', 1), ('powder', 4), ('lightning_rod', 3)],
    'steel_core': [('iron_block', 1), ('iron', 3), ('powder', 4)],
    'lead_core': [('deepslate_bricks', 1), ('iron', 3), ('alloy', 2), ('powder', 4)],
    'trick_bullet': [('gold_block', 1), ('gold', 2), ('brass', 1), ('powder', 4)],
    'spiral_tip': [('iron', 2), ('brass', 1), ('nautilus_shell', 1), ('powder', 4)],
    'wind_chamber': [('copper', 1), ('brass', 1), ('wind_charge', 1), ('powder', 4)],
}
for name, inputs in COMPACTING.items():
    basin(name + '_modifier', 'compacting', inputs)

MIXING = {
    'antigravity_powder': [('powder', 4), ('ender_pearl', 1)],
    'seeking_powder': [('powder', 4), ('amethyst_cluster', 1)],
    'overcharged_powder': [('powder', 8), ('redstone_block', 1), ('blaze_powder', 2)],
    'enchanted_bullet': [('bullet', 1), ('powder', 4), ('lapis_lazuli', 3)],
    'singularity_charge': [('powder', 4), ('amethyst_shard', 4), ('ender_eye', 1), ('brass', 1)],
    'venom_capsule': [('bullet', 1), ('glass_bottle', 1), ('spider_eye', 3)],
    'bloodletting_tip': [('powder', 4), ('quartz', 3), ('ghast_tear', 1), ('redstone', 1)],
}
for name, inputs in MIXING.items():
    basin(name + '_modifier', 'mixing', inputs, heat='heated' if name == 'overcharged_powder' else None)


def main():
    assert len(RECIPES) == 46 and len(ITEMS) == 23 and len(HEX_RECIPES) == 5 and len(HEX_ITEMS) == 5
    assert len(EARLY_RECIPES) == 5
    for name, recipe in RECIPES.items():
        write_json(RES / 'data/irons_artifice/recipe' / (name + '.json'), recipe)
        # These are processing recipes, not recipe-book crafting unlocks. Override
        # only their old recipe-unlock advancements, leaving gameplay goals alone.
        write_json(RES / 'data/irons_artifice/advancement/recipes' / UNLOCK_CATEGORY.get(name, 'misc') / (name + '.json'),
                   {'neoforge:conditions': [{'type': 'neoforge:false'}]})
    for name, recipe in EARLY_RECIPES.items():
        write_json(RES / 'data' / MOD / 'recipe' / (name + '.json'), recipe)
        if recipe['type'] != 'minecraft:crafting_shapeless':
            continue
        # Handloading stays a real table recipe, so it shows up in the recipe book.
        recipe_id = MOD + ':' + name
        sheet = '#' + recipe['ingredients'][0]['tag']
        write_json(RES / 'data' / MOD / 'advancement/recipes/combat' / (name + '.json'), {
            'parent': 'minecraft:recipes/root',
            'criteria': {
                'has_sheet': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': sheet}]}},
                'has_the_recipe': {'trigger': 'minecraft:recipe_unlocked', 'conditions': {'recipe': recipe_id}}},
            'requirements': [['has_sheet', 'has_the_recipe']],
            'rewards': {'recipes': [recipe_id]}})
    for path in HEX_RECIPES:
        write_json(RES / 'data' / HEX / 'recipe' / (path + '.json'), HEX_RECIPES[path])
        # Same suppression as above; the old shaped recipe's unlock is stale.
        write_json(RES / 'data' / HEX / 'advancement/recipes/combat' / (path + '.json'),
                   {'neoforge:conditions': [{'type': 'neoforge:false'}]})
    lang = {'itemGroup.' + MOD: 'Artifice: Factory Workpieces',
            'tooltip.' + MOD + '.incomplete': 'Unfinished workpiece — continue its assembly line.'}
    for name in [*ITEMS, *HEX_ITEMS]:
        lang['item.' + MOD + '.' + name] = name.replace('_', ' ').title().replace('Royaltys', "Royalty's")
        write_json(RES / 'assets' / MOD / 'models/item' / (name + '.json'),
                   {'parent': 'minecraft:item/generated', 'textures': {'layer0': MOD + ':item/' + name}})
    write_json(RES / 'assets' / MOD / 'lang/en_us.json', lang)
    # Shared registry manifest keeps assets and runtime registration in sync.
    def names(items):
        return '\n'.join('            "' + name + '",' for name in items).rstrip(',')

    java = f'''// Generated by tools/generate_recipes.py; do not edit by hand.
package dev.jam.artificecreaterecipes;

import java.util.List;

public final class WorkpieceNames {{
    public static final List<String> ALL = List.of(
{names(ITEMS)}
    );
    /** Registered only when Hazen's Archaic Hexerei Armaments is installed. */
    public static final List<String> HEXEREI = List.of(
{names(HEX_ITEMS)}
    );
    private WorkpieceNames() {{}}
}}
'''
    (ROOT / 'src/main/java/dev/jam/artificecreaterecipes/WorkpieceNames.java').write_text(java, encoding='utf-8')
    print(f'Generated {len(RECIPES)} replacements, {len(EARLY_RECIPES)} early routes, and {len(ITEMS)} workpieces, '
          f'plus {len(HEX_RECIPES)} optional Hexerei replacements.')


if __name__ == '__main__':
    main()
