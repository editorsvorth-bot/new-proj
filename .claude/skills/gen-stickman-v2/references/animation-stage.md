# Stage 2: full animation and delivery

Start after `APPROVED`, or immediately when the storyboard is disabled.

## Build

- Continue in the same file: set `CONFIG.mode = 'player'` and keep every approved composition, pose and geometry. Never simplify an approved design to make it easier to animate.
- Choreograph each scene through several beats: establish → reveal part → act/transform → show the result → hand off. There should be meaningful motion throughout, with short reading holds.
- Fill `SFX_CUES` (if SFX are enabled), `MUSIC.accents` (soft musical hits on the 3–6 biggest reveals, if music is enabled) and `CUES` (if subtitles are enabled).
- Recheck Rule 1 before publishing: scan every on-screen string against the beat map.

## Controls (already in the engine)

Play/Pause, Restart, seek bar, time display, Export Video → Download link. Conditional: Music/Sound toggle, Load voiceover, Subtitles toggle + Download SRT. Don't add editors or dashboards.

## Light QA (keep it short)

1. The Artifact loads and plays, and the duration matches the config (or voiceover).
2. Check 4–6 timestamps (one per scene plus a transition and a morph midpoint): figures are recognisable, there are no broken paths, labels aren't clipped, and there's one red focus per beat.
3. There are no long unintended blank or static holds. Render a grid of in-between times (morph midpoints, transitions, walk-ins) with `renderAt(t, smallCanvas)` and look at it once.
   - Morphing one rounded rect into another: interpolate the parameters (`rrectPoly(...mix(a, b, p))`), not the points, or the in-betweens turn into chamfered blobs.
   - Long walk-ins from off-screen: ease the segment with `E.out`, or the figures stay off-screen for the first half.
4. The enabled audio plays.
5. Export once where the environment allows it, and confirm the result is a real MP4 (the engine checks `ftyp`).

Fix real failures (missing content, JS errors, broken morphs, snaps, missing audio). Don't loop on minor artistic tweaks.

## Delivery

- Publish the Artifact (Artifact tool) with `capabilities: {downloads: true}` so **Download Video** can save the MP4, and give the link. Also save the full HTML (with doctype) in the user's project folder; the Artifact copy omits the `<!doctype>/<html>/<head>/<body>` wrapper, because the Artifact tool adds its own.
- If export works in the Artifact, say so. If it doesn't, give the self-contained HTML file (already self-contained) and say: "Open in desktop Chrome/Edge → Export Video → MP4."
- Briefly mention any real limitation, such as provisional voiceover alignment or real-time recording fallback. Never claim an MP4 that wasn't produced.
