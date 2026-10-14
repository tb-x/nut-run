# The fir branch: the autumn branch (the natural twiggy shape used in every season) in winter bark, with snow along its top.
# Usage: python art-src/fir-branch.py <assets dir>
import sys, random
from PIL import Image
A = sys.argv[1]; R = random.Random(7)
hx = lambda h: tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
MAP = {'916242': '6f8498', '855135': '51545c', '674132': '2e3448', '45232f': '172f4b', 'f2793d': '2e3448'}
src = Image.open(f'{A}/branch-autumn.png').convert('RGBA'); W, H = src.size
im = Image.new('RGBA', (W, H + 3), (0, 0, 0, 0)); im.paste(src, (0, 3)); px = im.load()
for y in range(H + 3):
    for x in range(W):
        p = px[x, y]
        if p[3]: px[x, y] = hx(MAP.get('%02x%02x%02x' % p[:3], '2e3448')) + (255,)
for x in range(W):
    ys = [y for y in range(H + 3) if px[x, y][3]]
    if not ys: continue
    y0 = ys[0]
    px[x, y0] = hx('e5f0f3') + (255,)                                    # snow lying on the bark
    px[x, y0 - 1] = hx('ffffff') + (255,)
    if R.random() < .45: px[x, y0 - 2] = hx('ffffff') + (255,)            # a few lumps
    if R.random() < .2 and y0 + 1 < H + 3 and px[x, y0 + 1][3]: px[x, y0 + 1] = hx('c8d9dd') + (255,)
im.save(f'{A}/branch-fir.png', optimize=True)
