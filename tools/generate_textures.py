"""Draw original 16x16 workpiece sprites. Requires Pillow; no source art is copied.

All geometry is authored on the native pixel grid. The contact sheet is scaled
with nearest-neighbor sampling for inspection; only 16x16 PNGs ship in the mod.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from generate_recipes import ROOT, MOD, ITEMS, HEX_ITEMS

OUT = ROOT / 'src/main/resources/assets' / MOD / 'textures/item'
PALETTE = {
    'outline': '#272027', 'shadow': '#414048', 'metal': '#7b8085',
    'light': '#bec2bf', 'glint': '#eee3ce',
    'wood_dark': '#57362b', 'wood': '#925438', 'wood_light': '#ca8950',
    'copper_dark': '#7b3f2c', 'copper': '#c5753b', 'copper_light': '#f1ac62',
    'brass_dark': '#796039', 'brass': '#c6a24d', 'brass_light': '#f4d482',
    'red': '#a7483e', 'blue': '#7395a5', 'oil': '#e3a83e',
    'steel': '#9aa5b1', 'steel_light': '#d3dbe3', 'nether': '#4b3a4a', 'star': '#f6e27a',
    'ember': '#e0702a', 'quartz': '#ece6dc', 'mithril': '#7fd0d8',
}


class Sprite:
    def __init__(self):
        self.image = Image.new('RGBA', (16, 16))
        self.draw = ImageDraw.Draw(self.image)

    def box(self, xy, color):
        self.draw.rectangle(xy, fill=PALETTE.get(color, color))

    def line(self, points, color, width=1):
        self.draw.line(points, fill=PALETTE.get(color, color), width=width)

    def poly(self, points, color):
        self.draw.polygon(points, fill=PALETTE.get(color, color))

    def gear(self, x, y, tone='brass', large=False):
        r = 3 if large else 2
        self.box((x-r+1, y-r, x+r-1, y+r), 'outline')
        self.box((x-r, y-r+1, x+r, y+r-1), 'outline')
        self.box((x-r+1, y-r+1, x+r-1, y+r-1), tone)
        self.line([(x-r+1, y-r+1), (x+r-1, y-r+1)], tone + '_light')
        self.box((x, y, x, y), 'shadow')

    def plate(self, xy, tone='metal'):
        x, y, a, b = xy
        self.box(xy, 'outline')
        self.box((x+1, y+1, a-1, b-1), tone)
        self.line([(x+1, b-1), (a-1, b-1)], 'shadow')
        self.line([(x+1, y+1), (a-1, y+1)], 'light' if tone == 'metal' else tone + '_light')


def gun(kind):
    s = Sprite()
    long = kind in ('musket', 'blunderbuss', 'arquebus', 'clockwork_rifle')
    # An unfinished stock and exposed receiver, visibly missing its full barrel.
    if long:
        s.poly([(1, 11), (4, 8), (10, 5), (12, 6), (9, 9), (5, 10), (3, 14), (1, 14)], 'outline')
        s.poly([(2, 11), (5, 9), (10, 6), (10, 8), (4, 11), (3, 13), (2, 13)], 'wood')
        s.line([(2, 11), (5, 9), (9, 7)], 'wood_light')
        s.line([(3, 13), (4, 10), (8, 9)], 'wood_dark')
        s.plate((6, 5, 11, 8))
        s.line([(9, 4), (12, 1), (13, 1), (13, 3), (11, 5)], 'outline')
        s.line([(10, 4), (12, 2)], 'light')
        s.box((7, 6, 8, 6), 'shadow')  # open receiver
        s.box((5, 11, 6, 12), 'outline')
        if kind == 'blunderbuss':
            s.poly([(11, 1), (14, 1), (14, 4), (11, 5), (10, 3)], 'outline')
            s.line([(12, 2), (13, 2), (13, 4)], 'copper')
            s.box((8, 6, 9, 7), 'copper')
        elif kind == 'arquebus':
            s.gear(9, 7, 'brass')
            s.box((5, 9, 5, 10), 'brass_light')
        elif kind == 'clockwork_rifle':
            s.gear(8, 7, 'brass')
            s.box((11, 2, 13, 4), 'shadow')
            s.line([(12, 2), (13, 2)], '#8d7988')
            s.line([(3, 11), (4, 12)], 'brass')
            s.box((10, 9, 11, 10), 'red')
    else:
        s.poly([(3, 6), (6, 4), (12, 4), (13, 6), (8, 9), (6, 14), (3, 13), (4, 9)], 'outline')
        s.poly([(4, 7), (7, 5), (10, 5), (8, 8), (6, 9), (5, 13), (4, 12)], 'wood')
        s.line([(4, 7), (7, 5), (10, 5)], 'wood_light')
        s.line([(4, 12), (5, 13), (6, 10)], 'wood_dark')
        s.plate((6, 4, 12, 7))
        s.box((8, 5, 9, 6), 'outline')
        s.line([(11, 3), (14, 3), (14, 5)], 'metal')
        s.line([(6, 9), (8, 9), (8, 8)], 'shadow')
        if kind == 'flintlock':
            s.line([(5, 5), (4, 3), (6, 2)], 'outline')
            s.box((5, 3, 6, 3), 'light')
        elif kind == 'blackpowder_revolver':
            s.gear(8, 6, 'copper')
            s.box((8, 6, 8, 7), 'outline')
        else:
            s.gear(8, 6, 'brass', large=True)
            for p in [(7, 5), (9, 5), (7, 7), (9, 7)]:
                s.box((*p, *p), 'shadow')
    return s


def star(s, x, y, tone='star'):
    """A five-pixel plus-shaped star glint centred on (x, y)."""
    s.line([(x-1, y), (x+1, y)], tone)
    s.line([(x, y-1), (x, y+1)], tone)
    s.box((x, y, x, y), 'glint')


def hexerei_gun(kind):
    s = gun('musket' if kind == 'tactical_crossgun' else 'blunderbuss')
    if kind == 'royaltys_barrel':
        # Flared barrel with quartz studs and a glowing ember core.
        s.box((11, 2, 13, 4), 'ember')
        s.box((12, 3, 12, 3), 'glint')
        s.box((7, 8, 8, 8), 'quartz')
        s.box((4, 10, 4, 10), 'quartz')
    elif kind == 'star_cannon':
        s.box((11, 1, 13, 4), 'shadow')
        star(s, 12, 3)
        s.box((8, 8, 9, 9), 'mithril')
        s.box((2, 12, 2, 12), 'brass')
    elif kind == 'super_star_shooter':
        s.box((10, 1, 14, 5), 'nether')
        star(s, 12, 3)
        star(s, 8, 9, 'mithril')
        s.line([(1, 14), (3, 14)], 'brass_light')
    elif kind == 'tactical_crossgun':
        # Unstrung crossbar and steel limbs over a bare stock.
        s.line([(8, 2), (12, 6)], 'steel', 1)
        s.line([(12, 2), (8, 6)], 'steel', 1)
        s.box((10, 4, 10, 4), 'nether')
        s.box((5, 8, 6, 8), 'mithril')
    return s


def cog():
    s = Sprite()
    # A heavy steel cog with a dark netherite hub and a ring of teeth.
    s.box((6, 1, 9, 14), 'outline')
    s.box((1, 6, 14, 9), 'outline')
    s.box((2, 2, 13, 13), 'outline')
    s.box((3, 3, 12, 12), 'steel')
    s.line([(3, 3), (12, 3)], 'steel_light')
    s.line([(3, 3), (3, 12)], 'steel_light')
    s.line([(4, 12), (12, 12)], 'shadow')
    s.line([(12, 4), (12, 12)], 'shadow')
    s.box((5, 5, 10, 10), 'outline')
    s.box((6, 6, 9, 9), 'nether')
    s.box((7, 7, 8, 8), 'red')
    s.box((6, 6, 6, 6), 'mithril')
    for x, y in [(2, 2), (13, 2), (2, 13), (13, 13)]:
        s.box((x, y, x, y), (0, 0, 0, 0))
    for x, y in [(3, 3), (12, 3), (3, 12), (12, 12)]:
        s.box((x, y, x, y), 'outline')
    return s


def mechanism(kind):
    s = Sprite()
    if kind == 'simple_mechanical_components':
        s.poly([(2, 5), (10, 2), (14, 7), (11, 12), (4, 14), (1, 10)], 'outline')
        s.poly([(3, 6), (10, 3), (12, 7), (10, 11), (4, 12), (2, 9)], 'copper_dark')
        s.line([(3, 6), (10, 3), (12, 5)], 'copper_light')
        s.gear(6, 9, 'copper', True)
        s.line([(7, 5), (10, 7), (12, 7)], 'light')
        s.box((10, 9, 12, 10), 'outline')
        s.box((2, 12, 3, 13), 'metal')
    elif kind == 'mechanical_components':
        s.plate((2, 3, 13, 12))
        s.box((4, 5, 11, 10), 'outline')
        s.gear(5, 9, 'copper', True)
        s.gear(10, 5, 'brass')
        s.line([(7, 10), (10, 10), (12, 12)], 'red')
        s.line([(3, 2), (3, 3), (12, 3)], 'light')
        s.box((11, 13, 12, 14), 'metal')
    else:
        s.poly([(2, 4), (9, 1), (14, 5), (13, 12), (6, 14), (1, 10)], 'outline')
        s.poly([(3, 5), (9, 2), (13, 5), (12, 11), (6, 13), (2, 9)], 'brass_dark')
        s.line([(3, 4), (9, 2), (12, 4)], 'brass_light')
        s.gear(6, 9, 'brass', True)
        s.gear(10, 5, 'copper')
        s.line([(9, 10), (11, 10), (11, 8)], 'light')
        s.box((3, 5, 4, 6), 'outline')
        s.box((12, 13, 13, 14), 'brass')
    return s


def ammo(copper):
    s = Sprite()
    tone, highlight = ('copper', 'copper_light') if copper else ('metal', 'light')
    s.poly([(1, 10), (10, 6), (14, 9), (14, 12), (5, 15), (1, 13)], 'outline')
    s.poly([(2, 11), (10, 8), (13, 10), (5, 13)], tone)
    s.line([(2, 12), (5, 14), (13, 11)], 'shadow')
    for x, y in [(3, 4), (7, 3), (11, 2)]:
        s.box((x, y, x+2, y+6), 'outline')
        s.box((x+1, y+2, x+1, y+5), tone)
        s.box((x, y, x+2, y), highlight)
        s.box((x+1, y+1, x+1, y+1), 'outline')
    return s


def attachment(kind):
    s = Sprite()
    if kind == 'hair_trigger':
        s.plate((3, 2, 7, 5), 'copper')
        s.line([(6, 5), (10, 6), (11, 9), (9, 12), (6, 12)], 'outline', 3)
        s.line([(6, 5), (9, 6), (10, 9), (8, 11)], 'metal')
        s.box((3, 13, 4, 14), 'copper_light')
    elif kind == 'buffer_spring':
        s.line([(3, 3), (12, 12)], 'outline', 3)
        for x in (3, 6, 9):
            s.line([(x, x+3), (x+3, x), (x+4, x+1), (x+1, x+4)], 'light')
        s.plate((1, 1, 5, 4))
        s.box((11, 12, 14, 14), 'shadow')
    elif kind == 'gas_vent':
        s.plate((3, 2, 12, 12))
        for y in (4, 7, 10):
            s.box((5, y, 9, y), 'outline')
        s.line([(2, 5), (2, 11), (5, 14)], 'copper')
        s.box((11, 9, 13, 11), (0, 0, 0, 0))
    elif kind in ('mechanical_accelerator', 'mechanical_repeater'):
        tone = 'copper' if kind.endswith('accelerator') else 'brass'
        s.plate((2, 4, 13, 12))
        s.box((4, 6, 11, 10), 'outline')
        s.gear(5, 8, tone)
        s.gear(10, 6 if tone == 'brass' else 9, tone)
        s.line([(3, 3), (6, 1), (9, 3), (12, 1)], 'metal')
        if tone == 'brass':
            s.box((11, 12, 12, 14), 'brass_light')
        else:
            s.line([(1, 11), (3, 13), (6, 13)], 'copper_light')
    elif kind == 'scope_attachment':
        s.poly([(1, 10), (10, 1), (14, 5), (5, 14)], 'outline')
        s.poly([(3, 10), (10, 3), (12, 5), (5, 12)], 'copper')
        s.line([(3, 9), (9, 3)], 'copper_light')
        s.line([(5, 9), (9, 5)], 'shadow', 2)
        s.box((10, 2, 12, 4), 'blue')
        s.box((10, 2, 10, 2), 'glint')
        s.line([(7, 11), (10, 13), (12, 11)], 'metal')
    elif kind == 'bayonet_attachment':
        s.poly([(2, 13), (3, 9), (12, 1), (14, 1), (13, 5), (6, 12)], 'outline')
        s.poly([(5, 9), (12, 2), (13, 2), (12, 5), (6, 10)], 'metal')
        s.line([(5, 9), (12, 2)], 'glint')
        s.line([(2, 9), (7, 14)], 'shadow', 2)
        s.box((2, 12, 3, 14), 'wood')
        s.box((8, 10, 10, 12), 'copper')
        s.box((9, 11, 10, 12), (0, 0, 0, 0))
    elif kind == 'suppressor_attachment':
        s.poly([(2, 9), (10, 1), (14, 5), (6, 13)], 'outline')
        s.poly([(3, 9), (10, 2), (13, 5), (6, 12)], 'shadow')
        s.line([(4, 8), (10, 2)], 'light')
        for x, y in [(5, 9), (7, 7), (9, 5)]:
            s.line([(x-1, y-1), (x+2, y+2)], 'brass')
        s.line([(2, 12), (4, 14), (7, 14)], 'wood_dark')
    elif kind == 'gun_oil':
        s.box((6, 1, 9, 3), 'outline')
        s.poly([(5, 4), (10, 4), (12, 7), (12, 13), (3, 13), (3, 7)], 'outline')
        s.poly([(6, 5), (9, 5), (11, 8), (11, 12), (4, 12), (4, 8)], 'shadow')
        s.box((5, 10, 10, 12), 'oil')
        s.line([(5, 7), (5, 9)], 'light')
        s.box((8, 6, 10, 8), 'red')
        s.box((4, 14, 6, 14), 'metal')
    elif kind == 'chain_shot':
        for x, y in [(3, 3), (6, 6), (9, 9)]:
            s.box((x, y, x+3, y+3), 'outline')
            s.box((x+1, y+1, x+2, y+2), 'metal')
            s.box((x+2, y+2, x+2, y+2), (0, 0, 0, 0))
        s.plate((1, 9, 5, 14))
        s.plate((10, 1, 14, 6))
        s.line([(5, 11), (8, 11)], 'shadow')
    elif kind == 'hook_shot':
        s.line([(4, 14), (9, 9), (10, 4), (8, 2), (5, 3), (4, 6)], 'outline', 3)
        s.line([(4, 13), (8, 9), (9, 4), (8, 3), (6, 3), (5, 5)], 'light')
        s.line([(8, 9), (12, 8), (14, 5)], 'outline', 3)
        s.line([(9, 9), (12, 7), (13, 5)], 'metal')
        s.box((1, 11, 3, 14), 'copper')
    else:
        raise ValueError(kind)
    return s


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    previews = []
    for name in [*ITEMS, *HEX_ITEMS]:
        kind = name.removeprefix('incomplete_')
        if kind == 'warhog_cog':
            sprite = cog()
        elif name in HEX_ITEMS:
            sprite = hexerei_gun(kind)
        elif kind.endswith('bullet_batch'):
            sprite = ammo(kind.startswith('copper'))
        elif kind.endswith('components'):
            sprite = mechanism(kind)
        elif kind.endswith('_modifier'):
            sprite = attachment(kind.removesuffix('_modifier'))
        else:
            sprite = gun(kind)
        sprite.image.save(OUT / (name + '.png'), optimize=False)
        previews.append((kind, sprite.image))
    cols, width, height = 5, 220, 202
    sheet = Image.new('RGB', (cols * width, ((len(previews)+cols-1)//cols) * height), '#20232a')
    d = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=13)
    for i, (name, sprite) in enumerate(previews):
        x, y = (i % cols)*width, (i // cols)*height
        for a in range(16):
            for b in range(16):
                d.rectangle((x+46+a*8, y+12+b*8, x+53+a*8, y+19+b*8), fill='#30343c' if (a+b)%2 else '#393e46')
        sheet.paste(sprite.resize((128, 128), Image.Resampling.NEAREST), (x+46, y+12),
                    sprite.resize((128, 128), Image.Resampling.NEAREST))
        words = name.replace('_modifier', '').replace('_', ' ')
        lines, current = [], ''
        for word in words.split():
            if len(current + ' ' + word) > 24:
                lines.append(current)
                current = word
            else:
                current = (current + ' ' + word).strip()
        lines.append(current)
        for n, line in enumerate(lines):
            d.text((x+width/2, y+150+n*18), line, font=font, fill='#ede6d4', anchor='mt')
    sheet.save(ROOT / 'docs/workpiece-textures.png')
    print(f'Drew {len(previews)} distinct 16x16 sprites and docs/workpiece-textures.png')


if __name__ == '__main__':
    main()
