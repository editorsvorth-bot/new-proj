# Production playbook: raw script → finished stickman video

This is the exact sequence that produced an approved 90-second, 1920 × 1080 stickman explainer from a raw script. Follow the steps in order. Each step lists what to do, what it produces, and the checks that must pass before moving on. The numbers (coordinates, timings, sizes) are the values that worked; reuse them unless the format or script demands otherwise.

Nothing here is story content. Every idea, word and number in the video comes from the user's script ([script-fidelity.md](script-fidelity.md)), and every asset is drawn in code ([local-assets.md](local-assets.md)).

---

## Phase A: understand the script

### Step 1. Intake

1. Read the user's config block. Fill in missing fields with the defaults in SKILL.md (90 s, 16:9, 1920 × 1080, 30 fps, storyboard on, music on, SFX off, voiceover off, subtitles off).
2. If there is no script, ask for it and stop. Don't ask about anything else the defaults cover.
3. Exception: if the user asks for an *alternate take* of an existing video, ask one question only: keep the approved scene plan, or plan scenes fresh from the script.

**Output:** resolved config. **Check:** duration, size, fps, storyboard and audio switches are all known.

### Step 2. Split the script into idea units

1. Read the whole script once, end to end, before writing anything.
2. Cut it into idea units: one concept, definition, category, step, example, question or conclusion each. Keep the script's order.
3. For each unit, note:
   - a short excerpt in the script's own words (any language),
   - the plain-English meaning,
   - anything the script explicitly compares it to (metaphor, analogy, example), since only those may be drawn as metaphors,
   - any number it states,
   - any caveat it states (e.g. "approximate", "varies").
4. Ignore production tags in the script (segment-type notes like "talking head" or "AI video"). Animate every segment.
5. List things the script mentions but doesn't name or define (e.g. "a sequence of N stages" where only some stages are named). These appear on screen as numbers or unlabeled shapes only.

**Output:** idea-unit list. **Check:** nothing on the list is missing from the script, and nothing in the script is missing from the list.

### Step 3. Write the on-screen words

For each unit, write the only text that may appear on screen:

- **Headline** (2–6 words, uppercase): the unit's key claim, translated faithfully into English from the script's wording. Pick **one key word** in it for red.
- **Sublines** (≤ 8 words each, at most 3 per scene): supporting phrases from the script.
- **Labels and tags** (1–4 words): names of parts, categories, verdicts.
- **Question bubbles**: when the script lists someone's doubts or questions, each becomes one bubble, worded as that person's question.
- **Caveat**: if the script says the numbers are approximate, carry that as a small gray footnote.

**Check:** next to every string, write the excerpt it comes from. Delete any string without one.

---

## Phase B: design the video

### Step 4. Choose the spine object

Pick **one visual structure that represents the script's core idea** and carries through the whole video, changing state instead of being replaced. This continuity is what makes the result feel like one designed piece instead of slides. Match it to the script's shape:

| Script shape | Spine object that worked |
|---|---|
| A whole divided into shares/categories | A container that stretches into a proportional bar; figures stand on their share (one figure = one unit) |
| An ordered sequence of stages | Labelled blocks rising from the ground as a staircase, each step higher and lighter (fading) |
| Something blocking progress between two stages | A gap/pit between two blocks, coloured red, labelled with the script's name for the problem |
| The answer/solution to that blockage | The problem shape **morphs** into the solution shape (pit floor lifts into a bridge/ramp) and figures cross it |
| A comparison | Side-by-side groups; the contrast carried by colour (red vs ink vs gray) |
| A metaphor the script states | Drawn literally as a small set: a simple prop plus a sign; the figure reacts to it |

End by **reprising the spine object** with the answer highlighted in red (a small callback bar or diagram), not with a generic end card.

### Step 5. Cast the figures

- **One red hero figure per topic segment**: the person the script is currently talking about.
- **Groups in ink**, sized by the script's proportions when it gives numbers (e.g. one figure per 10%).
- **Gray** for inactive, past or background figures and objects.
- **Faces carry the script's feelings**: neutral → surprised → confused → happy/sad, changing on the beat where the script states the feeling.
- **A small identifying prop** when the script defines a group by a trait (drawn in ink on or near the figure).
- **Vary poses inside groups** (alternate `shrug`/`think`, `stand`/`cheer` by index) so figures never look cloned.

### Step 6. Scene plan and timeline

1. Group the idea units into **5–7 compositions** for 90 s (scale linearly for other lengths).
2. Budget the time by script weight. This split worked for a script with an intro, three topic segments and a payoff:
   - **Opening (concept + structure): about 20%.** Introduce the spine object and the whole structure, and hold it for reading.
   - **Each topic segment: about 10–12% per sub-scene,** usually two sub-scenes (a metaphor or evidence scene, then a "where it sits on the spine" scene).
   - **Payoff: about 35%,** the longest scene. Problem builds, then problem → solution morph, then everyone resolves, then a final hold.
3. Overlap consecutive scenes by **0.6 s** and give the incoming scene an `enter` mask of **0.9 s**.
4. Alternate transitions: `iris` from the exact point the next idea grows out of, then `wipe` for a change of topic. Never use the same one twice in a row.
5. End with a **2–3 s hold** on the final resolved frame plus the callback.

**Output:** a table with scene id, start, end, enter, the units it covers, and its beats.

### Step 7. Beat choreography inside a scene

Use this local-time skeleton (seconds from the scene start) and adjust it to the content:

| Local time | Beat |
|---|---|
| 0.0–0.9 | Enter mask opens; the camera settles from z 1.06–1.1 to 1.0 by about 2.2 s |
| 0.6–1.6 | Headline rises word by word (`headline`, red key word) |
| 0.7–2.6 | Main object or set builds (blocks rise, props drop in, staggered 0.12–0.25 s each) |
| 1.4–5.0 | Hero figure walks in (`walker`, entry segment eased `E.out`) or builds on (`draw`) |
| 4–7 | Reaction or action: pose change, expression change, thought or question bubble, tick or cross draws on |
| 5–7 | Sublines in, one per 0.6 s |
| 7–9 | Verdict tags pop (ink first, red last) |
| last 1.5 s | Hold, or a camera drift toward the next scene's iris point |

Rules: every completed state holds for **≥ 1.5 s** before it changes. Reveal windows are **0.5–1.0 s**. The red focus moves to the new element, and the old one returns to ink or gray.

### Step 8. Layout grid (1920 × 1080)

| Zone | Values |
|---|---|
| Ground line | y = 860 |
| Kicker (small gray label) | x 140, y 150, label 30 px |
| Headline | x 140, baseline y 190–230, 60–100 px (80 standard; reduce for long headlines so they end before x ≈ 1250) |
| Sublines | x 140, y 262 / 312 / 362, 36–44 px |
| Big answer word | x 140, y ≈ 446, 120 px red |
| Verdict tags | top-right x ≈ 1400, y 150–290, or bottom y ≈ 965 when the bottom is empty |
| Footnote/caveat | centred, y 960–1000, 30 px gray |
| Safe margin | 96 px on every edge |

Figure geometry: feet to head centre ≈ **298 × s** px, head top ≈ **334 × s** px above the feet. Scales: hero on ground 1.15–1.3; figures standing on blocks 0.8–0.95; group members 0.5–0.75.

Labelled blocks: width ≥ **230**, height step **110** for a staircase, number 48 px plus label 21 px in the top band (`labelBlock`).

Keep text zones and illustration zones apart. **Before placing a tag, compute the head-top line of every figure under it.**

---

## Phase C: build

### Step 9. Project files

```
<project>/<VIDEO NAME>/scenes.js            ← the only file you edit (keep it here, never only in the scratchpad)
<project>/<VIDEO NAME>/<video>.html         ← full standalone page (from build.py --out)
<scratchpad>/<video>.html                   ← Artifact copy (from build.py --artifact); disposable
```

- Keep `scenes.js` in the project folder. The scratchpad can be wiped between sessions, and the scenes file is what every later revision is built from.
- The output HTML must sit **inside the project folder** so the browser pane can run it (files outside render as static snapshots).
- For an alternate take, use a sub-folder with its own `scenes.js` (`<VIDEO NAME>/<take>/`).
- If a scenes file is ever lost, recover it from the built HTML: it is everything between the `SCENES` banner comment and `/* ================= renderAt`.

### Step 10. Write the scenes file

The scenes file holds only:

```js
let SCENES = [], CUES = [], SFX_CUES = [], STORYBOARD = [];
// project constants (ground y, block sizes, labels taken from the script)
// project-only drawing helpers (props unique to this script)
function buildScenes() {
  // 1. precompute geometry & morphs once (makeMorph, svgPoly, parametric rrect tweens)
  // 2. SCENES = [{ id, start, end, enter, camera(t,T), draw(g,t,T,c) }, ...]
  // 3. STORYBOARD = [{ t, title }]   one representative time per composition
  // 4. MUSIC.bpm / MUSIC.prog / MUSIC.accents   (biggest reveals, absolute seconds)
  // 5. SFX_CUES / CUES   only if enabled
}
```

Inside each `draw`:

1. `dotGrid(g, c)` for the background.
2. `world(g, c, () => { … })` for everything that lives in the scene: ground, blocks, props, figures, bubbles. The camera moves these.
3. After `world`, the screen-space text: headline, sublines, tags, footnote. The camera doesn't move it.
4. Time every element with `prog(t, a, b)` windows. Nothing may depend on the previous frame.

Reuse the engine helpers: `walker`, `idle`, `poseMix`, `drawStickman`, `thoughtBubble`, `speechBubble`, `labelBlock`, `flagTick`, `badge`, `crossMark`, `tag`, `headline`, `subline`, `leaderLabel`, `fadeAlpha`, `popAt`, `fillPoly`, `strokeOn`, `rrectPoly`, `makeMorph`. Don't redeclare engine names with `const`/`let`.

Morph rules:
- **Rounded rect → rounded rect:** interpolate the parameters, `rrectPoly(...mix([x,y,w,h,r], [x2,y2,w2,h2,r2], p))`.
- **Quadrilateral → quadrilateral** (pit → ramp): give both shapes the same number of points in the same order and `mix` the point arrays.
- **Unrelated outlines:** use `makeMorph(a, b)`, precomputed once.
- **Figures riding a morphing surface:** compute their y from the same blend, e.g. `y = lerp(yBefore(x), yAfter(x), m)`.

### Step 11. Build

```bash
python "<skill>/assets/build.py" --scenes "<project>/<VIDEO NAME>/scenes.js" --out "<project>/<VIDEO NAME>/<video>.html" --artifact "<scratchpad>/<video>.html" --title "<Short Name>" --file-name <short-name> --duration 90 --mode storyboard --music on --sfx off
```

Use `--mode player` once the storyboard is approved, or straight away when the storyboard is disabled.

---

## Phase D: check, approve, finish

### Step 12. Visual QA grid (one pass per build)

1. Open the local file in the browser pane (`file:///…/<video>.html`) and set the viewport to 1280 × 800.
2. Run this in the page to draw a grid of timestamps with the production `renderAt`:

```js
window.__grid = (ts) => {
  const wrap = document.getElementById('wrap'); document.getElementById('stage').style.display = 'none'; document.getElementById('bar').style.display = 'none';
  let grid = document.getElementById('qa'); if (grid) grid.remove();
  grid = document.createElement('div'); grid.id = 'qa'; grid.style.cssText = 'display:grid;grid-template-columns:repeat(3,1fr);gap:6px'; wrap.prepend(grid);
  const errs = [];
  for (const t of ts) { const c = document.createElement('canvas'); c.width = 624; c.height = 351; c.style.width = '100%';
    try { renderAt(t, c.getContext('2d')); } catch (e) { errs.push(t + ': ' + e.message); } grid.append(c); }
  window.scrollTo(0, 0); return errs;
};
__grid([/* 6 timestamps */]);
```

3. Choose timestamps that cover: each scene's resting state, each morph **midpoint**, each transition **midpoint**, each walk-in at its **start**, and the final frame. Take one screenshot per grid of 4–6 frames.
4. Fix only what this catalogue names (these are the failures that actually occurred):

| Symptom | Fix |
|---|---|
| Tag/label overlaps a figure's head | Move the tag above the head-top line (ground − 334 × s) or into the free top zone |
| Cross/mark hides a block's label | Smaller radius, placed over the label-free part of the block |
| Group figures overlap | Spacing ≥ 100 × s px for arms-out poses, ≥ 84 × s otherwise; widen the surface or reduce s |
| Mid-morph shape looks like a blob or octagon | Switch to a parametric or same-point-count morph (Step 10) |
| Figures still off-screen halfway through a walk-in | Ease the entry segment `E.out`; start ≤ 900 px off-screen |
| Camera push makes the art collide with screen-space text | Remove the push in that scene, or fade the headline out before pushing |
| Block labels unreadable | Blocks ≥ 230 px wide, label in the top band at 21 px |
| A bottom tag lands on the illustration | Move it to the top-left kicker area or top-right tag zone |
| A group looks cloned on arrival | Alternate poses by index |
| A blank cream frame mid-transition | Expected only while the iris opens before the new scene's first element. Otherwise start the scene's first build at 0.6–0.8 s local |

5. Rebuild and re-grid **only the affected timestamps**. Stop after one fix pass. Small aesthetic tweaks are for the user to ask for.

### Step 13. Storyboard stop (storyboard enabled only)

1. Build with `--mode storyboard` and confirm the contact sheet shows every `STORYBOARD` frame (`document.querySelectorAll('.sbCell').length`).
2. Publish the Artifact copy (no capabilities needed): `icon: "film"`, a one-sentence description, `label: "Storyboard v1"`.
3. Reply with the storyboard table (columns from [storyboard-stage.md](storyboard-stage.md)) and the link, and end with exactly:

   > Storyboard ready. Review the visual previews and reply APPROVED to generate the animation, or tell me what you'd like to change.

4. On requested changes, edit only those scenes, rebuild, re-grid, and republish **the same file path** (same URL).

### Step 14. Full animation

1. Rebuild with `--mode player`.
2. Re-run the QA grid on transition and morph midpoints (Step 12).
3. Confirm the console has no errors and the audio buffer rendered (`mixBuf.duration` equals the duration).

### Step 15. Export test (once)

In the browser pane, on the local file:

```js
for (let i = 0; i < 40 && !mixBuf; i++) await new Promise(r => setTimeout(r, 500));
window.__t0 = performance.now(); document.getElementById('export').click();
```

Then poll in separate calls of **≤ 40 s** each (a page-script call times out at 45 s):

```js
await new Promise(r => setTimeout(r, 40000)); ({ status: document.getElementById('status').textContent, dl: document.getElementById('dl').textContent })
```

- **Success** means status `MP4 ready (1920×1080, 30 fps, with audio).` and a link showing the file size.
- The pane has no WebCodecs, so it records in real time, taking about as long as the video plus about 10 s. In desktop Chrome/Edge the frame-exact WebCodecs route runs instead.
- Don't try to extract the file from the pane. The user downloads it from the published page.

### Step 16. Publish the final

Publish the Artifact copy with `capabilities: {downloads: true}`, so the page's Download Video button can save the MP4 (a published page can't start a download itself). Use `icon: "film"` on the first publish, a one-sentence description and a label such as "Final v1".

- Same file path → updates the same URL.
- An alternate take → a different file path → its own URL, leaving the original untouched.
- Also tell the user which full HTML file is saved in the project folder.

### Step 17. Delivery message

Keep it short:

1. The link (and the earlier version's link if this is an alternate take).
2. How to get the MP4: open the link → **Export Video** → wait for "MP4 ready" → **Download Video** → confirm the save.
3. What was verified: duration, resolution, fps, audio present, and the export route used (real-time recording can drop an occasional frame).
4. Any on-screen wording that is new compared with an earlier version, each with its script source.
5. The local HTML path.

### Step 18. Revisions

Edit the scenes file → rebuild → re-grid the affected timestamps → republish the same path. Never rebuild scenes the user didn't ask to change.
