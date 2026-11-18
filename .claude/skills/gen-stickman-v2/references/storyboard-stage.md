# Stage 1: storyboard (only when Storyboard is Enabled)

## Plan

1. Build the idea units and beat map from the script ([script-fidelity.md](script-fidelity.md)).
2. Group them into compositions sized to the duration (about 5–8 for 90 s). Each composition has several beats and a handoff to the next.
3. For each composition, decide: what the script says here, the figure acting, the diagram or prop, what changes, the red focus, and how it transforms into the next scene.

## Table

| Scene | Time | Script source (excerpt) | What it teaches | Stickman + composition | Animated beats (in order, ~timing) | Morph / transition | On-screen text | Sound |
|---|---|---|---|---|---|---|---|---|

- Describe concrete things ("ink figure slumps beside a gray box; box splits into three bars; third bar turns red"), never "an icon appears".
- The on-screen text column contains only words translated faithfully from the source column.
- The Sound column lists only enabled audio. Write "—" if music and SFX are off.
- The table must cover the full duration.

## Rendered contact sheet

- Copy `assets/engine-template.html`, write the real scenes in `buildScenes()`, set `CONFIG.mode = 'storyboard'`, and list one representative time per composition in `STORYBOARD` (`{t, title}`).
- The same `renderAt` draws 640-wide thumbnails. Clicking one shows that frame large in the main canvas (and the seek bar can scrub between frames).
- Frames must show the real rigged figures, poses, expressions, diagrams, palette, headlines, labels and framing. No placeholders.
- Stage 1 doesn't need complete motion, audio or export. Write the scene code so the representative frames are correct, and extend the in-between motion in Stage 2.

## Check and stop

Open the published Artifact and confirm that the thumbnails render, the text is readable and nothing is clipped. Fix obvious errors only. Then present the table plus the Artifact link and end with exactly:

> Storyboard ready. Review the visual previews and reply APPROVED to generate the animation, or tell me what you'd like to change.

If the user asks for changes, revise just those scenes and re-publish to the same Artifact.
