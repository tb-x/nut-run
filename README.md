# Nut Run

Two squirrels race through the treetops for nuts: your red squirrel against a grey one played by
the game. Whoever gathers more wins. Pixel art with a 1980s-style parallax forest: mountains, far
trees and near trees slide at different speeds, and the forest floor scrolls faster near the
bottom of the screen.

## How it plays

- Pick a level (new ones unlock as you win), tap the green play button, then "Three, two, one, go!"
- Tap anywhere and your squirrel goes there by itself: it runs along branches, climbs up trunks
  (and head-first down them) and leaps from branch to branch. Tap a nut to go straight for it.
  Tap a trunk and it climbs to that spot and hangs on there; a new tap while it's climbing turns it
  round straight away.
- Touching a nut grabs it; it flies up to your score at the top.
- Some nuts are in the trees at the start; more drop out of the treetops one by one.
- Nuts:
  - **Acorn**: 1 point.
  - **Big walnut**: 2 points.
  - **Golden acorn**: 3 points. It glows, and a voice calls out when one drops.
  - **Red berries**: no points, but whoever eats them zooms along at extra speed for 5 seconds,
    curled up in a spinning ball with afterimages and speed lines (and the music speeds up).
- A bouncing yellow arrow always marks the best nut to go for next (the quickest to reach, with
  bigger nuts counting extra). When that nut is off screen, a yellow pointer at the edge shows the way.
- The grey squirrel is slower than yours, stops to think between nuts, sometimes picks a farther
  nut, and dawdles more when it's ahead, so races stay close.
- While a squirrel waits it does little things now and then: grooms, yawns, sits up to look around
  or nibbles.
- When every nut is gathered, the end card shows both piles side by side. Win (or tie) and the
  next level opens; lose and it's "Grey wins this time. Try again!"
- From level 8 on, the grey squirrel plays rough: when it meets yours on a branch it punches it (a
  quick one-two jab and a comic "pow" burst), and sometimes it runs at your squirrel on purpose.
  Yours tumbles off the tree to the ground and sits dizzy for a moment, with stars going round its
  head and little birds tweeting; then it gets up and carries on (a tap while it's dizzy is
  remembered). The nuts you already have stay yours. Grey then waits at least 10 seconds before it
  can punch again, and stops to look pleased with itself first, so the race stays winnable.
- A friendly voice helps with learning English. It names the season and time of day, counts down,
  and says in simple sentences what the squirrels are doing: "The red squirrel is climbing up the
  tree.", "The grey squirrel is jumping.", "A nut is falling from the tree." It waits for a quiet
  moment before describing the next thing, so it doesn't talk all the time.
- Each season has its own cheerful music (Eleven Music), looping without a seam. It dips while the
  voice talks and plays a little faster during a speed boost. If a track can't load, a bouncy 8-bit
  tune made in the browser plays instead. The speaker button (top right) turns all sound off and on and is
  remembered.

### The twelve levels

| Level | Season | Trees | Nuts | New |
| --- | --- | --- | --- | --- |
| 1 | spring morning: blossom, flowers, drifting petals | 2 oaks | 10 acorns, all there at the start | learn to tap; grey is slow |
| 2 | summer noon: berry bushes, poppies, tall grass | 3 oaks | 14 | nuts drop from the treetops; walnuts; leaps between trees |
| 3 | afternoon in a birch wood: white trunks, ferns | 4 birches and oaks | 18 | a golden acorn |
| 4 | autumn sunset: orange, red and yellow trees, pink clouds, berry bushes, falling leaves | 5 oaks and maples | 20 | two golden acorns, berries |
| 5 | winter evening: snow, fir trees, snow-covered trees, snowmen, stars, snowfall | 6 firs and snowy trees | 24 | three golden acorns, bouncy mushrooms that throw you up high |
| 6 | summer night: moon, stars, fireflies, a darker forest | 5 oaks | 25 | more nuts, bouncy mushrooms in summer |
| 7 | spring rain: grey sky, rain, a rainbow | 6 oaks | 27 | three golden acorns, a quicker grey squirrel |
| 8 | winter night: northern lights, snow | 7 firs and snowy trees | 30 | the fastest grey squirrel, who punches you off the branches (on every level from here on) |
| 9 | foggy autumn morning: fog drifting through a grey-orange wood | 6 oaks and maples | 30 | two tall trees whose first branches are high up |
| 10 | birch wood at sunset: a big low sun, an orange sky, dandelion fluff | 7 birches and oaks | 32 | four berries |
| 11 | harvest moon: a summer night under a huge orange moon, fireflies | 7 oaks | 33 | five golden acorns, lots of walnuts |
| 12 | snowy dawn: pink snow, the sun coming up | 8 firs and snowy trees | 36 | the biggest wood of all |

Levels 6 to 12 reuse the pictures and music of the five seasons (`art` in `THEMES`) with their own
sky, light and weather: `worldTint` tints the trees (darker for the night, orange at sunset, pink at
dawn), `rainbow`, `aurora` and `fog` are drawn in code, `sunR`, `sunY`, `moonScale` and `moonTint` make
the big low sun and the harvest moon, and the fireflies, rain and dandelion fluff are drawn like the
falling leaves.

The grey squirrel gets a little quicker and smarter each level up to level 8. From level 9 it's a bit
slower again, because the punching already makes it harder: in test races, a player who waits a second
before each tap and sometimes picks a worse nut won about half the races on levels 8 to 11 and more on 12.

## Running it

Serve the folder, e.g. `python -m http.server 5212`, and open http://localhost:5212.
Works on phones in both orientations. Opened straight from disk it still works, but the browser
won't load the voice clips, so you hear the device's own voice instead.

## Tuning knobs

At the top of the script in `index.html`:

| Knob | What it does |
| --- | --- |
| `VIEW_MIN` | How many game pixels fit across the short side of the screen (smaller = bigger squirrels) |
| `WALK`, `CLIMB` | Squirrel run and climb speeds |
| `JUMP_DX`, `JUMP_UP` | How far a squirrel can leap sideways and up between branches |
| `BOUNCE_UP` | How high a bouncy mushroom throws a squirrel |
| `ZOOM`, `ZOOM_TIME` | Berries: speed boost and how long it lasts |
| `AI_AHEAD_SLOW` | How much longer grey dawdles when it's winning |
| `AI_EASE` | Makes grey slower and more thoughtful on every level (lower = easier) |
| `PUNCH_REACH`, `PUNCH_EVERY`, `PUNCH_CHASE` | Levels with punching: how close grey must be to punch you, the seconds it waits before it can punch again, and the chance it runs at you instead of a nut |
| `PUNCH_FPS`, `DIZZY_TIME` | How fast the punch plays; how long your squirrel sits dizzy after falling |
| `IDLE_TRICKS`, `IDLE_EVERY` | What a waiting squirrel does now and then, and how often |
| `PICK_DIST`, `TAP_NUT` | How close a squirrel must get to grab a nut; how close a tap must be to target one |
| `TAP_TRUNK` | How far beside a trunk a tap still counts as tapping the trunk |
| `VOICE_VOL`, `SFX_VOL` | Loudness of the voice and the beeps (the voice is evened out and gently compressed, and the music dips under it) |
| `NARRATE_GAP` | Seconds of quiet before the voice describes the next thing |
| `MUSIC_VOL`, `MUSIC_DUCK` | Loudness of the music, and how far it dips under the voice |
| `MUSIC_XFADE`, `MUSIC_ZOOM` | Seconds blended so each track loops smoothly; how much faster it plays during a boost |
| `CHIP_VOL`, `MUSIC_BPM`, `MUSIC_BPM_STEP` | The fallback 8-bit tune: loudness, tempo on level 1, and how much faster each level gets |
| `BG_GREY`, `BG_HAZE` | How much colour the background strips lose and how much haze they get, so the trees you play on stand out |
| `SUN_TOP` | The sun or moon stays at least this far below the top of the screen |
| `TIP_SHARE` | Branch tips of two trees closer than this share one leaf cluster instead of a mirrored pair |
| `CANOPY_SPREAD`, `CANOPY_DROP`, `CANOPY_SHADE` | How the treetops are filled out: two darker copies of each crown behind it, this far to the sides, this far down, this much darker |
| `THEMES` | Each season's colours: sky, clouds, hills, tree kinds, leaves, ground, bushes, decorations and what drifts in the air |
| `NUT_TYPES` | Points per nut |
| `LEVELS` | Per level: size, season, trees and branches, how many nuts and of which kinds, how often they drop, and the grey squirrel's `speed`, `think` (pause in seconds) and `mistake` (chance it picks a farther nut); `punch: true` turns on the punching |

Leaps between branch tips are worked out automatically from the trees, so a new level only needs
trees and branches.

## Credits

Pictures: made with [PixelLab](https://pixellab.ai) (the squirrels, nuts, trees, bushes, mushrooms, backgrounds and
moon). Voices: [elevenlabs.io](https://elevenlabs.io). Music: Eleven Music. The sky, ground and effects are drawn
in code; the beeps are made in the browser.

### Picture credits

All made on 2026-10-14 with PixelLab (trial account; PixelLab's terms let us use and share them
freely, with no attribution needed).

- `assets/squirrel-red.png`: one side-view squirrel (`create_character`, standard mode, cat
  quadruped template), one animation per row in 80x80 cells: idle (8 frames), running (6), jump
  (8) and eating (7) from PixelLab's templates, then custom (v3) animations: an early side-view
  climb (8, no longer used), leaping between branches (8), curled up spinning for the speed boost
  (8, the game uses the last 4 and turns them), an older from-behind climb (8, not used: its tail
  looked like two), then the climb the game uses, seen from behind with one tail and four legs
  reaching up (9; started from a from-behind pose made with `create_image_pixflux` and cut out of
  its bark background by a script), and three idle tricks: grooming (12, template "licking"),
  yawning (11, template) and sitting up to look around (8, custom).
  On 2026-10-19 three more rows were added for the punching levels, 8 frames each, made with PixelLab's
  `animate_image` from the squirrel's own side-view picture (custom character animations were
  failing that day): a one-two punch, being knocked flat, and a dizzy wobble. The frames are in
  `art-src/squirrel/`; `python art-src/squirrel-rows.py` (run from this folder) adds them to both sheets.
- `assets/squirrel-grey.png`: the same sheet recoloured to grey in a script (no extra generation);
  the three new rows take each colour's grey twin from the older rows.
- `assets/nut-acorn.png`, `nut-walnut.png`, `nut-golden.png`, `nut-berries.png`: one
  `create_image_pixflux` image each, trimmed to the picture.
- `assets/bush-spring.png` (blossom), `bush-summer.png` (red berries), `bush-birch.png` (fern),
  `bush-winter.png` (snowy evergreen),
  `mushroom-bounce.png` (a bouncy red toadstool, for any level without its own), `mushroom-bounce-winter.png` (the snowy one level 5 uses, standing in a snowdrift) and `mushroom-small.png` (a little
  brown pair on the ground): one `create_image_pixflux` image each, trimmed to the picture.
- Backgrounds, `assets/bg-<season>-hills.png`, `-far.png` and `-mid.png` (spring, summer, birch,
  autumn; winter has `-far` and `-mid` and keeps code-drawn mountains): one `create_image_pixflux`
  image each (400x160 or 400x300). PixelLab paints a sky behind them, so a script cut the sky out
  (flood fill or column scan from the top). The game shows each one next to its mirror image so it
  repeats without a seam, and tints the far ones towards the horizon colour. Most of the near strips
  are groves on a little island of ground, so the game fills the ground in all the way along (in the
  island's own colour) and nothing floats; then all the strips are greyed and hazed a little.
- `assets/moon.png`: the moon on the starry levels (one 48x48 `create_image_pixflux`, trimmed), with a
  faint glow drawn round it in code.
- Trees: `assets/bark-oak.png`, `bark-birch.png`, `bark-winter.png` (48x128 bark textures, stacked
  up each trunk with every other copy flipped), and the crowns `top-spring.png`, `top-summer.png`,
  `top-birch.png`, `top-autumn-a.png` (orange), `top-autumn-b.png` (red) and `top-winter.png`
  (a snowy fir top). Several of these came back as a whole tree, so a script kept only the crown.
  These smaller crowns are now only a fallback.
- Treetops: `assets/crown-autumn.png` (orange oak), `crown-maple.png` (red maple) and
  `crown-winter.png` (snowy fir): one big `create_image_pixflux` crown each (192x160 or so), cropped
  above the trunk by a script. Every other season's treetops are those two autumn crowns recoloured
  by `art-src/recolor.py` (no extra generation), so all the levels share the look of the autumn
  trees: `crown-<season>-a.png` (the oak shape) and `-b.png` (the maple shape) for spring (with
  blossom), summer and birch (birch wood turned white), and `crown-snow-b.png`, the snow-covered
  maple on winter's bare trees. Each tree's top is its crown in front of two darker copies set lower
  and to the sides (leaves only: the game clears their trunk and limbs, so there's still one trunk),
  so the canopy is full and comes down around the top branches. The first green
  crowns PixelLab made (`art-src/crown-spring.png` and so on) are now only used for their colours.
- `assets/bush-autumn.png`: the summer berry bush recoloured into autumn leaves by the same script
  (the PixelLab autumn bush, `art-src/bush-autumn.png`, looked like a tumbleweed).
- One palette with the squirrels: `art-src/palette.py` remaps every PixelLab picture (except the
  squirrels) onto a palette made of the squirrels' own 20 most-used colours plus about 30 colours
  picked from its group (each season's backgrounds, each season's trees and bushes, the oak bark,
  the mushrooms, the nuts). A pixel only takes a squirrel colour when it's already close to one, so
  wood stays wood. Play-area props also get their near-black outlines softened to a dark brown (cool
  dark blue in winter), closer to the squirrel's soft dark-red outline; backgrounds keep their darks.
  The trees (bark, crowns, branches) are also calmed: a speckle filter removes single-pixel noise
  (two passes on bark) and they get 24 tones of their own instead of 30, so they're flatter, like
  the squirrel's simple shading. Bushes, sprigs, mushrooms and nuts keep their small details.
  The untouched originals are in `art-src/`: change a picture there and run
  `python art-src/palette.py .` from this folder (then bump `ASSET_V`). `art-src/` isn't needed by
  the game itself.
- Branches: `assets/branch-spring.png`, `branch-summer.png`, `branch-birch.png` (white bark),
  `branch-autumn.png` and `branch-winter.png` (snow on top, fir needles below): one
  `create_image_pixflux` picture each (192x56, base on the left, tip on the right; the birch one is
  a second try). The game finds the line along the top of the bark, stretches each picture to the
  branch's length and lays it column by column along the line the squirrels run on, so they stand
  right on the bark. Each one gets a shaded collar where it grows out of the trunk (in its own bark
  colours), and a branch level with one on the other side of the trunk is lifted a little so the two
  don't look like one stick through it.
- Fir branches, `assets/branch-fir.png`: the autumn branch (the same natural twiggy shape as every
  other season) recoloured to the winter bark with snow along its top by `art-src/fir-branch.py`
  (no extra generation), with the fir tuft `cluster-winter.png` at its tip on the firs (the snowy trees' branches stay bare).
  It replaced a snowy log.
- Branch leaves that match the treetops: the branches are drawn bare (`art-src/branch-bare.png` is the
  spring branch with its leaves taken off, used for spring, summer, autumn and, recoloured white with
  dark marks and an outline, birch; winter uses its own snowy branch with the needles taken off), and
  the leaves are `assets/cluster-<crown>.png`: small leaf clusters PixelLab redrew from a patch of each
  crown, forced to that crown's own colours (`create_image_pixflux` with an init image and a colour
  image). Each branch gets one at its tip and long branches one more. The orange, red and fir
  clusters were cut from the crown's edge and trimmed to a rounded leafy shape by a script; the green
  and birch ones (`cluster-<season>-a.png` and `-b.png`) are those recoloured, to match their crowns.
- Leafy sprigs, `assets/leaf-*.png` (one per season): only used if a branch picture can't be read
  (e.g. when the game is opened straight from disk), on the code-drawn branches. 

### Audio credits

All spoken lines were made on **2026-10-14** with the ElevenLabs **Starter** (paid) plan:
voice "Jessica - Playful, Bright, Warm" (a stock ElevenLabs voice), model Eleven Multilingual v2,
speed 0.85, stability 0.6. Starter-plan audio may be used commercially; we credit
"elevenlabs.io" anyway. All of it was made by AI in a stock voice; no real person's voice was used.
The clips are here only as this game's own sounds: they are not licensed for anyone else to reuse,
and they are not covered by any licence that may later be put on this game's code.

`assets/say-*.mp3`, 50 clips:
- Levels: "Level one. It is spring. It is morning.", "Level two. It is summer. The sun is high.",
  "Level three. Look at the white trees.", "Level four. It is autumn. The leaves are orange.",
  "Level five. It is winter. Look at the snow and the stars!", "Level six. It is night. Look at the
  fireflies!", "Level seven. It is raining. Look, a rainbow!", "Level eight. It is a cold night. Look
  at the lights in the sky!" (the last three on 2026-10-14 too, same plan and settings), and on
  2026-10-20 (same plan, voice and settings) "Level nine. It is foggy. Can you see the trees?", "Level
  ten. The sun is going down. The sky is orange.", "Level eleven. Look at the big orange moon!" and
  "Level twelve. The sun is coming up. The snow is pink!"
- Countdown and help: "Three!", "Two!", "One!", "Go!", "Tap where you want to go!",
  "The red squirrel is waiting. Tap a nut!"
- What the squirrels do: "The red squirrel is running.", "… is climbing up the tree.",
  "… is climbing down the tree.", "… is jumping.", "Boing! The red squirrel is bouncing up.",
  "The red squirrel is eating berries. Now it is fast!", "The grey squirrel is climbing up the
  tree.", "… is jumping.", "The grey squirrel is eating berries. Now it is fast!",
  "A nut is falling from the tree.", "Look! A golden acorn is falling!"
- For the punching levels (made on 2026-10-19, same plan, voice and settings): "The grey squirrel punched
  the red squirrel!" and "Oh no! The red squirrel fell down. It is dizzy!"
- Naming the tree, now and then when your squirrel starts climbing: "The red squirrel is climbing an
  oak tree." / "a birch tree." / "a maple tree." / "a fir tree.", and on the bare winter trees
  "This tree has no leaves in winter. The red squirrel is climbing up."
- Grabbing nuts, with different verbs to learn (the game takes turns with them): "The red
  squirrel found / got / picked up / grabbed an acorn.", "The red squirrel found / picked up a big
  walnut.", "Wow! The red squirrel found a golden acorn!", "The grey squirrel found / got / picked
  up an acorn."
- The end: "You win!", "It's a tie!", "Grey wins this time. Try again!", "You won every level! Hooray!"

### Music credits

`assets/music-spring.mp3`, `music-summer.mp3`, `music-birch.mp3`, `music-autumn.mp3` and
`music-winter.mp3`: one 45-second instrumental track each, made on **2026-10-14** with Eleven Music
(model music_v2, instrumental only) on the ElevenLabs **Starter** plan, from a short description of
the season and instruments. The game loops each one by blending its last 2 seconds into its start.
Eleven Music's terms don't allow the tracks in games that are sold or make money in any way, so
**this game must stay free, with no ads or payments**. The tracks must not be offered for others to
download or reuse as a music library; they're here only as this game's own music.
All the words are in `LINES` in `index.html`; if you change one, regenerate its clip too.
