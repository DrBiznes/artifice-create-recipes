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


def assembly(recipe_id, start, steps, loops=1, output=None, count=1, incomplete=None):
    assert len(steps) <= 6, recipe_id + ' exceeds the six steps Create can display'
    item = incomplete or 'incomplete_' + recipe_id
    transitional = MOD + ':' + item
    ITEMS[item] = {'recipe': recipe_id, 'output': output or recipe_id}
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
    RECIPES[recipe_id] = {
        'type': 'create:sequenced_assembly', 'ingredient': ingredient(start),
        'transitional_item': {'id': transitional}, 'loops': loops,
        'sequence': sequence, 'results': [{'id': IA + (output or recipe_id), 'count': count}],
    }


def basin(recipe_id, kind, inputs, output=None, count=1, heat=None):
    recipe = {'type': 'create:' + kind,
              'ingredients': [ingredient(name) for name, quantity in inputs for _ in range(quantity)],
              'results': [{'id': IA + (output or recipe_id), 'count': count}]}
    if kind == 'mixing':
        recipe['processing_time'] = 100
    if heat:
        recipe['heat_requirement'] = heat
    RECIPES[recipe_id] = recipe


basin('blackpowder_from_charcoal', 'mixing', [('charcoal', 2)], 'blackpowder')
basin('blackpowder', 'mixing', [('charcoal', 1), ('redstone', 1)], count=3)
basin('blackpowder_from_gunpowder', 'mixing', [('charcoal', 1), ('redstone', 1), ('gunpowder', 1)], 'blackpowder', 8)
assembly('bullet_from_iron', 'iron', D('powder', 4) + P, 6, 'bullet', 24, 'incomplete_iron_bullet_batch')
assembly('bullet_from_copper', 'copper', D('powder', 3) + P, 2, 'bullet', 6, 'incomplete_copper_bullet_batch')
assembly('simple_mechanical_components', 'copper', D('alloy') + D('cog') + D('iron') + D('powder') + P, 2)
assembly('mechanical_components', 'simple', D('brass') + D('large_cog') + D('iron', 2) + D('redstone') + P, 2)
assembly('clockwork_components', 'precision', D('mechanical') + D('brass', 2) + D('gold') + P, 2)

# Create's viewer fits six steps, so costs repeat through loops and one-off
# parts become the starting item. Short guns loop twice, long guns three times;
# each loop deploys one log. Start + first deployment stay unique per recipe.
WOOD = D('log') + D('iron', 2)
assembly('flintlock', 'flint', WOOD + D('alloy') + C + P, 2)
assembly('musket', 'simple', WOOD + D('alloy') + C + P, 3)
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
}
for name, (start, steps, *loops) in ASSEMBLY_MODIFIERS.items():
    assembly(name + '_modifier', start, steps, *loops)

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
    assert len(RECIPES) == 44 and len(ITEMS) == 23
    for name, recipe in RECIPES.items():
        write_json(RES / 'data/irons_artifice/recipe' / (name + '.json'), recipe)
        # These are processing recipes, not recipe-book crafting unlocks. Override
        # only their old recipe-unlock advancements, leaving gameplay goals alone.
        write_json(RES / 'data/irons_artifice/advancement/recipes/misc' / (name + '.json'),
                   {'neoforge:conditions': [{'type': 'neoforge:false'}]})
    lang = {'itemGroup.' + MOD: 'Artifice: Factory Workpieces',
            'tooltip.' + MOD + '.incomplete': 'Unfinished workpiece — continue its assembly line.'}
    for name in ITEMS:
        lang['item.' + MOD + '.' + name] = name.replace('_', ' ').title()
        write_json(RES / 'assets' / MOD / 'models/item' / (name + '.json'),
                   {'parent': 'minecraft:item/generated', 'textures': {'layer0': MOD + ':item/' + name}})
    write_json(RES / 'assets' / MOD / 'lang/en_us.json', lang)
    # Shared registry manifest keeps assets and runtime registration in sync.
    lines = '\n'.join('            "' + name + '",' for name in ITEMS).rstrip(',')
    java = f'''// Generated by tools/generate_recipes.py; do not edit by hand.
package dev.jam.artificecreaterecipes;

import java.util.List;

public final class WorkpieceNames {{
    public static final List<String> ALL = List.of(
{lines}
    );
    private WorkpieceNames() {{}}
}}
'''
    (ROOT / 'src/main/java/dev/jam/artificecreaterecipes/WorkpieceNames.java').write_text(java, encoding='utf-8')
    print(f'Generated {len(RECIPES)} replacements and {len(ITEMS)} workpieces.')


if __name__ == '__main__':
    main()
