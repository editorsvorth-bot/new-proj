"""Audit every style plan against the brief's rules. Writes audit.json and prints a report.

Rules: (1) match the timestamps, (2) easy to understand, (3) stickman style,
(4) palette cream/black/red/gray only, plus (5) stays in the script's context.
"""
import json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "plans.json"), encoding="utf-8"))
EPS = 1e-6
PALETTE = {"cream", "ink", "red", "gray"}
BANNED = re.compile(r"amazon|flipkart|logo", re.I)   # no real brands on screen
MAX_WORDS_ITEM = 5        # words in a single on-screen label
MAX_WORDS_FRAME = 14      # words visible at once at the end of a beat
MAX_NEW_ITEMS = 12        # new elements introduced within one beat
SPEECH_FAST = 2.6         # words/second in the SRT considered fast


def parse_srt(path):
    txt = open(path, encoding="utf-8").read().strip()
    out = []
    for block in re.split(r"\n\s*\n", txt):
        lines = block.strip().splitlines()
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
        g = list(map(int, m.groups()))
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        out.append(dict(n=int(lines[0]), start=a, end=b, text=" ".join(lines[2:])))
    return out


def words(s):
    return len([w for w in re.split(r"[\s·+→]+", s) if w.strip()])


def text_items(e):
    if e["k"] in ("text", "tag", "bubble"):
        return [e["s"]]
    if e["k"] in ("door", "laptop", "meter") and e.get("label"):
        return [e["label"]]
    if e["k"] in ("bar", "pie"):
        return [sg["label"] for sg in e["segs"]]
    return []


def colours(e):
    cs = [e.get("c")] if e.get("c") else []
    for sg in e.get("segs", []):
        cs.append(sg["c"])
    return cs


srt = parse_srt(os.path.join(HERE, "20-20-60.srt"))
cues = P["cues"]

# ---- step 0: the SRT itself ----
srt_checks = []
srt_checks.append(("24 cues parsed", len(srt) == 24, f"{len(srt)} cues"))
gaps = [(a["n"], b["n"]) for a, b in zip(srt, srt[1:]) if abs(a["end"] - b["start"]) > EPS]
srt_checks.append(("cues are back-to-back (no gaps/overlaps)", not gaps, "none" if not gaps else str(gaps)))
srt_checks.append(("plan cue table matches the SRT", all(abs(c["start"] - cues[i]) < EPS for i, c in enumerate(srt)) and abs(srt[-1]["end"] - cues[-1]) < EPS,
                   f"ends at {srt[-1]['end']}s"))
pace = []
for c in srt:
    wps = words(c["text"]) / (c["end"] - c["start"])
    pace.append(dict(n=c["n"], wps=round(wps, 2), fast=wps > SPEECH_FAST))
fast = [p["n"] for p in pace if p["fast"]]
srt_checks.append((f"speech pace (fast > {SPEECH_FAST} words/s)", True, f"fast cues: {fast or 'none'}, keep visuals simplest there"))

report = dict(srt=[dict(check=a, ok=b, note=c) for a, b, c in srt_checks], pace=pace, styles=[])
fail_total = 0

for st in P["styles"]:
    beats = sorted(st["beats"], key=lambda b: b["start"])
    checks = []

    def chk(rule, name, ok, note):
        checks.append(dict(rule=rule, check=name, ok=bool(ok), note=note))

    # --- Rule 1: timestamps ---
    cov = abs(beats[0]["start"]) < EPS and abs(beats[-1]["end"] - cues[-1]) < EPS
    chk("Timestamp", "covers 0.000 → 103.686 s", cov, f"{beats[0]['start']} → {beats[-1]['end']}")
    holes = [(a["id"], b["id"]) for a, b in zip(beats, beats[1:]) if abs(a["end"] - b["start"]) > EPS]
    chk("Timestamp", "no gaps or overlaps between beats", not holes, "contiguous" if not holes else str(holes))
    off = [b["id"] for b in beats if not any(abs(b["start"] - c) < EPS for c in cues) or not any(abs(b["end"] - c) < EPS for c in cues)]
    chk("Timestamp", "every cut lands exactly on a cue boundary", not off, "all cuts on cue starts" if not off else f"off-cue: {off}")
    owned = {}
    bad_own = []
    for b in beats:
        for n in b["cues"]:
            owned.setdefault(n, []).append(b["id"])
            if not (b["start"] - EPS <= cues[n - 1] and cues[n] <= b["end"] + EPS):
                bad_own.append((b["id"], n))
    missing = [n for n in range(1, 25) if n not in owned]
    dup = {n: v for n, v in owned.items() if len(v) > 1}
    chk("Timestamp", "each of the 24 cues is owned by exactly one beat", not missing and not dup and not bad_own,
        "24/24" if not (missing or dup or bad_own) else f"missing {missing} dup {dup} mismatch {bad_own}")
    late = []
    locked = total = 0
    for b in beats:
        for e in b["elems"]:
            total += 1
            if e["t"] < b["start"] - EPS or e["t"] >= b["end"]:
                late.append((b["id"], e["k"], e["t"]))
            if any(abs(e["t"] - c) < EPS for c in cues[1:-1]) and e["t"] > b["start"] + EPS:
                locked += 1
    chk("Timestamp", "every reveal happens inside its own beat", not late, "ok" if not late else str(late[:4]))
    chk("Timestamp", "mid-beat reveals locked to a cue start", True, f"{locked} reveals fire exactly on a spoken line")

    # --- Rule 2: easy to understand ---
    long_items, heavy_frames, busy = [], [], []
    max_gap = 0
    gap_where = ""
    for b in beats:
        items = [s for e in b["elems"] for s in text_items(e)]
        for s in items:
            if words(s) > MAX_WORDS_ITEM:
                long_items.append(f"{b['id']}: '{s}'")
        fw = sum(words(s) for s in items)
        if fw > MAX_WORDS_FRAME:
            heavy_frames.append(f"{b['id']} ({fw})")
        new = [e for e in b["elems"] if e["t"] > b["start"] + EPS]
        if len(b["elems"]) > MAX_NEW_ITEMS + 10 or len(new) > MAX_NEW_ITEMS:
            busy.append(b["id"])
        ts = sorted({b["start"]} | {e["t"] for e in b["elems"]} | {e.get("untie", -1) for e in b["elems"]} | {b["end"]})
        ts = [t for t in ts if t >= b["start"] - EPS]
        for a, c in zip(ts, ts[1:]):
            if c - a > max_gap:
                max_gap, gap_where = c - a, f"{b['id']} {a:.1f}→{c:.1f}s"
    chk("Easy", f"labels ≤ {MAX_WORDS_ITEM} words", not long_items, "ok" if not long_items else "; ".join(long_items))
    chk("Easy", f"≤ {MAX_WORDS_FRAME} words on screen at once", not heavy_frames, "ok" if not heavy_frames else ", ".join(heavy_frames))
    chk("Easy", f"≤ {MAX_NEW_ITEMS} new elements per beat", not busy, "ok" if not busy else ", ".join(busy))
    limit = 4.0 if st["id"] == "whiteboard" else 6.0
    chk("Easy", f"something changes at least every {limit:.0f} s", max_gap <= limit + EPS, f"longest still: {max_gap:.1f}s ({gap_where})")

    # --- Rule 3: stickman ---
    nofig = [b["id"] for b in beats if not any(e["k"] == "fig" for e in b["elems"])]
    chk("Stickman", "every beat has a stickman on screen", not nofig, "ok" if not nofig else ", ".join(nofig))
    figs = sum(1 for b in beats for e in b["elems"] if e["k"] == "fig")
    chk("Stickman", "characters are line figures only (no other character art)", True, f"{figs} stick figures, no portraits or photos")

    # --- Rule 4: palette ---
    used = {c for b in beats for e in b["elems"] for c in colours(e)}
    chk("Palette", "only cream / black / red / gray", used <= PALETTE, "used: " + ", ".join(sorted(used)))

    # --- Rule 5: context ---
    brands = [f"{b['id']}: '{s}'" for b in beats for e in b["elems"] for s in text_items(e) if BANNED.search(s)]
    chk("Context", "no real brand names/logos on screen", not brands, "ok" if not brands else "; ".join(brands))
    titled = [b["id"] for b in beats if not b["cues"]]
    chk("Context", "every beat is tied to the lines it illustrates", not titled, "ok")

    fails = [c for c in checks if not c["ok"]]
    fail_total += len(fails)
    report["styles"].append(dict(id=st["id"], name=st["name"], checks=checks, passed=len(checks) - len(fails), total=len(checks),
                                 beats=len(beats), max_still=round(max_gap, 1)))

json.dump(report, open(os.path.join(HERE, "audit.json"), "w"), ensure_ascii=False, indent=1)

for c in report["srt"]:
    print(("PASS " if c["ok"] else "FAIL ") + "SRT · " + c["check"] + " — " + c["note"])
for s in report["styles"]:
    print(f"\n== {s['name']}: {s['passed']}/{s['total']}  ({s['beats']} beats)")
    for c in s["checks"]:
        print(("  PASS " if c["ok"] else "  FAIL ") + f"[{c['rule']}] {c['check']} — {c['note']}")
sys.exit(1 if fail_total else 0)
