# Rule 1: script only

The user's script is the only content source. The animation's job is to **show** what the script says, as clearly and beautifully as possible. It must never say more than the script does.

## What the script controls

- The order of ideas (follow the script's order; don't reorder unless the user asks)
- Every claim, explanation, category, step, cause and consequence
- Every number, percentage, ratio, name and label
- Every metaphor or analogy (use the script's own, e.g. if it says "like a vegetarian who walked into a fish market by mistake", draw *that*)
- The takeaway or ending (if the script has no conclusion, don't write one)

## What you decide yourself (allowed creative choices)

- How each idea is *depicted*: poses, expressions, props, diagrams, layouts, morphs, camera, colour emphasis
- Which **existing** word of the script becomes the headline, label or red key word
- Timing, pacing and transitions
- Neutral structural graphics that carry no new meaning: arrows, brackets, dividers, ground lines, bubbles, a "?" for confusion that the script describes

## Forbidden additions

- New facts, statistics, studies, quotes, dates, examples or brand names
- New characters with roles the script doesn't describe (generic stickmen acting out the script's people are fine)
- Extra steps, layers, categories or list items
- Jokes, CTAs ("subscribe", "follow for more"), title cards or end cards with text that isn't in the script
- "Improving" the script's numbers (if the script says the numbers are approximate, keep that caveat on screen, e.g. "approx." / "for understanding")
- Research to fill gaps. If something essential is ambiguous, ask the user instead of guessing.

## Step 0: idea units and beat map

1. Read the whole script. Split it into **idea units**: one claim, definition, category, step or example each.
2. For each unit, record: source excerpt (short, the script's words), its meaning in plain English, the visual that shows it, and the on-screen words (if any).
3. Allocate time in proportion to each unit's weight in the script (or to the voiceover timing when voiceover is enabled). Aim for roughly 12–18 meaningful visual developments per 90 s, scaled to the script; never pad with filler.
4. Group units into compositions (scenes). Each composition develops through several beats and hands off an element to the next scene.

Beat-map table (shown in Stage 1, kept internally otherwise):

| # | Time | Script source (excerpt) | Meaning | Visual / action | On-screen words | Morph / transition |
|---|---|---|---|---|---|---|

Before building, check every row: does the on-screen text trace to the source column? If not, remove it.

## Language and on-screen text

- The default on-screen language is **English taken from the script's own words**. For Tanglish/Tamil/mixed scripts, translate faithfully and briefly ("Never Buy", "Definitely Buy", "Confused Buyers"), keeping English terms the script already uses exactly as written.
- If the config sets `Text language:`, use that language instead.
- Keep it short: headlines of 2–6 words, labels of 1–3 words. Never put a paragraph on screen. Split long ideas across beats.
- Don't change the meaning when translating. If a phrase can't be rendered in a few words without changing its meaning, show it visually and keep the label minimal.

## Segment tags inside scripts

Scripts may contain production tags such as `Talking head`, `Motion graphics (images + code)` or `AI video (painterly)`. **Animate every segment as stickman scenes** and ignore these tags as content; they are never shown on screen. They describe the user's other edit plans, not instructions to use AI video (Rule 2 still applies).

## Numbers

- Show only the numbers the script states. Animate them honestly: bars or areas proportional to the stated values, and counters that end on the stated value.
- If the script calls the numbers approximate or illustrative, include a small gray caveat label taken from that wording.
