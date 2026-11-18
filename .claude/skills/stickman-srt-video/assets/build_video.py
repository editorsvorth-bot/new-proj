"""Build a stickman-srt-video page: kit.js + the video's scenes.js -> gen-stickman-v2 engine page.

  python build_video.py --scenes <video>/scenes.js --out <video>/<name>.html [--artifact <scratch>/<name>.html]
         --title "Short Name" --file-name short-name --duration <seconds>
         --mode review|storyboard|player  [--music on|off] [--sfx on|off] [--voiceover on|off] [--subtitles on|off]

--mode review   = storyboard contact sheet + the approval panel (per-board Approve / Needs changes + comment,
                  saved to the page's db). Publish with capabilities {db: {}, user: {}}.
--mode storyboard / player = the engine's own modes (player: full animation + MP4 export).
"""
import argparse, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scenes', required=True); ap.add_argument('--out', required=True); ap.add_argument('--artifact')
    ap.add_argument('--title', required=True); ap.add_argument('--file-name', required=True)
    ap.add_argument('--duration', type=float, required=True)
    ap.add_argument('--mode', choices=['review', 'storyboard', 'player'], default='review')
    for k in ('music', 'sfx', 'voiceover', 'subtitles'): ap.add_argument('--' + k, default='off')
    ap.add_argument('--width', type=int, default=1920); ap.add_argument('--height', type=int, default=1080); ap.add_argument('--fps', type=int, default=30)
    a = ap.parse_args()
    kit = open(os.path.join(HERE, 'kit.js'), encoding='utf-8').read()
    sc = open(a.scenes, encoding='utf-8').read()
    # scenes first (declares SCENES/C/SRT_TEXT and config), then the kit (helpers are function declarations / lazy consts)
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(sc.rstrip() + '\n\n' + kit); merged = f.name
    engine_mode = 'storyboard' if a.mode in ('review', 'storyboard') else 'player'
    cmd = [sys.executable, os.path.join(HERE, 'engine', 'build.py'), '--scenes', merged, '--out', a.out, '--title', a.title,
           '--file-name', a.file_name, '--duration', str(a.duration), '--mode', engine_mode, '--width', str(a.width), '--height', str(a.height),
           '--fps', str(a.fps), '--music', a.music, '--sfx', a.sfx, '--voiceover', a.voiceover, '--subtitles', a.subtitles]
    if a.artifact: cmd += ['--artifact', a.artifact]
    subprocess.run(cmd, check=True); os.unlink(merged)
    if a.mode == 'review':
        panel = open(os.path.join(HERE, 'review', 'review.js'), encoding='utf-8').read()
        tag = '\n<script>\n' + panel + '\n</script>\n'
        for path in [a.out] + ([a.artifact] if a.artifact else []):
            html = open(path, encoding='utf-8').read()
            html = html.replace('</body>', tag + '</body>', 1) if '</body>' in html else html.rstrip() + tag
            open(path, 'w', encoding='utf-8').write(html)
        print('added the storyboard approval panel (publish with capabilities {db: {}, user: {}})')

if __name__ == '__main__':
    main()
