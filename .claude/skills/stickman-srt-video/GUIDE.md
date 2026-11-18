# How to use stickman-srt-video, step by step

You give a script, its subtitle file (SRT) and the voiceover. Claude plans a storyboard and stops so you can approve
or comment on each board. Then it animates, checks and renders the final MP4, and scores it. You are asked to act
only twice: at the storyboard and at the end.

---

## Step 1 · Install or update the skill (once per new version)
1. In claude.ai open **Settings → Capabilities → Skills**.
2. If an older `stickman-srt-video` is listed, remove it.
3. Upload `stickman-srt-video.skill`.

In a Claude Code project you can instead keep the folder at `.claude/skills/stickman-srt-video/`.

## Step 2 · Prepare three files
| File | What it should be |
|---|---|
| **Script** | The text you will say, in any language (Tanglish is fine). This is the only content source: nothing appears on screen that the script doesn't say. |
| **SRT** | Subtitles made **from the same voiceover recording**, one line per sentence or phrase. Its timings drive every scene, so it must match the audio. |
| **Voiceover** (optional but recommended) | The final MP3/WAV. If it already has background music, Claude detects that and turns its own music off. |

Tip: export the SRT from the same edit as the audio (e.g. your editor's caption export), so the last subtitle ends
where the audio ends.

## Step 3 · Start a new video
Upload the files and send this (change anything after the dashes, or leave the defaults):

```
Use stickman-srt-video for a new video.
Title: <short video title>
Script: <paste, or "attached">
SRT: attached          Voiceover: attached
- Storyboard approval: on
- Visual ideation: off        (on = see 3-5 style options first)
- Format: 16:9, 1920 x 1080, 30 fps
- Subtitles in the video: off
- Background music: auto      - Sound effects: on
```

## Step 4 · Watch the stages (no action needed)
Claude works one stage at a time and posts a short report after each one (what it made, which checks passed, what's
next):

| Stage | What happens |
|---|---|
| 0 Intake | Checks the SRT, and the voiceover length against it |
| 1 Understand | Splits the script into ideas, with the English meaning and the only words allowed on screen |
| 2 Design | Picks the main diagram, the characters (looks and actions that match each group), props and transitions |
| 3 Storyboard | Builds the boards on the SRT timing and runs the first checks |

## Step 5 · Approve the storyboard (your first stop)
1. Open the **storyboard approval link** Claude gives you (sign in to claude.ai).
2. For **each board**: read the spoken line under it, then press **Approve**, or **Needs changes** and write what to
   change in that board's comment box (**Save comment**).
3. The bar at the top counts approved / needs changes / to review. **Approve all unreviewed** approves the rest.
4. Go back to the chat and reply **"reviewed"** (or **APPROVED** if everything is fine).

Claude reads your decisions, shows them as a table, changes only the boards you flagged, and gives you the updated
boards at the same link. Repeat until every board is approved.

## Step 6 · Wait for the final video (no action needed)
| Stage | What happens |
|---|---|
| 5 Polish | Makes each idea clearer and livelier (actions, word-timed reveals, transitions, motion and layout passes) |
| 6 Checks | Timing, text overlap/size, ≤ 12 words on screen, no frozen moments, no jumps, a visual review of every 2 s |
| 7 Render | Mixes your voiceover with quiet sound effects and renders the MP4; checks the voice is in sync |

## Step 7 · Receive the video (your second stop)
You get:
- the **MP4** (1920 × 1080, 30 fps, your voiceover);
- the **wow / understanding scorecard**: a score per scene, the overall score, the change since the previous version,
  why anything is below 10, and a muted viewing test;
- what each check found, and the **token cost**.

## Step 8 · Ask for changes (optional)
Name the scene or the time, e.g. *"at 1:04 make the bubbles say …"* or *"scene 2: the wallet is too small"*. Claude
changes only that, re-runs the checks, re-renders and gives you a new scorecard that shows what changed.
Storyboard-level changes (a different idea for a scene) go back to the approval page.

## Continuing later
Each video keeps `STATUS.md` (current stage), `FLOW.md` (the plan), `SCORES.md` (scores and history) and the approval
page. In a new chat say *"continue the <title> stickman video"*: Claude reads them and resumes at the right stage.

## Good to know
- **Content:** only what the script says appears on screen. Brand names may appear as text, not logos.
- **Look:** black, red, cream and gray only; stick figures with faces, accessories and actions.
- **Fonts:** headlines use Arial Black / Segoe UI where installed; other machines substitute a similar font. Ask to
  bundle a font if the exact typeface matters.
- **The approval page doesn't save:** open the published link while signed in to claude.ai (a local copy can't save).
- **Time:** the render takes ~2-3 minutes for a 100-second video once the storyboard is approved.
