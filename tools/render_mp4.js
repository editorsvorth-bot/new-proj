/* Frame-exact MP4 render for gen-stickman-v2 pages (headless Chromium + ffmpeg).
   - Loads the voiceover into the page as the engine's voiceBuf and renders the engine's own offline mix
     (voice + enabled music/SFX), then writes it as WAV.
   - Calls renderAt(i / fps) for every frame at native resolution and pipes JPEG frames into ffmpeg.
   - Muxes H.264 (yuv420p, CRF 16) + AAC 192k with faststart.
   Usage: node tools/render_mp4.js <page.html> <voiceover audio> <out.mp4>                          */
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
const [page, voice, out] = process.argv.slice(2);
(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'render-'));
  const wavIn = path.join(tmp, 'voice.wav'), wavMix = path.join(tmp, 'mix.wav'), vid = path.join(tmp, 'video.mp4');
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', voice, '-ar', '44100', '-ac', '2', wavIn]);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(page)); await p.waitForTimeout(1500);
  // 1) audio: the engine's own mix with the voiceover as master clock
  const b64 = fs.readFileSync(wavIn).toString('base64');
  const info = await p.evaluate(async (b64) => {
    const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
    const ac = new OfflineAudioContext(2, 44100, 44100);
    voiceBuf = await ac.decodeAudioData(bytes.buffer);
    CONFIG.duration = voiceBuf.duration; buildScenes();
    mixBuf = await renderMix();
    window.__mix = [mixBuf.getChannelData(0), mixBuf.getChannelData(1)];
    return { duration: CONFIG.duration, fps: CONFIG.fps, w: CONFIG.width, h: CONFIG.height, len: mixBuf.length, sr: mixBuf.sampleRate };
  }, b64);
  console.log('audio mix:', info);
  const L = new Float32Array(info.len), R = new Float32Array(info.len), CH = 1 << 20;
  for (let o = 0; o < info.len; o += CH) {
    const [l, r] = await p.evaluate(([o, CH]) => {
      const enc = a => { const u = new Uint8Array(a.buffer, a.byteOffset, a.byteLength); let s = ''; for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000)); return btoa(s); };
      return [enc(window.__mix[0].slice(o, o + CH)), enc(window.__mix[1].slice(o, o + CH))];
    }, [o, CH]);
    L.set(new Float32Array(Buffer.from(l, 'base64').buffer.slice(0)), o); R.set(new Float32Array(Buffer.from(r, 'base64').buffer.slice(0)), o);
  }
  const pcm = Buffer.alloc(info.len * 4); for (let i = 0; i < info.len; i++) { pcm.writeInt16LE(Math.max(-1, Math.min(1, L[i])) * 32767 | 0, i * 4); pcm.writeInt16LE(Math.max(-1, Math.min(1, R[i])) * 32767 | 0, i * 4 + 2); }
  const hdr = Buffer.alloc(44); hdr.write('RIFF', 0); hdr.writeUInt32LE(36 + pcm.length, 4); hdr.write('WAVEfmt ', 8); hdr.writeUInt32LE(16, 16); hdr.writeUInt16LE(1, 20); hdr.writeUInt16LE(2, 22);
  hdr.writeUInt32LE(info.sr, 24); hdr.writeUInt32LE(info.sr * 4, 28); hdr.writeUInt16LE(4, 32); hdr.writeUInt16LE(16, 34); hdr.write('data', 36); hdr.writeUInt32LE(pcm.length, 40);
  fs.writeFileSync(wavMix, Buffer.concat([hdr, pcm]));
  // 2) video: every frame through the production renderAt
  const n = Math.round(info.duration * info.fps);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(info.fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', String(info.fps), vid], { stdio: ['pipe', 'inherit', 'inherit'] });
  await p.evaluate(([w, h]) => { const c = document.createElement('canvas'); c.width = w; c.height = h; window.__c = c; window.__g = c.getContext('2d'); }, [info.w, info.h]);
  const B = 10, t0 = Date.now();
  for (let i = 0; i < n; i += B) {
    const frames = await p.evaluate(([i, B, n, fps]) => { const o = []; for (let k = i; k < Math.min(n, i + B); k++) { renderAt(k / fps, window.__g); o.push(window.__c.toDataURL('image/jpeg', .96).split(',')[1]); } return o; }, [i, B, n, info.fps]);
    for (const f of frames) { if (!ff.stdin.write(Buffer.from(f, 'base64'))) await new Promise(r => ff.stdin.once('drain', r)); }
    if (i % 300 === 0) console.log(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise((res, rej) => ff.on('close', c => c ? rej(new Error('ffmpeg ' + c)) : res()));
  await b.close();
  // 3) mux
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', vid, '-i', wavMix, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', out]);
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('wrote', out, (fs.statSync(out).size / 1e6).toFixed(1) + ' MB', errs.length ? 'page errors: ' + errs.join('; ') : '');
})().catch(e => { console.error(e); process.exit(1); });
