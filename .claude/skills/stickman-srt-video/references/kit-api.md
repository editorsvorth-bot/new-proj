# kit.js API (all coordinates in the 1920 × 1080 world; `t` = absolute seconds)

**SRT clock**
- `cue(n)` start of cue n · `wordAt(n, phrase, lead = .1)` estimated time the phrase is spoken in cue n (throws if absent)
- `headlineWords(g, t, words[], times[], x, y, {size, red: [i], align})` headline whose words appear at their own times
- `NOW` set it at the top of every scene `draw` (`NOW = t`): drives blinks and tie sway

**Spine** (config in scenes.js: `GY`, `BAR {x,w,h}`, `SHARES`, `GROUP`)
- `spineBar(g, p, colours[], nums, labelAlphas[], {x,y,w,h, crack, grow, noLabels, labSize})`
- `miniBar(g, focusIndex, p, word?)` corner reprise, top-right

**People** (`F = {x, y, s, pose, facing, color, expr, seed, wear, alpha, draw}`; poses from the engine `POSES`)
- `person(g, F)` figure + wearables (`F.wear`: `cap`, `capBack`, `beanie`, `bucket`, `bun`, `specs`, or an array) + blinks
- `tieFigure(g, F)` / `salesman` helper with a red tie that sways · `phoneHolder(g, F, p)` / `sureBuyer` ticked phone in hand
- `pacing(x, t, i, amount)` → `{x, facing, pose}` restless on-the-spot motion (use `amount` .35 for ambient)
- `neckOf(F, r)` neck point of a drawn figure

**Props**
`browserWin(g, x, y, w, h, title, p, fn(x,y,w,h))` · `checkRow(g, text, x, y, p)` · `cart(g, x, y, s, p)` ·
`featureScroll(g, hx, hy, length)` · `featureCard(g, x, y, p, crossP)` · `briefcase(g, x, y, s, a)` ·
`shopBag(g, hx, hy, s, p)` · `emptyWallet(g, hx, hy, s, p, tip)` · `pitchBubble(g, x, y, s, colour, a)` ·
`qBubble(g, text, x, y, tailX, tailY, p, icon, alpha)` with icons `need`, `whom`, `use`, `when`, `else` ·
`stampX(g, x, y, r, p)` · `band(g, a, b, thickness, colour)`

**Thread (the clarity ending)**
Build `THREAD` points in `buildScenes` (see the example), then draw the knot up to the unravel front and a straight
line to the helper's hand (`threadPts` pattern in the example's scene 6); `knotPts`, `linePts`, `linePts2`, `KN`.

Engine helpers you will use most: `headline`, `subline`, `tag`, `speechBubble`, `thoughtBubble`, `badge`,
`crossMark`, `strokeOn`, `fillPoly`, `rrectPoly`, `tween`, `prog`, `E.*`, `walker`, `idle`, `poseMix`, `world`,
`dotGrid`, `groundLine`, `fadeAlpha`, `popAt` (see `assets/engine/engine-template.html`).
