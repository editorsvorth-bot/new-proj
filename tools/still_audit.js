/* Stillness audit: renders every STEP s at 480x270 and flags any span longer than MAX_STILL s
   in which consecutive frames differ by less than THRESH of their pixels (nothing visibly moving).
   Usage: node tools/still_audit.js <page.html> [step=0.25] [maxStill=1.5]                        */
const { chromium } = require('playwright');
const [file, stepArg, maxArg] = process.argv.slice(2);
const STEP = +(stepArg || .25), MAX_STILL = +(maxArg || 1.5), THRESH = 0.0015;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(file)); await p.waitForTimeout(1500);
  const r = await p.evaluate(({ STEP, MAX_STILL, THRESH }) => {
    const cv = document.createElement('canvas'); cv.width = 480; cv.height = 270; const g = cv.getContext('2d', { willReadFrequently: true });
    let prev = null, runStart = null; const spans = []; let maxRun = 0;
    for (let t = 0; t <= CONFIG.duration; t += STEP) {
      renderAt(t, g); const d = g.getImageData(0, 0, 480, 270).data;
      if (prev) { let ch = 0; for (let i = 0; i < d.length; i += 4) if (Math.abs(d[i] - prev[i]) + Math.abs(d[i + 1] - prev[i + 1]) + Math.abs(d[i + 2] - prev[i + 2]) > 30) ch++;
        const still = ch / (480 * 270) < THRESH;
        if (still) { if (runStart === null) runStart = t - STEP; } else if (runStart !== null) { const L = t - STEP - runStart; maxRun = Math.max(maxRun, L); if (L > MAX_STILL) spans.push([+runStart.toFixed(2), +(t - STEP).toFixed(2)]); runStart = null; } }
      prev = d;
    }
    if (runStart !== null) { const L = CONFIG.duration - runStart; maxRun = Math.max(maxRun, L); if (L > MAX_STILL) spans.push([+runStart.toFixed(2), CONFIG.duration]); }
    return { spans, maxRun: +maxRun.toFixed(2) };
  }, { STEP, MAX_STILL, THRESH });
  console.log(`longest still span ${r.maxRun}s; spans over ${MAX_STILL}s: ${r.spans.length ? JSON.stringify(r.spans) : 'none'}`);
  await b.close(); process.exit(r.spans.length ? 1 : 0);
})();
