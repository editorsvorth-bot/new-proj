"""Voiceover checks for stickman-srt-video.

  python audio_probe.py bed <voiceover.mp3>              -> does the recording already carry a music bed? (decides --music)
  python audio_probe.py sync <voiceover.mp3> <final.mp4>  -> offset and correlation of the voice in the final MP4
  python audio_probe.py duration <voiceover.mp3> <srt>    -> decoded length vs the SRT end (they should match)

Needs ffmpeg. A recording that never drops below about -40 dBFS between phrases has a bed: build with --music off.
"""
import array, math, os, re, subprocess, sys, tempfile

def pcm(path, sr=8000):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    a = array.array('h'); a.frombytes(raw); return a

def env(x, w):
    return [math.sqrt(sum(v * v for v in x[i:i + w]) / w) + 1e-9 for i in range(0, len(x) - w, w)]

def bed(path):
    a = pcm(path); w = 2000
    db = [10 * math.log10(sum(v * v for v in a[i:i + w]) / w / 32768 ** 2 + 1e-12) for i in range(0, len(a) - w, w)]
    quiet = sum(1 for d in db if d < -40)
    print(f"windows {len(db)} (0.25 s) | min {min(db):.0f} dBFS, median {sorted(db)[len(db)//2]:.0f}, quiet(<-40) {quiet}")
    print("music bed detected -> build with --music off" if quiet < max(2, len(db) * .02) else "pauses are silent -> engine music can stay on (--music on)")

def sync(voice, mp4):
    a, b = env(pcm(voice), 400), env(pcm(mp4), 400); n = min(len(a), len(b)); best = None
    for lag in range(-20, 21):
        pr = [(a[i], b[i + lag]) for i in range(max(0, -lag), min(n, n - lag))]
        ma = sum(p[0] for p in pr) / len(pr); mb = sum(p[1] for p in pr) / len(pr)
        c = sum((x - ma) * (y - mb) for x, y in pr) / math.sqrt(sum((x - ma) ** 2 for x, _ in pr) * sum((y - mb) ** 2 for _, y in pr))
        if best is None or c > best[1]: best = (lag, c)
    print(f"voice offset {best[0] * 50} ms, correlation {best[1]:.3f} -> {'IN SYNC' if best[0] == 0 and best[1] > .9 else 'CHECK SYNC'}")

def duration(voice, srt):
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', voice], capture_output=True, text=True).stdout)
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f: tmp = f.name
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', voice, tmp], check=True)
    dec = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', tmp], capture_output=True, text=True).stdout); os.unlink(tmp)
    ends = re.findall(r'-->\s*(\d+):(\d+):(\d+)[,.](\d+)', open(srt, encoding='utf-8-sig').read())
    h, m, s, ms = map(int, ends[-1]); end = h * 3600 + m * 60 + s + ms / 1000
    print(f"container {d:.3f} s | decoded {dec:.3f} s | SRT end {end:.3f} s | difference {abs(dec - end) * 1000:.0f} ms")

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    {'bed': lambda: bed(sys.argv[2]), 'sync': lambda: sync(sys.argv[2], sys.argv[3]), 'duration': lambda: duration(sys.argv[2], sys.argv[3])}.get(cmd, lambda: print(__doc__))()
