# Gates (automated checks; run after every rebuild that changes the affected part)

| Gate | Command | Pass |
|---|---|---|
| Timing | `node scripts/timing_check.js <page>` | every scene `opensOnCue` and `endsOnCue` true (2 ms tolerance); the last scene may end at the voiceover end |
| Text | `node scripts/frame_audit.js <page> 0.25` | no text over text, no text over a figure, nothing < 24 px, nothing past the 40 px margin, ≤ 12 words; single-frame pop-ins (a label mid-scale for ~0.1 s) are allowed |
| Stillness | `node scripts/still_audit.js <page>` | longest still span ≤ 1.5 s |
| Smoothness | `node scripts/smooth_check.js <page>` | no frame-to-frame jumps over the whole video at 30 fps |
| Visual | `node scripts/qa_sheet.js <page> <png> <from> <to> 2` | looked at every frame: no shape overlaps (props over faces, ticks over hats, figures outside their box), nothing cut by the camera |
| Audio | `python scripts/audio_probe.py sync <voice> <mp4>` | offset 0 ms, correlation > 0.9 |

The text audit cannot see shapes: always do the visual gate too. A flagged jump in the middle of a long cross-fade is
the detector's threshold, not a jump: lengthen the fade (≥ 0.8 s) rather than ignoring it.
