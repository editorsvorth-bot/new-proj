# The 20-20-60 Split: production flow (gen-stickman-v2, SRT-timed)

This is the kit's playbook applied to `20-20-60.srt`, with one addition: **the SRT is the master clock**.
Every scene opens fully on a cue start, and every reveal is written as `cue(n) + offset`.

## 1. Config (resolved)

```
gen-stickman-v2
Script: 20-20-60.srt (24 cues, Tanglish)
- Storyboard: Enabled          (stop for APPROVED before Stage 2)
- Voiceover: Enabled           (Sequence_02.mp3: 103.687 s decoded, ending exactly where the SRT ends, so the cues are already in sync)
- Subtitles: Disabled          (CUES are already filled from the SRT; switch on with --subtitles on)
- Duration: the voiceover length (103.687 s decoded; the MP3 container reports 103.728 s with padding)
- Format: Horizontal 16:9, 1920 × 1080, 30 fps
- Background music: Disabled   (the voiceover already carries a music bed: it never drops below about -24 dB)
- Sound effects: Enabled (46 cue-locked SFX: pops, clicks, whooshes, thuds, chimes)
- Final video: MP4
```

## 2. SRT sync (the addition to the kit)

1. `python tools/srt_sync.py videos/20-20-60-split/20-20-60.srt videos/20-20-60-split/scenes.js`
   writes `C` (cue start times) and `SRT_TEXT` into the scenes file. Re-run it if the SRT changes.
2. In `scenes.js`, `cue(n)` = start of cue n. Times are never typed as raw numbers.
3. Scene k starts at `cue(first) − 0.7 s` with a 0.7 s iris or wipe, so it is **fully open on its cue**.
   The previous scene ends on that same cue.
4. Build with `--duration` set to the voiceover length (103.728), or the SRT end if there is no voiceover.

## 3. Idea units → on-screen words (Rule 1: script only)

| Cue | Time | Script (excerpt) | Meaning | On-screen words |
|---|---|---|---|---|
| 1 | 0:00.0 | Idha konjam diagrammatic-ah explain panren | Let me explain with a diagram | *Let me explain it with a diagram* |
| 2 | 0:02.4 | 20-20-60 split-nu solluvaanga | It's called the 20-20-60 split | **THE 20-20-60 SPLIT** · 20% 20% 60% |
| 3 | 0:04.9 | first 20 percentage … Never Buy | First 20% are Never Buy | **20% NEVER BUY** |
| 4 | 0:10.5 | yen inga irukkaanga-nu avangalukkum theriyaadhu, namakkum theriyaadhu | Neither they nor we know why they're here | **WHY ARE THEY HERE?** *They don't know. We don't know.* · US |
| 5 | 0:13.8 | need irukkaadhu, pay panna mudiyaadhu | No need, can't pay | **NO NEED. CAN'T PAY.** |
| 6 | 0:16.8 | evlo kashtappattu sell pannaalum … vaanga maattaanga | However hard we sell, they won't buy | **THEY WON'T BUY** *However hard we sell* |
| 7 | 0:21.5 | efforts poduradhu … waste of time; sales thevaiye kidaiyaadhu | Effort is wasted; no sales needed | **SALES? NOT NEEDED.** *Our effort here = waste of time* |
| 8 | 0:26.4 | innoru 20 percentage … Definitely Buy | Next 20% are Definitely Buy | **20% DEFINITELY BUY** |
| 9 | 0:29.6 | Amazon purchasers maadhiri | Like Amazon buyers | **LIKE AN AMAZON BUYER** · AMAZON (text only, no logo) |
| 10 | 0:35.0 | vaangurom—cart-la podrathu kidaiyaadhu … decide pannuvom, product-ah paappom | Really buy, not cart; decide; look at it | *Really buying, not just adding to cart* · DECIDE: I WANT IT · SEE THE PRODUCT |
| 11 | 0:39.8 | search, description, details, features | They check everything | SEARCH · DESCRIPTION · DETAILS · FEATURES |
| 12 | 0:44.8 | nallaa irukkaa, purchase pannittu | It's good → purchase, done | PURCHASE · *Looks good → purchase → done* |
| 13 | 0:48.0 | Adhe maadhiri … namma website, namma enna sell panrom | Same with us: about us, our website, what we sell | **SAME WITH US** *They check everything about us* · OUR WEBSITE · ABOUT US · WHAT WE SELL |
| 14 | 0:52.5 | namma dhaan venum … decide pannittu … lead-ah vandhiruppaanga | Decided they want us; come as a lead | DECIDED ON US · **THEY COME AS A LEAD** · LEAD |
| 15 | 0:58.0 | features-ah kashtappattu sell pannanum … avasiyamum kidaiyaadhu | No need to hard-sell features | **NO NEED TO SELL FEATURES** · FEATURES (crossed out) |
| 16 | 1:03.2 | Enna irukku, evlo-nu sonnaa podhum, kandippaa vaangirvaanga | Say what it is and how much; they'll buy | **THEY'LL SURELY BUY** *Just say what it is and how much* · WHAT IT IS · HOW MUCH · DEFINITELY BUY |
| 17 | 1:08.5 | 60 percentage … Confused Buyers | 60% are Confused Buyers | **60% CONFUSED BUYERS** · NEVER BUY · DEFINITELY BUY · CONFUSED BUYERS |
| 18 | 1:13.4 | need irukkaa illaiyaa, yaarukitta vaanguradhu | Do I need it? From whom? | *Do I need it?* · *Buy it from whom?* |
| 19 | 1:18.4 | use pannuvaangalaa maattaangalaa | Will they use it? | *Will I use it?* |
| 20 | 1:21.5 | ippo … illa future-la … vera edhaavadhu | Now or later? Something else? | *Now or later?* · *Or something else?* |
| 21 | 1:25.8 | multiple confusions … decision making-la help thevaippadum | Many confusions; need help deciding | **SO MANY CONFUSIONS** *They need help to decide* |
| 22 | 1:30.6 | yaaraavadhu help pannaa mattum dhaan … decide panna mudiyum | Only with help can they decide | **ONLY WITH HELP** *can they decide what they need* · US |
| 23 | 1:36.2 | Ivangalukkaaga dhaan sales … exist aagudhu | This is why sales exists | **THIS IS WHY SALES EXISTS** |
| 24 | 1:39.5 | confusion-la irukkavangalukku clarity kodutthu, decision making-la help | Clarity for the confused, help to decide | CLARITY · DECISION · *Clarity for the confused. Help to decide.* · SALES |

The salesperson is the script's *namma* (we/us), labelled **SALES** (the script's own word). No number, fact, example or analogy appears that the script doesn't state.

## 4. Design

- **Spine object:** one bar under ten buyers (1 figure = 10%), split 20 | 20 | 60. It opens the video, returns
  full-size at cue 17, and stays as a small corner reprise with the active group in red (ending with **SALES** on the 60%).
- **Cast:** the group being talked about is a **red** hero; inactive groups are **gray**.
  - **SALES:** ink figure with a **red tie** and a SALES pill.
  - **Never Buy:** pockets turned inside out ("can't pay"), arms crossed, turns their back when pitched ("won't buy").
  - **Definitely Buy:** phone in hand with a ticked screen (researched online, arrives decided).
  - **Confused:** paces on the spot, turns left/right, alternates head-scratch and shrug.
- **Wearables (drawn in code):** SALES has a red tie and a briefcase. Never Buy wears a bucket hat or backwards cap.
  Definitely Buy wears glasses and leaves with a shopping bag. The Confused crowd mixes beanies, caps and hair buns (`WEAR` in scenes.js).
- **Camera:** push into the two-shot during the pitch (cue 6), track the walk to SALES (cue 14), track along the questions (cues 18–20),
  push in on the pull (cue 23), then pull back for the resolution (cue 24).
- **Props (drawn in code):** a browser window (AMAZON, then OUR WEBSITE) with a ticking checklist, a FEATURES card
  that gets crossed out, and a tangle of confusion that straightens into an arrow.
- **Faces carry the script's feelings:** confused on cue 4 and cues 17–22, sad when effort is wasted (cue 7), happy on purchase and clarity.

## 5. Scene plan on the SRT clock

| Scene | Opens (fully) → ends | Cues | Composition | Beats (all on the cue named) | Transition in |
|---|---|---|---|---|---|
| 1 split | 0:00.0 → 0:10.5 | 1–3 | Row of 10 buyers on the spine bar | c1 walk in + gray line · c2 bar grows, 20/20/60, headline · c3 first 2 turn red, others gray, camera pushes left | — |
| 2 never | 0:10.5 → 0:26.4 | 4–7 | Red buyer vs US, two-shot | c4 both shrug + red ? · c5 buyer "stop" palm · c6 SALES walks in offering; 3 product bubbles bounce off the raised palm and drop gray; buyer turns away, arms crossed · c7 US slumps (sad), big red X | iris from the red pair |
| 3 definite | 0:26.4 → 0:48.0 | 8–12 | Hero beside an AMAZON window | c8 hero walks in, corner bar (middle red) · c9 window pops · c10 DECIDE, SEE THE PRODUCT tick · c11 SEARCH, DESCRIPTION, DETAILS, FEATURES tick · c12 PURCHASE button, hero cheers | wipe |
| 4 lead | 0:48.0 → 1:08.5 | 13–16 | Our website → hero walks to US | c13 window ABOUT US, WHAT WE SELL tick · c14 DECIDED ON US, walk to US, LEAD tag · c15 FEATURES card crossed out · c16 WHAT IT IS / HOW MUCH bubbles, hero cheers, tick, DEFINITELY BUY | iris from the purchase button |
| 5 confused | 1:08.5 → 1:25.8 | 17–20 | Spine bar returns; 60% lit red | c17 six figures turn red + confused · c18 2 question bubbles · c19 1 bubble · c20 2 bubbles | wipe |
| 6 clarity | 1:25.8 → 1:43.7 | 21–24 | Six confused figures, a tangle overhead | c21 tangle draws on · c22 SALES walks in, grabs the loose end · c23 headline, SALES pulls the tangle into a straight thread · c24 CLARITY on the thread, figures calm, a tick over each head, corner bar 60% = SALES, hold | iris from the bubbles |

## 6. Checks run (storyboard build)

- Every scene is fully open on its cue and ends on a cue (6/6). Hand-offs line up, and the duration equals the SRT end (103.686 s).
- 24 subtitle cues loaded from the SRT. All 18 storyboard frames render, with no console errors.
- QA grid on resting frames + transition midpoints: one collision fixed (cue 16 tick over the HOW MUCH bubble).

## 6b. Frame audit (`tools/frame_audit.js`, every 0.25 s, 403 frames)

Checks text over text, text over a figure, text under 24 px at 1080p, and text outside a 40 px margin.
Fixed: "60%" cut off during the cue 3 push, unreadable numbers on the corner bar, and a double-drawn frame at each scene boundary
(scenes now end 1 ms before the next cue). Remaining: two single-frame pop-ins (labels mid-scale for about 0.1 s), which is intended.
Shape overlaps (bag over face, ticks on hats, window cut off by the camera) were found on the QA grid and fixed.

## 7. Commands

```bash
python tools/srt_sync.py videos/20-20-60-split/20-20-60.srt videos/20-20-60-split/scenes.js
python .claude/skills/gen-stickman-v2/assets/build.py --scenes videos/20-20-60-split/scenes.js --out videos/20-20-60-split/the-20-20-60-split.html --title "The 20-20-60 Split" --file-name the-20-20-60-split --duration 103.728 --mode player --music off --sfx on --voiceover on --subtitles off
```

Final MP4 (frame-exact, headless; voiceover + SFX through the engine's own mix):

```bash
node tools/render_mp4.js videos/20-20-60-split/the-20-20-60-split.html <voiceover.mp3> videos/20-20-60-split/the-20-20-60-split.mp4
```

The ending (cues 21–24) is one continuous thread: it draws on as a coil, SALES takes the loose end, the loops come undone
from his end (two small tugs), the straight thread is released, levels to the 60% width, sinks behind the group, and
lands under their feet as the red 60% segment while the gray 20% segments slide in. A 30 fps frame-difference check
over all 3111 frames finds no jumps (the two diagonal wipes were lengthened to 1.0 s for this).
