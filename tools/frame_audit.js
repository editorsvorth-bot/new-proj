/* Frame audit for gen-stickman-v2 pages: renders every STEP seconds at full 1920x1080 and checks
   - text over text (two different strings whose glyph boxes intersect)
   - text over a stick figure (glyph box intersects a figure's body box)
   - text too small to read in the export (rendered cap size < MIN_PX at 1080p)
   - text outside the safe area (MARGIN px from each edge)
   Frames inside a scene's enter transition are skipped (two scenes are mid-swap by design).
   Usage: node tools/frame_audit.js <page.html> [step=0.25] [out.json]                                  */
const { chromium } = require('playwright');
const [file, stepArg, outFile] = process.argv.slice(2);
const STEP = +(stepArg || 0.25), MIN_PX = 24, MARGIN = 40, ALPHA = 0.35;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + require('path').resolve(file)); await p.waitForTimeout(1500);
  const res = await p.evaluate(({ STEP, MIN_PX, MARGIN, ALPHA }) => {
    const W = CONFIG.width, H = CONFIG.height, cv = document.createElement('canvas'); cv.width = W; cv.height = H;
    const g = cv.getContext('2d'); let rec = null;
    const tbox = (ctx, x0, y0, x1, y1) => { const m = ctx.getTransform(), pts = [[x0, y0], [x1, y0], [x0, y1], [x1, y1]].map(([x, y]) => [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f]);
      return [Math.min(...pts.map(q => q[0])), Math.min(...pts.map(q => q[1])), Math.max(...pts.map(q => q[0])), Math.max(...pts.map(q => q[1]))]; };
    const ft = CanvasRenderingContext2D.prototype.fillText;
    CanvasRenderingContext2D.prototype.fillText = function (s, x, y, ...r) {
      if (rec && this.canvas === cv && this.globalAlpha >= ALPHA && String(s).trim()) {
        const m = this.measureText(s), bx = tbox(this, x - m.actualBoundingBoxLeft, y - m.actualBoundingBoxAscent, x + m.actualBoundingBoxRight, y + m.actualBoundingBoxDescent);
        const em = parseFloat((this.font.match(/(\d+(?:\.\d+)?)px/) || [0, 0])[1]) * Math.hypot(this.getTransform().a, this.getTransform().b);
        rec.text.push({ s: String(s), bx, em });
      }
      return ft.call(this, s, x, y, ...r);
    };
    const ds = window.drawStickman;
    window.drawStickman = function (gg, F) {
      const r = ds(gg, F);
      if (rec && gg.canvas === cv && (F.draw ?? 1) > .6 && (F.alpha ?? 1) >= ALPHA && r) {
        const s = F.s || 1; rec.figs.push(tbox(gg, F.x - 48 * s, r.head[1] - 38 * s, F.x + 48 * s, F.y));
      }
      return r;
    };
    const hit = (a, c, pad = 0) => a[0] < c[2] - pad && c[0] < a[2] - pad && a[1] < c[3] - pad && c[1] < a[3] - pad;
    const area = a => Math.max(0, a[2] - a[0]) * Math.max(0, a[3] - a[1]);
    const inter = (a, c) => area([Math.max(a[0], c[0]), Math.max(a[1], c[1]), Math.min(a[2], c[2]), Math.min(a[3], c[3])]);
    const issues = {}, add = (k, t, msg) => { (issues[k] = issues[k] || []).push({ t: +t.toFixed(2), msg }); };
    let frames = 0;
    for (let t = 0; t <= CONFIG.duration - 0.01; t += STEP) {
      if (SCENES.some(s => s.enter && t >= s.start && t < s.start + s.enter.dur)) continue;
      rec = { text: [], figs: [] }; renderAt(t, g); frames++;
      const T = rec.text;
      for (let i = 0; i < T.length; i++) {
        const a = T[i];
        if (a.em > 0 && a.em < MIN_PX) add('small', t, `"${a.s}" ${a.em.toFixed(0)}px`);
        if (a.bx[0] < MARGIN || a.bx[1] < MARGIN || a.bx[2] > W - MARGIN || a.bx[3] > H - MARGIN) add('edge', t, `"${a.s}"`);
        for (let j = i + 1; j < T.length; j++) { const c = T[j]; if (a.s === c.s && Math.abs(a.bx[0] - c.bx[0]) < 2) continue;
          if (hit(a.bx, c.bx, 1)) add('textOnText', t, `"${a.s}" × "${c.s}"`); }
        for (const f of rec.figs) if (inter(a.bx, f) > 0.08 * area(a.bx)) add('textOnFigure', t, `"${a.s}"`);
      }
    }
    rec = null;
    const summary = {}; for (const k in issues) { const by = {}; issues[k].forEach(x => { (by[x.msg] = by[x.msg] || []).push(x.t); });
      summary[k] = Object.entries(by).map(([msg, ts]) => ({ msg, from: ts[0], to: ts.at(-1), frames: ts.length })); }
    return { frames, summary };
  }, { STEP, MIN_PX, MARGIN, ALPHA });
  res.errors = errs;
  if (outFile) require('fs').writeFileSync(outFile, JSON.stringify(res, null, 1));
  const n = Object.values(res.summary).reduce((a, v) => a + v.length, 0);
  console.log(`audited ${res.frames} frames every ${STEP}s: ${n} issue groups`);
  for (const [k, v] of Object.entries(res.summary)) { console.log(`\n[${k}]`); v.forEach(x => console.log(`  ${x.from}-${x.to}s (${x.frames}f) ${x.msg}`)); }
  if (errs.length) console.log('page errors:', errs);
  await b.close(); process.exit(n ? 1 : 0);
})();
