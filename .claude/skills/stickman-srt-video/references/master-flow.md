# Master flow: every stage, with commands

`SK` = this skill's folder, `V` = `<project>/videos/<slug>`, `S` = the session scratchpad. Run Node scripts with
`NODE_PATH=$(npm root -g)` so the pre-installed Playwright resolves. All times are seconds on the SRT clock.

## Stage 0: Intake
1. Put `<slug>.srt` (and the voiceover, if any) in `V/`. Ask only if the SRT is missing: it is the clock.
2. Voiceover: `python SK/scripts/audio_probe.py duration <voice> V/<slug>.srt`. The decoded length should equal the
   SRT end (±50 ms; MP3 containers report ~40 ms of padding: ignore it). A bigger gap means the SRT was made from
   another cut: ask before continuing.
3. `python SK/scripts/audio_probe.py bed <voice>` decides `--music` (bed found → off).

**Gate:** SRT parses back-to-back (srt_sync warns on gaps); audio length known.

## Stage 1: Understand the script (write `V/FLOW.md`)
For every cue: excerpt (script's own words) → plain-English meaning → the only on-screen words allowed (headline
2–6 words with one red key word, sublines ≤ 8 words, labels 1–4 words, question bubbles in the speaker's voice).
Note the group/category names and where in the cue they are spoken (`wordAt`). Ignore production tags in scripts.
**Gate:** every on-screen string has a source cue; nothing in the script is missing.

## Stage 2: Design
- **Spine object** that carries the structure through every scene (shares → one proportional bar, `SHARES`/`GROUP`).
  It opens the video, returns when the last group is introduced, and the ending lands back on it.
- **Cast:** one red hero = the group being talked about now; past groups gray; neutral ink before a group is named.
- **Character kits from the script's description of each group** (examples from the reference: the helper gets a red
  tie and briefcase; people who have researched carry a ticked phone and glasses; confused people pace and scratch
  their heads; people who will never buy cross their arms and turn away). Behaviour > costume.
- **Props for concrete script ideas** (a cart when the script says cart, a website window when it says website, a
  features scroll when it says features). A metaphor only if the script states it.
- **Transitions** alternate iris (from the object the next idea grows out of) and wipe (topic change). Iris 0.7 s,
  wipe 1.0 s, finishing exactly on the cue.
**Gate:** one meaning per colour; one scale per scene; every planned reveal has a cue/word time.

## Stage 3: Build the storyboard
```bash
cp SK/assets/scenes-template.js V/scenes.js
python SK/scripts/srt_sync.py V/<slug>.srt V/scenes.js          # writes C and SRT_TEXT, prints the duration
python SK/assets/build_video.py --scenes V/scenes.js --out V/<slug>.html --artifact S/<slug>-review.html \
  --title "<Short Name>" --file-name <slug> --duration <seconds> --mode review --music off --sfx on
node SK/scripts/qa_sheet.js V/<slug>.html S/sheet1.png 0 30 2      # look at every sheet
node SK/scripts/frame_audit.js V/<slug>.html 0.25
node SK/scripts/timing_check.js V/<slug>.html
```
Write each scene as a function of `cue(n)`/`wordAt(n, …)`; one `STORYBOARD` entry per board (≈ one per cue group,
12–20 for 90–120 s). Layout: headline x 140, y 230 (84–96 px), sublines y 302 (40 px), tags/labels ≥ 24 px,
ground y 860, safe margin 40 px. **Gate:** `references/gates.md` storyboard gates pass.

## Stage 4: Storyboard approval (hard stop)
Publish `S/<slug>-review.html` with the Artifact tool: `capabilities: {db: {}, user: {}}`, `icon: "film"`, label
"Storyboard v1". Then tell the user: every board has Approve / Needs changes and its own comment box; nothing is
animated further until the boards are approved. End the turn. On their reply, read the decisions:
`ArtifactData list` on collection `reviews` (documents `board-01`… with `status`, `comment`, `title`, `cue`).
Revise only boards with `status: "changes"` (and any comment on approved boards), rebuild with `--mode review`,
republish the **same file path** (same URL; stored reviews stay). Repeat until every board is `approved` or the user
writes APPROVED. Details: `references/storyboard-review.md`.

## Stage 5: Animate and polish
1. Score each scene with the rubric (`references/quality.md`) before changing anything; record it.
2. Phase A (understanding): show-don't-tell actions for each line, word-timed reveals, one idea per beat.
3. Phase B (wow): one signature moment per scene (a morph, a physical gag from the line), object-grown transitions,
   acting (anticipation, follow-through, blinks), cue-locked SFX.
4. Motion + composition passes with the numbers in `references/motion-composition.md`.
5. Re-score; keep the before/after table.

## Stage 6: Gates (all must pass)
```bash
node SK/scripts/timing_check.js V/<slug>.html
node SK/scripts/frame_audit.js V/<slug>.html 0.25
node SK/scripts/still_audit.js V/<slug>.html
node SK/scripts/smooth_check.js V/<slug>.html
node SK/scripts/qa_sheet.js V/<slug>.html S/s1.png 1 31 2     # and 33-63, 65-95, 97-end: score every frame
```
Fix only what fails, using `references/lessons.md`; re-run the affected gate.

## Stage 7: Audio and render
```bash
python SK/assets/build_video.py --scenes V/scenes.js --out V/<slug>.html --title "<Short Name>" --file-name <slug> \
  --duration <voice seconds> --mode player --music <on|off> --sfx on --voiceover on
node SK/scripts/render_mp4.js V/<slug>.html <voice.mp3> V/<slug>.mp4      # ~2-3 min for 100 s
python SK/scripts/audio_probe.py sync <voice.mp3> V/<slug>.mp4            # must say IN SYNC
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of csv=p=0 V/<slug>.mp4
```
The last scene's `end` is `Math.max(cue(N+1), CONFIG.duration)` so it holds to the end of the audio.

## Stage 8: Deliver (hard stop)
Send the MP4 (SendUserFile), the before/after score table, what each gate found, and
`python SK/scripts/cost_report.py ~/.claude/projects/<project>/<session>.jsonl` (check current prices first).
Commit `scenes.js`, `FLOW.md`, the SRT, the HTML and the MP4. Changes requested → back to Stage 5 for the named
scenes only, then Stages 6–8 again.
