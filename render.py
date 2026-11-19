#!/usr/bin/env python3
"""Render the front page for 19 November 2026 with PIL (build time only).

This script draws ``entry.png`` — a 1024x1024 newspaper front page — from
fixed coordinates and fixed text. It uses no randomness and no network, so
every run produces the same picture. The committed ``entry.png`` is what
``main.py`` hands to the grader; this script is kept in the repository so
anyone can see exactly how the picture was made and rebuild it.

The page is built around one big table: twelve stories of Thursday
19 November 2026, each with a small pictogram drawn in the page's
indigo-and-vermilion style, its country and a two-line summary. A
schematic dot map of the world in the masthead band numbers the places
to match the table's rows. The twelve stories:

 1. Trump, Xi and Putin meet face to face in Shenzhen at APEC — the
    first trilateral meeting of the three leaders; Xi and Putin blast
    Western protectionism and Europe is absent. (Reuters.)
 2. The US and Iran exchange fire: Iran hits US sites in Kuwait and
    Bahrain, the US strikes Qeshm Island, and tankers are hit in the
    Strait of Hormuz. (Reuters.)
 3. Anthropic prices its IPO at $83 a share and raises $81.3bn — the
    largest stock-market debut in history — at a valuation of about
    $1.5 trillion, ticker ANT on the Nasdaq. (Reuters, CNN.)
 4. The International Court of Justice at The Hague rules in Gambia v
    Myanmar, the genocide case over the 2017 crackdown on the Rohingya.
    (BBC, Al Jazeera.)
 5. Israeli tanks cross the Gaza ceasefire "Yellow Line" in a rare
    ground operation; Australia, Canada, Italy and the UK jointly call
    for unrestricted aid access. (BBC.)
 6. The Crimean (Kerch) Bridge is attacked again and traffic halts,
    while Russia and Ukraine trade drone strikes amid Abu Dhabi peace
    talks. (BBC.)
 7. COP31 in Antalya, Türkiye reaches its final week: the presidency
    draft admits the Paris 1.5°C limit will be passed, with 144 items
    still in dispute before Friday's close. (Reuters, AFP.)
 8. Minutes of the Federal Reserve's October meeting show nearly all
    officials expect further rate hikes may be needed to return
    inflation to the 2% target.
 9. Nvidia's board will not reinstate Jensen Huang, who resigned as
    CEO on 12 November; Colette Kress is interim CEO, and H-series
    chip shipments to mainland China have been halted. (CNN,
    TechCrunch.)
10. NASA's Voyager 1, launched 49 years ago, reaches one light-day
    from Earth: its radio signals now take a full 24 hours to arrive.
    (Al Jazeera.)
11. France sees a fourth straight weekend of cost-of-living protests
    while hundreds of thousands march in Prague for a free press.
    (Reuters.)
12. Grand Theft Auto VI launches worldwide after a 13-year wait;
    PlayStation's network stumbles hours before the release. (BBC.)
"""

import pathlib

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "entry.png"

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = H = 1024
PAPER = (246, 246, 243)
INK = (26, 24, 30)
INDIGO = (36, 40, 88)
INDIGO_DEEP = (23, 26, 60)
VERMILION = (203, 60, 29)
AMBER = (240, 178, 84)
MAP_DOT = (198, 201, 226)
WHITE = (248, 248, 246)
GREY = (100, 100, 112)
ROW_ALT = (233, 233, 242)
GRID = (206, 206, 219)

M = 34  # page margin


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, s, f, max_w, fill, lh):
    x, y = xy
    for line in wrap(draw, s, f, max_w):
        draw.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def centered(draw, y, s, f, fill):
    draw.text(((W - text_w(draw, s, f)) / 2, y), s, font=f, fill=fill)


def fit_font(draw, s, path, size, max_w, min_size=10):
    """Largest size <= size at which s fits max_w (never below min_size)."""
    while size > min_size and text_w(draw, s, font(path, size)) > max_w:
        size -= 1
    return font(path, size)


# Schematic world landmass, one entry per grid row (north to south).
# Each span is an inclusive (first, last) pair of grid columns, 0..95.
LAND = {
    0: [(8, 12), (34, 40), (60, 63), (75, 78), (88, 91)],
    1: [(3, 9), (12, 30), (33, 42), (57, 70), (74, 95)],
    2: [(3, 10), (11, 32), (34, 41), (51, 55), (57, 95)],
    3: [(3, 10), (12, 24), (28, 33), (35, 40), (44, 44), (50, 56), (57, 95)],
    4: [(4, 10), (12, 23), (28, 33), (36, 39), (50, 56), (56, 94)],
    5: [(5, 9), (13, 33), (46, 47), (50, 57), (56, 93)],
    6: [(14, 32), (46, 47), (49, 58), (59, 90)],
    7: [(15, 31), (47, 58), (59, 88)],
    8: [(15, 30), (46, 58), (60, 86), (87, 88)],
    9: [(15, 30), (46, 57), (59, 84), (86, 88)],
    10: [(15, 30), (46, 55), (56, 62), (63, 84), (82, 87)],
    11: [(16, 30), (46, 48), (52, 53), (55, 64), (64, 72), (70, 84), (85, 87)],
    12: [(16, 30), (44, 58), (59, 64), (65, 71), (71, 83)],
    13: [(17, 29), (29, 30), (43, 57), (58, 64), (66, 71), (72, 82)],
    14: [(17, 27), (43, 57), (58, 63), (66, 70), (72, 77), (74, 81)],
    15: [(18, 26), (43, 56), (59, 62), (67, 70), (72, 77), (79, 80)],
    16: [(19, 26), (43, 49), (50, 57), (60, 61), (67, 69), (72, 76), (79, 80)],
    17: [(23, 27), (43, 49), (50, 58), (68, 69), (72, 75)],
    18: [(28, 32), (44, 49), (50, 59), (68, 68), (72, 74), (79, 79)],
    19: [(28, 33), (44, 48), (49, 56), (59, 62), (70, 72), (73, 73)],
    20: [(28, 34), (48, 56), (59, 61), (71, 73), (75, 77)],
    21: [(29, 35), (49, 56), (74, 78), (79, 79)],
    22: [(30, 38), (49, 56), (72, 72), (74, 76), (75, 78), (82, 85)],
    23: [(30, 39), (49, 56), (74, 79), (82, 88)],
    24: [(29, 39), (50, 55), (77, 79), (84, 89)],
    25: [(29, 38), (50, 55), (59, 59), (80, 82)],
    26: [(29, 37), (50, 55), (59, 60), (79, 88)],
    27: [(29, 36), (50, 56), (59, 60), (78, 89)],
    28: [(29, 35), (51, 56), (78, 89)],
    29: [(29, 34), (51, 56), (59, 59), (78, 88)],
    30: [(29, 34), (51, 56), (79, 88)],
    31: [(29, 33), (52, 55), (80, 87)],
    32: [(29, 32), (52, 54), (81, 86)],
    33: [(29, 31), (82, 85), (93, 94)],
    34: [(29, 30), (87, 87), (93, 94)],
    35: [(29, 30), (92, 93)],
    36: [(29, 29), (92, 92)],
}

# Numbered markers keyed to the table rows: (col, row, label).
MARKERS = [
    (77, 15, "1"),    # Shenzhen, China — the trilateral summit
    (64, 12, "2"),    # Strait of Hormuz — US–Iran exchange of fire
    (15, 9, "3"),     # San Francisco — Anthropic's IPO
    (47, 6, "4"),     # The Hague — the Rohingya ruling
    (59, 15, "5"),    # Gaza — the ground operation
    (61, 8, "6"),     # Crimea — the bridge attack
    (56, 11, "7"),    # Antalya, Türkiye — COP31
    (29, 10, "8"),    # Washington — the Fed minutes
    (18, 13, "9"),    # Silicon Valley — Nvidia
    (52, 8, "11"),    # Prague — Europe's street protests
    (36, 15, "12"),   # mid-Atlantic — a worldwide launch
]
VOYAGER = (2, 1)  # star in open "space" at the panel's top-left corner

# The twelve stories: (no, headline, country, summary).
STORIES = [
    ("1", "THREE PRESIDENTS MEET IN SHENZHEN", "CHINA — SHENZHEN",
     "First face-to-face of the three leaders, at APEC. Xi and Putin blast "
     "Western protectionism; Europe is absent from the table."),
    ("2", "US AND IRAN TRADE FIRE IN THE GULF", "KUWAIT · BAHRAIN · HORMUZ",
     "Iran hits US sites in Kuwait and Bahrain; the US strikes Qeshm "
     "Island. Tankers are hit in the Strait of Hormuz."),
    ("3", "ANTHROPIC'S RECORD-BREAKING IPO", "UNITED STATES",
     "Priced at $83 a share, the Claude maker raises $81.3bn — a $1.5tn "
     "valuation, ticker ANT on the Nasdaq."),
    ("4", "WORLD COURT RULES ON ROHINGYA CASE", "THE HAGUE · MYANMAR",
     "The ICJ decides Gambia v Myanmar, the genocide case over the 2017 "
     "crackdown that drove 700,000 Rohingya into exile."),
    ("5", "ISRAELI TANKS CROSS GAZA LINE", "GAZA · ISRAEL",
     "Tanks cross the ceasefire “Yellow Line” in a rare ground push. "
     "Australia, Canada, Italy and the UK demand aid access."),
    ("6", "CRIMEAN BRIDGE ATTACKED AGAIN", "RUSSIA · UKRAINE",
     "The Kerch Bridge is hit and traffic halts, as Russian and Ukrainian "
     "drones trade strikes amid Abu Dhabi peace talks."),
    ("7", "COP31: 1.5°C PROMISE SLIPS AWAY", "TÜRKIYE — ANTALYA",
     "The presidency draft admits the Paris limit will be passed. 144 "
     "items remain in dispute; the summit closes Friday."),
    ("8", "FED MINUTES LEAN TO MORE HIKES", "UNITED STATES",
     "Minutes of the October meeting: nearly all officials see further "
     "rate hikes may be needed to get inflation back to 2%."),
    ("9", "NVIDIA BOARD BARS HUANG RETURN", "UNITED STATES",
     "The board will not reinstate Jensen Huang, who resigned on 12 "
     "November. Kress is interim CEO; H-series shipments to China halt."),
    ("10", "VOYAGER 1 REACHES ONE LIGHT-DAY", "UNITED STATES — NASA",
     "Forty-nine years after launch, the probe is so far away that its "
     "radio signals take a full 24 hours to reach Earth."),
    ("11", "EUROPE TAKES TO THE STREETS", "FRANCE · CZECHIA",
     "France marches a fourth straight weekend over living costs; in "
     "Prague, hundreds of thousands defend a free press."),
    ("12", "GTA VI LAUNCHES WORLDWIDE", "WORLDWIDE",
     "After a 13-year wait the game rolls out worldwide — and "
     "PlayStation's network stumbles hours before the release."),
]

# ---------- row pictograms ----------
# One flat duotone glyph per story, drawn with PIL shapes on a 4x canvas
# and downscaled, so every row of the table carries a small illustration
# in the page's own indigo + vermilion (amber only inside the flame).
SS = 4
TILE = 52            # pictogram tile size (drawn at 4x, downscaled)
TILE_BG = (231, 232, 242)


def icon_flags(d):
    # 1 — three presidents meet: three flags on poles
    for x, c in ((56, INDIGO), (102, VERMILION), (148, INDIGO)):
        d.line([(x, 48), (x, 158)], fill=INDIGO, width=6)
        d.ellipse([x - 5, 39, x + 5, 49], fill=c)
        d.polygon([(x, 51), (x + 36, 58), (x, 69)], fill=c)
    d.line([(34, 164), (174, 164)], fill=INDIGO, width=6)


def icon_flame(d):
    # 2 — fire traded in the Gulf: a flame over waves
    d.polygon([(104, 28), (127, 76), (141, 103), (137, 129), (120, 147),
               (104, 151), (88, 147), (71, 129), (67, 103), (81, 76)],
              fill=VERMILION)
    d.polygon([(104, 82), (118, 107), (116, 129), (104, 137), (92, 129),
               (90, 107)], fill=AMBER)
    wave = [(30, 168), (48, 160), (66, 168), (84, 176), (102, 168),
            (120, 160), (138, 168), (156, 176), (176, 168)]
    d.line(wave, fill=INDIGO, width=6)
    wave2 = [(x, y + 18) for x, y in wave]
    d.line(wave2, fill=INDIGO, width=6)


def icon_chart(d):
    # 3 — a record-breaking IPO: bars and a rising arrow
    d.line([(46, 38), (46, 162)], fill=INDIGO, width=6)
    d.line([(46, 162), (172, 162)], fill=INDIGO, width=6)
    for x, h in ((62, 42), (94, 68), (126, 96)):
        d.rectangle([x, 162 - h, x + 22, 162], fill=INDIGO)
    d.line([(56, 116), (92, 92), (120, 100), (160, 54)], fill=VERMILION, width=9)
    d.polygon([(162, 52), (142, 55), (155, 72)], fill=VERMILION)


def icon_scales(d):
    # 4 — the World Court: scales of justice
    d.line([(50, 58), (158, 58)], fill=INDIGO, width=8)
    d.line([(104, 50), (104, 146)], fill=INDIGO, width=8)
    d.ellipse([97, 41, 111, 55], fill=VERMILION)
    for cx in (58, 150):
        d.line([(cx, 58), (cx - 15, 102)], fill=INDIGO, width=5)
        d.line([(cx, 58), (cx + 15, 102)], fill=INDIGO, width=5)
        d.pieslice([cx - 24, 92, cx + 24, 122], 0, 180, fill=INDIGO)
    d.line([(88, 146), (120, 146)], fill=INDIGO, width=6)
    d.line([(74, 157), (134, 157)], fill=INDIGO, width=8)


def icon_tank(d):
    # 5 — tanks cross the line: a tank silhouette
    d.rounded_rectangle([32, 124, 176, 154], 14, fill=INDIGO)
    d.polygon([(46, 124), (62, 106), (146, 106), (162, 124)], fill=INDIGO)
    d.rectangle([80, 86, 128, 106], fill=INDIGO)
    d.line([(126, 94), (180, 94)], fill=INDIGO, width=9)
    d.ellipse([97, 90, 109, 102], fill=VERMILION)
    for cx in (58, 84, 110, 136, 158):
        d.ellipse([cx - 6, 133, cx + 6, 145], fill=PAPER)


def icon_bridge(d):
    # 6 — the Crimean Bridge: towers, cable, a burst in the deck
    d.line([(30, 96), (67, 70), (80, 84), (92, 91), (104, 94), (116, 91),
            (128, 84), (141, 70), (178, 96)], fill=INDIGO, width=6)
    d.rectangle([62, 70, 72, 130], fill=INDIGO)
    d.rectangle([136, 70, 146, 130], fill=INDIGO)
    for x, y in ((85, 87), (104, 94), (123, 87)):
        d.line([(x, y), (x, 128)], fill=INDIGO, width=4)
    d.line([(28, 130), (94, 130)], fill=INDIGO, width=8)
    d.line([(114, 130), (180, 130)], fill=INDIGO, width=8)
    d.polygon([(104, 110), (108, 123), (121, 121), (111, 131), (119, 142),
               (106, 137), (100, 149), (98, 135), (85, 140), (95, 130),
               (87, 119), (100, 123)], fill=VERMILION)


def icon_globe_thermo(d):
    # 7 — COP31: a globe with a thermometer against it
    d.ellipse([36, 40, 140, 144], outline=INDIGO, width=7)
    d.ellipse([66, 40, 110, 144], outline=INDIGO, width=4)
    d.line([(38, 66), (138, 66)], fill=INDIGO, width=3)
    d.line([(36, 92), (140, 92)], fill=INDIGO, width=4)
    d.line([(38, 118), (138, 118)], fill=INDIGO, width=3)
    d.rounded_rectangle([136, 44, 160, 128], 10, fill=WHITE,
                        outline=VERMILION, width=6)
    d.rectangle([144, 88, 152, 126], fill=VERMILION)
    d.ellipse([130, 118, 166, 154], fill=VERMILION)
    d.ellipse([141, 129, 155, 143], fill=AMBER)


def icon_percent(d):
    # 8 — the Fed leans to hikes: a bold per cent
    d.line([(64, 152), (144, 56)], fill=VERMILION, width=13)
    d.ellipse([48, 44, 94, 90], outline=INDIGO, width=10)
    d.ellipse([114, 118, 160, 164], outline=INDIGO, width=10)


def icon_chip(d):
    # 9 — Nvidia: a computer chip
    for x in (74, 98, 122, 146):
        d.line([(x, 30), (x, 52)], fill=INDIGO, width=8)
        d.line([(x, 156), (x, 178)], fill=INDIGO, width=8)
    for y in (74, 98, 122, 146):
        d.line([(30, y), (52, y)], fill=INDIGO, width=8)
        d.line([(156, y), (178, y)], fill=INDIGO, width=8)
    d.rounded_rectangle([52, 52, 156, 156], 10, outline=INDIGO, width=8)
    d.rectangle([80, 80, 128, 128], fill=VERMILION)


def icon_satellite(d):
    # 10 — Voyager: a probe with dish and solar panel
    d.pieslice([22, 56, 98, 152], 90, 270, fill=INDIGO)
    d.line([(60, 104), (98, 86)], fill=INDIGO, width=7)
    d.ellipse([93, 80, 105, 92], fill=VERMILION)
    d.rectangle([102, 84, 134, 118], fill=INDIGO)
    d.line([(134, 101), (142, 101)], fill=INDIGO, width=6)
    d.rectangle([142, 62, 176, 140], outline=INDIGO, width=6)
    d.line([(142, 101), (176, 101)], fill=INDIGO, width=4)
    d.line([(159, 62), (159, 140)], fill=INDIGO, width=4)


def icon_crowd(d):
    # 11 — Europe marches: a crowd, one placard raised
    d.rectangle([82, 22, 126, 54], fill=WHITE, outline=VERMILION, width=6)
    d.line([(92, 38), (116, 38)], fill=VERMILION, width=5)
    d.line([(104, 54), (104, 78)], fill=VERMILION, width=6)
    for cx in (54, 104, 154):
        d.ellipse([cx - 14, 78, cx + 14, 106], fill=INDIGO)
        d.pieslice([cx - 27, 104, cx + 27, 158], 180, 360, fill=INDIGO)


def icon_controller(d):
    # 12 — GTA VI: a game controller
    d.rounded_rectangle([28, 70, 180, 142], 30, fill=WHITE,
                        outline=INDIGO, width=8)
    d.rectangle([59, 88, 75, 120], fill=INDIGO)
    d.rectangle([48, 96, 86, 112], fill=INDIGO)
    d.ellipse([128, 84, 146, 102], fill=VERMILION)
    d.ellipse([146, 106, 164, 124], fill=VERMILION)
    d.ellipse([100, 118, 110, 128], fill=INDIGO)


ICON_FUNCS = [icon_flags, icon_flame, icon_chart, icon_scales, icon_tank,
              icon_bridge, icon_globe_thermo, icon_percent, icon_chip,
              icon_satellite, icon_crowd, icon_controller]


def make_tile(fn):
    t = Image.new("RGB", (TILE * SS, TILE * SS), TILE_BG)
    fn(ImageDraw.Draw(t))
    return t.resize((TILE, TILE), Image.LANCZOS)


ICON_TILES = [make_tile(f) for f in ICON_FUNCS]

# Table geometry.
COL_NO_R = 56        # right edge of the NO. column
COL_ICON = 64        # ICON column left edge (pictogram tile)
COL_STORY = 126      # STORY column left edge
COL_STORY_W = 248
COL_COUNTRY = 384    # COUNTRY column left edge
COL_COUNTRY_W = 162
COL_SUMMARY = 562    # SUMMARY column left edge
COL_SUMMARY_W = W - M - COL_SUMMARY
ROW_H = 57


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead (left block) ----------
    d.line([(M, 22), (W - M, 22)], fill=VERMILION, width=3)
    d.text((M, 32), "TWELVE STORIES  •  ONE TABLE  •  EVERY COUNTRY",
           font=font(SANS_BOLD, 13), fill=INDIGO)
    d.text((M, 50), "THE DAILY ATLAS", font=font(SERIF_BOLD, 56), fill=INK)
    d.rectangle([M, 122, 640, 152], fill=INDIGO)
    d.text((M + 14, 129), "THURSDAY 19 NOVEMBER 2026",
           font=font(SANS_BOLD, 18), fill=WHITE)
    right = "THE DAY, IN ONE TABLE"
    rf = font(SANS_BOLD, 12)
    d.text((640 - 12 - text_w(d, right, rf), 132), right, font=rf, fill=AMBER)
    draw_wrapped(
        d, (M, 164),
        "Three presidents in Shenzhen, a shooting war in the Gulf, the "
        "biggest share sale in history and a probe one light-day from "
        "home — Thursday's world, set out in a single table.",
        font(SERIF, 13), 606, INK, 17)

    # ---------- masthead (map panel, right) ----------
    px0, py0, px1, py1 = 656, 30, W - M, 200
    d.rectangle([px0, py0, px1, py1], fill=INDIGO_DEEP)
    d.rectangle([px0, py0, px1, py1], outline=VERMILION, width=2)
    ix = px0 + 16
    d.text((ix, py0 + 10), "WHERE IT HAPPENED", font=font(SANS_BOLD, 13), fill=WHITE)
    d.text((ix, py0 + 28), "Numbered dots match the table · ★ 10 = deep space",
           font=font(SANS, 10), fill=MAP_DOT)

    gx0, gy0 = ix, py0 + 46
    pitch = 3.1
    for row, spans in LAND.items():
        for c0, c1 in spans:
            for col in range(c0, c1 + 1):
                cx = gx0 + col * pitch + pitch / 2
                cy = gy0 + row * pitch + pitch / 2
                d.ellipse([cx - 1.15, cy - 1.15, cx + 1.15, cy + 1.15], fill=MAP_DOT)
    # Voyager star, out in open space at the corner
    vx = gx0 + VOYAGER[0] * pitch + pitch / 2
    vy = gy0 + VOYAGER[1] * pitch + pitch / 2
    star = [(vx, vy - 8), (vx + 2.1, vy - 2.1), (vx + 8, vy), (vx + 2.1, vy + 2.1),
            (vx, vy + 8), (vx - 2.1, vy + 2.1), (vx - 8, vy), (vx - 2.1, vy - 2.1)]
    d.polygon(star, fill=AMBER)
    d.text((vx + 11, vy - 6), "10", font=font(SANS_BOLD, 10), fill=WHITE)
    # numbered story markers
    for col, row, label in MARKERS:
        cx = gx0 + col * pitch + pitch / 2
        cy = gy0 + row * pitch + pitch / 2
        mf = font(SANS_BOLD, 9 if len(label) == 1 else 8)
        d.ellipse([cx - 7.5, cy - 7.5, cx + 7.5, cy + 7.5], fill=VERMILION)
        d.text((cx - text_w(d, label, mf) / 2, cy - (5 if len(label) == 1 else 4.5)),
               label, font=mf, fill=WHITE)

    # ---------- table title ----------
    d.text((M, 214), "THE DAY IN TWELVE STORIES", font=font(SERIF_BOLD, 25), fill=INK)
    right = "ALL OF THURSDAY, ONE PAGE"
    rf = font(SANS_BOLD, 11)
    d.text((W - M - text_w(d, right, rf), 224), right, font=rf, fill=VERMILION)
    d.line([(M, 246), (W - M, 246)], fill=INK, width=3)

    # ---------- table header ----------
    hf = font(SANS_BOLD, 12)
    d.text((COL_NO_R - text_w(d, "NO.", hf), 254), "NO.", font=hf, fill=INDIGO)
    d.text((COL_STORY, 254), "STORY", font=hf, fill=INDIGO)
    d.text((COL_COUNTRY, 254), "COUNTRY", font=hf, fill=INDIGO)
    d.text((COL_SUMMARY, 254), "THE SHORT OF IT", font=hf, fill=INDIGO)
    d.line([(M, 272), (W - M, 272)], fill=INK, width=2)

    # ---------- table rows ----------
    nf = font(SANS_BOLD, 15)
    sf = font(SANS, 12)
    cf = font(SANS_BOLD, 12)
    top = 278
    for i, (no, head, country, summary) in enumerate(STORIES):
        ry = top + i * ROW_H
        if i % 2 == 1:
            d.rectangle([M, ry, W - M, ry + ROW_H], fill=ROW_ALT)
        # number, right-aligned
        d.text((COL_NO_R - text_w(d, no, nf), ry + 8), no, font=nf, fill=VERMILION)
        # pictogram tile for this story
        ty = ry + (ROW_H - TILE) // 2
        img.paste(ICON_TILES[i], (COL_ICON, ty))
        d.rectangle([COL_ICON, ty, COL_ICON + TILE - 1, ty + TILE - 1],
                    outline=INDIGO, width=1)
        # headline, shrunk only if it would overflow its column
        hf2 = fit_font(d, head, SANS_BOLD, 14, COL_STORY_W)
        d.text((COL_STORY, ry + 8), head, font=hf2, fill=INK)
        # country, up to two lines
        cy = ry + 9
        for line in wrap(d, country, cf, COL_COUNTRY_W)[:2]:
            d.text((COL_COUNTRY, cy), line, font=cf, fill=INDIGO)
            cy += 14
        # summary, up to two lines
        sy = ry + 8
        for line in wrap(d, summary, sf, COL_SUMMARY_W)[:2]:
            d.text((COL_SUMMARY, sy), line, font=sf, fill=INK)
            sy += 16
        if i < len(STORIES) - 1:
            d.line([(M, ry + ROW_H), (W - M, ry + ROW_H)], fill=GRID, width=1)

    # ---------- footer ----------
    foot_y = top + len(STORIES) * ROW_H + 12
    d.line([(M, foot_y), (W - M, foot_y)], fill=INK, width=3)
    centered(d, foot_y + 10,
             "Stories from the news of Thursday 19 November 2026  •  "
             "Compiled from Reuters, BBC, Al Jazeera, CNN and AP reporting",
             font(SANS, 11), GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
