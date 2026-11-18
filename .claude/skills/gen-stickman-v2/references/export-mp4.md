# Export: a real MP4 only

The final deliverable is a real downloadable MP4 containing the full composited animation and every enabled audio track. Everything the viewer sees is drawn into the single captured canvas, so the export matches the preview.

## Route order (implemented in the engine)

1. **WebCodecs + Mediabunny** (`exportWebCodecs`): frame-exact. It calls `renderAt(i / fps)` for every frame on a full-resolution canvas, encodes H.264 video and AAC audio from the offline mix buffer, and muxes MP4 with `fastStart: 'in-memory'`. Pin an exact Mediabunny version in `MEDIABUNNY_URL`.
2. **MediaRecorder MP4** (`exportNative`): real time, used when WebCodecs or AAC is unavailable. The audio buffer plays into a `MediaStreamDestination`, and the AudioContext clock drives `renderAt`. Dropped frames are possible under load, so say so if this route was used.
3. **Restricted environment:** if neither route works, the Artifact HTML is already self-contained, so tell the user to open it in desktop Chrome/Edge and export there. A **WebM** fallback may be offered, but it is clearly labelled as not MP4 (and has no audio).

## Honesty checks

- The engine verifies the `ftyp` box before offering an `.mp4`. Never rename a WebM to `.mp4`.
- Use the configured resolution, fps and duration exactly, with no extra hold at the end.
- Report what actually happened (route used, with or without audio). Don't claim frame-perfect output from a real-time recording.

## Getting the file out of a published Artifact

- A claude.ai Artifact page cannot start a download itself: `<a download>` and blob links are inert there. The engine resolves `claude.use('downloads')` at boot and, when it is available, saves through `downloads.save({filename, data: blob})` on the viewer's click on **Download Video**. **Publish the final animation with `capabilities: {downloads: true}`** (the storyboard stage doesn't need it).
- Opened as a local HTML file in Chrome/Edge, the same link falls back to a normal browser download. Always also save the self-contained HTML locally in the project folder.
- Some embedded browsers (e.g. the desktop app's preview pane on a local file) have no WebCodecs. The engine then falls back to real-time MediaRecorder MP4, which takes as long as the video. Say which route was used.

Tested: the template exported a 14 s 1920 × 1080 30 fps MP4 with AAC audio via route 1 in the Claude desktop browser pane.

Tested on a real 90 s project (The 20-20-60 Split): the real-time MediaRecorder route produced a valid 52.7 MB MP4 with music in the desktop preview pane, which has no WebCodecs.
