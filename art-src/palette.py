# palette.py <nut-run dir>
# Aligns all PixelLab pictures to the squirrel. Every group (a season, or things shared between seasons) gets one
# palette: a CORE of the squirrels' own most-used colours, plus colours picked from the group's pictures by median cut.
# Each picture is remapped onto its group's palette (no dithering). Play-area props also have their near-black
# outline pixels turned into a softer dark colour, closer to the squirrel's outline; backgrounds keep their darks.
# Always starts from the originals in art-src/, so it can be re-run or undone (copy art-src/ back to assets/).
import sys, os
from collections import Counter
from PIL import Image

root = sys.argv[1]
SRC, OUT = os.path.join(root, 'art-src'), os.path.join(root, 'assets')
CORE_N, GROUP_N = 20, 30
PROP_N = 24      # props get fewer tones of their own than backgrounds: flatter, closer to the squirrel's simple shading
CALM = {'bark': 2, 'other': 1}   # passes of the speckle filter: bark is the busiest
NEAR = 26   # a pixel only takes a squirrel colour if it's this close to it (sum of RGB differences); else its own group's nearest

def opaque(im):
    return [p[:3] for p in im.getdata() if p[3] > 128]

def calm(im, passes):
    # Speckle filter: each opaque pixel takes the most common colour among itself and its opaque neighbours (3x3),
    # which removes single-pixel noise but keeps edges and larger shapes.
    for _ in range(passes):
        src = im.copy(); ps, pd = src.load(), im.load(); W, H = im.size
        for y in range(H):
            for x in range(W):
                if ps[x, y][3] < 128: continue
                cnt = Counter(ps[i, j][:3] for i in range(max(0, x - 1), min(W, x + 2)) for j in range(max(0, y - 1), min(H, y + 2)) if ps[i, j][3] >= 128)
                c, n = cnt.most_common(1)[0]
                if n >= 3: pd[x, y] = c + (ps[x, y][3],)
    return im

# the core: the most used colours of the red and the grey squirrel
core = []
for name, k in (('squirrel-red', 12), ('squirrel-grey', 8)):
    cnt = Counter(opaque(Image.open(os.path.join(OUT, name + '.png')).convert('RGBA')))
    for c, _ in cnt.most_common(200):
        if all(sum(abs(a - b) for a, b in zip(c, d)) > 18 for d in core): core.append(c)   # skip near-duplicates
        if len(core) >= (12 if name == 'squirrel-red' else 20): break

# Still read for their colours, but no longer written: the game uses recoloured autumn crowns for these
# seasons and a recoloured summer bush for autumn instead (art-src/recolor.py, run at the end).
PALETTE_ONLY = {'crown-spring', 'crown-summer', 'crown-birch', 'bush-autumn'}
GROUPS = {   # name: (pictures, outline colour for props)
    'spring': (['bg-spring-hills', 'bg-spring-far', 'bg-spring-mid', 'crown-spring', 'branch-spring', 'bush-spring', 'leaf-spring'], (90, 46, 38)),
    'summer': (['bg-summer-hills', 'bg-summer-far', 'bg-summer-mid', 'crown-summer', 'branch-summer', 'bush-summer', 'leaf-summer'], (74, 42, 30)),
    'birch':  (['bg-birch-hills', 'bg-birch-far', 'bg-birch-mid', 'crown-birch', 'branch-birch', 'bark-birch', 'bush-birch', 'leaf-birch'], (74, 66, 56)),
    'autumn': (['bg-autumn-hills', 'bg-autumn-far', 'bg-autumn-mid', 'crown-autumn', 'crown-maple', 'branch-autumn', 'bush-autumn', 'leaf-autumn'], (74, 34, 22)),
    'winter': (['bg-winter-far', 'bg-winter-mid', 'crown-winter', 'branch-winter', 'bark-winter', 'bush-winter', 'leaf-winter', 'mushroom-bounce-winter'], (46, 52, 72)),
    'bark':   (['bark-oak'], (74, 42, 30)),
    'mushrooms': (['mushroom-small', 'mushroom-bounce'], (74, 42, 30)),
    'nuts':   (['nut-acorn', 'nut-walnut', 'nut-golden', 'nut-berries'], (74, 36, 24)),
}

# backgrounds and play-area props get separate palettes, so a few bark highlights aren't crowded out by big green hills
SPLIT = {}
for group, (names, outline) in GROUPS.items():
    bg = [n for n in names if n.startswith('bg-')]
    trees = [n for n in names if n.split('-')[0] in ('bark', 'crown', 'branch')]
    details = [n for n in names if n not in bg and n not in trees]   # bushes, sprigs, mushrooms, nuts: small bright bits
    if bg: SPLIT[group + ' backgrounds'] = (bg, outline)
    if trees: SPLIT[group + ' trees'] = (trees, outline)
    if details: SPLIT[group + ' details'] = (details, outline)
for group, (names, outline) in SPLIT.items():
    names = [n for n in names if os.path.exists(os.path.join(SRC, n + '.png'))]
    ims = {n: Image.open(os.path.join(SRC, n + '.png')).convert('RGBA') for n in names}
    is_props = not group.endswith('backgrounds')
    is_trees = group.endswith('trees')
    # smooth only the big tree parts; berries, blossoms, nut caps and mushroom spots are small on purpose
    if is_trees: ims = {n: calm(im, CALM['bark'] if n.startswith('bark') else CALM['other']) for n, im in ims.items()}
    # median cut over all the group's opaque pixels (laid out in one strip)
    px = [c for im in ims.values() for c in opaque(im)]
    strip = Image.new('RGB', (len(px), 1)); strip.putdata(px)
    picked = strip.quantize(colors=PROP_N if is_trees else GROUP_N, method=Image.Quantize.MEDIANCUT).convert('RGB')
    own = [c for c, _ in Counter(picked.getdata()).most_common()]
    cols = core + own
    dist = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
    cache = {}
    def nearest(c):   # the squirrels' colour if it's really close, otherwise the group's own nearest colour
        if c not in cache:
            k = min(core, key=lambda d: dist(c, d))
            cache[c] = k if dist(c, k) <= NEAR else min(own, key=lambda d: dist(c, d))
        return cache[c]
    for n, im in ims.items():
        out = Image.new('RGBA', im.size); po, pa = out.load(), im.load()
        prop = not n.startswith('bg-')
        for y in range(im.height):
            for x in range(im.width):
                if pa[x, y][3] < 128: continue
                c = nearest(pa[x, y][:3])
                if prop and c[0] * .3 + c[1] * .59 + c[2] * .11 < 32: c = outline   # near-black outline -> softer dark
                po[x, y] = c + (255,)
        if n not in PALETTE_ONLY: out.save(os.path.join(OUT, n + '.png'), optimize=True)
    print(f'{group}: {len(names)} pictures -> {len(cols)} colours ({len(core)} from the squirrels)')

# ---- tree parts: branch leaves come from the crowns, so a tree's leaves all look the same ----
import colorsys
def is_leaf(c):
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255); h *= 360
    return (45 <= h <= 190 and s > 0.22) or (s > 0.45 and v > 0.55) or ((h >= 300 or h <= 15) and s > 0.2 and v > 0.6)

def strip_leaves(path):
    # the branch picture without its own leaves: bark, twigs (and snow) stay
    im = Image.open(path).convert('RGBA'); px = im.load(); W, H = im.size
    for y in range(H):
        for x in range(W):
            if px[x, y][3] >= 128 and is_leaf(px[x, y][:3]): px[x, y] = (0, 0, 0, 0)
    for _ in range(3):   # leftover leaf outline specks
        for y in range(H):
            for x in range(W):
                if px[x, y][3] >= 128 and sum(1 for i, j in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                                              if not (0 <= i < W and 0 <= j < H) or px[i, j][3] < 128) >= 3: px[x, y] = (0, 0, 0, 0)
    im.save(path, optimize=True)

def clumps(crown_path, out_prefix, outline):
    # three leaf clumps cut out of a crown with an oval mask, outlined like the crown
    im = Image.open(crown_path).convert('RGBA'); W, H = im.size; px = im.load()
    for k, (fx, fy, rw, rh) in enumerate(((0.28, 0.5, 20, 14), (0.7, 0.45, 18, 13), (0.5, 0.3, 15, 11))):
        cx, cy = int(W * fx), int(H * fy)
        out = Image.new('RGBA', (rw * 2 + 3, rh * 2 + 3)); po = out.load()
        inside = lambda x, y: ((x - rw - 1) / rw) ** 2 + ((y - rh - 1) / rh) ** 2 <= 1
        for y in range(out.height):
            for x in range(out.width):
                sx, sy = cx - rw - 1 + x, cy - rh - 1 + y
                if inside(x, y) and 0 <= sx < W and 0 <= sy < H and px[sx, sy][3] >= 128: po[x, y] = px[sx, sy]
        filled = [[po[x, y][3] > 0 for x in range(out.width)] for y in range(out.height)]
        for y in range(out.height):
            for x in range(out.width):
                if filled[y][x] and any(not (0 <= i < out.width and 0 <= j < out.height) or not filled[j][i]
                                        for i, j in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))): po[x, y] = outline + (255,)
        out.crop(out.getbbox()).save(f'{out_prefix}-{k}.png', optimize=True)

# The branch pictures in art-src are already bare (branch-bare.png: the spring branch with its leaves taken off,
# also used for summer, autumn and, recoloured white, birch; branch-winter-bare.png). Their leaves are the
# cluster-*.png pictures, made by PixelLab from patches of each crown, so a tree's leaves all match.

# ---- green, birch and snowy crowns and clusters, and the autumn bush: recoloured from the finished assets ----
import subprocess
subprocess.run([sys.executable, os.path.join(SRC, 'recolor.py'), OUT, OUT], check=True)
