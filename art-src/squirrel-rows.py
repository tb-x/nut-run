# Adds the punch, knock and dizzy animations (art-src/squirrel/<name>-<i>.png, 68x68 PixelLab frames)
# as rows 12-14 of assets/squirrel-red.png, and the same rows recoloured into assets/squirrel-grey.png.
# The grey colours come from the first 12 rows: every red colour there already has its grey twin;
# a colour that's new in these frames takes the twin of the nearest known red colour.
# Run from the game folder: python art-src/squirrel-rows.py   (then bump ASSET_V)
from PIL import Image

CELL, OFF, BASE_ROWS = 80, 6, 12          # 68px frames sit 6px into each 80px cell, like the other rows
ROWS = [('punch', 9), ('knock', 9), ('dizzy', 9)]

red = Image.open('assets/squirrel-red.png').convert('RGBA')
grey = Image.open('assets/squirrel-grey.png').convert('RGBA')
W = red.width
red = red.crop((0, 0, W, BASE_ROWS * CELL)); grey = grey.crop((0, 0, W, BASE_ROWS * CELL))

twin = {}
rp, gp = red.load(), grey.load()
for y in range(red.height):
    for x in range(W):
        if rp[x, y][3]: twin[rp[x, y]] = gp[x, y]

def to_grey(c):
    if c[3] == 0: return c
    if c not in twin:
        near = min(twin, key=lambda k: sum((a - b) ** 2 for a, b in zip(k, c)))
        twin[c] = twin[near][:3] + (c[3],)
    return twin[c]

H = (BASE_ROWS + len(ROWS)) * CELL
out_r = Image.new('RGBA', (W, H)); out_g = Image.new('RGBA', (W, H))
out_r.paste(red, (0, 0)); out_g.paste(grey, (0, 0))
for r, (name, n) in enumerate(ROWS):
    for i in range(n):
        f = Image.open(f'art-src/squirrel/{name}-{i}.png').convert('RGBA')
        g = Image.new('RGBA', f.size); g.putdata([to_grey(c) for c in f.getdata()])
        at = (i * CELL + OFF, (BASE_ROWS + r) * CELL + OFF)
        out_r.paste(f, at); out_g.paste(g, at)
out_r.save('assets/squirrel-red.png'); out_g.save('assets/squirrel-grey.png')
print('sheets now', W, 'x', H)
