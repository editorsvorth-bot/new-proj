# Visual style: premium flat-vector stickman

The look should be confident ink-black stick figures on warm cream, with bold flat shapes, crisp type and a single red accent. It should read like a high-end editorial explainer, not doodles on a whiteboard and not a PowerPoint deck.

## Palette logic (locked: black, red, cream, gray)

- **Cream** is the ground for every scene. Fill the whole frame with it; there are no other background colours.
- **Ink** is the default for figures, outlines, main shapes and headlines.
- **Red** marks the active idea only: the key word of a headline, the figure the script is talking about, the arrow that matters, the section being explained. At most one red focus per beat; two only for a deliberate comparison.
- **Gray** marks the inactive, secondary, past or "background crowd" state. When focus moves on, the old red element turns gray or ink.
- Variation comes **only** from opacity of these four colours (`rgba(PAL.x, a)`). No gradients between hues, no glow, no glossy 3D, no noisy textures.
- Colour shifts are information: a figure turning from gray to red means "this one now".

## Stickman design (use the engine rig)

- Proportions (scale 1): head r 36, neck 12, torso 112, upper arm 60, forearm 56, thigh 70, shin 68, foot 16, stroke 13 with round caps and joins.
- The head is a solid filled circle in the figure's colour. The face is drawn in cream: two eye dots set toward the facing side (3/4 view) and a mouth/brow that carries the expression.
- Expressions: `neutral`, `happy`, `sad`, `confused`, `surprised`, `angry`, `closed`. Choose them from what the script says the person feels.
- Poses are angle sets (degrees from straight down, positive toward facing): `stand`, `point`, `shrug`, `think`, `cheer`, `cross`, `slump`, `reach`, `stop`, plus `walkPose(phase)`. Add new presets in the same format when the script needs them (sitting, holding a box, running, etc.) and keep them anatomically plausible.
- Scale by role: hero 1.1–1.4, groups 0.6–0.9, crowds 0.35–0.5. Keep feet on a shared ground line unless the script's idea needs otherwise.
- Props (boxes, money, phones, doors, shops, charts) are built from the same grammar: flat filled shapes, rounded corners (radius 18–28 at hero size), 6–8 px ink outlines only where they help recognition, and small cut-outs or notches that explain what the object is.
- Crowds and percentages are made of real figures (e.g. a 10-figure row coloured by share) rather than generic dots, when that makes the idea clearer.

## Shape grammar (one production, not a collage)

- Repeat the same corner radii, line weights (ink lines 6–8, figures 13, arrows 8, leader lines 4) and arrow style everywhere.
- Diagrams are flat filled regions (boxes, bars, sectors, layers, bridges and paths) that can morph into each other.
- Use negative space generously. Each frame has one dominant illustration, a few supporting elements and one clear text hierarchy.
- Keep a 96 px safe margin (1920 × 1080). Nothing important touches the edges.

## Typography

- Headlines: `Arial Black` / `Segoe UI Black`, uppercase, 64–96 px, ink with one red key word, masked word-by-word rise.
- Labels: `Segoe UI` bold, 30–40 px, attached by leader lines to what they name.
- Tags/pills: ink or red pill with cream text for category names and takeaways.
- Caveats and small notes: gray, 24–28 px.
- Never more than ~12 words on screen at once. No paragraphs.

## Composition variety

Rotate between these layouts so no two consecutive scenes share the same arrangement:

- hero figure + headline
- a figure acting beside a diagram (pointing, reaching, walking into it)
- side-by-side comparison
- a row or crowd split by colour
- a layered or stacked diagram with a camera push-in
- a path or bridge the figure travels along
- a close-up on an expression or prop

## Avoid

Generic icons, emoji, clip-art people, stick figures with no faces or rig, random decorative shapes, multiple competing red elements, gradients, drop-shadow stacks, and text-heavy slides.
