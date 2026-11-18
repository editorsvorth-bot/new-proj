"""Wow / understanding scorecard for a stickman-srt-video build. Run after EVERY render (Stage 8).

  python scorecard.py init  <video dir>                     -> writes <video>/scores.input.json to fill in (one row per scene)
  python scorecard.py write <video dir> --label "v3 final"  -> appends the filled scores to <video>/SCORES.json (history)
                                                              and writes <video>/SCORES.md (latest table + change since
                                                              the previous version + history)

Scores are 0-10 per scene on both axes, judged with references/quality.md (a first-time viewer, muted, not knowing
the script's language). Every score under 10 needs a reason. Scene ids/titles are read from scenes.js.
"""
import datetime, json, os, re, sys

def scenes_of(vdir):
    src = open(os.path.join(vdir, 'scenes.js'), encoding='utf-8').read()
    out = []
    for m in re.finditer(r"/\*\s*(\d+)\.\s*([^*]+?)\*/\s*\{\s*id:\s*'([^']+)'", src):
        title = re.split(r'\s{2,}|\(cue', m.group(2).strip())[0].strip()
        out.append({'id': m.group(3), 'scene': f"{m.group(1)} {title.title()}"})
    if not out:
        out = [{'id': i, 'scene': i} for i in re.findall(r"\{\s*id:\s*'([^']+)'", src)]
    return out

def init(vdir):
    path = os.path.join(vdir, 'scores.input.json')
    rows = [dict(s, wow=None, understanding=None, why='') for s in scenes_of(vdir)]
    json.dump({'label': '', 'mute_test': [{'question': '', 'answerable_from_frames': None}], 'scenes': rows}, open(path, 'w'), indent=1)
    print('fill in', path, '(wow / understanding 0-10, a reason for anything under 10), then run: scorecard.py write', vdir)

def avg(rows, k):
    v = [r[k] for r in rows if isinstance(r.get(k), (int, float))]
    return round(sum(v) / len(v), 2) if v else None

def write(vdir, label):
    inp = json.load(open(os.path.join(vdir, 'scores.input.json')))
    rows = inp['scenes']
    missing = [r['scene'] for r in rows if r.get('wow') is None or r.get('understanding') is None]
    if missing: sys.exit('score every scene first: ' + ', '.join(missing))
    vague = [r['scene'] for r in rows if (r['wow'] < 10 or r['understanding'] < 10) and not r.get('why', '').strip()]
    if vague: sys.exit('give a reason for every score under 10: ' + ', '.join(vague))
    hist_path = os.path.join(vdir, 'SCORES.json')
    hist = json.load(open(hist_path)) if os.path.exists(hist_path) else []
    entry = {'label': label or inp.get('label') or f'v{len(hist) + 1}', 'date': datetime.date.today().isoformat(),
             'wow': avg(rows, 'wow'), 'understanding': avg(rows, 'understanding'), 'scenes': rows, 'mute_test': inp.get('mute_test', [])}
    prev = hist[-1] if hist else None
    hist.append(entry); json.dump(hist, open(hist_path, 'w'), indent=1)
    pv = {r['id']: r for r in (prev or {}).get('scenes', [])}
    d = lambda a, b: '' if b is None else (f" ({a - b:+.1f})" if abs(a - b) > 1e-9 else ' (=)')
    L = [f"# Wow / understanding: {entry['label']} ({entry['date']})", '',
         'Judged as a first-time viewer, muted, without knowing the script\'s language (rubric: stickman-srt-video references/quality.md).', '',
         '| Scene | Wow | Understanding | Why not 10 |', '|---|---:|---:|---|']
    for r in rows:
        p = pv.get(r['id'], {})
        L.append(f"| {r['scene']} | {r['wow']}{d(r['wow'], p.get('wow'))} | {r['understanding']}{d(r['understanding'], p.get('understanding'))} | {r.get('why', '') or '—'} |")
    L.append(f"| **Overall** | **{entry['wow']}**{d(entry['wow'], (prev or {}).get('wow'))} | **{entry['understanding']}**{d(entry['understanding'], (prev or {}).get('understanding'))} | |")
    mt = [m for m in entry['mute_test'] if m.get('question')]
    if mt:
        L += ['', '**Muted viewing test** (answerable from the frames alone?)', ''] + [f"- {m['question']}: {'yes' if m.get('answerable_from_frames') else 'NO'}" for m in mt]
    L += ['', '## History', '', '| Version | Date | Wow | Understanding |', '|---|---|---:|---:|'] + [f"| {h['label']} | {h['date']} | {h['wow']} | {h['understanding']} |" for h in hist]
    open(os.path.join(vdir, 'SCORES.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))

if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] not in ('init', 'write'): sys.exit(__doc__)
    label = sys.argv[sys.argv.index('--label') + 1] if '--label' in sys.argv else ''
    init(sys.argv[2]) if sys.argv[1] == 'init' else write(sys.argv[2], label)
