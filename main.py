#!/usr/bin/env python3
"""The World Today - 24 November 2026.

Draws one dense newspaper front page summing up the world's news of
Tuesday 24 November 2026 and writes it to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png outside the grader).

Pure PIL drawing: no network, no randomness, no timestamps, so two runs
produce byte-identical output. Canvas is 1024x1024, the gate's maximum.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 22
GUTTER = 12
COL_W = (W - 2 * MARGIN - 2 * GUTTER) // 3  # 318

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PAPER = (252, 250, 244)
RED = (139, 0, 0)
GREY = (90, 90, 90)
RULE = (40, 40, 40)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
F_REG = lambda s: font("DejaVuSans.ttf", s)           # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Wrap text, truncating to max_lines with an ellipsis if needed."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "...", font=fnt) > width:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] = lines[-1] + "..."
    return lines


# ---------------------------------------------------------------- stories
# (headline, one-line summary) -- every summary is kept short on purpose
# so the whole page stays legible at 1024 px across.

LEAD = (
    "COP31 COLLAPSES WITHOUT A DEAL",
    "Climate talks in Antalya end two days late with no pact, as 130 nations "
    "refuse a text silent on fossil fuels. The UN chief calls the failure "
    "\u201cdeeply disappointing\u201d; focus now shifts to COP32 in Addis Ababa.",
)

FEATURED = [
    (
        "TECH",
        "HUANG IS BACK AT NVIDIA",
        "The board reinstates Jensen Huang as chief 11 days after he quit. "
        "Shares jump about 30%, regaining nearly $1 trillion in value.",
    ),
    (
        "WAR IN UKRAINE",
        "KYIV COUNTS ITS DEAD AFTER NIGHT OF STRIKES",
        "Russian attacks kill 15 in the Kyiv region; Zelenskyy demands the "
        "Patriot missiles allies have already paid for.",
    ),
]

# Three columns; each column is a list of (SECTION NAME, [(headline, summary)]).
COLUMNS = [
    [
        ("AMERICAS", [
            ("Trump blames Democrats for $1tn rout",
             "Trump blames Democrats for the market sell-off."),
            ("Court opens path to erase hush-money verdict",
             "Court hands Trump a path to erase the conviction."),
            ("Trump assails Newsom at Justice Dept.",
             "Trump attacks governor over 548 commuted sentences."),
            ("O\u2019Hare ground stop snarls Thanksgiving rush",
             "Staffing shortage halts departures for 95 minutes."),
            ("Trump: penalties for overseas data centres",
             "Vows penalties for firms building centres abroad."),
        ]),
        ("AFRICA", [
            ("Nigeria boat tragedy kills at least 24",
             "Overloaded boat carrying mourners capsizes."),
            ("24 civilians killed in South Sudan",
             "Warrap State attack kills 24 civilians."),
            ("Kenya and DR Congo restore full ties",
             "Nairobi and Kinshasa rebuild ties after years apart."),
            ("Ebola spreads in DR Congo amid attacks",
             "Armed groups obstruct health teams in rural areas."),
        ]),
    ],
    [
        ("EUROPE", [
            ("Drone-hit Russian ship burns in Baltic",
             "Cargo ship Sparta II ablaze in the Gulf of Finland."),
            ("Ukraine sinks Russian warship off Libya",
             "Sea drones hit a corvette and cargo ship off Libya."),
            ("Denmark backs hardline \u201cghetto law\u201d",
             "Top court upholds hardline immigration rules."),
            ("Bomb threats hit 450 German schools",
             "Emailed threats close schools; no danger is seen."),
            ("Belgium strikers march on austerity",
             "National strike begins; thousands march in Brussels."),
            ("NATO sends AWACS to Poland",
             "AWACS jets sent after missiles land in Poland."),
        ]),
        ("TECH & SCIENCE", [
            ("OpenAI ships GPT-6.2; Google answers",
             "Rival labs release flagship models the same week."),
            ("Anthropic IPO is the largest on record",
             "Shares debut at $83 as investors pile into AI."),
            ("Killer-robot talks end with no pact",
             "UN talks stall as military powers resist limits."),
        ]),
    ],
    [
        ("MIDDLE EAST", [
            ("US severs Iran\u2019s \u201clast financial lifeline\u201d",
             "Treasury sanctions 30 exchange houses and fronts."),
            ("Iran vows force to break US blockade",
             "Tehran: it will use \u201call available means\u201d at sea."),
            ("Iran eyed in cyberattacks on 50 tankers",
             "Washington probes suspected attacks on 50 tankers."),
            ("Four nations urge Gaza aid before winter",
             "Four nations press Israel to let in Gaza aid."),
            ("Sudan blames Ethiopia for Khartoum drones",
             "Army says strikes killed four and hit a UN building."),
        ]),
        ("ASIA-PACIFIC", [
            ("Factory fire kills 24 in Indonesia",
             "Candy-plant blaze leaves dozens missing."),
            ("Modi unveils $1.7bn Nepal package",
             "India and Nepal sign eight deals on energy and trade."),
            ("India and China hold border talks",
             "Commanders meet in Arunachal to ease tensions."),
            ("Seoul reshuffles foreign, spy chiefs",
             "Seoul names a new foreign minister and spy chief."),
            ("Bangladesh vows to arrest Hasina",
             "Dhaka: ex-premier faces arrest if she returns."),
        ]),
        ("SPORT & CULTURE", [
            ("Alcaraz lifts first ATP Finals crown",
             "Spaniard beats Zverev in Turin to end season on top."),
            ("India and NZ share Wellington draw",
             "Visitors bat out 120 overs on day five to save Test."),
            ("Gukesh begins title defence in Geneva",
             "World champion faces Sindarov as the match opens."),
            ("Liverpool rout United 4-0 at Anfield",
             "Champions humiliate rivals in a wild league weekend."),
        ]),
    ],
]

# Extra stories carried in the footer ticker, so the page names more of the day.
TICKER = (
    "SENSEX SLIDES 1,484 POINTS  \u2022  LAHORE AIR WORST IN THE WORLD, AQI OVER 500  "
    "\u2022  SUPERMOON MEETS THE SEVEN SISTERS TONIGHT  \u2022  FIFA PICKS 2031 & 2035 "
    "WOMEN\u2019S WORLD CUP HOSTS  \u2022  MOSSAD SAVED SWIFT\u2019S VIENNA SHOWS, EX-CHIEF SAYS"
)


def draw_section_header(draw, x, y, width, name):
    draw.rectangle([x, y, x + width, y + 22], fill=BLACK)
    draw.text((x + 8, y + 4), name, font=F_BOLD(14), fill=WHITE)
    return y + 22


def draw_story(draw, x, y, width, headline, summary):
    """One compact story block. Returns the y below it."""
    lines = fit_lines(draw, headline, F_BOLD(13), width, 2)
    yy = y
    for line in lines:
        draw.text((x, yy), line, font=F_BOLD(13), fill=BLACK)
        yy += 16
    sum_lines = fit_lines(draw, summary, F_REG(11), width, 1)
    for line in sum_lines:
        draw.text((x, yy), line, font=F_REG(11), fill=(50, 50, 50))
        yy += 14
    return yy + 4


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=BLACK, width=2)

    y = 18
    # --- top dateline bar
    d.text((MARGIN, y), "TUESDAY 24 NOVEMBER 2026", font=F_BOLD(14), fill=BLACK)
    right = "ONE DAY  \u2022  THE WORLD IN FULL"
    d.text((W - MARGIN - d.textlength(right, font=F_BOLD(14)), y),
           right, font=F_BOLD(14), fill=BLACK)
    y += 20
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 8

    # --- masthead
    title = "THE WORLD TODAY"
    tf = F_SERIF(66)
    d.text(((W - d.textlength(title, font=tf)) / 2, y), title, font=tf, fill=BLACK)
    y += 78
    sub = "The world\u2019s news of Tuesday 24 November 2026 \u2014 in one page"
    sf = F_REG(19)
    d.text(((W - d.textlength(sub, font=sf)) / 2, y), sub, font=sf, fill=GREY)
    y += 26
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=BLACK, width=3)
    y += 10

    # --- lead story: COP31
    d.text((MARGIN, y), "CLIMATE  \u2022  COP31 IN ANTALYA", font=F_BOLD(13), fill=RED)
    y += 16
    lead_lines = fit_lines(d, LEAD[0], F_BOLD(31), W - 2 * MARGIN, 2)
    for line in lead_lines:
        d.text((MARGIN, y), line, font=F_BOLD(31), fill=BLACK)
        y += 36
    lead_sum = fit_lines(d, LEAD[1], F_REG(15), W - 2 * MARGIN, 2)
    for line in lead_sum:
        d.text((MARGIN, y), line, font=F_REG(15), fill=(40, 40, 40))
        y += 19
    y += 4
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 6

    # --- featured row: two stories side by side
    feat_y = y
    feat_w = (W - 2 * MARGIN - GUTTER) // 2
    max_feat = feat_y
    for i, (kicker, head, summ) in enumerate(FEATURED):
        fx = MARGIN + i * (feat_w + GUTTER)
        yy = feat_y
        d.text((fx, yy), kicker, font=F_BOLD(12), fill=RED)
        yy += 17
        for line in fit_lines(d, head, F_BOLD(19), feat_w, 2):
            d.text((fx, yy), line, font=F_BOLD(19), fill=BLACK)
            yy += 23
        for line in fit_lines(d, summ, F_REG(13), feat_w, 2):
            d.text((fx, yy), line, font=F_REG(13), fill=(40, 40, 40))
            yy += 16
        max_feat = max(max_feat, yy)
    d.line([(MARGIN + feat_w + GUTTER // 2, feat_y),
            (MARGIN + feat_w + GUTTER // 2, max_feat)], fill=(180, 180, 180), width=1)
    y = max_feat + 6
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=BLACK, width=2)
    y += 10

    # --- three columns of region sections
    col_top = y
    col_bottom = H - 60  # reserve room for the ticker footer
    col_ys = [col_top] * 3
    for ci, sections in enumerate(COLUMNS):
        x = MARGIN + ci * (COL_W + GUTTER)
        yy = col_top
        for name, stories in sections:
            yy = draw_section_header(d, x, yy, COL_W, name)
            yy += 5
            for head, summ in stories:
                yy = draw_story(d, x, yy, COL_W, head, summ)
            yy += 3
        col_ys[ci] = yy
    y = max(col_ys)
    if y > col_bottom:
        raise SystemExit("layout overflow: columns end at %d, limit %d" % (y, col_bottom))

    # --- footer ticker: more of the day in one strip
    ty = H - 50
    d.line([(MARGIN, ty), (W - MARGIN, ty)], fill=BLACK, width=2)
    tick = fit_lines(d, TICKER, F_BOLD(12), W - 2 * MARGIN, 2)
    yy = ty + 7
    for line in tick:
        d.text((MARGIN, yy), line, font=F_BOLD(12), fill=BLACK)
        yy += 15

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path, img.size, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    build()
