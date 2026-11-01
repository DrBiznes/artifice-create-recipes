"""Check resource completeness against the audited upstream recipe inventory.

Standard-library only. Runtime/registry/sequence tests are run separately with
gradlew runGameTestServer, because valid JSON alone cannot prove a recipe works.
"""
import hashlib
import json
import re
import struct
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'src/main/resources'
MOD = 'artifice_create_recipes'
HEX = 'hazens_archaic_hexerei_armaments'
HEX_RECIPES = ['crafting/materials/warhog_cog', 'crafting/guns/royaltys_barrel', 'crafting/guns/star_cannon',
               'crafting/guns/super_star_shooter', 'crafting/guns/tactical_crossgun']
HEX_MODS = {HEX, 'irons_spellbooks', 'hazentouvelib'}
HANDLOADED = {'bullet_handloaded_iron_from_gunpowder': 4, 'bullet_handloaded_copper_from_gunpowder': 2,
              'bullet_handloaded_iron': 2, 'bullet_handloaded_copper': 1}
EARLY = {*HANDLOADED, 'simple_mechanical_components_compacted'}


def main():
    original = set(re.findall(r'^\| `([^`]+)` \|', (ROOT / 'docs/existing-recipes.md').read_text(encoding='utf-8-sig'), re.M))
    files = list((RES / 'data/irons_artifice/recipe').glob('*.json'))
    assert {f.stem for f in files} == original - {'cowboy_hat', 'tricorne'}, 'Missing/extra upstream overrides'
    hex_files = [RES / 'data' / HEX / 'recipe' / (r + '.json') for r in HEX_RECIPES]
    assert {f.relative_to(RES / 'data' / HEX / 'recipe').as_posix()[:-5] for f in (RES / 'data' / HEX / 'recipe').rglob('*.json')} == set(HEX_RECIPES)
    types, workpieces, signatures, hex_workpieces = Counter(), set(), set(), set()
    for file in files + hex_files:
        recipe = json.loads(file.read_text())
        is_hex = file in hex_files
        if is_hex:
            conditions = recipe.pop('neoforge:conditions')
            assert {c['modid'] for c in conditions if c['type'] == 'neoforge:mod_loaded'} == HEX_MODS, file.stem
            assert recipe['results'][0]['id'] == HEX + ':' + file.stem
        else:
            types[recipe['type']] += 1
        assert len(recipe['results']) == 1 and recipe['results'][0].get('chance', 1) == 1
        if recipe['type'] != 'create:sequenced_assembly':
            continue
        item = recipe['transitional_item']['id']
        assert item.startswith(MOD + ':incomplete_') and item not in workpieces | hex_workpieces
        (hex_workpieces if is_hex else workpieces).add(item)
        assert recipe['loops'] >= 1 and recipe['sequence'][0]['type'] == 'create:deploying'
        assert len(recipe['sequence']) <= 6, 'Too many steps for the recipe viewer: ' + file.stem
        signature = json.dumps([recipe['ingredient'], recipe['sequence'][0]['ingredients'][1]], sort_keys=True)
        assert signature not in signatures, 'Conflicting first operation: ' + file.stem
        signatures.add(signature)
        for step in recipe['sequence']:
            assert step['ingredients'][0] == {'item': item}
            assert step['results'] == [{'id': item}]
            assert step['type'] in {'create:deploying', 'create:pressing', 'create:cutting', 'create:filling'}
    assert types == {'create:sequenced_assembly': 23, 'create:compacting': 13, 'create:mixing': 10}, types
    assert len(hex_workpieces) == 5 and len(signatures) == 28
    # Additive early routes never occupy an upstream ID and never need a deployer.
    early = {f.stem: json.loads(f.read_text()) for f in (RES / 'data' / MOD / 'recipe').glob('*.json')}
    assert set(early) == EARLY and not EARLY & original
    for name, count in HANDLOADED.items():
        assert early[name]['type'] == 'minecraft:crafting_shapeless'
        assert early[name]['result'] == {'id': 'irons_artifice:bullet', 'count': count}
        unlock = json.loads((RES / 'data' / MOD / 'advancement/recipes/combat' / (name + '.json')).read_text())
        assert unlock['rewards']['recipes'] == [MOD + ':' + name]
    assert early['simple_mechanical_components_compacted']['type'] == 'create:compacting'
    for name in ('flintlock', 'musket'):
        assert json.loads((RES / 'data/irons_artifice/recipe' / (name + '.json')).read_text())['type'] == 'create:compacting'
    expected_names = {i.split(':')[1] for i in workpieces | hex_workpieces}
    assets = RES / 'assets' / MOD
    assert {p.stem for p in (assets / 'textures/item').glob('*.png')} == expected_names
    assert {p.stem for p in (assets / 'models/item').glob('*.json')} == expected_names
    lang = json.loads((assets / 'lang/en_us.json').read_text())
    hashes = set()
    for item in expected_names:
        png = (assets / 'textures/item' / (item + '.png')).read_bytes()
        assert png[:8] == b'\x89PNG\r\n\x1a\n'
        assert struct.unpack('>II', png[16:24]) == (16, 16), item
        assert png[25] == 6, 'Expected RGBA: ' + item
        hashes.add(hashlib.sha256(png).hexdigest())
        assert lang['item.' + MOD + '.' + item]
        model = json.loads((assets / 'models/item' / (item + '.json')).read_text())
        assert model['textures']['layer0'] == MOD + ':item/' + item
    assert len(hashes) == 28, 'Every workpiece needs a distinct texture'
    unlocks = RES / 'data/irons_artifice/advancement/recipes'
    overrides = [*(unlocks / 'misc').glob('*.json'), *(unlocks / 'tools').glob('*.json')]
    assert sorted(f.stem for f in overrides) == sorted(f.stem for f in files)
    hex_overrides = [RES / 'data' / HEX / 'advancement/recipes/combat' / (r + '.json') for r in HEX_RECIPES]
    for f in overrides + hex_overrides:
        assert json.loads(f.read_text()) == {'neoforge:conditions': [{'type': 'neoforge:false'}]}
    print('PASS: all 46 overrides + 5 optional Hexerei overrides + 5 early routes, 28 unique 16x16 RGBA sprites/models/translations, unique assembly starters, and 51 stale unlock suppressions.')


if __name__ == '__main__':
    main()
