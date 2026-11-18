# Motion and composition passes (numbers from animation-principles and critique-composition)

## Motion
| Topic | Rule used | In the kit/engine |
|---|---|---|
| Enters | ease-out, 0.3–0.5 s (big: 0.5–0.8 s) | `E.out`, `E.outQuint` for headline rises, `E.back` for pops |
| Exits | gentle ease-in over 0.4 s (a hard cubic ease-in on big text reads as a snap) | `const q = prog(t, a - .1, b); 1 - q * q` |
| Moves | ease-in-out, 0.3–0.4 s; cinematic camera 0.8–2 s | `E.inOut`, camera `tween` |
| Stagger | 40–120 ms per item, cap the group at ~0.8 s | crowd walk-ins .08 s, ticks .08–.1 s |
| 1/3 rule | with 3+ figures, ≤ 1/3 in full motion; the rest ambient | `pacing(x, t, i, on * amp)`: the speaker amp 1, others .35 |
| Anticipation | 60–200 ms counter-move before a big action | a dip before a cheer, a lean-in before a pull |
| Follow-through | attached parts settle after the body | tie sway around the knot (`salesman`) |
| Arcs | no long straight slides for organic things | `- Math.sin(Math.PI * p) * 70` on hand-offs and flights |
| Colour changes | cross-fade, never switch a large area in one frame | draw the old, then `fadeAlpha(p, new)` over ≥ 0.8 s |
| Wipes | 1.0 s for diagonal wipes (0.7 s flags as a jump) | `TRW` |

## Composition (critique each scene's resting frame: balance, whitespace, rhythm, gestalt)
- Balance: when one side empties (a prop fades out), move the camera so the action sits near the centre.
- Rhythm: one headline/subline baseline for the whole video; labels the same size everywhere.
- Gestalt: labels sit directly under their figure/segment; same function → same treatment.
- Figure/ground: dim (alpha ~.3) what is no longer the subject rather than leaving it at full strength.
