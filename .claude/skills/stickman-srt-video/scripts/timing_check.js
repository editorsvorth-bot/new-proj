/* Scene timing gate: every scene fully open on a cue start, ends on a cue (2 ms tolerance), duration = SRT/voiceover end. Usage: node timing_check.js <page.html> */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto("file://" + require("path").resolve(process.argv[2])); await p.waitForTimeout(2500);
  const r = await p.evaluate(() => {
    const out = [], on = x => C.some(c => Math.abs(c - x) < 2e-3);
    SCENES.forEach((s, i) => {
      const full = s.start + (s.enter ? s.enter.dur : 0);
      out.push({ id: s.id, start: +s.start.toFixed(3), fullyOpen: +full.toFixed(3), end: s.end, opensOnCue: on(full), endsOnCue: on(s.end),
        handoff: i ? Math.abs(SCENES[i - 1].end - full) < 2e-3 : true });
    });
    return { scenes: out, duration: CONFIG.duration, srtEnd: C[C.length - 1], cues: CUES.length, sbCells: document.querySelectorAll('.sbCell').length, sbFrames: STORYBOARD.length, mode: CONFIG.mode };
  });
  console.log(JSON.stringify(r, null, 1), 'errors:', errs); await b.close();
})();
