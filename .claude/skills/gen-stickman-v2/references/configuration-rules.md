# Configuration behaviour

Read the whole configuration once, before producing anything. It fixes production values only; the content always comes from the script.

## Storyboard

- **Enabled:** Stage 1 (beat-map table + rendered contact sheet), then stop for an explicit `APPROVED`. After approval, build Stage 2 from the same file and the same geometry.
- **Disabled:** plan internally, then build and deliver the finished animation in the same turn. Don't stop for approval or offer alternative concepts.

## Voiceover

- **Enabled:** the attached recording is the master clock. Set `CONFIG.voiceover = true` so the player shows **Load voiceover** (the Artifact can't read chat attachments). Once loaded, the decoded duration becomes `CONFIG.duration`, `buildScenes()` re-runs, and the audio mix is re-rendered. Write scene times as functions of the transcript timing (or of `CONFIG.duration` when only rough alignment is possible) and label estimated timing as provisional. Never stretch, trim or replace the recording, and never synthesise a narration.
- **Disabled:** use the fixed duration from the config (default 90 s). The visuals and short labels carry the whole explanation, with no narration UI.

## Subtitles

- **Enabled:** `CONFIG.subtitles = true`. Fill `CUES` with `{start, end, text}`. With voiceover, the text is the transcript wording. Without it, the captions are the script's own sentences, shortened faithfully. Captions are drawn inside the captured canvas, and the player gets a toggle and an SRT download.
- **Disabled:** no cues, no subtitle UI. Headlines and labels still appear.

## Music and SFX

- Set `CONFIG.music` and `CONFIG.sfx` from the config. Disabled tracks get no engine, no button and no export audio.
- If all audio is disabled and there is no voiceover, export video only, with no silent track invented.

## Format

| Format | Resolution |
|---|---|
| Horizontal 16:9 | 1920 × 1080 |
| Vertical 9:16 | 1080 × 1920 (re-compose: stack layouts vertically, larger type, figures centred) |
| Square 1:1 | 1080 × 1080 |

Use the configured fps for export. Animation timing is always in seconds, never per frame.

## Missing or conflicting fields

Use the defaults in SKILL.md. Ask only when the script is missing or a core part of it can't be understood. A conflict between the config and the script on *content* is always resolved in favour of the script.
