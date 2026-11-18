"""Visual ideation plans for the 20-20-60 script: five stickman styles.

Single source of truth. Run `python3 plans.py` to write plans.json.
Every element carries an absolute appearance time `t` (seconds) so reveals can be
locked to SRT cue starts. Canvas is 640x360. Colours are palette tokens only:
cream (background), ink (black), red, gray.
"""
import json

CUES = [0, 2.4, 4.9, 10.5, 13.8, 16.8, 21.5, 26.4, 29.6, 35.0, 39.8, 44.8, 48.0,
        52.5, 58.0, 63.2, 68.5, 73.4, 78.4, 81.5, 85.8, 90.6, 96.2, 99.5, 103.686]

def cs(n):  # cue start (1-based)
    return CUES[n - 1]

GLOSS = [
    "Let me explain this with a diagram.",
    "This is called the 20-20-60 split.",
    "The first 20% of people fall into the Never Buy category.",
    "Neither they nor we know why they are here.",
    "They have no need, and they can't pay.",
    "However hard we try to sell, they will definitely not buy.",
    "So our effort on them is a waste of time. They don't need sales.",
    "Another 20% are Definitely Buy.",
    "They are like Amazon shoppers. When we buy something on Amazon,",
    "really buy (not just add to cart), we decide we want it, go look at the product,",
    "search, read the description, check the details and the features,",
    "see it's good, purchase it and leave.",
    "These people are the same. About us, our website, what we sell,",
    "they've checked everything, decided they want us, and come to us as a lead.",
    "So there's no need to work hard selling them the features.",
    "Tell them what it is and the price, and they'll buy. They are Definitely Buy.",
    "But there's another 60% of people. They are the Confused Buyers.",
    "First: do they even need this product? Whom should they buy from?",
    "If they buy it, will they use it?",
    "Do they need it now or in the future? Or something else instead?",
    "They have many confusions like this, and need help making the decision.",
    "Only if someone helps can they decide what they need and what they don't.",
    "This is exactly why sales exists:",
    "to give clarity to the confused and help them decide.",
]

# ---------- element helpers ----------
G = 292  # ground line (feet)

def fig(x, t, c="ink", pose="stand", s=1.0, y=G, tie=False, q=False, fx=None, label=None, flip=False):
    e = dict(k="fig", x=x, y=y, t=t, c=c, pose=pose, s=s)
    if tie: e["tie"] = True
    if q: e["q"] = True
    if fx is not None: e["fx"] = fx
    if label: e["label"] = label
    if flip: e["flip"] = True
    return e

def txt(x, y, s, t, c="ink", size=22, anchor="middle"):
    return dict(k="text", x=x, y=y, s=s, t=t, c=c, size=size, anchor=anchor)

def tag(x, y, s, t, c="ink", size=16):
    return dict(k="tag", x=x, y=y, s=s, t=t, c=c, size=size)

def bub(x, y, s, t, c="ink", w=None, size=15, think=True):
    e = dict(k="bubble", x=x, y=y, s=s, t=t, c=c, size=size, think=think)
    if w: e["w"] = w
    return e

def arr(x1, y1, x2, y2, t, c="ink"):
    return dict(k="arrow", x1=x1, y1=y1, x2=x2, y2=y2, t=t, c=c)

def X(x, y, t, s=34, c="red"):
    return dict(k="x", x=x, y=y, s=s, t=t, c=c)

def CK(x, y, t, s=26, c="red"):
    return dict(k="check", x=x, y=y, s=s, t=t, c=c)

def bar(x, y, w, h, segs, t):
    # segs: list of (value, colour, filled, label, reveal_time)
    return dict(k="bar", x=x, y=y, w=w, h=h, t=t,
                segs=[dict(v=v, c=c, fill=f, label=l, t=st) for v, c, f, l, st in segs])

def pie(cx, cy, r, segs, t):
    return dict(k="pie", cx=cx, cy=cy, r=r, t=t,
                segs=[dict(v=v, c=c, fill=f, label=l, t=st) for v, c, f, l, st in segs])

def laptop(x, y, t, s=1.0, label="online shop", c="ink"):
    return dict(k="laptop", x=x, y=y, s=s, t=t, label=label, c=c)

def door(x, y, w, h, label, t, c="ink", open_t=None):
    e = dict(k="door", x=x, y=y, w=w, h=h, label=label, t=t, c=c)
    if open_t is not None: e["open"] = open_t
    return e

def meter(x, y, t, v0, v1, t1, label="effort"):
    return dict(k="meter", x=x, y=y, t=t, v0=v0, v1=v1, t1=t1, label=label, c="red")

def knot(x, y, t, r=34, c="red", untie=None):
    e = dict(k="knot", x=x, y=y, r=r, t=t, c=c)
    if untie is not None: e["untie"] = untie
    return e

def board(x, y, w, h, t):
    return dict(k="board", x=x, y=y, w=w, h=h, t=t, c="ink")

def rect(x, y, w, h, t, c="ink", fill=False):
    return dict(k="rect", x=x, y=y, w=w, h=h, t=t, c=c, fill=fill)

def drops(x, y, t, c="gray"):
    return dict(k="drops", x=x, y=y, t=t, c=c)

def flow(x, y, items, times, c="ink", dx=118, size=15):
    out = []
    for i, (it, tt) in enumerate(zip(items, times)):
        out.append(tag(x + i * dx, y, it, tt, c=c if it != "BUY" else "red", size=size))
        if i:
            out.append(arr(x + (i - 1) * dx + 44, y, x + i * dx - 44, y, tt))
    return out

def B(id, start, end, cues, title, elems, **fields):
    return dict(id=id, start=start, end=end, cues=cues, title=title, elems=elems, fields=fields)

# =====================================================================
# STYLE 1: "Ten People"  (skill: storyboard-previsualization)
# Continuity bible: the same 10 stickmen, each = 10%, fixed slots on one ground line.
# =====================================================================
SLOT = [70 + i * 55 for i in range(10)]

def ten(t, never=None, definite=None, confused=None, q6=False):
    out = []
    for i, x in enumerate(SLOT):
        c, q = "ink", False
        if never is not None and i < 2: c = "gray"
        if confused is not None and i >= 4: c = "red"; q = q6
        out.append(fig(x, t, c=c, s=0.8, q=q))
    return out

s1 = [
 B("S01", 0, 4.9, [1, 2], "Ten people, one line",
   [fig(x, 0.0, s=0.8, fx=x - 260, pose="walk") for x in SLOT]
   + [txt(320, 70, "20  ·  20  ·  60", cs(2), size=40)]
   + [rect(SLOT[0] - 24, 196, 2 * 55 - 7, 110, cs(2), c="gray"),
      rect(SLOT[2] - 24, 196, 2 * 55 - 7, 110, cs(2), c="ink"),
      rect(SLOT[4] - 24, 196, 6 * 55 - 7, 110, cs(2), c="red")],
   question="Where are we?", frame="Wide, eye level, 10 figures centred", action="Figures walk in left to right and stop on their slots. At 2.4s the three group boxes draw on.",
   camera="Static wide", continuity="Bible set here: 10 figures, 1 figure = 10%"),
 B("S02", 4.9, 10.5, [3], "The first two step out",
   ten(4.9) + [fig(SLOT[0], 5.4, c="gray", s=0.8), fig(SLOT[1], 5.4, c="gray", s=0.8),
               tag(SLOT[0] + 27, 150, "NEVER BUY · 20%", 5.9, c="gray", size=18)],
   question="Who is the first group?", frame="Wide, push-in on figures 1-2", action="Figures 1-2 turn gray, label drops in",
   camera="Slow push-in to the left third", continuity="Gray = never buy for the rest of the film"),
 B("S03", 10.5, 13.8, [4], "Nobody knows why",
   [fig(150, 10.5, c="gray", pose="shrug", q=True, s=1.2), fig(230, 10.5, c="gray", pose="shrug", q=True, s=1.2),
    fig(450, 10.8, tie=True, pose="shrug", q=True, s=1.2, label="us")],
   question="Why are they here?", frame="Medium: 2 gray figures + our salesman", action="All three shrug with ? at the same time",
   camera="Static medium", continuity="Salesman intro: black with red tie, label 'us'"),
 B("S04", 13.8, 21.5, [5, 6], "Pitch bounces off",
   [fig(170, 13.8, c="gray", pose="arms", s=1.2), fig(450, 13.8, tie=True, pose="point", s=1.2),
    bub(150, 120, "no need", cs(5), c="gray"), bub(250, 120, "₹0", 15.3, c="gray", w=60),
    arr(400, 200, 240, 200, cs(6), c="red"), arr(380, 225, 250, 245, 17.8, c="red"),
    X(200, 150, 19.5, s=40)],
   question="Can selling change them?", frame="Two-shot, buyer left, salesman right", action="Bubbles 'no need' and '₹0' pop on cue 5. Red pitch arrows on cue 6 bounce off, then a red X",
   camera="Static two-shot", continuity="Screen direction: salesman always on the right"),
 B("S05", 21.5, 26.4, [7], "Effort wasted",
   [fig(450, 21.5, tie=True, pose="shrug", s=1.2), drops(470, 190, 21.8), fig(170, 21.5, c="gray", pose="arms", s=1.2),
    tag(320, 80, "SALES", 22.4, c="ink", size=26), X(320, 80, 24.0, s=46)],
   question="So what?", frame="Same two-shot", action="Sweat drops on the salesman, the word SALES is crossed out on cue 7b",
   camera="Static", continuity="Same positions as S04"),
 B("S06", 26.4, 35.0, [8, 9], "Next two: definitely buy",
   ten(26.4, never=True) + [fig(SLOT[2], 26.8, s=0.8), fig(SLOT[3], 26.8, s=0.8),
     tag(SLOT[2] + 27, 150, "DEFINITELY BUY · 20%", 27.2, c="ink", size=18),
     laptop(470, 120, cs(9), s=1.0)],
   question="Who is the second group?", frame="Wide line again, then laptop inset", action="Figures 3-4 get a bold outline. On cue 9 an 'online shop' laptop appears as an analogy inset",
   camera="Wide, pan right", continuity="No store logo, generic 'online shop'"),
 B("S07", 35.0, 48.0, [10, 11, 12], "How they shop online",
   [fig(110, 35.0, pose="sit", s=1.2), laptop(230, 200, 35.0, s=1.1)]
   + flow(330, 110, ["decide", "look"], [35.0, 37.4])
   + flow(330, 170, ["search", "details", "features"], [cs(11), 41.4, 43.0])
   + [tag(520, 250, "BUY", cs(12), c="red", size=22), CK(575, 250, 46.0)],
   question="What does a sure buyer do?", frame="Over-the-shoulder at laptop, step chips on the right", action="One chip per spoken step, in the order the words are spoken",
   camera="Static OTS", continuity="Buyer = figure 3 (black)"),
 B("S08", 48.0, 58.0, [13, 14], "They come to us ready",
   [laptop(150, 150, 48.0, s=1.1, label="our website"), tag(150, 230, "about us · what we sell", 49.5, size=14),
    fig(300, 52.5, fx=200, pose="walk"), fig(520, 48.0, tie=True), tag(400, 90, "LEAD", 55.0, c="red", size=22)],
   question="How do they reach us?", frame="Wide: website left, our counter right", action="Buyer walks from the website to the salesman. 'LEAD' tag on cue 14",
   camera="Truck right with the walk", continuity="Salesman on the right"),
 B("S09", 58.0, 68.5, [15, 16], "Just what + price",
   [fig(250, 58.0), fig(420, 58.0, tie=True, pose="point"),
    tag(320, 90, "features · features · features", 58.4, c="gray", size=14), X(320, 90, 60.5, s=30),
    tag(300, 140, "what?", cs(16), size=18), tag(380, 140, "₹ price", 64.0, c="red", size=18), CK(250, 180, 66.0)],
   question="How much selling do they need?", frame="Two-shot", action="Feature list is crossed out. 'What? + price' appear, then a check over the buyer",
   camera="Static", continuity="Same salesman"),
 B("S10", 68.5, 73.4, [17], "The big group: 60%",
   ten(68.5, never=True, confused=True, q6=True) + [tag(SLOT[4] + 137, 150, "CONFUSED BUYERS · 60%", 69.2, c="red", size=18)],
   question="Who is left?", frame="Wide line, figures 5-10 lit red", action="Six figures turn red with ? marks",
   camera="Pull back to wide", continuity="Red = confused (and later: where sales helps)"),
 B("S11", 73.4, 85.8, [18, 19, 20], "Their questions",
   [fig(x, 73.4, c="red", s=0.9) for x in (110, 200, 290, 380, 470, 560)]
   + [bub(110, 120, "need it?", cs(18), c="red"), bub(200, 95, "from whom?", 75.9, c="red"),
      bub(290, 120, "will I use it?", cs(19), c="red"), bub(380, 95, "now or later?", cs(20), c="red"),
      bub(500, 120, "something else?", 83.6, c="red")],
   question="What confuses them?", frame="Medium wide of the six", action="One thought bubble per question, popping as each is spoken",
   camera="Static", continuity="Same six figures"),
 B("S12", 85.8, 96.2, [21, 22], "Tangled, until someone helps",
   [fig(x, 85.8, c="red", s=0.9) for x in (110, 170, 230, 290)]
   + [knot(200, 140, 86.0, r=50), fig(470, cs(22), tie=True, pose="point", fx=640), tag(470, 120, "help", 92.5, c="red", size=18)],
   question="What do they need?", frame="Group left, knot of questions above", action="Bubbles knot together. On cue 22 the salesman walks in from the right",
   camera="Static", continuity="Salesman enters from the right"),
 B("S13", 96.2, 103.686, [23, 24], "This is why sales exists",
   [fig(x, 96.2, c="red", s=0.9) for x in (110, 170, 230, 290)]
   + [knot(200, 140, 96.2, r=50, untie=cs(24)), fig(420, 96.2, tie=True, pose="point"),
      tag(500, 70, "SALES exists here", 96.6, c="red", size=20), tag(200, 230, "CLARITY", 100.5, c="ink", size=20), CK(270, 230, 101.5)],
   question="So why does sales exist?", frame="Same as S12", action="The knot straightens into a line on cue 24, then the CLARITY label and a check",
   camera="Slow push-in, end on a hold", continuity="Ends on the red group"),
]

# =====================================================================
# STYLE 2: "Living Bar"  (skill: motion-graphics-direction)
# A persistent 20|20|60 bar is the orientation anchor. Stickmen live inside it.
# =====================================================================
BX, BY, BW, BH = 40, 40, 560, 60
def bar_state(t, g=None, d=None, c=None):
    return bar(BX, BY, BW, BH, [
        (20, "gray", g is not None, "NEVER BUY", g if g is not None else 1e9),
        (20, "ink", False, "DEFINITELY BUY", d if d is not None else 1e9),
        (60, "red", False, "CONFUSED", c if c is not None else 1e9)], t)

s2 = [
 B("G01", 0, 2.4, [1], "Empty frame, guide figure",
   [fig(560, 0.0, pose="point", s=1.1, flip=True), rect(BX, BY, BW, BH, 0.6)],
   job="Orientation", purpose="Draw an empty bar so the viewer knows a diagram is coming", timing="Draw-on 0.8s ease-out, hold"),
 B("G02", 2.4, 4.9, [2], "Bar splits 20 | 20 | 60",
   [fig(560, 2.4, pose="point", s=1.1, flip=True), bar_state(2.4),
    txt(BX + 56, 150, "20", 2.6, size=34), txt(BX + 168, 150, "20", 3.0, size=34), txt(BX + 392, 150, "60", 3.4, size=34)],
   job="Explanation", purpose="Snap the three numbers in, left to right, in the order spoken", timing="Step reveals 0.4s apart, hold 1.1s"),
 B("G03", 4.9, 10.5, [3], "Segment 1: Never Buy",
   [bar_state(4.9, g=5.2), fig(90, 5.6, c="gray", s=1.1), fig(150, 5.6, c="gray", s=1.1),
    tag(BX + 56, 130, "NEVER BUY", 6.0, c="gray", size=18)],
   job="Identification", purpose="Label the first group and give it bodies", timing="Fill 0.5s, label ease-out, long hold for reading"),
 B("G04", 10.5, 16.8, [4, 5], "Why? No need, no money",
   [bar_state(10.5, g=10.5), fig(90, 10.5, c="gray", s=1.1, pose="shrug", q=True), fig(150, 10.5, c="gray", s=1.1, pose="shrug", q=True),
    bub(300, 170, "no need", cs(5), c="gray"), bub(420, 170, "can't pay", 15.2, c="gray")],
   job="Emphasis", purpose="Show the two reasons as two separate pops so neither gets lost", timing="? at cue 4, two bubbles 1.4s apart on cue 5"),
 B("G05", 16.8, 26.4, [6, 7], "Effort bounces off",
   [bar_state(16.8, g=16.8), fig(90, 16.8, c="gray", s=1.1, pose="arms"), fig(150, 16.8, c="gray", s=1.1, pose="arms"),
    fig(470, 16.8, tie=True, pose="point", s=1.1), arr(420, 220, 190, 220, 17.2, c="red"), arr(420, 250, 190, 250, 18.6, c="red"),
    txt(300, 180, "effort → 0 sales", 20.0, c="red", size=20), tag(BX + 56, 70, "SKIP", cs(7), c="red", size=20)],
   job="Explanation (cause and effect)", purpose="Make wasted effort visible: arrows go in, nothing comes out", timing="Arrows linear in, ease-in fade. SKIP stamp step-hold on cue 7"),
 B("G06", 26.4, 29.6, [8], "Segment 2: Definitely Buy",
   [bar_state(26.4, g=26.4, d=26.6), fig(210, 27.0, s=1.1), fig(270, 27.0, s=1.1), tag(BX + 168, 130, "DEFINITELY BUY", 27.3, size=18)],
   job="Identification", purpose="Same entrance grammar as segment 1, so the pattern is learnable", timing="Mirror of G03"),
 B("G07", 29.6, 48.0, [9, 10, 11, 12], "Their own buying path",
   [bar_state(29.6, g=29.6, d=29.6), fig(80, 29.6, pose="sit", s=1.0), laptop(170, 215, cs(9), s=0.9)]
   + flow(280, 150, ["decide", "look", "search"], [cs(10), 37.4, cs(11)], dx=110)
   + flow(280, 210, ["details", "features", "BUY"], [41.6, 43.2, cs(12)], dx=110)
   + [CK(560, 210, 46.0)],
   job="Explanation (process)", purpose="Reveal each step exactly as it is spoken, to show they sell to themselves", timing="Each chip 0.3s ease-out on its word, BUY gets a red snap"),
 B("G08", 48.0, 58.0, [13, 14], "They arrive as a lead",
   [bar_state(48.0, g=48.0, d=48.0), laptop(130, 200, 48.0, s=0.9, label="our website")]
   + flow(260, 170, ["about us", "what we sell"], [48.6, 50.5], dx=120)
   + [fig(470, cs(14), fx=380, pose="walk"), fig(560, 48.0, tie=True, flip=True), tag(500, 130, "LEAD", 55.0, c="red", size=20)],
   job="Explanation", purpose="Reuse the same chip grammar for our website so the analogy carries over", timing="Chips 0.3s, walk 0.6s, LEAD snap"),
 B("G09", 58.0, 68.5, [15, 16], "Only what + price",
   [bar_state(58.0, g=58.0, d=58.0), fig(220, 58.0, s=1.1), fig(420, 58.0, tie=True, pose="point", s=1.1),
    tag(320, 150, "features…", 58.3, c="gray", size=16), X(320, 150, 60.5, s=26),
    tag(280, 200, "what?", cs(16), size=18), tag(370, 200, "₹ price", 64.2, c="red", size=18), CK(220, 160, 66.2)],
   job="Emphasis", purpose="Contrast: features struck out, two small cards are enough", timing="Strike 0.3s, cards ease-out, check holds to the end"),
 B("G10", 68.5, 73.4, [17], "Segment 3: Confused, 60%",
   [bar_state(68.5, g=68.5, d=68.5, c=68.7)] + [fig(330 + i * 50, 69.2, c="red", s=1.0, q=True) for i in range(6)]
   + [tag(BX + 392, 130, "CONFUSED BUYERS", 69.6, c="red", size=18)],
   job="Identification", purpose="The biggest segment fills last and fills widest, so size reads as importance", timing="Fill 0.6s, six figures stagger 0.1s"),
 B("G11", 73.4, 85.8, [18, 19, 20], "Questions as kinetic type",
   [bar_state(73.4, g=73.4, d=73.4, c=73.4)] + [fig(330 + i * 50, 73.4, c="red", s=1.0) for i in range(6)]
   + [txt(140, 150, "need it?", cs(18), c="red", size=22), txt(140, 180, "who from?", 75.9, c="red", size=22),
      txt(140, 210, "use it?", cs(19), c="red", size=22), txt(140, 240, "now/later?", cs(20), c="red", size=22),
      txt(140, 270, "else?", 83.6, c="red", size=22)],
   job="Explanation (kinetic type)", purpose="Stack one question per spoken question, to show the pile-up", timing="Each line step-hold on its word, nothing exits"),
 B("G12", 85.8, 96.2, [21, 22], "Stuck at the fork, help arrives",
   [bar_state(85.8, g=85.8, d=85.8, c=85.8), fig(200, 85.8, c="red", pose="shrug", s=1.1),
    arr(240, 220, 330, 170, 86.2), arr(240, 220, 330, 270, 86.2), knot(400, 220, 87.0, r=40),
    fig(540, cs(22), tie=True, pose="point", fx=650, flip=True), tag(540, 150, "help", 92.6, c="red", size=18)],
   job="Explanation (cause and effect)", purpose="A fork plus knot equals can't decide alone. The helper enters on 'only if someone helps'", timing="Fork draw-on, knot wobble, helper walk 0.6s"),
 B("G13", 96.2, 103.686, [23, 24], "Sales lives in the 60",
   [bar_state(96.2, g=96.2, d=96.2, c=96.2), fig(200, 96.2, c="red", s=1.1), knot(400, 220, 96.2, r=40, untie=cs(24)),
    fig(540, 96.2, tie=True, pose="point", flip=True), arr(392, 120, 392, 104, 96.5, c="red"),
    tag(392, 140, "SALES EXISTS HERE", 96.7, c="red", size=18), tag(400, 290, "clarity", 100.6, size=18), CK(460, 290, 101.6)],
   job="Brand affect / payoff", purpose="Bracket the 60% segment. The knot becomes a straight line on 'clarity'", timing="Arrow ease-out, untie 0.8s ease-in-out, hold to the end"),
]

# =====================================================================
# STYLE 3: "Three Doors"  (skill: explainer-video-production)
# Learning contract: the viewer can sort prospects into 3 groups and knows where sales effort belongs.
# Colour meaning locked: gray = no-go, black = ready buyer, red = sales help / confusion.
# =====================================================================
def doors(t, o1=None, o2=None, o3=None):
    return [door(60, 110, 110, 180, "20%", t, c="gray", open_t=o1), door(220, 110, 110, 180, "20%", t, open_t=o2),
            door(380, 80, 200, 210, "60%", t, c="red", open_t=o3)]

s3 = [
 B("D01", 0, 4.9, [1, 2], "Salesman faces three doors",
   [door(60, 110, 110, 180, "", 0.3, c="gray"), door(220, 110, 110, 180, "", 0.3), door(380, 80, 200, 210, "", 0.3, c="red"),
    fig(320, 0.0, tie=True, s=0.9, fx=-20, pose="walk"),
    txt(115, 100, "20%", cs(2), c="gray", size=24), txt(275, 100, "20%", 3.0, size=24), txt(480, 70, "60%", 3.6, c="red", size=24)],
   learn="Three groups exist, sized 20/20/60", grammar="Scale: door width = share", access="Numbers are written, not only colour-coded"),
 B("D02", 4.9, 13.8, [3, 4], "Door 1: Never Buy",
   doors(4.9, o1=5.2) + [fig(115, 5.6, c="gray", s=0.9), tag(115, 312, "NEVER BUY", 6.0, c="gray", size=16),
    fig(115, cs(4), c="gray", s=0.9, pose="shrug", q=True)],
   learn="Group 1 is called Never Buy, with no clear reason to be here", grammar="Definition: labelled object", access="Label sits under the door, high contrast"),
 B("D03", 13.8, 21.5, [5, 6], "No need, no money, no sale",
   [door(60, 110, 110, 180, "20%", 13.8, c="gray", open_t=13.8), fig(115, 13.8, c="gray", s=0.9, pose="arms"),
    bub(115, 70, "no need · ₹0", cs(5), c="gray", w=120), fig(300, 13.8, tie=True, pose="point"),
    arr(270, 200, 160, 200, cs(6), c="red"), door(60, 110, 110, 180, "20%", 20.2, c="gray")],
   learn="No need + can't pay = no amount of selling works", grammar="Cause/effect: the pitch goes in, the door shuts", access="The door slam is a soft movement, no flash"),
 B("D04", 21.5, 26.4, [7], "Walk away",
   doors(21.5) + [fig(300, 21.5, tie=True, pose="walk", fx=180), drops(310, 200, 22.0), X(115, 200, 23.2, s=44),
    tag(115, 312, "skip", 23.8, c="red", size=16)],
   learn="Spending sales effort here is waste", grammar="Before/after: the door is X'd out", access="The X is a shape as well as red"),
 B("D05", 26.4, 48.0, [8, 9, 10, 11, 12], "Door 2: they shop like online buyers",
   doors(26.4, o2=26.6) + [fig(275, 27.0, s=0.9), tag(275, 312, "DEFINITELY BUY", 27.4, size=16),
    laptop(470, 40, cs(9), s=0.7, label="online shop")]
   + flow(400, 120, ["decide", "look"], [cs(10), 37.4], dx=100, size=13)
   + flow(400, 170, ["search", "details"], [cs(11), 41.6], dx=100, size=13)
   + flow(400, 220, ["features", "BUY"], [43.2, cs(12)], dx=100, size=13),
   learn="Sure buyers research and decide alone", grammar="Process: numbered chain beside the door",
   access="Analogy maps: they research before contact. Doesn't map: they're on our site, not a marketplace. Stop: no reviews or discounts implied"),
 B("D06", 48.0, 58.0, [13, 14], "They come out holding a lead ticket",
   doors(48.0, o2=48.0) + [laptop(470, 60, 48.0, s=0.7, label="our website"), tag(470, 140, "what we sell", 49.8, size=14),
    fig(380, cs(14), fx=275, pose="walk"), tag(380, 180, "LEAD", 55.0, c="red", size=18)],
   learn="They arrive already decided, as a lead", grammar="Process: exit through the door toward us", access="LEAD shown as a word, not an icon"),
 B("D07", 58.0, 68.5, [15, 16], "Price tag, handshake",
   doors(58.0, o2=58.0) + [fig(330, 58.0), fig(440, 58.0, tie=True, pose="point"),
    tag(470, 120, "features…", 58.4, c="gray", size=14), X(470, 120, 60.6, s=24),
    tag(470, 170, "what + ₹ price", cs(16), c="red", size=16), CK(275, 80, 66.0, s=30)],
   learn="Only say what it is and the price", grammar="Contrast: features out, price in", access="Check mark is a shape, not colour only"),
 B("D08", 68.5, 73.4, [17], "Door 3: the biggest room",
   doors(68.5, o3=68.7) + [fig(410 + i * 28, 69.2, c="red", s=0.7, q=True) for i in range(6)]
   + [tag(480, 312, "CONFUSED BUYERS", 69.6, c="red", size=16)],
   learn="60% are confused buyers", grammar="Scale: widest door, most people", access="Count is visible (6 figures = 60%)"),
 B("D09", 73.4, 85.8, [18, 19, 20], "Every person holds a question",
   [door(380, 80, 200, 210, "60%", 73.4, c="red", open_t=73.4)] + [fig(80 + i * 85, 73.4, c="red", s=0.85) for i in range(5)]
   + [bub(80, 150, "need it?", cs(18), c="red"), bub(165, 110, "from whom?", 75.9, c="red"),
      bub(250, 150, "will I use it?", cs(19), c="red"), bub(335, 110, "now/later?", cs(20), c="red"),
      bub(420, 150, "something else?", 83.6, c="red")],
   learn="Their confusion has concrete forms", grammar="System: actors × questions", access="Each question is short; 4 words max"),
 B("D10", 85.8, 96.2, [21, 22], "Going in circles, help steps in",
   [door(380, 80, 200, 210, "60%", 85.8, c="red", open_t=85.8)] + [fig(80 + i * 70, 85.8, c="red", s=0.85, pose="shrug") for i in range(4)]
   + [knot(185, 140, 86.2, r=46), fig(420, cs(22), tie=True, pose="point", fx=620), tag(420, 150, "helps decide", 92.8, c="red", size=16)],
   learn="They can only decide with help", grammar="Social: a helper enters", access="The helper's action is shown, not only described"),
 B("D11", 96.2, 103.686, [23, 24], "This door is where sales belongs",
   [door(380, 80, 200, 210, "60%", 96.2, c="red", open_t=96.2)] + [fig(80 + i * 70, 96.2, c="red", s=0.85) for i in range(4)]
   + [knot(185, 140, 96.2, r=46, untie=cs(24)), fig(420, 96.2, tie=True),
      tag(480, 28, "SALES BELONGS HERE", 96.6, c="red", size=18), tag(185, 220, "clarity", 100.6, size=18), CK(245, 220, 101.6)],
   learn="Sales = clarity for the confused (core takeaway)", grammar="Payoff: sign on the door", access="Final hold of more than 3s for reading"),
]

# =====================================================================
# STYLE 4: "Effort Meter"  (skill: explainer-video, iart-ai)
# Core idea: "Sales effort only pays off with confused buyers."
# One analogy ridden throughout: the salesman's effort battery.
# =====================================================================
def boards(t, hi=None):
    out = []
    for i, (x, lab, c) in enumerate([(90, "20", "gray"), (250, "20", "ink"), (450, "60", "red")]):
        out.append(rect(x - 40, 60, 80 if i < 2 else 160, 40, t, c=c, fill=(hi == i)))
        out.append(txt(x if i < 2 else x + 40, 88, lab + "%", t, c="cream" if hi == i else c, size=22))
    return out

s4 = [
 B("E01", 0, 4.9, [1, 2], "Salesman with a full effort battery",
   [fig(320, 0.0, tie=True, s=1.2), meter(360, 180, 0.2, 1.0, 1.0, 1.0)] + boards(cs(2)),
   stage="Setup", pace="Brisk", why="Introduce the single analogy (effort battery) before the problem"),
 B("E02", 4.9, 13.8, [3, 4], "First target: Never Buy",
   boards(4.9, hi=0) + [fig(320, 4.9, tie=True, s=1.1, pose="point"), meter(360, 180, 4.9, 1.0, 1.0, 4.9),
    fig(110, 5.6, c="gray"), fig(160, 5.6, c="gray"), tag(130, 140, "NEVER BUY", 6.0, c="gray", size=16),
    fig(110, cs(4), c="gray", pose="shrug", q=True), fig(160, cs(4), c="gray", pose="shrug", q=True)],
   stage="Problem", pace="Brisk", why="Name the first group fast"),
 B("E03", 13.8, 26.4, [5, 6, 7], "Battery drains, nothing happens",
   boards(13.8, hi=0) + [fig(110, 13.8, c="gray", pose="arms"), fig(160, 13.8, c="gray", pose="arms"),
    bub(135, 150, "no need · ₹0", cs(5), c="gray", w=120), fig(380, 13.8, tie=True, pose="point", s=1.1),
    meter(420, 180, 13.8, 1.0, 0.15, 24.0), arr(340, 230, 190, 230, cs(6), c="red"), drops(395, 190, 20.0),
    tag(135, 320, "0 sales", 21.0, c="gray", size=16), tag(320, 320, "WASTED", cs(7), c="red", size=22)],
   stage="Stakes", pace="Tense, faster cuts", why="Make the viewer feel the cost: the battery empties for zero"),
B("E04", 26.4, 35.0, [8, 9], "Definitely Buy: battery stays full",
   boards(26.4, hi=1) + [fig(560, 26.4, tie=True, s=1.0, flip=True), meter(590, 180, 26.4, 1.0, 1.0, 26.4),
    fig(150, 26.8), fig(210, 26.8), tag(250, 140, "DEFINITELY BUY", 27.2, size=16),
    fig(330, cs(9), pose="sit"), laptop(430, 200, 30.0, s=0.9)],
   stage="Solution, part 1", pace="Even", why="Introduce the sure buyer; battery untouched"),
 B("E04b", 35.0, 48.0, [10, 11, 12], "They do the work themselves",
   boards(35.0, hi=1) + [fig(560, 35.0, tie=True, s=1.0, flip=True), meter(590, 180, 35.0, 1.0, 1.0, 35.0),
    fig(90, 35.0, pose="sit"), laptop(190, 200, 35.0, s=0.9)]
   + flow(300, 160, ["decide", "look"], [cs(10), 37.4], dx=105, size=14)
   + flow(300, 215, ["search", "details", "features"], [cs(11), 41.6, 43.2], dx=105, size=14)
   + [tag(410, 280, "BUY", cs(12), c="red", size=20), CK(460, 280, 46.0)],
   stage="Solution, part 1", pace="Deliberate", why="Contrast: the buyer sells to themselves while the battery stays full"),
 B("E05", 48.0, 68.5, [13, 14, 15, 16], "Lead arrives; only what + price",
   boards(48.0, hi=1) + [laptop(130, 200, 48.0, s=0.9, label="our website"), tag(130, 270, "what we sell", 49.5, size=14),
    fig(330, cs(14), fx=200, pose="walk"), tag(330, 150, "LEAD", 55.0, c="red", size=18),
    fig(470, 48.0, tie=True, pose="point"), meter(510, 180, 48.0, 1.0, 0.95, 66.0),
    tag(420, 130, "features…", cs(15), c="gray", size=14), X(420, 130, 60.6, s=24),
    tag(420, 320, "what + ₹ price", cs(16), c="red", size=16), CK(330, 110, 66.0)],
   stage="Solution, part 2", pace="Relief, one clear hold", why="Effort used here: about 5%. Selling features is unnecessary"),
 B("E06", 68.5, 85.8, [17, 18, 19, 20], "60%: one question at a time",
   boards(68.5, hi=2) + [fig(100 + i * 60, 69.0, c="red", s=0.85) for i in range(6)]
   + [tag(250, 140, "CONFUSED BUYERS", 69.4, c="red", size=16),
      bub(100, 175, "need it?", cs(18), c="red"), bub(220, 175, "from whom?", 75.9, c="red"),
      bub(340, 175, "use it?", cs(19), c="red"), bub(460, 175, "now/later?", cs(20), c="red"),
      bub(560, 230, "else?", 83.6, c="red", w=60)],
   stage="How, part 1", pace="Deliberate, hold each", why="Slow down: one bubble per spoken question"),
 B("E07", 85.8, 96.2, [21, 22], "Effort finally pays off",
   boards(85.8, hi=2) + [fig(100 + i * 70, 85.8, c="red", s=0.85, pose="shrug") for i in range(4)]
   + [knot(205, 150, 86.0, r=44), fig(500, cs(22), tie=True, pose="point", fx=640),
      meter(540, 180, cs(22), 1.0, 0.6, 95.0), arr(460, 200, 300, 160, 92.0, c="red")],
   stage="How, part 2", pace="Deliberate", why="The same battery now flows into people who need it: the analogy pays off"),
 B("E08", 96.2, 103.686, [23, 24], "Payoff: effort → clarity",
   boards(96.2, hi=2) + [fig(100 + i * 70, 96.2, c="red", s=0.85) for i in range(4)]
   + [knot(205, 150, 96.2, r=44, untie=cs(24)), fig(500, 96.2, tie=True), meter(540, 180, 96.2, 0.6, 0.6, 96.2),
      tag(320, 320, "sales = clarity", 96.6, c="red", size=22), CK(270, 150, 101.5)],
   stage="Payoff", pace="Confident, hold the end", why="Repeatable line: sales = clarity for the confused"),
]

# =====================================================================
# STYLE 5: "Whiteboard Teacher"  (skill: scripting-and-storyboarding, SCENE + 2-column AV)
# Setups: A = wide teacher + board, B = close-up board drawing, C = doodle vignette.
# Rule from the skill: a visual change every ~2-4 s. One shot per cue, micro-beats in long cues.
# =====================================================================
PX, PY, PR = 230, 185, 95
def pie_state(t, g=None, d=None, c=None):
    return pie(PX, PY, PR, [(20, "gray", g is not None, "20", g if g is not None else 1e9),
                            (20, "ink", False, "20", d if d is not None else 1e9),
                            (60, "red", False, "60", c if c is not None else 1e9)], t)

def A(t):
    return [board(40, 30, 440, 300, t), fig(560, t, pose="point", s=1.2, flip=True)]

def Bset(t):
    return [board(40, 30, 520, 300, t), fig(600, t, s=0.8, pose="point", flip=True)]

s5 = [
 B("01", 0, 2.4, [1], "Teacher at the board", A(0.0) + [txt(260, 120, "let's draw it", 0.6, size=24)], setup="A", av="[Action] uncaps marker, turns to board"),
 B("02", 2.4, 4.9, [2], "Pie: 20 · 20 · 60", Bset(2.4) + [pie_state(2.4)], setup="B", av="[Action] draws circle, splits it, writes the numbers"),
 B("03", 4.9, 10.5, [3], "Shade the first 20% gray", Bset(4.9) + [pie_state(4.9, g=5.2), tag(470, 100, "NEVER BUY", 5.8, c="gray", size=18),
   fig(470, 7.7, c="gray", s=0.9, y=260)], setup="B", av="[Action] shades the slice, writes the label. Micro-beat 7.7s: tiny doodle figure"),
 B("04", 10.5, 13.8, [4], "Doodle shrugs", [rect(150, 60, 340, 250, 10.5), fig(270, 10.5, c="gray", pose="shrug", q=True, y=270), fig(370, 11.2, pose="shrug", q=True, y=270, tie=True)],
   setup="C", av="[Action] doodle and teacher's doodle-self both shrug"),
 B("05", 13.8, 16.8, [5], "No need, no money", [rect(150, 60, 340, 250, 13.8), fig(320, 13.8, c="gray", pose="arms", y=270),
   bub(240, 110, "no need", 13.9, c="gray"), bub(400, 110, "₹0", 15.3, c="gray", w=60)], setup="C", av="[Action] two empty thought bubbles"),
 B("06", 16.8, 21.5, [6], "Pitch, back turned", [rect(150, 60, 340, 250, 16.8), fig(240, 16.8, c="gray", pose="arms", y=270, flip=True),
   fig(400, 16.8, tie=True, pose="point", y=270), arr(370, 180, 270, 180, 17.2, c="red"), X(240, 150, 19.1, s=30)],
   setup="C", av="[Action] salesman pitches, buyer turns away. Micro-beat 19.1s: red X"),
 B("07", 21.5, 26.4, [7], "Cross out SALES", A(21.5) + [pie_state(21.5, g=21.5), tag(390, 80, "SALES", 22.0, size=22), X(390, 80, 23.8, s=40)],
   setup="A", av="[Action] writes SALES by the gray slice, slashes it in red"),
 B("08", 26.4, 29.6, [8], "Second slice: Definitely Buy", Bset(26.4) + [pie_state(26.4, g=26.4, d=26.6), tag(470, 150, "DEFINITELY BUY", 27.0, size=18)],
   setup="B", av="[Action] outlines the second slice in bold black"),
 B("09", 29.6, 35.0, [9], "Online shopper doodle", [rect(150, 60, 340, 250, 29.6), fig(230, 29.6, pose="sit", y=270),
   laptop(360, 170, 29.9, s=1.0), tag(360, 270, "like an online shopper", 32.3, size=15)], setup="C", av="[Action] doodle at a laptop. Micro-beat 32.3s: caption"),
 B("10", 35.0, 39.8, [10], "Buy ≠ add to cart", Bset(35.0) + [tag(200, 100, "buy", 35.2, c="red", size=24), txt(270, 108, "≠", 35.8, size=28),
   tag(370, 100, "add to cart", 36.0, c="gray", size=18)] + flow(200, 200, ["decide", "look"], [37.0, 38.4], dx=130, size=18),
   setup="B", av="[Action] writes buy ≠ cart, then decide → look"),
 B("11", 39.8, 44.8, [11], "Search → details → features", Bset(39.8) + flow(140, 160, ["search", "details", "features"], [39.9, 41.6, 43.2], dx=150, size=18),
   setup="B", av="[Action] chain written link by link"),
 B("12", 44.8, 48.0, [12], "BUY ✓", Bset(44.8) + flow(140, 160, ["features", "BUY"], [44.8, 45.0], dx=150, size=20) + [CK(360, 160, 46.2, s=34)],
   setup="B", av="[Action] chain ends in a red BUY + check"),
 B("13", 48.0, 52.5, [13], "Reading our website", [rect(150, 60, 340, 250, 48.0), fig(220, 48.0, y=270),
   laptop(360, 160, 48.2, s=1.0, label="our website"), tag(360, 260, "about us · what we sell", 49.8, size=14)], setup="C", av="[Action] doodle scrolls our site"),
 B("14", 52.5, 58.0, [14], "Walks in as a lead", [rect(150, 60, 340, 250, 52.5), fig(330, 52.5, fx=200, pose="walk", y=270),
   fig(430, 52.5, tie=True, y=270, flip=True), tag(330, 120, "LEAD", 55.2, c="red", size=22)], setup="C", av="[Action] walks to our counter. Micro-beat 55.2s: LEAD"),
 B("15", 58.0, 63.2, [15], "Features list crossed out", Bset(58.0) + [txt(260, 110, "feature 1", 58.2, c="gray", size=18), txt(260, 145, "feature 2", 58.5, c="gray", size=18),
   txt(260, 180, "feature 3", 58.8, c="gray", size=18), X(260, 145, 60.6, s=60)], setup="B", av="[Action] lists features, then a big red X"),
 B("16", 63.2, 68.5, [16], "What? + how much? → ✓", Bset(63.2) + [tag(200, 140, "what?", 63.3, size=22), txt(270, 148, "+", 63.6, size=26),
   tag(350, 140, "₹ how much?", 64.0, c="red", size=22), CK(470, 140, 65.8, s=34)], setup="B", av="[Action] two words, then a check. Micro-beat 65.8s"),
 B("17", 68.5, 73.4, [17], "Circle the 60% in red", A(68.5) + [pie_state(68.5, g=68.5, d=68.5, c=68.7), tag(390, 80, "CONFUSED", 69.6, c="red", size=20)],
   setup="A", av="[Action] teacher circles the big slice in red"),
 B("18", 73.4, 78.4, [18], "Need it? From whom?", Bset(73.4) + [txt(300, 120, "need it?", 73.5, c="red", size=26), txt(300, 175, "from whom?", 75.9, c="red", size=26)],
   setup="B", av="[Action] writes 2 questions"),
 B("19", 78.4, 81.5, [19], "Will I use it?", Bset(78.4) + [txt(300, 120, "need it?", 78.4, c="gray", size=20), txt(300, 150, "from whom?", 78.4, c="gray", size=20),
   txt(300, 200, "will I use it?", 78.5, c="red", size=26)], setup="B", av="[Action] older questions go gray, new one in red"),
 B("20", 81.5, 85.8, [20], "Now or later? Something else?", Bset(81.5) + [txt(300, 110, "now or later?", 81.6, c="red", size=26),
   txt(300, 170, "something else?", 83.6, c="red", size=26)], setup="B", av="[Action] last two questions"),
 B("21", 85.8, 90.6, [21], "Tangled doodle", [rect(150, 60, 340, 250, 85.8), fig(320, 85.8, c="red", pose="shrug", y=270), knot(320, 130, 86.0, r=50), tag(320, 225, "needs help deciding", 88.2, c="red", size=16)],
   setup="C", av="[Action] scribble knot grows over the doodle's head. Micro-beat 88.2s: 'needs help deciding'"),
 B("22", 90.6, 96.2, [22], "A hand to help", [rect(150, 60, 340, 250, 90.6), fig(260, 90.6, c="red", pose="shrug", y=270), knot(260, 130, 90.6, r=44),
   fig(420, 90.8, tie=True, pose="point", y=270, fx=520), tag(420, 120, "help", 93.4, c="red", size=20)],
   setup="C", av="[Action] salesman doodle steps in. Micro-beat 93.4s: 'help'"),
 B("23", 96.2, 99.5, [23], "SALES exists for this slice", A(96.2) + [pie_state(96.2, g=96.2, d=96.2, c=96.2), arr(400, 90, 310, 170, 96.4, c="red"),
   tag(400, 70, "SALES exists here", 96.6, c="red", size=18)], setup="A", av="[Action] red arrow to the 60% slice"),
 B("24", 99.5, 103.686, [24], "Tangle → straight → CLARITY", Bset(99.5) + [knot(220, 160, 99.5, r=50, untie=99.9),
   tag(400, 160, "CLARITY", 100.8, size=26), CK(480, 160, 101.6, s=34)], setup="B", av="[Action] the scribble pulls straight, then CLARITY ✓"),
]

STYLES = [
 dict(id="ten-people", name="Ten People", skill="storyboard-previsualization",
      source="calesthio/generative-media-skills",
      promise="Out of every ten people, only the six confused ones need a salesperson.",
      method=["Delivery promise in one sentence", "Beats → viewer question per beat", "Minimum shot count",
              "Continuity bible before shots", "Shot board: ID, frame, action, camera, continuity"],
      bible=["10 stickmen on one ground line, 1 figure = 10%", "Gray = never buy, black = sure buyer, red = confused",
             "Salesman: black, red tie, always enters/stands screen-right", "No store logos: generic 'online shop'"],
      columns=[("question", "Viewer question"), ("frame", "Frame"), ("action", "Action"), ("camera", "Camera"), ("continuity", "Continuity")],
      beats=s1),
 dict(id="living-bar", name="Living Bar", skill="motion-graphics-direction",
      source="calesthio/generative-media-skills",
      promise="One 20 | 20 | 60 bar stays on screen the whole time and fills with people as each group is explained.",
      method=["Classify each graphic by job", "One-sentence motion purpose", "Hierarchy across time: establish → reveal → context → hold",
              "Entry / hold / exit timing per graphic", "Motion QA"],
      bible=["Bar stays pinned at the top: the orientation anchor", "Easing: step-hold for numbers, ease-out for labels",
             "Never more than two jobs per graphic", "No spring/overshoot on claims"],
      columns=[("job", "Job"), ("purpose", "Motion purpose"), ("timing", "Entry / hold / exit")],
      beats=s2),
 dict(id="three-doors", name="Three Doors", skill="explainer-video-production",
      source="calesthio/generative-media-skills",
      promise="After watching, the viewer can sort prospects into three groups and knows which door sales effort belongs behind.",
      method=["Learning contract", "Decompose: terms → parts → contrast → example → consequence",
              "Analogy check: what maps / what doesn't / where to stop", "Storyboard as information design", "One colour = one meaning"],
      bible=["Door width = group share", "Gray = no-go, black = ready, red = confusion and sales help",
             "Analogy 'online shopper': maps research-before-contact; doesn't map marketplace; stops before reviews/discounts"],
      columns=[("learn", "Learning beat"), ("grammar", "Visual grammar"), ("access", "Accessibility / analogy check")],
      beats=s3),
 dict(id="effort-meter", name="Effort Meter", skill="explainer-video",
      source="iart-ai/explainer-video-skills",
      promise="Sales effort only pays off with confused buyers.",
      method=["One core idea", "Script-first: VO is the spine", "Ride one analogy (effort battery)",
              "Arc: problem → stakes → solution → how → payoff", "Pacing per beat + VO timing math (2.3 words/s)"],
      bible=["Red battery on the salesman = his effort", "Battery drains only on gray, flows usefully only to red",
             "Three target boards pinned on top: 20 / 20 / 60"],
      columns=[("stage", "Arc stage"), ("pace", "Pace"), ("why", "Why this beat")],
      beats=s4),
 dict(id="whiteboard", name="Whiteboard Teacher", skill="scripting-and-storyboarding",
      source="social-media-skills/skills",
      promise="A stickman teacher draws the 20-20-60 pie live, cutting to small doodle scenes for each idea.",
      method=["S: start from the spine", "C: two-column AV script", "E: envision every beat (stick-figure board)",
              "N: number shots, group by setup", "E: edit on paper (stopwatch pass, change every 2–4 s)"],
      bible=["Setup A: wide, teacher + board", "Setup B: board close-up", "Setup C: doodle vignette",
             "Markers: black, red; gray for 'done' text"],
      columns=[("setup", "Setup"), ("av", "Visual column (audio = SRT line)")],
      beats=s5),
]

EXPLORED = [
 dict(name="Ten People", kept=True, why="Most literal reading of the percentages; one continuity bible"),
 dict(name="Living Bar", kept=True, why="Diagrammatic, as the speaker says in cue 1"),
 dict(name="Three Doors", kept=True, why="Spatial sorting; door size encodes share"),
 dict(name="Effort Meter", kept=True, why="One analogy makes the 'why sales exists' payoff felt"),
 dict(name="Whiteboard Teacher", kept=True, why="Matches 'let me explain diagrammatically'; fast visual rhythm"),
 dict(name="Fishing net (cast net over a crowd)", kept=False, why="Adds a metaphor the speaker never uses, so it leaves the script's context"),
 dict(name="Traffic light (red / amber / green)", kept=False, why="Needs green and amber, which are outside the palette"),
 dict(name="Amazon checkout screen recreation", kept=False, why="Uses a real brand's UI and logo; replaced with a generic 'online shop'"),
 dict(name="Pie-chart-only infographic", kept=False, why="No stickman characters, so it breaks the style rule"),
 dict(name="Sales funnel diagram", kept=False, why="A funnel implies stages that people move through; the script describes three fixed groups"),
]

AUDIT_LOG = [
 dict(round=1, style="Living Bar", beat="G11", rule="Easy", issue="18 words on screen at once (limit 14)", fix="Questions shortened to 1-2 words each: need it? / who from? / use it? / now/later? / else?"),
 dict(round=1, style="Effort Meter", beat="E08", rule="Easy", issue="6-word end label", fix="Cut to 'sales = clarity'"),
 dict(round=1, style="Effort Meter", beat="E05", rule="Easy", issue="16 words on screen", fix="'about us · what we sell' → 'what we sell'"),
 dict(round=1, style="Effort Meter", beat="E04", rule="Easy", issue="13 new elements in one 21.6 s beat", fix="Split into E04 (cues 8-9) and E04b (cues 10-12)"),
 dict(round=1, style="Whiteboard Teacher", beat="21", rule="Easy", issue="4.6 s with nothing changing (skill rule: change every 2-4 s)", fix="Micro-beat at 88.2 s: 'needs help deciding'"),
]

if __name__ == "__main__":
    srt_text = open(__file__.replace("plans.py", "20-20-60.srt"), encoding="utf-8").read()
    json.dump(dict(cues=CUES, gloss=GLOSS, styles=STYLES, explored=EXPLORED, audit_log=AUDIT_LOG), open(__file__.replace(".py", ".json"), "w"), ensure_ascii=False, indent=1)
    print("wrote plans.json:", sum(len(s["beats"]) for s in STYLES), "beats across", len(STYLES), "styles")
