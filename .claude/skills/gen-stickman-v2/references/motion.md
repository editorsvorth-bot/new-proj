# Motion: acting, morphing, camera, transitions

Motion should be fast-paced, fluid and purposeful. Every movement shows something from the script.

## Figure acting

- **Pose blends, not snaps.** Move between presets with `poseMix(a, b, E.inOut(p))` over 0.3–0.6 s. Add anticipation (a small opposite move) before big gestures, and let the head lag the body by about 0.1 s.
- **Walk cycles** come from `walkPose(phase, amp)`. Tie the phase to distance travelled (≈ 14 rad per 770 px at scale 1.25) so the feet don't slide, and blend `amp` to 0 when stopping.
- **Build-on:** introduce key figures with `draw: prog(...)` (torso → legs → arms → head pop). Bring in crowds with staggered build-ons, 0.08–0.15 s apart.
- **Expressions** change on the beat where the script names the feeling (confusion → `confused` + "?" bubble, a decision → `happy`, no need → `neutral`/`cross`).
- **Facing** turns toward whatever the figure is engaging with.
- Idle figures never freeze completely: allow a tiny breathing bob (±2 px, ~3 s period) or a head tilt.

## Signature shape morphing

- Precompute every interpolator in `buildScenes()` with `makeMorph(a, b, N)`; it resamples, matches winding and aligns start points. Never resample per frame.
- Every morph must mean something from the script: one shape splitting into categories, a box becoming a bar chart, a bubble becoming a box, a line growing into a path or bridge, a stack of layers opening.
- For complex changes, morph parts separately (one morph per segment), or cover the swap with a mask, instead of forcing one monster path.
- Ease morphs with `E.inOut` over 0.6–1.2 s. Hold both endpoints still long enough to be recognised (≥ 0.4 s).
- A changing value changes the proportions (bar width, sector size, crowd count) and never just the number.

## Camera

- Each scene has `camera(t, T) → {x, y, z, r}`: gentle push-ins toward the element being explained, lateral tracking that follows a walking figure, pull-outs to reveal the whole system.
- Use `E.inOut` with no hard starts. Rotation stays rare and small (|r| < 0.03). Hold the camera still while the viewer reads.
- The dot grid uses parallax depth 0.35 for a subtle sense of space. Keep the art strictly 2D.

## Transitions (built from the graphics)

- `enter: {type:'iris', x, y}` opens the next scene from a meaningful point (a bubble, a head, a box). Overlap scenes by the transition duration (0.6–1.0 s).
- `enter: {type:'wipe'}` is a diagonal ink-rimmed wipe for a change of topic.
- Shape-driven handoffs: a box grows to fill the frame and becomes the next background, a path line carries the camera into the next scene, or a figure walks out of one scene into the next.
- Don't repeat the same transition twice in a row. Don't use fades to black, scale-pops or slide-deck card swaps.

## Pacing and easing

- Vary the tempo: quick structural changes (0.3–0.6 s), slower comprehension holds (1–2 s) around key labels, then fast connected handoffs.
- Overlap motions: the next element starts while the previous one settles. Avoid identical delays everywhere.
- Easing vocabulary: `E.out` for arrivals, `E.inOut` for moves and morphs, `E.back` for small pops (tags, heads, bubbles), `E.outQuint` for type rises. Use `E.settle` sparingly for a decisive landing.
- Reveal labels at the exact moment the idea appears, never all at once.
- Never increment state per frame; everything is a pure function of `t`.
