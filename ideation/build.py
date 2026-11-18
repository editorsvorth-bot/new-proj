"""Build index.html from template.html + plans.json + audit.json + the SRT."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(HERE, "plans.py")], check=True)
subprocess.run([sys.executable, os.path.join(HERE, "audit.py")], check=True, stdout=subprocess.DEVNULL)
data = open(os.path.join(HERE, "plans.json"), encoding="utf-8").read()
audit = open(os.path.join(HERE, "audit.json"), encoding="utf-8").read()
srt = open(os.path.join(HERE, "20-20-60.srt"), encoding="utf-8").read().strip()
lines = [" ".join(b.strip().splitlines()[2:]) for b in re.split(r"\n\s*\n", srt)]
html = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
safe = lambda s: s.replace("</", "<\\/")
html = html.replace("__DATA__", safe(data)).replace("__AUDIT__", safe(audit)).replace("__SRT__", safe(json.dumps(lines, ensure_ascii=False)))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
print("built index.html", len(html) // 1024, "KB")
