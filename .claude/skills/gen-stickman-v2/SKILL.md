---
name: gen-stickman-v2
description: Turn a script the user supplies (any language, including Tanglish talking-head scripts) into a premium flat-vector stickman explainer animation in a locked black / red / cream / gray palette, built entirely in JavaScript inside one playable HTML Artifact (Canvas 2D + Web Audio) with rigged stick figures, precomputed shape morphs, a 2D camera, mask transitions, optional procedural music/SFX/subtitles/voiceover, an optional storyboard approval stop, and real MP4 export from the browser. Use whenever the user says gen-stickman, stickman / stick-figure explainer, "animate this script with stickmen", or pastes a script together with a configuration block (Storyboard, Voiceover, Subtitles, Duration, Format, fps, SFX, Music). Content comes ONLY from the user's script, and every asset is generated locally in code: no AI image/video/music generators, no stock, no downloaded media. Not for Remotion/FFmpeg pipelines or text-to-video.
---

# gen-stickman-v2: script → stickman explainer

Turn the user's script into a polished, fast-paced, flat-vector stickman explainer. Rigged stick figures act out the script's ideas, while shapes, diagrams and type morph into one another, so it reads like a high-end 2D motion piece and not an animated slide deck. Build it as a playable HTML Artifact with a deterministic `renderAt(t)` engine and a real MP4 export.

## The two hard rules (they override everything else)

1. **Script only.** Every idea, claim, example, number, label, character and metaphor on screen must come from the user's script (or their voiceover/transcript). Don't add facts, statistics, examples, analogies, characters, jokes, CTAs or conclusions that aren't in the script, and don't fill gaps with research. Visuals may *depict* what the script says, but they must not *say* anything new. Full rules: [references/script-fidelity.md](references/script-fidelity.md).
2. **Local assets only.** Generate every visual and sound locally in the Artifact's own code: Bézier paths, polygons, Canvas drawing and Web Audio synthesis. Don't use AI image/video/music/voice generators, MCP media tools (Creative Claw, Adobe, Figma, etc.), stock libraries, icon packs, emoji art, web images, or downloaded audio. The only allowed external load is the technical MP4 muxer (Mediabunny). Files the user supplies themselves (a voiceover, their own logo) may be used. Full rules: [references/local-assets.md](references/local-assets.md).

## Palette (locked)

| Token | Hex | Role |
|---|---|---|
| ink (black) | `#141414` | figures, outlines, headlines, primary shapes |
| red | `#D62828` | the ONE thing that matters right now: key word, active figure, key arrow |
| cream | `#F4EDE0` | background / paper, faces, text on dark |
| gray | `#8C8C8C` | inactive / secondary figures, guides, grids, past states |

Don't use any other hue. Create variation only through the opacity of these four colours. Keep red scarce, so that it always means "look here".

## 1. Configuration

Read the user's config block. Fill any missing field with these defaults. **Ask only if the script is missing.**

```
Script: <pasted text or attached file>   (required, the only content source)
- Storyboard: Enabled            (Enabled | Disabled)
- Voiceover: Disabled            (Enabled = attached recording is the master clock)
- Voiceover transcript (optional): ""
- Subtitles: Disabled
- Duration without voiceover: 90 seconds
- Format: Horizontal, 16:9       (Vertical 9:16 -> 1080 × 1920; Square 1:1 -> 1080 × 1080)
- Native resolution: 1920 × 1080
- Target export frame rate: 30 fps
- Preview: smooth, 60 fps where supported
- Style: Premium flat-vector stickman explainer
- Sound effects: Disabled
- Background music: Enabled
- Final video format: MP4
```

The config is the single source of truth for production values. The script is the single source of truth for content. Behaviour per setting: [references/configuration-rules.md](references/configuration-rules.md).

## 2. Stage flow

**Step 0: beat map (always, internally or shown).** Split the script into idea units, then map each unit to visual beats, as set out in [references/script-fidelity.md](references/script-fidelity.md). Give every on-screen word a source line in the script.

**Storyboard Enabled → Stage 1, then STOP.** Present the beat-map/storyboard table and an Artifact contact sheet rendered by the *production engine* (`CONFIG.mode = 'storyboard'`). End the turn with exactly:

> Storyboard ready. Review the visual previews and reply APPROVED to generate the animation, or tell me what you'd like to change.

Don't start Stage 2 without an explicit approval. When the user asks for changes, revise only the affected scenes. See [references/storyboard-stage.md](references/storyboard-stage.md).

**Storyboard Disabled → Stage 2 directly.** Don't show a storyboard, ask for approval or offer alternative concepts.

**Stage 2: full animation.** Switch the same file to `CONFIG.mode = 'player'` and build every scene with its full choreography, then add the enabled audio, the controls and MP4 export. Reuse the approved storyboard's geometry exactly. See [references/animation-stage.md](references/animation-stage.md).

## 3. Reference files: read before building

| File | Covers |
|---|---|
| [references/production-playbook.md](references/production-playbook.md) | **Start here.** The exact 18-step sequence from raw script to published video: idea units, on-screen words, spine object, timeline budget, beat skeleton, layout grid, scenes file, build command, QA grid and fix catalogue, storyboard stop, export test, publish, delivery, revisions |
| [references/script-fidelity.md](references/script-fidelity.md) | Rule 1: idea units, beat map, translating Tanglish into English labels, segment tags, numbers, forbidden additions |
| [references/local-assets.md](references/local-assets.md) | Rule 2: what counts as a local asset, what is banned, user-supplied files, brands |
| [references/configuration-rules.md](references/configuration-rules.md) | Storyboard / voiceover / duration / subtitles / audio switches |
| [references/visual-style.md](references/visual-style.md) | Palette logic, stickman design and rig, shape grammar, typography, composition |
| [references/motion.md](references/motion.md) | Pose acting, shape morphs, camera, transitions, pacing and easing |
| [references/storyboard-stage.md](references/storyboard-stage.md) | Stage 1 table and contact sheet, approval stop |
| [references/animation-stage.md](references/animation-stage.md) | Stage 2 build, controls, light QA, delivery |
| [references/audio.md](references/audio.md) | Offline-rendered procedural music and SFX, voiceover, subtitles, mix |
| [references/export-mp4.md](references/export-mp4.md) | WebCodecs + Mediabunny → MediaRecorder MP4 → honest fallbacks |
| [assets/engine-template.html](assets/engine-template.html) | **Tested working engine**: RNG, easing/tween, rig + poses + walk cycle + faces, morphs, draw-on, headline/labels/tags, scene helpers (`walker`, `idle`, `speechBubble`, `labelBlock`, `flagTick`, `badge`, `crossMark`, `subline`, `fadeAlpha`, `popAt`), camera, iris/wipe transitions, offline audio, storyboard sheet, player, MP4 export with the `downloads` capability. Never edit it per project |
| [assets/build.py](assets/build.py) | Splices a project's scenes file into the template, sets `CONFIG` from the config, and writes the full local HTML plus the Artifact copy |

## 4. Working method

Follow [references/production-playbook.md](references/production-playbook.md) step by step. In short:

1. Parse the config and fill in the defaults. If there's no script, ask for it and stop.
2. Read the script fully, split it into idea units, and write the on-screen words, each traced to a script excerpt.
3. Choose one spine object that carries the script's structure through every scene, cast the figures, and budget the timeline.
4. Write only a scenes file (`buildScenes()` plus project-only props) and build it with `assets/build.py`.
5. Run one QA grid of resting, morph-midpoint and transition-midpoint frames, and fix only the catalogued failures.
6. Storyboard enabled: publish `--mode storyboard`, show the table, and stop with the approval sentence.
7. After approval (or straight away if the storyboard is disabled): build `--mode player`, run QA once, test the export once, and publish with `capabilities: {downloads: true}`.
8. Delivery: the link, how to download the MP4, what was verified, and the local HTML path. No long reports.

The storyboard setting never lowers the quality bar, and neither rule may be traded for visual flair.
