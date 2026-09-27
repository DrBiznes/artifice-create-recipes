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


def main():
    original = set(re.findall(r'^\| `([^`]+)` \|', (ROOT / 'docs/existing-recipes.md').read_text(encoding='utf-8-sig'), re.M))
    files = list((RES / 'data/irons_artifice/recipe').glob('*.json'))
    assert {f.stem for f in files} == original - {'cowboy_hat', 'tricorne'}, 'Missing/extra upstream overrides'
    types, workpieces, signatures = Counter(), set(), set()
    for file in files:
        recipe = json.loads(file.read_text())
        types[recipe['type']] += 1
        assert len(recipe['results']) == 1 and recipe['results'][0].get('chance', 1) == 1
        if recipe['type'] != 'create:sequenced_assembly':
            continue
        item = recipe['transitional_item']['id']
        assert item.startswith(MOD + ':incomplete_') and item not in workpieces
        workpieces.add(item)
        assert recipe['loops'] >= 1 and recipe['sequence'][0]['type'] == 'create:deploying'
        signature = json.dumps([recipe['ingredient'], recipe['sequence'][0]['ingredients'][1]], sort_keys=True)
        assert signature not in signatures, 'Conflicting first operation: ' + file.stem
        signatures.add(signature)
        for step in recipe['sequence']:
            assert step['ingredients'][0] == {'item': item}
            assert step['results'] == [{'id': item}]
            assert step['type'] in {'create:deploying', 'create:pressing', 'create:cutting', 'create:filling'}
    assert types == {'create:sequenced_assembly': 23, 'create:compacting': 11, 'create:mixing': 10}, types
    expected_names = {i.split(':')[1] for i in workpieces}
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
    assert len(hashes) == 23, 'Every workpiece needs a distinct texture'
    overrides = list((RES / 'data/irons_artifice/advancement/recipes/misc').glob('*.json'))
    assert {f.stem for f in overrides} == {f.stem for f in files}
    for f in overrides:
        assert json.loads(f.read_text()) == {'neoforge:conditions': [{'type': 'neoforge:false'}]}
    print('PASS: all 44 overrides, 23 unique 16x16 RGBA sprites/models/translations, unique assembly starters, and 44 stale unlock suppressions.')


if __name__ == '__main__':
    main()
