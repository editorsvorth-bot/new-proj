/* ======================================================================================
   stickman-srt-video KIT: reusable helpers for SRT-timed gen-stickman-v2 videos.
   Concatenated BEFORE a video's scenes.js by assets/build_video.py. Never edit per video.
   The scenes file must define (see assets/scenes-template.js):
     C, SRT_TEXT            from scripts/srt_sync.py
     GY, BAR {x,w,h}, SHARES [..], GROUP [..]   spine bar geometry, shares and group labels
     WEAR [..] (optional)   crowd-slot looks for wear(): cap | capBack | beanie | bucket | bun | specs | none
   Every reveal is placed on the SRT clock: cue(n), wordAt(n, phrase). Palette: PAL only.
   ====================================================================================== */

/* ---------------- SRT clock: cues and words ---------------- */
const cue = n => C[n - 1];             // start of cue n (absolute seconds)
/** Estimated time a phrase is spoken inside cue n: its character position within the cue text, mapped onto the cue's
    duration (the SRT has no word timings). lead = seconds earlier, so visuals land with the word, not after it. */
const wordAt = (n, phrase, lead = .1) => { const s = SRT_TEXT[n - 1], i = s.toLowerCase().indexOf(phrase.toLowerCase());
  if (i < 0) throw new Error(`wordAt: "${phrase}" not in cue ${n}`); return cue(n) + (C[n] - C[n - 1]) * i / s.length - lead; };
/** Headline whose words appear one by one at their own times: words[], times[] (absolute), red = word indices. */
function headlineWords(g, t, words, times, x, y, o = {}) {
  const size = o.size || 84; g.save(); g.font = font('head', size); const sp = g.measureText(' ').width, ws = words.map(w => g.measureText(w).width); g.restore();
  let cx = o.align === 'center' ? x - (ws.reduce((a, b) => a + b, 0) + sp * (words.length - 1)) / 2 : x;
  words.forEach((w, i) => { headline(g, w, cx, y, prog(t, times[i], times[i] + .8), { size, red: (o.red || []).includes(i) ? [0] : [] }); cx += ws[i] + sp; });
}

/* ---------------- spine, props, characters, wearables, thread ---------------- */
/** The spine bar: one proportional bar split by SHARES (e.g. [.2, .2, .6]) with labels GROUP, placed by BAR {x, w, h}.
    col: colour per segment; p: build 0..1; nums: 0..1 (or per segment) for the % numbers; lab: label alpha per segment.
    o: {x, y, w, h} override (corner reprise), crack 0..1 (one bar splits into its segments), grow 0..1 (non-last segments grow in),
    noLabels, labSize. */
function spineBar(g, p, col, nums = 1, lab = [], o = {}) {
  if (p <= 0) return;
  const x0 = o.x ?? BAR.x, w = (o.w ?? BAR.w), y = o.y ?? GY, h = o.h ?? BAR.h, k = w / BAR.w, n = SHARES.length;
  const ws = SHARES.map(f => f * w), sp = E.out(clamp(p));
  if (o.crack !== undefined && o.crack <= 0) { fillPoly(g, rrectPoly(x0 + 4 * k, y, (w - 8 * k) * sp, h, 14 * k), col[Math.min(1, n - 1)]); return; }
  const cr = o.crack === undefined ? 1 : clamp(o.crack), gap = 4 * k * E.back(cr), hop = o.crack === undefined ? 0 : -16 * Math.sin(Math.PI * cr);
  let x = x0;
  for (let s = 0; s < n; s++) {
    const segP = o.crack !== undefined ? 1 : o.grow !== undefined ? (s < n - 1 ? E.out(clamp(o.grow)) : 1) : prog(sp, s * 0.18, s * 0.18 + 0.55);
    if (segP > 0) fillPoly(g, rrectPoly(x + gap, y + (s % 2 ? 0 : hop), (ws[s] - 2 * gap) * E.out(segP), h, 14 * k), col[s]);
    const na = Array.isArray(nums) ? nums[s] : nums;
    if (na > 0 && segP >= 1) {
      g.save(); g.globalAlpha *= na; g.font = font('head', Math.round(40 * k)); g.fillStyle = PAL.cream; g.textAlign = 'center'; g.textBaseline = 'middle';
      g.fillText(Math.round(SHARES[s] * 100) + '%', x + ws[s] / 2, y + h / 2 + 2); g.restore();
    }
    if ((lab[s] || 0) > 0 && !o.noLabels) subline(g, GROUP[s], x + ws[s] / 2, y + h + 52, lab[s], 0, { face: 'label', size: o.labSize || 30, align: 'center', color: col[s] === PAL.red ? PAL.red : PAL.ink });
    x += ws[s];
  }
}
/** Small corner reprise of the spine (top-right), one segment highlighted, optional word under it. */
function miniBar(g, focus, p, tagText) {
  if (p <= 0) return;
  const mid = SHARES.map((f, i) => SHARES.slice(0, i).reduce((a, b) => a + b, 0) + f / 2);
  fadeAlpha(g, E.out(p), () => {
    spineBar(g, 1, SHARES.map((_, i) => i === focus ? PAL.red : rgba(PAL.ink, .85)), 0, [], { x: 1300, y: 120, w: 480, h: 44, noLabels: true });
    if (tagText) subline(g, tagText, 1300 + 480 * mid[focus], 210, 1, 0, { face: 'label', size: 26, align: 'center', color: PAL.red });
  });
}
/** Screen prop (browser window): title bar in ink with cream title; body painted by fn(x, y, w, h). */
function browserWin(g, x, y, w, h, title, p, fn) {
  if (p <= 0) return;
  const q = E.back(clamp(p));
  popAt(g, x + w / 2, y + h / 2, q, () => {
    fillPoly(g, rrectPoly(x - 8, y - 8, w + 16, h + 16, 26), PAL.ink);
    fillPoly(g, rrectPoly(x, y + 56, w, h - 56, 18), PAL.cream);
    g.fillStyle = PAL.cream; [0, 1, 2].forEach(i => { g.beginPath(); g.arc(x + 30 + i * 28, y + 26, 8, 0, 7); g.fill(); });
    g.font = font('head', 30); g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(title, x + w / 2, y + 28);
    if (fn) fn(x, y + 56, w, h - 56);
  });
}
/** Checklist row: text, then a red tick badge drawing on at p. */
function checkRow(g, text, x, y, p, o = {}) {
  if (p <= 0) return;
  subline(g, text, x + 54, y + 13, prog(p, 0, .5), 0, { face: 'label', size: o.size || 34, color: PAL.ink });
  g.save(); g.beginPath(); g.arc(x + 20, y, 20, 0, 7); g.lineWidth = 4; g.strokeStyle = rgba(PAL.ink, .35); g.stroke(); g.restore();
  badge(g, x + 20, y, prog(p, .35, 1), 'tick', PAL.red, PAL.cream, 20);
}
/** A card with gray lines (a list of features) that can be crossed out. */
function featureCard(g, x, y, p, crossP) {
  if (p <= 0) return;
  popAt(g, x + 170, y + 120, E.back(clamp(p)), () => {
    fillPoly(g, rrectPoly(x, y, 340, 240, 22), PAL.cream);
    g.save(); tracePoly(g, rrectPoly(x, y, 340, 240, 22)); g.lineWidth = 6; g.strokeStyle = PAL.ink; g.stroke(); g.restore();
    g.font = font('head', 34); g.fillStyle = PAL.ink; g.textAlign = 'left'; g.fillText('FEATURES', x + 28, y + 58);
    for (let i = 0; i < 3; i++) { fillPoly(g, rrectPoly(x + 28, y + 92 + i * 44, 22, 22, 11), PAL.gray); fillPoly(g, rrectPoly(x + 66, y + 95 + i * 44, 220 - i * 40, 16, 8), rgba(PAL.gray, .6)); }
  });
  crossMark(g, x + 170, y + 120, 120, crossP, 20);
}
/* ---------------- wearables: hats, glasses, bags (all drawn in code, palette only) ---------------- */
function wear(g, F, r, kinds) {
  if (!r || !kinds) return; const list = [].concat(kinds).filter(k => k && k !== 'none'); if (!list.length) return;
  const P = F.pose || POSES.stand, fac = F.facing || 1, s = F.s || 1, body = F.color || PAL.ink;
  const dark = body === PAL.ink, hatC = dark ? PAL.gray : PAL.ink, ang = rad((P.head || 0) + (P.lean || 0) * .5) * fac;
  g.save(); g.globalAlpha *= F.alpha ?? 1; g.translate(r.head[0], r.head[1]); g.rotate(ang); g.scale(s, s);
  for (const k of list) {
    if (k === 'cap' || k === 'capBack') { const d = k === 'cap' ? fac : -fac;
      g.beginPath(); g.arc(0, -6, 39, Math.PI, 0); g.closePath(); g.fillStyle = hatC; g.fill();
      fillPoly(g, rrectPoly(d > 0 ? 18 : -70, -14, 52, 11, 5), hatC); g.beginPath(); g.arc(0, -45, 5, 0, 7); g.fill(); }
    if (k === 'beanie') { g.beginPath(); g.arc(0, -8, 40, Math.PI, 0); g.closePath(); g.fillStyle = hatC; g.fill();
      fillPoly(g, rrectPoly(-42, -16, 84, 14, 6), hatC); g.fillStyle = PAL.cream; g.fillRect(-40, -12, 80, 3);
      g.beginPath(); g.arc(0, -52, 11, 0, 7); g.fillStyle = hatC; g.fill(); }
    if (k === 'bucket') { fillPoly(g, [[-28, -58], [28, -58], [36, -22], [-36, -22]], hatC); fillPoly(g, rrectPoly(-52, -26, 104, 12, 6), hatC); }
    if (k === 'bun') { g.beginPath(); g.arc(-fac * 18, -40, 16, 0, 7); g.fillStyle = dark ? PAL.gray : PAL.ink; g.fill(); }
    if (k === 'specs') { const ex = fac * 8, c = dark ? PAL.cream : PAL.ink; g.lineWidth = 4; g.strokeStyle = c;
      [[ex - 9, -6], [ex + 11, -6]].forEach(([x, y]) => { g.beginPath(); g.arc(x, y, 9.5, 0, 7); g.stroke(); });
      g.beginPath(); g.moveTo(ex - 0.5, -7); g.lineTo(ex + 1.5, -7); g.moveTo(ex - (fac > 0 ? 18.5 : -20.5), -7); g.lineTo(-fac * 32, -12); g.stroke(); }
  }
  g.restore();
}
/** Any figure + its wearables (F.wear). */
function person(g, F) {
  const seed = F.seed ?? Math.round((F.x || 0) / 131), per = 3.4 + (seed % 5) * .37;
  const blink = ((NOW + seed * .77) % per) < .13 && ['neutral', 'happy', 'confused'].includes(F.expr || 'neutral');
  const r = drawStickman(g, blink ? Object.assign({}, F, { expr: 'closed' }) : F); wear(g, F, r, F.wear); return r;
}
/** Briefcase standing on the ground (SALES), or carried at a hand point. */
function briefcase(g, x, y, s = 1, a = 1) {
  if (a <= 0) return; fadeAlpha(g, a, () => {
    g.save(); g.translate(x, y); g.scale(s, s);
    g.lineWidth = 7; g.strokeStyle = PAL.ink; g.beginPath(); g.arc(0, -56, 14, Math.PI, 0); g.stroke();
    fillPoly(g, rrectPoly(-42, -56, 84, 56, 10), PAL.ink); g.fillStyle = PAL.cream; g.fillRect(-42, -36, 84, 4); g.fillRect(-6, -40, 12, 10);
    g.restore(); });
}
/** Shopping bag held at a hand point (the Definitely Buy purchase), product peeking out. */
function shopBag(g, hx, hy, s = 1, q = 1) {
  if (q <= 0) return; popAt(g, hx, hy, E.back(clamp(q)), () => {
    g.save(); g.translate(hx, hy); g.scale(s, s);
    fillPoly(g, rrectPoly(-18, 4, 30, 24, 4), PAL.ink); fillPoly(g, rrectPoly(-6, 4, 7, 24, 2), PAL.red);
    fillPoly(g, [[-34, 22], [34, 22], [28, 92], [-28, 92]], PAL.cream);
    tracePoly(g, [[-34, 22], [34, 22], [28, 92], [-28, 92]]); g.lineWidth = 6; g.strokeStyle = PAL.ink; g.stroke();
    g.beginPath(); g.moveTo(-16, 22); g.quadraticCurveTo(0, -6, 16, 22); g.stroke();
    g.restore(); });
}

/* ---------------- character kits: each group acts like the script describes it ---------------- */
function neckOf(F, r) { const P = F.pose || POSES.stand, L = rad(P.lean || 0), fac = F.facing || 1, hd = (RIG.neck + RIG.head) * (F.s || 1);
  return [r.head[0] - Math.sin(L) * hd * fac, r.head[1] + Math.cos(L) * hd]; }
/** SALES: ink figure with a red tie (knot + blade follow the torso). */
function salesman(g, F) {
  const r = person(g, Object.assign({ color: PAL.ink }, F)); if ((F.draw ?? 1) < .6) return r;
  const s = F.s || 1, n = neckOf(F, r), h = r.hip, L = Math.hypot(h[0] - n[0], h[1] - n[1]) || 1, ux = (h[0] - n[0]) / L, uy = (h[1] - n[1]) / L, px = -uy, py = ux;
  const P = (a, b) => [n[0] + ux * a * s + px * b * s, n[1] + uy * a * s + py * b * s];
  // follow-through: the blade swings a little around the knot, lagging the body (lean + a slow pendulum)
  const sw = .07 * Math.sin(NOW * 2.4 + (F.seed || 0)) + ((F.pose && F.pose.lean) || 0) * .012 * (F.facing || 1);
  const k = P(20, 0), rot = ([x, y]) => [k[0] + (x - k[0]) * Math.cos(sw) - (y - k[1]) * Math.sin(sw), k[1] + (x - k[0]) * Math.sin(sw) + (y - k[1]) * Math.cos(sw)];
  g.save(); g.globalAlpha *= F.alpha ?? 1;
  fillPoly(g, [P(8, -8), P(8, 8), P(20, 7), P(20, -7)], PAL.red);
  fillPoly(g, [P(20, -6), P(20, 6), P(64, 12), P(80, 0), P(64, -12)].map(rot), PAL.red);
  g.restore(); return r;
}
/** NEVER BUY: wears its hat; 'can't pay' is shown with an empty wallet (emptyWallet). */
function neverBuyer(g, F) { return person(g, F); }
/** DEFINITELY BUY: phone in hand with a ticked screen (already researched, already decided). */
function sureBuyer(g, F, ph = 1) {
  const r = person(g, F); if (ph <= 0) return r;
  const s = F.s || 1, q = E.back(clamp(ph)), [hx, hy] = r.handF;
  popAt(g, hx, hy - 18 * s, q, () => {
    fillPoly(g, rrectPoly(hx - 17 * s, hy - 48 * s, 34 * s, 58 * s, 8 * s), PAL.ink);
    fillPoly(g, rrectPoly(hx - 12 * s, hy - 42 * s, 24 * s, 42 * s, 4 * s), PAL.cream);
    strokeOn(g, [[hx - 7 * s, hy - 22 * s], [hx - 2 * s, hy - 16 * s], [hx + 7 * s, hy - 29 * s]], prog(ph, .4, 1), PAL.red, 4 * s);
  });
  return r;
}
/** CONFUSED: pacing on the spot, turning left/right, alternating head-scratch and shrug. Returns {x, facing, pose}. */
function pacing(x0, t, i, on = 1) {
  const ph = t * 1.4 + i * 1.7, x = x0 + Math.sin(ph) * 18 * on, facing = Math.cos(ph) >= 0 ? 1 : -1;
  const alt = .5 + .5 * Math.sin(t * 1.1 + i * 2.3);
  return { x, facing, pose: poseMix(POSES.stand, poseMix(POSES.shrug, POSES.think, alt), on) };
}
/** A pitch: a speech bubble carrying a product (box with a red band). */
function pitchBubble(g, x, y, s, col, a = 1) {
  if (a <= 0) return;
  fadeAlpha(g, a, () => {
    g.beginPath(); g.arc(x, y, 38 * s, 0, 7); g.fillStyle = PAL.cream; g.fill(); g.lineWidth = 5; g.strokeStyle = col; g.stroke();
    fillPoly(g, rrectPoly(x - 17 * s, y - 14 * s, 34 * s, 28 * s, 5 * s), col === PAL.gray ? PAL.gray : PAL.ink);
    fillPoly(g, rrectPoly(x - 4 * s, y - 14 * s, 8 * s, 28 * s, 2), col === PAL.gray ? rgba(PAL.cream, .7) : PAL.red);
  });
}
function linePts2(x0, y0, x1, y1) { const o = []; for (let i = 0; i < KN; i++) o.push([lerp(x0, x1, i / (KN - 1)), lerp(y0, y1, i / (KN - 1))]); return o; }

/** A red X that lands like a rubber stamp. */
function stampX(g, x, y, r, p) { if (p <= 0) return; const q = lerp(1.7, 1, E.out(clamp(p)));
  fadeAlpha(g, clamp(p * 3), () => popAt(g, x, y, q, () => crossMark(g, x, y, r, 1, 20))); }

let THREAD = [], THC = [930, 430]; const LYS = 430;
/** Deterministic tangle (a knot of confusion) with N points; untangles into a straight arrow shaft. */
const KN = 240;
function knotPts(cx, cy, r) {
  const o = [];
  for (let i = 0; i < KN; i++) { const a = i / (KN - 1) * Math.PI * 10, rr = r * (0.55 + 0.45 * Math.sin(a * 1.37 + 0.8));
    o.push([cx + Math.cos(a) * rr * 1.25, cy + Math.sin(a * 1.13) * rr * 0.8]); }
  return o;
}
function linePts(x0, x1, y) { const o = []; for (let i = 0; i < KN; i++) o.push([lerp(x0, x1, i / (KN - 1)), y]); return o; }


/* ---------------- Phase A props (script ideas drawn as objects) ---------------- */
let NOW = 0;   // absolute time of the frame being drawn (set at the top of every scene draw); used for blinks
/** Empty wallet held at a hand: opens, then tips upside down (nothing inside). */
function emptyWallet(g, hx, hy, s, p, tip) {
  if (p <= 0) return;
  popAt(g, hx, hy, E.back(clamp(p)), () => {
    g.save(); g.translate(hx, hy - 10 * s); g.rotate(-.2 + tip * 2.6); g.scale(s, s);
    fillPoly(g, rrectPoly(-38, -26, 76, 52, 10), PAL.ink);
    fillPoly(g, rrectPoly(-30, -18, 60, 30, 6), PAL.cream);
    g.strokeStyle = rgba(PAL.ink, .35); g.lineWidth = 3; g.beginPath(); g.moveTo(-24, -4); g.lineTo(24, -4); g.stroke();
    g.restore();
  });
}
/** Shopping cart with the product sitting in it. */
function cart(g, x, y, s, p) {
  if (p <= 0) return;
  popAt(g, x, y, E.back(clamp(p)), () => {
    g.save(); g.translate(x, y); g.scale(s, s); g.lineCap = g.lineJoin = 'round';
    fillPoly(g, rrectPoly(-28, -86, 46, 38, 6), PAL.ink); fillPoly(g, rrectPoly(-9, -86, 9, 38, 2), PAL.red);
    g.strokeStyle = PAL.ink; g.lineWidth = 9;
    g.beginPath(); g.moveTo(-96, -96); g.lineTo(-70, -96); g.lineTo(-52, -20); g.lineTo(52, -20); g.lineTo(66, -70); g.lineTo(-62, -70); g.stroke();
    g.fillStyle = PAL.ink; [-38, 40].forEach(wx => { g.beginPath(); g.arc(wx, 4, 13, 0, 7); g.fill(); });
    g.restore();
  });
}
/** FEATURES scroll hanging from a hand, unrolled to length L. */
function featureScroll(g, hx, hy, L) {
  if (L <= 4) return; const w = 170, x = hx - w / 2;
  fillPoly(g, rrectPoly(x, hy, w, L, 8), PAL.cream);
  g.save(); tracePoly(g, rrectPoly(x, hy, w, L, 8)); g.lineWidth = 5; g.strokeStyle = PAL.ink; g.stroke(); g.restore();
  g.save(); g.beginPath(); g.rect(x, hy, w, L); g.clip();
  g.font = font('head', 26); g.fillStyle = PAL.ink; g.textAlign = 'center'; g.fillText('FEATURES', hx, hy + 44);
  for (let k = 0; k < 8; k++) fillPoly(g, rrectPoly(x + 22, hy + 70 + k * 30, 126 - (k % 3) * 26, 12, 6), rgba(PAL.gray, .7));
  g.restore();
  fillPoly(g, rrectPoly(x - 14, hy - 10, w + 28, 20, 10), PAL.ink);
  fillPoly(g, rrectPoly(x - 14, hy + L - 10, w + 28, 20, 10), PAL.ink);
}
/** Small picture for a question bubble (drawn inside a cream disc). */
function qIcon(g, kind, x, y, p) {
  if (p <= 0) return;
  popAt(g, x, y, E.back(clamp(p)), () => {
    g.beginPath(); g.arc(x, y, 34, 0, 7); g.fillStyle = PAL.cream; g.fill(); g.lineWidth = 5; g.strokeStyle = PAL.ink; g.stroke();
    g.save(); g.translate(x, y); g.lineCap = g.lineJoin = 'round';
    const box = (bx, by, c = PAL.ink) => { fillPoly(g, rrectPoly(bx - 12, by - 10, 24, 20, 4), c); };
    if (kind === 'need') { box(-6, 6); g.font = font('head', 26); g.fillStyle = PAL.red; g.textAlign = 'center'; g.fillText('?', 14, -2); }
    if (kind === 'whom') [-11, 11].forEach(sx => { fillPoly(g, [[sx - 9, 14], [sx + 9, 14], [sx + 9, -2], [sx, -12], [sx - 9, -2]], PAL.ink); g.fillStyle = PAL.cream; g.fillRect(sx - 3, 4, 6, 10); });
    if (kind === 'use') { box(0, 8, PAL.gray); g.fillStyle = PAL.gray; [[-10, -12], [2, -18], [12, -10]].forEach(([dx, dy]) => { g.beginPath(); g.arc(dx, dy, 3, 0, 7); g.fill(); }); }
    if (kind === 'when') { g.beginPath(); g.arc(0, 0, 18, 0, 7); g.lineWidth = 4; g.strokeStyle = PAL.ink; g.stroke(); g.beginPath(); g.moveTo(0, 0); g.lineTo(0, -12); g.moveTo(0, 0); g.lineTo(9, 4); g.stroke(); }
    if (kind === 'else') { box(-11, 4); box(11, 4, PAL.gray); }
    g.restore();
  });
}
/** Question bubble with its picture on the left; a = emphasis (older questions dim). */
function qBubble(g, text, x, y, tx, ty, p, icon, a = 1) {
  if (p <= 0) return;
  fadeAlpha(g, a, () => {
    g.save(); g.font = font('label', 32); const w = g.measureText(text).width + 48; g.restore();
    speechBubble(g, text, x + 22, y, tx, ty, p, { size: 32 });
    qIcon(g, icon, x + 22 - w / 2 - 20, y, prog(p, .2, 1));
  });
}
/** Thick straight band between two points (the thread becoming the bar). */
function band(g, a, b, th, col) { const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L * th / 2, ny = dx / L * th / 2;
  fillPoly(g, [[a[0] + nx, a[1] + ny], [b[0] + nx, b[1] + ny], [b[0] - nx, b[1] - ny], [a[0] - nx, a[1] - ny]], col); }

/* role aliases (the kit's names are from the first video; use whichever reads better in a new script) */
const tieFigure = (g, F) => salesman(g, F);          // the helper / seller / expert: ink figure with a red tie
const phoneHolder = (g, F, ph = 1) => sureBuyer(g, F, ph);   // someone who has already researched
