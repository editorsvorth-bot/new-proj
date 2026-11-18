# Rule 2: all new assets are generated locally in code

Every new visual and sound in the video is created by the Artifact's own JavaScript at run time. This keeps the style consistent, the output deterministic, and the project free of licensing or cost.

## Allowed (local generation)

- Canvas 2D drawing: paths, `Path2D`, polygons, arcs, Béziers, clipping and masks
- SVG path strings that **you author in code** and then sample into points (`svgPoly(d)`)
- Procedural geometry: the rig, poses, morph interpolators, draw-on strokes
- Text rendered from system fonts (`Arial Black`, `Segoe UI`, `Helvetica`, `Arial`)
- Web Audio synthesis rendered offline: oscillators, filters, envelopes, seeded noise
- A seeded RNG for any variation (never `Math.random()` inside `renderAt`)

## Allowed (technical, not an asset)

- The Mediabunny ESM module from a pinned CDN version, used only to mux MP4
- Browser APIs: WebCodecs, MediaRecorder, OfflineAudioContext

## Allowed (user-supplied)

- A voiceover recording or transcript the user attaches
- A logo or image the user explicitly uploads for this video. Redraw it in the palette only if they ask; otherwise place it as supplied.

## Banned

- AI image, video, music, voice or SFX generators of any kind, including MCP/connectors (Creative Claw, Adobe Firefly/Express, Figma generative tools, etc.)
- Stock photos, stock video, stock music, sound libraries and freesound-style downloads
- Icon fonts, icon packs, emoji used as artwork, clip-art, Lottie files and other people's templates or demos
- Hot-linked web images, or logos fetched from the internet
- Pre-rendered video segments of any kind

## Brands named in the script

Write the brand name as text (in the palette). Don't fetch or draw a logo. If the user wants the real logo, they upload it (see above).

## When something seems impossible locally

Don't escape to a generator. Use a stronger diagram, a clearer metaphor taken from the script, a pose with an expression, or typography. Flat-vector stickmen can express almost anything through pose, prop and layout.
