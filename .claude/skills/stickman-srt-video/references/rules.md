# Rules

## Content (script only)
- Every idea, number, group name, example, metaphor and claim on screen comes from the script/SRT. Visuals may
  *depict* what is said; they may not *say* anything new. No CTAs, title or end cards with new text, jokes, research.
- Translate faithfully into short English (Tanglish → "Never Buy", "Definitely Buy", "Confused Buyers"); keep English
  terms the script already uses. Brands the script names may appear as plain text, never as a logo.
- Numbers only as stated; bars/areas proportional to them. Keep caveats the script states ("approximate").
- Speech bubbles are the speaker's own words in the script (the user may reword them, e.g. "WHAT WE HAVE",
  "THIS IS THE PRICE").

## Timing (the SRT is the clock)
- Scene k starts `TR` (iris 0.7 s) or `TRW` (wipe 1.0 s) before its first cue so it is fully open **on** the cue;
  the previous scene ends 1 ms before that cue (avoids a double-drawn frame).
- Reveals: `cue(n)` for line-level beats, `wordAt(n, 'phrase')` for word-level beats (character position within the
  cue, 0.1 s lead). **Nothing is revealed before it is spoken**: a group stays neutral (ink, no accessories, no label)
  until its name; headlines with a group name use `headlineWords` so each word lands on its own time.
- Every completed state holds ≥ 1.5 s unless the next line arrives sooner; nothing is fully still for > 1.5 s.

## Look
- Palette locked (ink, red, cream, gray); variation only by opacity. Red = the one thing to look at now.
- One scale for everyone in a scene (the helper is never taller). Figures, arms and props stay inside the box or
  segment they stand on. Feet on the ground line.
- Text: headline 84–96 px, sublines 40 px, labels ≥ 24 px at 1080p; ≤ 12 words on screen; 40 px safe margin;
  never over a figure or another text. One headline/subline baseline for the whole video (y 230 / 302).
- Accessories and actions express each group's nature as the script describes it; no costume that implies a fact
  the script doesn't state.

## Assets
Everything drawn/synthesised in code by the engine and kit. User-supplied voiceover/logo only. The MP4 muxer
(Mediabunny) is the only external load in the browser export; `render_mp4.js` uses ffmpeg locally instead.
