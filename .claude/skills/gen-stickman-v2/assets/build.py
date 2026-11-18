"""gen-stickman-v2 build script.

Splices a project's scenes file into the engine template, sets CONFIG from the
user's configuration, and writes two copies:

  --out       full standalone HTML (doctype/html/head/body) -> the user's project folder
  --artifact  the same page WITHOUT the doctype/html/head/body wrapper -> publish this
              with the Artifact tool (the tool adds its own wrapper)

The scenes file must define, at top level:
  let SCENES = [], CUES = [], SFX_CUES = [], STORYBOARD = [];
  function buildScenes() { ... }
and nothing else that the engine already defines (helpers in the template are reused).

Example:
  python build.py --scenes scenes.js --out "F:/Project/video.html" --artifact "<scratchpad>/video.html" \
      --title "Short Page Name" --file-name short-name --duration 90 --mode storyboard --music on --sfx off
Re-run with --mode player after storyboard approval.
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'engine-template.html')
START = '/* ======================================================================================\n   DEMO SCENES'
END = '/* ================= renderAt'

def onoff(v):
    return 'true' if str(v).lower() in ('1', 'on', 'true', 'yes', 'enabled') else 'false'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scenes', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--artifact')
    ap.add_argument('--title', required=True)
    ap.add_argument('--file-name', required=True)
    ap.add_argument('--mode', choices=['storyboard', 'player'], default='storyboard')
    ap.add_argument('--duration', type=float, required=True)
    ap.add_argument('--width', type=int, default=1920)
    ap.add_argument('--height', type=int, default=1080)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--music', default='on')
    ap.add_argument('--sfx', default='off')
    ap.add_argument('--voiceover', default='off')
    ap.add_argument('--subtitles', default='off')
    a = ap.parse_args()

    t = open(TEMPLATE, encoding='utf-8').read()
    sc = open(a.scenes, encoding='utf-8').read()
    i, j = t.index(START), t.index(END)
    t = t[:i] + sc.rstrip() + '\n\n' + t[j:]

    subs = [
        (r"  mode: '[a-z]+',", f"  mode: '{a.mode}',"),
        (r"  width: \d+, height: \d+,", f"  width: {a.width}, height: {a.height},"),
        (r"  fps: \d+,", f"  fps: {a.fps},"),
        (r"  duration: [\d.]+,", f"  duration: {a.duration:g},"),
        (r"  music: (true|false),", f"  music: {onoff(a.music)},"),
        (r"  sfx: (true|false),", f"  sfx: {onoff(a.sfx)},"),
        (r"  voiceover: (true|false),", f"  voiceover: {onoff(a.voiceover)},"),
        (r"  subtitles: (true|false),", f"  subtitles: {onoff(a.subtitles)},"),
        (r"  fileName: '[^']*',", f"  fileName: '{a.file_name}',"),
        (r"<title>[^<]*</title>", f"<title>{a.title}</title>"),
    ]
    for pat, rep in subs:
        t, n = re.subn(pat, rep, t, count=1)
        if n != 1:
            sys.exit(f'build.py: pattern not found in template: {pat}')

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, 'w', encoding='utf-8').write(t)

    if a.artifact:
        art = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*', '', t, count=1)
        art = art.replace('<meta charset="utf-8">\n', '', 1)
        art = art.replace('<meta name="viewport" content="width=device-width, initial-scale=1">\n', '', 1)
        art = art.replace('</head>\n<body>\n', '', 1).replace('</body>\n</html>\n', '', 1)
        os.makedirs(os.path.dirname(os.path.abspath(a.artifact)), exist_ok=True)
        open(a.artifact, 'w', encoding='utf-8').write(art)

    print(f'built {a.mode}: {a.out}' + (f' + {a.artifact}' if a.artifact else ''))

if __name__ == '__main__':
    main()
