# Storyboard approval: per-board decisions and comments

## What the viewer gets
`build_video.py --mode review` adds a panel to the engine's storyboard contact sheet:
- a sticky bar: "N approved · N need changes · N to review" and **Approve all unreviewed**;
- under every board: board number, cue, time, the spoken SRT line, **Approve** / **Needs changes**, a comment box
  ("What should change on this board?") and **Save comment**. Boards turn ink-bordered when approved and red when
  they need changes. Clicking a thumbnail still shows it large in the main canvas.

## Publishing
Artifact tool: publish the review HTML (the `--artifact` copy) with `capabilities: {db: {}, user: {}}`,
`icon: "film"` on the first publish, label "Storyboard v1". Republish revisions to the **same file path** so the
URL and the stored reviews survive (new versions: label "Storyboard v2" …). Default db rules apply: anyone who can
use the page (Contributor or above) writes; Viewers/Commenters see the decisions read-only.

## Storage (what Claude reads)
Collection `reviews`, one document per board: `reviews/board-01`, `board-02`, … (board numbers follow the
`STORYBOARD` order — keep that order stable across revisions; add new boards at the end or renumber deliberately).
Fields: `board`, `boardId`, `title`, `t` (seconds), `cue`, `status` (`approved` | `changes` | `pending`), `comment`,
`by` (opaque viewer id), `updatedAt` (ISO time).

Read them with the ArtifactData tool (`list`, collection `reviews`, the artifact's URL). Then:
1. Summarise to the user: approved boards, boards needing changes with their comments, comments left on approved boards.
2. Change only those boards in `scenes.js` (comments are instructions from the user; still apply the script-only rule
   and say if a comment would add content the script doesn't have).
3. Rebuild with `--mode review`, run the storyboard gates, republish the same path, and say which boards changed.
4. Optionally reset a revised board to `pending` with ArtifactData `update` so it is reviewed again.
Proceed to animation only when every board is `approved` or the user writes APPROVED.
