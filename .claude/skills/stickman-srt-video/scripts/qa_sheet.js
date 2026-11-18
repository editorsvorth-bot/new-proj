/* QA contact sheet: renders frames from..to every step seconds with the production renderAt. Usage: node qa_sheet.js <page.html> <out.png> <from> <to> <step> */
const { chromium } = require('playwright');
(async () => {
  const [file, out, from, to, step] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto("file://" + require("path").resolve(file)); await p.waitForTimeout(1200);
  await p.evaluate(([from, to, step]) => {
    const grid = document.createElement('div'); grid.style.cssText = 'position:fixed;inset:0;z-index:99;background:#fff;display:grid;grid-template-columns:repeat(4,1fr);gap:4px;padding:4px;font:12px monospace';
    for (let t = +from; t <= +to + 1e-6; t += +step) { const d = document.createElement('div'); const c = document.createElement('canvas'); c.width = 640; c.height = 360; c.style.width = '100%';
      renderAt(Math.min(t, CONFIG.duration - .01), c.getContext('2d')); d.append(c, Object.assign(document.createElement('div'), { textContent: t.toFixed(1) + 's' })); grid.append(d); }
    document.body.append(grid);
  }, [from, to, step]);
  await p.screenshot({ path: out }); await b.close();
})();
