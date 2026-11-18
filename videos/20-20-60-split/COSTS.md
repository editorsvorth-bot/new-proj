# Token cost: script → final video

Measured from this session's own transcript (`usage` on every model call), priced at Claude Opus 5.5 API rates:
$4 / MTok input, $20 / MTok output, $0.20 / MTok cache read, $8 / MTok 1-hour cache write (2× input; every write in this session was a 1-hour write).
This is the API-equivalent cost; on a Claude subscription the work counts against plan usage rather than being billed this way.

| Phase | Model calls | Output tokens | Cache-read tokens | Cache-write tokens | Cost (USD) |
|---|---:|---:|---:|---:|---:|
| 1. Setup: install find-skills, create repo, push | 13 | 2,931 | 1,207,518 | 34,163 | $0.57 |
| 2. Find skills for the script (search, shortlist) | 8 | 5,308 | 875,911 | 18,481 | $0.43 |
| 3. Ideation: 5 styles, plans, audit, review page | 17 | 64,876 | 3,010,348 | 99,271 | $2.69 |
| 4. Study the gen-stickman-v2 kit | 9 | 5,255 | 2,149,182 | 37,505 | $0.84 |
| 5. Storyboard v1 on the SRT clock (flow, scenes, SRT sync) | 14 | 39,142 | 4,238,384 | 66,863 | $2.17 |
| 6. Viewer audit, characters, 10/10 plan, overlap audit, wearables (v2-v3) | 17 | 44,464 | 6,138,361 | 60,032 | $2.60 |
| 7. Fixes + Phases A, B, C (storyboard v4) | 17 | 62,816 | 7,607,837 | 99,052 | $3.57 |
| 8. Voiceover, smooth ending, first final MP4 | 25 | 26,818 | 12,919,690 | 43,617 | $3.47 |
| 9. Review the listed skills | 4 | 3,417 | 2,158,972 | 8,985 | $0.57 |
| 10. New skills pass + updated MP4 + this cost report | 12 | 15,849 | 6,775,023 | 72,039 | $2.25 |
| **Total** | **136** | **270,876** | **47,081,226** | **540,008** | **$19.15** |

Where the money goes: cache reads $9.42 (49%), output $5.42 (28%), cache writes $4.32 (23%), uncached input about $0.
Cache reads dominate because every call re-reads the whole conversation (cheaply, at 5% of the input price); it grows with every turn,
so late phases cost more per call even when they write little.

The core script-to-video path (phases 3, 5, 6, 7, 8, 10) is about $16.75; setup, skill search, kit study and skill review are about $2.40.
Rendering, audits and ffmpeg run locally and cost no tokens. The final phase's figure includes the calls up to the cost report itself.
