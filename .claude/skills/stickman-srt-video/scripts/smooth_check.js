/* 30 fps frame-difference check: flags any frame whose change is > 4x its neighbours and > 1.5% of the frame (a visible jump). */
const { chromium } = require('playwright');
(async () => {
  const [file, a = 0, b = 1e9] = process.argv.slice(2);  // usage: node smooth_check.js <page.html> [from] [to]
  const br = await chromium.launch(); const p = await br.newPage();
  await p.goto("file://" + require("path").resolve(file)); await p.waitForTimeout(1200);
  const r = await p.evaluate(([a, b]) => {
    const cv = document.createElement('canvas'); cv.width = 480; cv.height = 270; const g = cv.getContext('2d', { willReadFrequently: true });
    let prev = null; const d = [];
    for (let i = Math.round(a * 30); i <= Math.round(Math.min(b, CONFIG.duration - .01) * 30); i++) { renderAt(i / 30, g); const px = g.getImageData(0, 0, 480, 270).data;
      if (prev) { let ch = 0; for (let k = 0; k < px.length; k += 4) if (Math.abs(px[k] - prev[k]) + Math.abs(px[k + 1] - prev[k + 1]) + Math.abs(px[k + 2] - prev[k + 2]) > 40) ch++; d.push([i / 30, ch]); }
      prev = px; }
    // a "jump": a frame whose change is > 4x the median of its 10 neighbours and > 1.5% of the frame
    const jumps = d.filter(([t, ch], k) => { const nb = d.slice(Math.max(0, k - 5), k + 6).map(x => x[1]).sort((x, y) => x - y); const med = nb[5] || nb[Math.floor(nb.length / 2)]; return ch > 4 * Math.max(med, 50) && ch > 480 * 270 * .015; });
    return { frames: d.length, jumps: jumps.map(([t, ch]) => [+t.toFixed(2), ch]) };
  }, [+a, +b]);
  console.log(JSON.stringify(r)); await br.close();
})();
