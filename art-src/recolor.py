# Recolours the finished autumn crowns and clusters (oak = a, maple = b) into the green, birch and snowy seasons,
# so every level's trees share one look. Usage: python recolor.py <assets dir> <out dir> (palette.py runs it).
import sys, colorsys
from PIL import Image
SRC = sys.argv[1]; OUT = sys.argv[2]
WOOD = {'4a2216','45232f','916242','855135','674132'}
RAMPS = {
 'summer': ['b4e070','87c84c','4f9a3e','33803a','1f5e36','164939'],
 'spring': ['e8f882','bde55e','a1d865','67a757','247245','114446'],
 'snow':   ['ffffff','f2f6fc','dce6f2','bccbe0','90a6c2','64809e'],
 'birch':  ['f4f478','e9f054','bae139','9ad044','60a348','3e6e2a'],
}
def lum(c): return c[0]*.3+c[1]*.59+c[2]*.11
def run(name, ramp, out, blossom=None, seed=1):
    im = Image.open(f'{SRC}/{name}.png').convert('RGBA'); px = im.load(); W, H = im.size
    leaf = sorted({px[x,y][:3] for x in range(W) for y in range(H) if px[x,y][3] > 0 and '%02x%02x%02x' % px[x,y][:3] not in WOOD}, key=lum, reverse=True)
    R = [tuple(int(h[i:i+2],16) for i in (0,2,4)) for h in RAMPS[ramp]]
    m = {c: R[min(len(R)-1, round(i * (len(R)-1) / max(1, len(leaf)-1)))] for i, c in enumerate(leaf)}
    if ramp == 'birch':   # birch wood is white with dark marks, not brown
        for w, b in [('916242','e8e4d8'),('855135','cfc9ba'),('674132','aaa496'),('4a2216','4a4640'),('45232f','2e2a26')]:
            m[tuple(int(w[i:i+2],16) for i in (0,2,4))] = tuple(int(b[i:i+2],16) for i in (0,2,4))
    import random; rnd = random.Random(seed)
    for y in range(H):
        for x in range(W):
            p = px[x,y]
            if p[3] and p[:3] in m:
                c = m[p[:3]]
                if blossom and c in R[:2] and rnd.random() < .12: c = blossom[rnd.randrange(len(blossom))]
                px[x,y] = c + (p[3],)
    im.save(f'{OUT}/{out}.png')
for season in ['summer','spring','birch','snow']:
    bl = [(246,177,189),(255,214,226),(255,255,255)] if season=='spring' else None
    run('crown-maple', season, f'crown-{season}-b', bl, 2)
    if season == 'snow': continue   # winter's bare trees only need the snowy maple crown
    run('crown-autumn', season, f'crown-{season}-a', bl, 1)
    run('cluster-autumn', season, f'cluster-{season}-a', bl, 3)
    run('cluster-maple', season, f'cluster-{season}-b', bl, 4)

# The autumn bush: the summer berry bush in autumn leaves (the PixelLab autumn bush looked like a tumbleweed).
def bush_autumn():
    im = Image.open(f'{SRC}/bush-summer.png').convert('RGBA'); px = im.load(); W, H = im.size
    greens = ['a1ce49','9ecd45','499a4b','43964a','438d4c','16593d','0b4439','094038']
    ramp = ['fcf14b','f6d137','f1a728','f07d3b','d55b28','bd4f22','7a2a18','4a2216']
    m = {tuple(int(g[i:i+2],16) for i in (0,2,4)): tuple(int(r[i:i+2],16) for i in (0,2,4)) for g, r in zip(greens, ramp)}
    m[(240,80,111)] = (188,16,43)   # berries a deeper red so they show on orange
    for y in range(H):
        for x in range(W):
            p = px[x,y]
            if p[3] and p[:3] in m: px[x,y] = m[p[:3]] + (p[3],)
    im.save(f'{OUT}/bush-autumn.png')
bush_autumn()

# Small leaf bunches for the branches, cut from each finished crown so they match it: three puff shapes each,
# filled with a patch of the crown's leaves and outlined in the crown's own outline colour.
from collections import Counter
PUFFS = [[(7, 8, 6.5), (14, 6, 6), (19, 10, 5), (12, 12, 5.5)],
         [(6, 7, 5.5), (12, 9, 6.5), (8, 13, 4.5), (17, 11, 4)],
         [(8, 6, 5), (13, 9, 5.5), (6, 11, 4.5), (11, 14, 3.5)]]
def bunches(key):
    im = Image.open(f'{OUT}/crown-{key}.png').convert('RGBA'); px = im.load(); W, H = im.size
    op = lambda x, y: 0 <= x < W and 0 <= y < H and px[x, y][3] > 0
    edge = Counter(px[x, y][:3] for y in range(H) for x in range(W) if op(x, y) and not all(op(x + i, y + j) for i, j in ((1, 0), (-1, 0), (0, 1), (0, -1))))
    outline = edge.most_common(1)[0][0]
    wood = {tuple(int(w[i:i+2], 16) for i in (0, 2, 4)) for w in WOOD | {'e8e4d8', 'cfc9ba', 'aaa496', '4a4640', '2e2a26'}}
    # patches of solid leaves (no sky, no wood) from the upper part of the crown, lit from above
    spots = []
    for cy in range(10, int(H * .7), 3):
        for cx in range(13, W - 13, 3):
            box = [(x, y) for y in range(cy - 9, cy + 10) for x in range(cx - 12, cx + 13)]
            good = [(x, y) for x, y in box if op(x, y) and px[x, y][:3] not in wood]
            if len(good) >= len(box) * .97:
                L = sum(lum(px[x, y]) for x, y in good) / len(good); spots.append((L, cx, cy))
    leaves = Counter(px[x, y][:3] for y in range(H) for x in range(W) if op(x, y) and px[x, y][:3] not in wood)
    green = key.split('-')[0] in ('spring', 'summer', 'birch')   # leave blossom (pink, white) out of the shading steps
    ramp = sorted((c for c, n in leaves.items() if n > 20 and not (green and (c[0] > c[1] or lum(c) > 240))), key=lum, reverse=True)   # leaf colours, light to dark
    mid = ramp[len(ramp) // 2]
    spots.sort(reverse=True)
    picks = [spots[len(spots) // 5], spots[len(spots) // 3], spots[len(spots) // 2]]
    for k, (shape, (_, cx, cy)) in enumerate(zip(PUFFS, picks)):
        w, h = 26, 20; out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); po = out.load()
        inside = lambda x, y: any((x + .5 - a) ** 2 + (y + .5 - b) ** 2 <= r * r for a, b, r in shape)
        for y in range(h):
            for x in range(w):
                if inside(x, y):
                    q = px[cx - 12 + x, cy - 9 + y]
                    c = q[:3] if q[3] and q[:3] not in wood else mid
                    # the front-most circle this pixel is in (lower ones are in front), lit from the upper left
                    a, b, r = max((cc for cc in shape if (x + .5 - cc[0]) ** 2 + (y + .5 - cc[1]) ** 2 <= cc[2] ** 2), key=lambda cc: cc[1])
                    l = -((x + .5 - a) * .6 + (y + .5 - b)) / r
                    if c not in ramp and c in leaves and green: po[x, y] = c + (255,); continue   # a blossom stays as it is
                    i = ramp.index(c) if c in ramp else len(ramp) // 2
                    i = i - 2 if l > .55 else i - 1 if l > .2 else i + 2 if l < -.55 else i + 1 if l < -.2 else i
                    po[x, y] = ramp[max(0, min(len(ramp) - 1, i))] + (255,)
        filled = [[po[x, y][3] > 0 for x in range(w)] for y in range(h)]
        for y in range(h):
            for x in range(w):
                if filled[y][x] and any(not (0 <= i < w and 0 <= j < h) or not filled[j][i] for i, j in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                    po[x, y] = outline + (255,)
        out.crop(out.getbbox()).save(f'{OUT}/bunch-{key}-{k}.png', optimize=True)
for key in ['autumn', 'maple', 'spring-a', 'spring-b', 'summer-a', 'summer-b', 'birch-a', 'birch-b']: bunches(key)
