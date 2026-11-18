# Audio: all procedural, offline-rendered, conditional

The engine renders all enabled audio (voiceover + music + SFX) into **one AudioBuffer** with `OfflineAudioContext` (`renderMix()`). Preview plays that buffer from the seek offset, and export muxes the same buffer. As a result, seeking can't double-fire sounds, the preview matches the export, and everything stays deterministic.

## Background music (only when enabled)

- An original synthesised bed: triangle-pluck arpeggio, sine bass, soft kick and seeded-noise hats, with a 2-bar intro without drums, a fade-in of about 1.6 s, a fade-out of about 2.5 s ending inside the runtime, and a sustained tonic chord on the last bar.
- Adapt it to the script's tone by editing `MUSIC`: `bpm` (84–110), the `prog` chord list (MIDI triads), and the arp density. A curious or problem-solving script suits minor → relative major; a confident, upbeat script suits major.
- `MUSIC.accents = [t, ...]` adds soft bell hits on the biggest reveals.
- Never use downloaded loops or imitate a specific commercial track.

## Sound effects (only when enabled)

- `SFX_CUES = [{t, type}]` with types `whoosh` (morphs, transitions), `pop` (figure/tag appears), `click` (connection, label lands), `draw` (draw-on lines), `thud` (heavy landing), `chime` (resolution/takeaway).
- Cue only the meaningful events, about 1–3 per beat. SFX sit under the voice when one is present.

## Voiceover (only when enabled)

- Loaded through the **Load voiceover** file picker. The decoded length becomes the duration, and music is ducked to about 0.28.
- Never synthesise or replace narration.

## Subtitles (only when enabled)

`CUES` drawn inside the canvas (bottom, ink pill, cream text) plus an SRT download. Text comes from the transcript or script wording only.

## Mix

Every source goes through a shared gain into a gentle compressor (threshold −14 dB, ratio 4). There are no per-frame audio nodes, and nothing is created in `renderAt`. If music, SFX and voiceover are all disabled, there's no audio track at all.
