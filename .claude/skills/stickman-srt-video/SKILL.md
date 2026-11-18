---
name: stickman-srt-video
description: Master flow for turning a script plus its SRT (any language, including Tanglish talking-head scripts) and an optional voiceover into a premium flat-vector stickman explainer MP4 in the locked black / red / cream / gray palette, with every scene and reveal timed to the SRT (down to the spoken word), a storyboard approval stage where each board is approved or commented on separately, automated quality gates (timing, text overlap, readability, stillness, smoothness), a wow/understanding scoring rubric, and a frame-exact MP4 render with the voiceover. Use when the user wants "the same kind of video" as the 20-20-60 stickman explainer for a new script, gives an SRT or voiceover for a stickman explainer, or asks for the stickman master flow. Builds on the gen-stickman-v2 engine (bundled). Content comes only from the script; every asset is drawn or synthesised in code.
---

# stickman-srt-video: script + SRT → approved storyboard → final MP4

This is the master flow that produced *The 20-20-60 Split*. Follow the stages in order. Each stage ends in a **gate**;
do not move on until it passes. Two stages are **hard stops for the user**: the storyboard approval (Stage 4) and the
final delivery (Stage 8).

## The rules (they override everything)

1. **Script only.** Every word, number, group, metaphor and claim on screen comes from the script or SRT, translated
   faithfully into short English (see `references/rules.md`). Nothing new: no facts, CTAs, brands' logos, jokes.
2. **Local assets only.** Everything is drawn or synthesised in code (the bundled engine). No AI image/video/music
   generators, stock, icon packs or downloads. User-supplied voiceover/logo are allowed.
3. **The SRT is the clock.** Scenes open fully *on* a cue start; reveals use `cue(n)` and `wordAt(n, phrase)`.
   **Nothing is revealed before it is spoken**: a group's colour, accessories, label and headline appear on its name.
4. **Palette locked:** ink `#141414`, red `#D62828` (the one thing to look at), cream `#F4EDE0`, gray `#8C8C8C`.
5. **Always score.** After every video (and every re-render) give the wow / understanding score per scene and overall,
   with the change since the previous version and a reason for anything under 10 (`scripts/scorecard.py`). Never skip it.
6. **Readable and clean:** at most 12 words on screen, no text over text or over a figure, text ≥ 24 px at 1080p,
   40 px safe margin, every figure and its arms inside its box/segment, everyone in a scene at the same scale.

## Configuration (fill defaults, ask only if the script/SRT is missing)

```
stickman-srt-video
Script: <text or file>            SRT: <file>  (required: it is the clock)
- Voiceover: <file> | none        (if given it is the master audio; its length must match the SRT end)
- Storyboard approval: Enabled    (per-board Approve / Needs changes + comments)
- Visual ideation: Disabled       (Enabled = 3-5 style options before the storyboard)
- Format: 16:9, 1920 × 1080, 30 fps        - Subtitles: Off
- Background music: Auto          (off when the voiceover already has a bed: scripts/audio_probe.py bed)
- Sound effects: On               - Final: MP4
```

## Stages

| # | Stage | Do | Gate |
|---|---|---|---|
| 0 | Intake | Resolve config; put files in `<project>/videos/<slug>/`; `audio_probe.py duration` if a voiceover exists | SRT parses; voice length ≈ SRT end (±50 ms) |
| 1 | Understand | Idea units per cue: excerpt → meaning → on-screen words (each traced to its cue) → FLOW.md table | Every string has a source cue |
| 2 | Design | Spine object, cast (red = current group, gray = past, ink = neutral), **character kits** (looks + behaviour from the script's own description of each group), props, transitions | One meaning per colour; one scale per scene |
| 3 | Build storyboard | `srt_sync.py` → `scenes.js` from `assets/scenes-template.js` → `build_video.py --mode review` → `qa_sheet.js` + `frame_audit.js` + `timing_check.js` | Gates in `references/gates.md` pass |
| 4 | **Storyboard approval (STOP)** | Publish the review page with `capabilities {db: {}, user: {}}`; the user approves or comments **per board**; read `reviews` with ArtifactData; revise only flagged boards; republish the same file path | Every board `approved`, or the user writes APPROVED |
| 5 | Animate + polish | Phase A understanding, Phase B wow (`references/quality.md`), motion pass + composition pass (`references/motion-composition.md`) | Rubric scores recorded per scene |
| 6 | Gates | `timing_check`, `frame_audit` (overlap, size, edge, ≤12 words), `still_audit` (≤1.5 s), `smooth_check` (no jumps at 30 fps), 2-second QA sheets scored by eye | All pass (single-frame pop-ins allowed) |
| 7 | Audio + render | `audio_probe.py bed` → `--music on/off`; `build_video.py --mode player --voiceover on`; `render_mp4.js`; `audio_probe.py sync` | Voice offset 0 ms, correlation > .9; 1920×1080, 30 fps |
| 8 | Deliver (STOP) | Send the MP4 + **the wow/understanding scorecard** (`scorecard.py` → SCORES.md: per scene, overall, change since the last version, why not 10, muted test) + `cost_report.py`; commit `scenes.js`, FLOW.md, SCORES.*, MP4 | Scorecard written and shown in the reply; user accepts or asks for changes (→ revise from Stage 5) |

Full instructions, commands and checklists for each stage: **`references/master-flow.md`** (read it first).

## Files

| Path | What it is |
|---|---|
| `assets/engine/` | The gen-stickman-v2 engine + its build (rig, morphs, camera, transitions, audio, player, MP4 export). Never edit per video. |
| `assets/kit.js` | Reusable helpers: SRT clock (`cue`, `wordAt`, `headlineWords`), spine bar, browser window, checklist, wearables (`person` + `WEAR`), `tieFigure`, `phoneHolder`, briefcase, bag, wallet, cart, scroll, question bubbles with icons, product pitch bubbles, stamp X, thread unravel, pacing. API: `references/kit-api.md` |
| `assets/scenes-template.js` | The only file written per video: SRT block, config, scenes, STORYBOARD, SFX |
| `assets/build_video.py` | kit + scenes → page; `--mode review` adds the approval panel (`assets/review/review.js`) |
| `scripts/` | `srt_sync.py`, `timing_check.js`, `frame_audit.js`, `still_audit.js`, `smooth_check.js`, `qa_sheet.js`, `render_mp4.js`, `audio_probe.py`, `scorecard.py` (wow/understanding after every video, with history), `cost_report.py` |
| `references/` | `master-flow.md`, `rules.md`, `quality.md`, `motion-composition.md`, `gates.md`, `kit-api.md`, `storyboard-review.md`, `lessons.md` |
| `examples/20-20-60-split/` | The finished reference video's scenes, flow and plan. Never reuse its story for another script. |

Requirements: Python 3, Node with Playwright + Chromium, ffmpeg/ffprobe.
