"""Draw the Modrinth banner and mod icon from the original workpiece sprites.

Requires Pillow. The title font, Rye (SIL Open Font License), is downloaded once
into the ignored .research directory; only the rendered PNGs are tracked.
"""
import math
import random
import urllib.request
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from generate_recipes import ROOT, MOD, ITEMS
from generate_textures import PALETTE, gun, mechanism, ammo, attachment

FONT_URL = 'https://github.com/google/fonts/raw/main/ofl/rye/Rye-Regular.ttf'
FONT = ROOT / '.research/fonts/Rye-Regular.ttf'
BG, BG_EDGE = '#2b211f', '#171211'
CREAM, INK = '#f3dfb2', '#1c1414'


def font(size):
    if not FONT.exists():
        FONT.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(FONT_URL, FONT)
    return ImageFont.truetype(str(FONT), size)


def sprite(name):
    kind = name.removeprefix('incomplete_')
    if kind.endswith('bullet_batch'):
        return ammo(kind.startswith('copper')).image
    if kind.endswith('components'):
        return mechanism(kind).image
    if kind.endswith('_modifier'):
        return attachment(kind.removesuffix('_modifier')).image
    return gun(kind).image


def backdrop(size):
    w, h = size
    image = Image.new('RGB', size, BG_EDGE)
    glow = Image.new('L', size, 0)
    ImageDraw.Draw(glow).ellipse((-w * 0.1, -h * 0.35, w * 1.1, h * 1.35), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(min(w, h) / 5))
    image.paste(Image.new('RGB', size, BG), mask=glow)
    return image.convert('RGBA')


def float_sprite(canvas, image, center, scale, angle, alpha=255):
    big = image.resize((16 * scale, 16 * scale), Image.Resampling.NEAREST)
    big = big.rotate(angle, Image.Resampling.NEAREST, expand=True)
    if alpha < 255:
        big.putalpha(big.getchannel('A').point(lambda a: a * alpha // 255))
    shadow = Image.new('RGBA', big.size, (0, 0, 0, 0))
    shadow.putalpha(big.getchannel('A').point(lambda a: a * 3 // 5))
    shadow = shadow.filter(ImageFilter.GaussianBlur(scale))
    x, y = center[0] - big.width // 2, center[1] - big.height // 2
    canvas.alpha_composite(shadow, (x + scale, y + scale * 2))
    canvas.alpha_composite(big, (x, y))


def title(canvas, text, center, size, fill=CREAM):
    f = font(size)
    d = ImageDraw.Draw(canvas)
    stroke = max(2, size // 14)
    d.text((center[0] + stroke, center[1] + stroke * 2), text, font=f, anchor='mm',
           fill=INK, stroke_width=stroke, stroke_fill=INK)
    d.text(center, text, font=f, anchor='mm', fill=fill, stroke_width=stroke, stroke_fill=INK)


def banner():
    w, h = 1500, 500
    canvas = backdrop((w, h))
    rng = random.Random(1873)
    keep_out = (310, 130, 1190, 380)  # title block
    placed = []
    names = list(ITEMS)
    rng.shuffle(names)
    for name in names:
        for _ in range(400):
            scale = rng.choice((5, 6, 7, 8))
            r = 8 * scale + 6
            x, y = rng.randint(r - 30, w - r + 30), rng.randint(r - 30, h - r + 30)
            inside = keep_out[0] - r < x < keep_out[2] + r and keep_out[1] - r < y < keep_out[3] + r
            if not inside and all(math.dist((x, y), p) > r + q for *p, q in placed):
                placed.append((x, y, r))
                float_sprite(canvas, sprite(name), (x, y), scale, rng.uniform(-24, 24),
                             255 if scale > 5 else 170)
                break
    title(canvas, 'Artifice', (w // 2, 205), 120)
    title(canvas, 'Create Recipes', (w // 2, 318), 76, PALETTE['brass_light'])
    return canvas.convert('RGB')


def gear_mask(size, teeth, outer, inner, tooth):
    """Pixel-grid gear silhouette, drawn aliased so it upscales as pixel art."""
    mask = Image.new('L', (size, size), 0)
    d = ImageDraw.Draw(mask)
    c = size / 2 - 0.5
    d.ellipse((c - inner, c - inner, c + inner, c + inner), fill=255)
    for i in range(teeth):
        a = 2 * math.pi * (i + 0.5) / teeth
        ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        d.polygon([(c + ux * r + vx * t, c + uy * r + vy * t)
                   for r, t in ((inner - 2, -tooth), (outer, -tooth), (outer, tooth), (inner - 2, tooth))],
                  fill=255)
    return mask


def icon():
    grid, scale = 64, 8
    base = Image.new('RGBA', (grid, grid), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((0, 0, grid - 1, grid - 1), 10, fill=PALETTE['outline'])
    d.rounded_rectangle((2, 2, grid - 3, grid - 3), 8, fill=BG)
    base.paste(PALETTE['outline'], mask=gear_mask(grid, 8, 29, 23, 5.5))
    base.paste(PALETTE['brass_dark'], mask=gear_mask(grid, 8, 27, 21, 3.5))
    base.paste(PALETTE['brass'], mask=gear_mask(grid, 8, 25.5, 19.5, 2.5))
    image = base.resize((grid * scale,) * 2, Image.Resampling.NEAREST)
    float_sprite(image, sprite('incomplete_flintlock'), (250, 262), 24, 0)
    return image


def main():
    docs = ROOT / 'docs'
    banner().save(docs / 'banner.png', optimize=True)
    art = icon()
    art.save(docs / 'icon.png', optimize=True)
    art.resize((128, 128), Image.Resampling.LANCZOS).save(
        ROOT / 'src/main/resources' / (MOD + '.png'), optimize=True)
    print('Drew docs/banner.png, docs/icon.png, and the packaged mod logo')


if __name__ == '__main__':
    main()
