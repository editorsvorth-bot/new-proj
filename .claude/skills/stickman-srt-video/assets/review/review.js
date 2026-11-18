/* stickman-srt-video: storyboard approval panel (added by build_video.py --mode review).
   Each storyboard board gets: its spoken line, Approve / Needs changes, and its own comment box.
   Decisions are stored in the page's db (collection "reviews", one document per board: reviews/board-01 ...)
   so Claude can read them with ArtifactData and revise only the boards that need it.
   Publish with capabilities {db: {}, user: {}}. */
(function () {
  const css = `
  #rvBar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; display: flex; flex-wrap: wrap; gap: 10px 16px; align-items: center;
    background: #141414; color: #F4EDE0; padding: 12px 16px; border-radius: 8px; margin: 14px 0 6px; font: 600 14px "Segoe UI", system-ui, sans-serif; }
  #rvBar b { font: 900 18px "Arial Black", "Segoe UI Black", sans-serif; letter-spacing: .02em; }
  #rvBar .rvCount span { display: inline-block; min-width: 1.4em; text-align: center; }
  #rvBar .rvNote { font-weight: 400; color: rgba(244,237,224,.75); flex: 1 1 260px; }
  #rvBar button { font: 700 13px "Segoe UI", system-ui, sans-serif; border: 0; border-radius: 999px; padding: 7px 14px; cursor: pointer; background: #F4EDE0; color: #141414; }
  #rvBar button:focus-visible, .rvCtl button:focus-visible, .rvCtl textarea:focus-visible { outline: 3px solid #D62828; outline-offset: 2px; }
  .sbCell { cursor: default; }
  .sbCell canvas { cursor: pointer; }
  .rvCtl { display: grid; gap: 7px; padding: 8px 8px 10px; background: #F4EDE0; border-top: 1px solid rgba(20,20,20,.12); font: 13px "Segoe UI", system-ui, sans-serif; color: #141414; }
  .rvCtl .rvLine { color: #5a5550; font-style: italic; line-height: 1.35; }
  .rvCtl .rvLine b { font-style: normal; color: #141414; }
  .rvBtns { display: flex; gap: 6px; flex-wrap: wrap; }
  .rvBtns button { flex: 1 1 auto; font: 700 12.5px "Segoe UI", system-ui, sans-serif; padding: 7px 10px; border-radius: 6px; cursor: pointer;
    border: 2px solid #141414; background: transparent; color: #141414; }
  .rvBtns button[aria-pressed="true"].ok { background: #141414; color: #F4EDE0; }
  .rvBtns button[aria-pressed="true"].fix { background: #D62828; border-color: #D62828; color: #F4EDE0; }
  .rvCtl textarea { width: 100%; box-sizing: border-box; min-height: 58px; resize: vertical; font: 13px "Segoe UI", system-ui, sans-serif;
    border: 1.5px solid rgba(20,20,20,.35); border-radius: 6px; padding: 7px 8px; background: #fffaf0; color: #141414; }
  .rvRow { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
  .rvRow button { font: 700 12.5px "Segoe UI", system-ui, sans-serif; border: 0; border-radius: 6px; padding: 6px 12px; cursor: pointer; background: #141414; color: #F4EDE0; }
  .rvRow button:disabled { opacity: .45; cursor: default; }
  .rvState { font-size: 12px; color: #6b655e; }
  .sbCell.rv-ok { border-color: #141414; } .sbCell.rv-fix { border-color: #D62828; }`;
  const st = document.createElement('style'); st.textContent = css; document.head.append(st);

  const pad = n => String(n).padStart(2, '0');
  const idOf = i => 'board-' + pad(i + 1);
  const fmtT = s => `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, '0')}`;
  const cueAt = t => { if (typeof C === 'undefined') return -1; for (let i = 0; i < C.length - 1; i++) if (t >= C[i] && t < C[i + 1]) return i; return C.length - 2; };

  let db = null, uid = null, canWrite = true, rows = {}, ui = [];
  const bar = document.createElement('div'); bar.id = 'rvBar';
  bar.innerHTML = `<b>STORYBOARD APPROVAL</b><span class="rvCount"><span id="rvOk">0</span> approved · <span id="rvFix">0</span> need changes · <span id="rvPend">0</span> to review</span>
    <span class="rvNote" id="rvNote">Approve each board or mark it "Needs changes" and say what to change. Claude reads these and revises only the flagged boards.</span>
    <button type="button" id="rvAll">Approve all unreviewed</button>`;

  function counts() {
    let ok = 0, fix = 0; ui.forEach(u => { const s = (rows[u.id] || {}).status; if (s === 'approved') ok++; else if (s === 'changes') fix++; });
    document.getElementById('rvOk').textContent = ok; document.getElementById('rvFix').textContent = fix; document.getElementById('rvPend').textContent = ui.length - ok - fix;
  }
  function paint(u) {
    const r = rows[u.id] || {};
    u.ok.setAttribute('aria-pressed', String(r.status === 'approved')); u.fix.setAttribute('aria-pressed', String(r.status === 'changes'));
    u.cell.classList.toggle('rv-ok', r.status === 'approved'); u.cell.classList.toggle('rv-fix', r.status === 'changes');
    if (document.activeElement !== u.ta && !u.dirty) u.ta.value = r.comment || '';
    u.state.textContent = u.busy ? 'Saving…' : (r.updatedAt ? 'Saved ' + new Date(r.updatedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : (db ? 'Not reviewed yet' : ''));
    u.save.disabled = !db || !canWrite || u.busy || !u.dirty;
    [u.ok, u.fix, u.ta].forEach(el => el.disabled = !db || !canWrite);
  }
  async function write(u, patch) {
    if (!db || !canWrite || u.busy) return;
    u.busy = true; paint(u);
    const f = STORYBOARD[u.i], cur = rows[u.id] || {};
    const doc = { board: u.i + 1, boardId: u.id, title: f.title, t: f.t, cue: cueAt(f.t) + 1,
      status: patch.status ?? cur.status ?? 'pending', comment: patch.comment ?? cur.comment ?? '', by: uid || '', updatedAt: new Date().toISOString() };
    try { await db.doc('reviews/' + u.id).set(doc); rows[u.id] = doc; u.dirty = false; }
    catch (e) { u.state.textContent = e && e.code === 'invalid_argument' ? 'You can view but not change approvals here.' : 'Could not save (' + ((e && e.code) || 'error') + '). Try again.';
      if (e && e.code === 'invalid_argument') canWrite = false; u.busy = false; ui.forEach(paint); return; }
    u.busy = false; paint(u); counts();
  }

  function attach() {
    const cells = document.querySelectorAll('.sbCell');
    if (!cells.length || typeof STORYBOARD === 'undefined' || cells.length < STORYBOARD.length) return false;
    const sb = document.getElementById('sb'); sb.insertBefore(bar, document.getElementById('sbGrid'));
    cells.forEach((cell, i) => {
      const f = STORYBOARD[i]; if (!f) return; const ci = cueAt(f.t);
      const box = document.createElement('div'); box.className = 'rvCtl';
      const line = (typeof SRT_TEXT !== 'undefined' && ci >= 0) ? SRT_TEXT[ci] : '';
      box.innerHTML = `<div class="rvLine"><b>Board ${i + 1} · cue ${ci + 1} · ${fmtT(f.t)}</b><br>${line.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]))}</div>
        <div class="rvBtns"><button type="button" class="ok" aria-pressed="false">Approve</button><button type="button" class="fix" aria-pressed="false">Needs changes</button></div>
        <label class="rvState" for="rvC${i}">Comment for board ${i + 1}</label>
        <textarea id="rvC${i}" placeholder="What should change on this board? (optional)"></textarea>
        <div class="rvRow"><span class="rvState"></span><button type="button" class="sv">Save comment</button></div>`;
      box.addEventListener('click', e => e.stopPropagation());
      cell.append(box);
      const u = { i, id: idOf(i), cell, ok: box.querySelector('.ok'), fix: box.querySelector('.fix'), ta: box.querySelector('textarea'),
        save: box.querySelector('.sv'), state: box.querySelector('.rvRow .rvState'), dirty: false, busy: false };
      u.ok.onclick = () => write(u, { status: 'approved', comment: u.ta.value });
      u.fix.onclick = () => { write(u, { status: 'changes', comment: u.ta.value }); u.ta.focus(); };
      u.ta.oninput = () => { u.dirty = true; paint(u); };
      u.save.onclick = () => write(u, { comment: u.ta.value });
      ui.push(u); paint(u);
    });
    document.getElementById('rvAll').onclick = async () => { for (const u of ui) if (!(rows[u.id] || {}).status || rows[u.id].status === 'pending') await write(u, { status: 'approved' }); };
    counts(); return true;
  }

  async function connect() {
    const note = document.getElementById('rvNote');
    const timer = setTimeout(() => { if (!db) note.textContent = 'Connecting to the approval store… if this stays, open the published page while signed in.'; }, 10000);
    try {
      if (!window.claude || !window.claude.use) throw 0;
      db = await window.claude.use('db');
      const user = await window.claude.use('user');
      if (user) { uid = await user.id(); const w = await user.can('data.write'); if (w === false) canWrite = false; }
    } catch (e) { db = null; }
    if (!db) { clearTimeout(timer); note.textContent = 'Saving approvals is not available in this view. Open the published page while signed in to approve or comment.'; ui.forEach(paint); return; }
    if (!canWrite) note.textContent = 'You can see the approvals, but your access level cannot change them.';
    db.collection('reviews').onSnapshot(snap => {
      clearTimeout(timer); rows = {}; snap.docs.forEach(d => { if (d.exists) rows[d.id] = d.data(); }); ui.forEach(paint); counts();
    }, e => { clearTimeout(timer); note.textContent = 'The approval store stopped answering (' + e.code + '). Reload the page to reconnect.'; });
    ui.forEach(paint);
  }

  let tries = 0;
  (function wait() { if (attach()) connect(); else if (tries++ < 100) setTimeout(wait, 100); })();
})();
