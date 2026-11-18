# Lessons: failures that happened, and the fix that worked

| Symptom | Fix |
|---|---|
| A group's look/label shows before it is spoken | Neutral (ink, no `wear`) until `wordAt(n, name)`; `headlineWords` for the name |
| Figures or arms stick out of their segment at the end | Space them inside the segment; final pose arms up (`cheer`), not out |
| Helper taller than everyone | One `s` for every figure in a scene |
| "Empty pockets" don't read | Use an object the viewer knows (an empty wallet tipped upside down) |
| Plain arrows for "selling" read as nothing | Product bubbles that bounce off a raised palm and fall gray |
| Tangle → line morph looks broken | One continuous thread: unravel from the pulled end (knot up to a moving front + straight to the hand), level it, sink it behind the group, thicken into the bar; cross-fade colour |
| "?" bubble over the subline | Move the character so the bubble clears the text column |
| Scroll/prop covering a character | Hang it from the far side of the hand; let the other character step back |
| CLARITY / tags over sublines or the thread | Put tags on the object they name, after the object has settled |
| Bag/product over a face during a cheer | Show the product held up during the cheer, the bag only after the arms come down |
| Ticks sitting on hats | Badges ~100 px above the head at s .8 |
| Too many words (13–20) | Remove repeated labels (kicker + tag + headline), dim old rows/questions to alpha .25–.3 |
| Frozen 2–4 s stretches | Give the line an action (nods on ticks, a dejected walk back, a slow camera drift) |
| Text cut at the edge during a camera push | Fade off-focus labels/numbers when the push starts |
| Tiny text in the corner reprise | No numbers in `miniBar` |
| One frame shows two scenes at a boundary | End each scene 1 ms before the next cue |
| Wipe flagged as a jump | Wipes 1.0 s |
| Large colour switch flagged as a jump | Cross-fade over ≥ 0.8 s |
| Exit fades snap | Gentle ease-in over 0.4 s, not a cubic ease-in over 0.3 s |
| Voiceover already has music | `audio_probe.py bed` → engine music off, SFX stay at the quiet voice-bus level |
| Fonts differ between machines | The engine asks for Arial Black/Segoe UI; Linux renders a fallback (Inter). Bundle a font if exact type matters |
