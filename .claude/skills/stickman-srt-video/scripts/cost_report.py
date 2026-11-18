"""Token cost of a Claude Code session, per user request, from its transcript(s).

  python cost_report.py <session.jsonl> [more.jsonl ...] [--in 4 --out 20 --read 0.20 --w5 5 --w1h 8]

Prices are $ per million tokens; defaults are Claude Opus 5.5 API rates (input 4, output 20, cache read 0.20,
5-minute cache write 5, 1-hour cache write 8). Check current prices before quoting them. Transcripts live under
~/.claude/projects/<project>/<session-id>.jsonl (a session that changed folders has one file per folder).
Each API call is counted once (deduplicated by message id). On a subscription this is API-equivalent cost.
"""
import json, sys

args = sys.argv[1:]; P = {'in': 4.0, 'out': 20.0, 'read': .20, 'w5': 5.0, 'w1h': 8.0}; files = []
i = 0
while i < len(args):
    if args[i].startswith('--'): P[args[i][2:]] = float(args[i + 1]); i += 2
    else: files.append(args[i]); i += 1
rows = []
for f in files:
    for line in open(f, encoding='utf-8'):
        try: rows.append(json.loads(line))
        except ValueError: pass
rows.sort(key=lambda r: r.get('timestamp', ''))
def text(r):
    c = r.get('message', {}).get('content')
    if isinstance(c, str): return c
    if isinstance(c, list):
        if any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c): return None
        return ' '.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text') or None
stages, seen = [], set()
for r in rows:
    if r.get('type') == 'user' and not r.get('isMeta') and not r.get('isSidechain'):
        t = text(r)
        if t and not t.lstrip().startswith('<') and 'Stop hook feedback' not in t:
            stages.append({'q': ' '.join(t.split())[:70], 'calls': 0, 'in': 0, 'out': 0, 'read': 0, 'w5': 0, 'w1h': 0})
    if r.get('type') == 'assistant' and stages:
        m = r.get('message', {}); u = m.get('usage')
        if not u or m.get('id') in seen: continue
        seen.add(m.get('id')); s = stages[-1]; cc = u.get('cache_creation') or {}
        w1, w5 = cc.get('ephemeral_1h_input_tokens'), cc.get('ephemeral_5m_input_tokens')
        if w1 is None and w5 is None: w5, w1 = u.get('cache_creation_input_tokens', 0), 0
        s['calls'] += 1; s['in'] += u.get('input_tokens', 0); s['out'] += u.get('output_tokens', 0)
        s['read'] += u.get('cache_read_input_tokens', 0); s['w5'] += w5 or 0; s['w1h'] += w1 or 0
cost = lambda s: sum(s[k] * P[k] for k in P) / 1e6
print('| # | Request | Calls | Output | Cache read | Cache write | USD |\n|---|---|---:|---:|---:|---:|---:|')
tot = {k: 0 for k in ('calls', 'in', 'out', 'read', 'w5', 'w1h')}
for n, s in enumerate([s for s in stages if s['calls']], 1):
    print(f"| {n} | {s['q']} | {s['calls']} | {s['out']:,} | {s['read']:,} | {s['w5'] + s['w1h']:,} | ${cost(s):.2f} |")
    for k in tot: tot[k] += s[k]
print(f"| | **Total** | **{tot['calls']}** | **{tot['out']:,}** | **{tot['read']:,}** | **{tot['w5'] + tot['w1h']:,}** | **${cost(tot):.2f}** |")
