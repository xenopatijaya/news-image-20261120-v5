#!/usr/bin/env python3
"""Render entry.png - Friday 20 November 2026 world news in one image."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (22, 20, 18)
RED = (179, 32, 42)
NAVY = (22, 50, 79)
TEAL = (18, 122, 114)
OCHRE = (198, 138, 28)
GREEN = (52, 120, 62)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
CREAM = (232, 220, 190)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(d, x, y, text, font, fill, maxw, leading=None, max_lines=None):
    lines = wrap(d, text, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(font.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def banner(d, x, y, label, color, fsize=10):
    f = F(SANS_B, fsize)
    tw = d.textlength(label, font=f)
    d.rectangle([x, y, x + tw + 12, y + fsize + 9], fill=color)
    d.text((x + 6, y + 4), label, font=f, fill=WHITE)
    return x + tw + 12

def chip(d, x, y, label):
    f = F(SANS_B, 7)
    tw = d.textlength(label, font=f)
    d.rectangle([x, y, x + tw + 8, y + 13], fill=(10, 10, 10))
    d.text((x + 4, y + 3), label, font=f, fill=WHITE)

def num_badge(d, cx, cy, n, r=9):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=WHITE, width=1)
    f = F(SANS_B, 9 if n < 10 else 8)
    s = str(n)
    tw = d.textlength(s, font=f)
    d.text((cx - tw / 2, cy - 5), s, font=f, fill=WHITE)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 14
CW = W - 2 * M

# ---------- MASTHEAD ----------
d.text((M, 8), "THE WORLD IN ONE DAY", font=F(SANS_B, 11), fill=RED)
right = "36 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
fr = F(SANS_B, 9)
d.text((W - M - d.textlength(right, font=fr), 10), right, font=fr, fill=INK)
d.line([M, 26, W - M, 26], fill=INK, width=2)
d.text((M, 30), "Friday 20 November 2026", font=F(SERIF_B, 40), fill=INK)
d.line([M, 76, W - M, 76], fill=INK, width=1)
sub = "Kyiv\u2019s bridges hit in the year\u2019s biggest barrage \u00b7 Akvan comes ashore in Odisha \u00b7 Asia\u2019s AI sell-off deepens \u00b7 Britain and the EU seal their reset"
text_block(d, M, 80, sub, F(SERIF_I, 12), NAVY, CW, leading=15, max_lines=2)

# ---------- STAT STRIP ----------
stats = [
    ("3", "BRIDGES OVER THE DNIPRO DAMAGED IN KYIV"),
    ("300,000+", "PEOPLE MOVED TO SHELTERS BEFORE AKVAN"),
    ("\u22126.2%", "TAIWAN\u2019S SHARE INDEX, FRIDAY\u2019S CLOSE"),
    ("100,000", "YOUTH VISAS A YEAR IN THE UK\u2013EU DEAL"),
    ("2.3%", "JAPAN\u2019S CONSUMER INFLATION IN OCTOBER"),
    ("118", "RUNS BY GLENN PHILLIPS AGAINST INDIA"),
]
sy = 112
cellw = CW // 6
d.rectangle([M, sy, W - M, sy + 44], outline=INK, width=1)
for i, (num, lab) in enumerate(stats):
    x = M + i * cellw
    if i:
        d.line([x, sy, x, sy + 44], fill=INK, width=1)
    d.text((x + 6, sy + 3), num, font=F(SERIF_B, 19), fill=RED)
    text_block(d, x + 6, sy + 27, lab, F(SANS_B, 6), INK, cellw - 10, leading=7, max_lines=2)

# ---------- REGION BAR ----------
regions = [("EUROPE", 9, NAVY), ("ASIA", 7, RED), ("MIDDLE EAST", 6, OCHRE),
           ("AFRICA", 5, GREEN), ("AMERICAS", 5, TEAL), ("OCEANIA", 3, (110, 70, 150)), ("GLOBAL", 1, GREY)]
ry = 160
x = M
total_w = CW
for name, cnt, col in regions:
    wseg = int((total_w - 58) * cnt / 35) if name != "GLOBAL" else 58
    if name == "GLOBAL":
        wseg = total_w - (x - M)
    d.rectangle([x, ry, x + wseg - 2, ry + 16], fill=col)
    lab = f"{name} {cnt}"
    f = F(SANS_B, 8)
    tw = d.textlength(lab, font=f)
    if tw < wseg - 6:
        d.text((x + (wseg - 2 - tw) / 2, ry + 4), lab, font=f, fill=WHITE)
    x += wseg

# ---------- LEAD SCENES ----------
def scene_kyiv(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 52))
    for sx, sy2 in [(20, 10), (70, 18), (150, 8), (240, 14), (290, 22)]:
        d.ellipse([x + sx, y + sy2, x + sx + 3, y + sy2 + 3], fill=WHITE)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(38, 78, 110))
    for bx in (30, 130, 230):
        d.line([x + bx, y + h - 26, x + bx + 60, y + h - 26], fill=(200, 200, 200), width=3)
        d.line([x + bx + 8, y + h - 26, x + bx + 8, y + h - 44], fill=(180, 180, 180), width=2)
        d.line([x + bx + 52, y + h - 26, x + bx + 52, y + h - 44], fill=(180, 180, 180), width=2)
    for tx, ty in [(40, 6), (120, 2), (210, 10)]:
        for k in range(5):
            d.point((x + tx + k * 9, y + ty + k * 5), fill=(255, 170, 60))
        d.line([x + tx, y + ty, x + tx + 40, y + ty + 22], fill=(255, 170, 60), width=3)
    for gx in (55, 160, 255):
        d.polygon([(x + gx + 2, y + h - 24), (x + gx + 11, y + h - 44), (x + gx + 20, y + h - 24)], fill=(255, 110, 30))
        d.ellipse([x + gx, y + h - 30, x + gx + 22, y + h - 22], fill=(255, 150, 40))

def scene_cyclone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx, cy = x + w // 2, y + h // 2
    for r in (34, 25, 16, 8):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=WHITE)
    d.polygon([(x + w - 70, y + h), (x + w, y + h - 30), (x + w, y + h)], fill=(214, 186, 130))
    for i in range(14):
        rx = x + 12 + i * 22
        d.line([rx, y + 6, rx - 6, y + 18], fill=(200, 235, 240), width=2)

def scene_markets(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 22, 34))
    pts = [(8, 14), (45, 20), (80, 34), (115, 30), (150, 52), (185, 64)]
    for i in range(len(pts) - 1):
        d.line([x + pts[i][0], y + pts[i][1], x + pts[i + 1][0], y + pts[i + 1][1]], fill=RED, width=3)
    for px, py in pts:
        d.ellipse([x + px - 3, y + py - 3, x + px + 3, y + py + 3], fill=RED)
    rows = ["Taipei \u22126.2%", "Seoul \u22125.2%", "Tokyo \u22125.1%", "Hong Kong \u22121.9%"]
    f = F(SANS_B, 9)
    for i, r in enumerate(rows):
        d.text((x + w - 108, y + 10 + i * 17), r, font=f, fill=(255, 120, 120) if i == 0 else WHITE)

leads = [
    dict(n=1, banner_t="KYIV", bcol=RED, chip_t="Officials\u2019 count", scene=scene_kyiv,
         kicker="KYIV, UKRAINE \u00b7 WAR", head="Russian missiles hit three Kyiv bridges",
         dek="An overnight barrage of more than 110 missiles and 400 drones killed at least nine people across Ukraine and cut power and water in the capital.",
         src="(Kyiv Independent, BBC)"),
    dict(n=2, banner_t="CYCLONE AKVAN", bcol=NAVY, chip_t="Weather office", scene=scene_cyclone,
         kicker="ODISHA, INDIA \u00b7 CYCLONE", head="Cyclone Akvan comes ashore in eastern India",
         dek="The storm crossed the coast near Gopalpur from about 8 am after more than 300,000 people were moved to shelters. No deaths were reported.",
         src="(IMD, Deccan Herald)"),
    dict(n=3, banner_t="AI SELL-OFF", bcol=RED, chip_t="Closing prices", scene=scene_markets,
         kicker="TAIPEI \u00b7 SEOUL \u00b7 TOKYO \u00b7 MARKETS", head="AI sell-off sinks Asia\u2019s stock markets",
         dek="Taiwan\u2019s index fell 6.2% to end its worst week since 1991. Seoul lost 5.2% and Tokyo 5.1% as chipmakers led the slide.",
         src="(Reuters, Bloomberg)"),
]
ly = 182
leadw = (CW - 12) // 3
sceneh = 76
for i, L in enumerate(leads):
    x = M + i * (leadw + 6)
    L["scene"](x, ly, leadw, sceneh)
    banner(d, x + 5, ly + 5, L["banner_t"], L["bcol"], 10)
    chip(d, x + 5, ly + sceneh - 18, L["chip_t"])
    num_badge(d, x + leadw - 13, ly + 13, L["n"])
    ty = ly + sceneh + 4
    d.text((x, ty), L["kicker"], font=F(SANS_B, 7), fill=RED); ty += 11
    ty = text_block(d, x, ty, L["head"], F(SERIF_B, 14), INK, leadw - 2, leading=16, max_lines=2)
    ty = text_block(d, x, ty + 1, L["dek"], F(SANS_R, 8), INK, leadw - 2, leading=10, max_lines=4)
    d.text((x, ty + 1), L["src"], font=F(SANS_B, 7), fill=GREY)


# ---------- TEN CARDS ----------
def card_scene(kind, x, y, w, h):
    if kind == 4:
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        d.rectangle([x + 14, y + 8, x + 58, y + h - 8], fill=(30, 70, 160))
        d.polygon([(x + 14, y + 8), (x + 58, y + h - 8), (x + 50, y + h - 8), (x + 14, y + 16)], fill=WHITE)
        d.polygon([(x + 58, y + 8), (x + 14, y + h - 8), (x + 22, y + h - 8), (x + 58, y + 16)], fill=WHITE)
        d.rectangle([x + 31, y + 8, x + 41, y + h - 8], fill=RED)
        d.rectangle([x + 14, y + h // 2 - 5, x + 58, y + h // 2 + 5], fill=RED)
        cx, cy = x + w - 66, y + h // 2
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=(255, 210, 60), width=2)
        import math
        for k in range(12):
            a = 2 * math.pi * k / 12
            sx, sy2 = cx + 15 * math.cos(a), cy + 15 * math.sin(a)
            d.ellipse([sx - 2, sy2 - 2, sx + 2, sy2 + 2], fill=(255, 210, 60))
    elif kind == 5:
        d.rectangle([x, y, x + w, y + h], fill=(96, 150, 70))
        d.polygon([(x + 40, y + 28), (x + 120, y + 20), (x + 128, y + 30), (x + 48, y + 38)], fill=(70, 70, 70))
        d.polygon([(x + 120, y + 20), (x + 138, y + 25), (x + 128, y + 30)], fill=(80, 80, 80))
        d.rectangle([x + 150, y + 10, x + 156, y + 34], fill=WHITE)
        d.rectangle([x + 150, y + 10, x + 156, y + 22], fill=RED)
    elif kind == 6:
        d.rectangle([x, y, x + w, y + h], fill=(30, 90, 110))
        d.ellipse([x + 55, y + 6, x + 105, y + h - 6], fill=(70, 170, 120))
        d.arc([x + 55, y + 6, x + 105, y + h - 6], 0, 360, fill=WHITE, width=2)
        d.ellipse([x + 118, y + 10, x + 150, y + 42], outline=WHITE, width=3)
        d.line([x + 134, y + 26, x + 134, y + 16], fill=WHITE, width=2)
        d.line([x + 134, y + 26, x + 142, y + 30], fill=WHITE, width=2)
    elif kind == 7:
        d.rectangle([x, y, x + w, y + h], fill=(240, 200, 90))
        for i, bx in enumerate(range(18, w - 10, 26)):
            d.ellipse([x + bx, y + h - 30, x + bx + 12, y + h - 18], fill=INK)
            d.rectangle([x + bx - 2, y + h - 18, x + bx + 14, y + h], fill=INK)
        d.rectangle([x + 60, y + 6, x + 150, y + 22], fill=RED)
        d.text((x + 68, y + 10), "STRIKE", font=F(SANS_B, 9), fill=WHITE)
    elif kind == 8:
        d.rectangle([x, y, x + w, y + h], fill=(250, 235, 210))
        d.ellipse([x + 18, y + 8, x + 58, y + 48], fill=RED)
        for i, bh in enumerate((12, 22, 34)):
            d.rectangle([x + 90 + i * 26, y + h - 8 - bh, x + 108 + i * 26, y + h - 8], fill=NAVY)
    elif kind == 9:
        d.rectangle([x, y, x + w, y + h], fill=(34, 42, 70))
        d.polygon([(x + 10, y + 16), (x + 62, y + 4), (x + 114, y + 16)], fill=(240, 235, 220))
        d.rectangle([x + 10, y + 17, x + 114, y + 21], fill=(240, 235, 220))
        for cx2 in (16, 36, 56, 76, 96):
            d.rectangle([x + cx2, y + 23, x + cx2 + 8, y + 40], fill=(240, 235, 220))
            d.rectangle([x + cx2 - 2, y + 21, x + cx2 + 10, y + 23], fill=(240, 235, 220))
        d.rectangle([x + 6, y + 40, x + 118, y + 43], fill=(215, 208, 190))
        d.rectangle([x + 3, y + 43, x + 121, y + 46], fill=(215, 208, 190))
        d.rectangle([x, y + 46, x + 124, y + 49], fill=(215, 208, 190))
        d.line([x + 136, y + 40, x + 162, y + 18], fill=OCHRE, width=5)
        d.rectangle([x + 154, y + 10, x + 172, y + 20], fill=(150, 100, 40))
        d.rectangle([x + 128, y + 42, x + 166, y + 46], fill=(150, 100, 40))
        d.arc([x + 168, y + 8, x + 184, y + 26], -55, 55, fill=WHITE, width=2)
    elif kind == 10:
        d.rectangle([x, y, x + w, y + h], fill=(40, 100, 140))
        d.polygon([(x + 30, y + 34), (x + 130, y + 34), (x + 118, y + 46), (x + 42, y + 46)], fill=(30, 30, 30))
        d.rectangle([x + 55, y + 24, x + 105, y + 34], fill=(90, 90, 90))
        d.rectangle([x + 168, y + 10, x + 175, y + h - 10], fill=RED)
        d.rectangle([x + 162, y + 10, x + 181, y + 17], fill=RED)
    elif kind == 11:
        d.rectangle([x, y, x + w, y + h], fill=(40, 110, 180))
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=WHITE)
        d.polygon([(x + 52, y + 2), (x + 96, y + 8), (x + 92, y + 34), (x + 48, y + 28)], fill=(250, 240, 220), outline=INK)
        d.line([x + 58, y + 18, x + 68, y + 25], fill=RED, width=3)
        d.line([x + 68, y + 25, x + 84, y + 10], fill=RED, width=3)
        d.polygon([(x + 44, y + 30), (x + 104, y + 30), (x + 112, y + 38), (x + 36, y + 38)], fill=(120, 70, 30))
        d.rectangle([x + 62, y + 32, x + 86, y + 35], fill=INK)
        d.rectangle([x + 36, y + 38, x + 112, y + h - 2], fill=(150, 95, 45))
        d.rectangle([x + 36, y + 38, x + 112, y + 41], fill=(120, 70, 30))
        for sx, sy2 in [(150, 12), (168, 12), (159, 24), (150, 36), (168, 36)]:
            d.ellipse([x + sx - 3, y + sy2 - 3, x + sx + 3, y + sy2 + 3], fill=(255, 210, 60))
    elif kind == 12:
        d.rectangle([x, y, x + w, y + h], fill=(60, 140, 70))
        d.polygon([(x + 60, y + 8), (x + 74, y + 6), (x + 96, y + 38), (x + 84, y + 42)], fill=(220, 190, 130))
        d.ellipse([x + 120, y + 14, x + 138, y + 32], fill=RED)
        for sx in (140, 148, 156):
            d.rectangle([x + sx, y + 22, x + sx + 4, y + 46], fill=(240, 220, 160))
    elif kind == 13:
        d.rectangle([x, y, x + w, y + h], fill=(50, 110, 160))
        d.polygon([(x + 50, y + 26), (x + 130, y + 26), (x + 112, y + 40), (x + 66, y + 40)], fill=(120, 70, 30))
        d.line([x + 90, y + 26, x + 90, y + 10], fill=INK, width=2)
        for wx in range(10, w - 10, 28):
            d.arc([x + wx, y + h - 16, x + wx + 22, y + h - 2], 0, 180, fill=WHITE, width=2)

cards = [
    (4, "UK\u2013EU DEAL", NAVY, "Agreed \u00b7 Reuters", "BRUSSELS \u00b7 DIPLOMACY", "UK and EU seal a \u2018reset\u2019 deal", "Food trade, youth visas, carbon link."),
    (5, "POLAND: OBJECTS DOWN", (90, 90, 90), "Officials", "EASTERN POLAND \u00b7 SECURITY", "Russian missiles and a drone come down in Poland", "A Kh-101 in a field; two airports paused; no one hurt."),
    (6, "COP31: NO DEAL", TEAL, "Draft text", "ANTALYA \u00b7 CLIMATE", "COP31 reaches its last day with no deal", "The draft text leaves out fossil fuels."),
    (7, "ITALY: STRIKE", RED, "Unions", "ITALY \u00b7 LABOUR", "General strike over Italy\u2019s budget", "Workers and students march."),
    (8, "JAPAN: +2.3%", RED, "Official data", "TOKYO \u00b7 ECONOMY", "Japan\u2019s inflation picks up to 2.3%", "A December rate rise stays in view."),
    (9, "SEOUL: IMPEACH", NAVY, "Party vote", "SEOUL \u00b7 POLITICS", "Korea\u2019s ruling party moves to impeach the chief justice", "It follows an overturned conviction."),
    (10, "HORMUZ: SHUT", (160, 40, 40), "Ship trackers", "STRAIT OF HORMUZ \u00b7 ENERGY", "Hormuz shut, Brent $92.50", "Tanker traffic halted; insurers pull cover."),
    (11, "BUKELE: 3RD BID", (40, 90, 170), "Filing", "SAN SALVADOR \u00b7 POLITICS", "Bukele files to run for a third term", "The vote is on 28 February 2027."),
    (12, "PHILLIPS: 118", GREEN, "Scorecard", "WELLINGTON \u00b7 CRICKET", "Phillips hits 118 against India", "Hundreds against India in all three formats."),
    (13, "DAKAR: BOAT SINKS", (30, 80, 140), "Rescuers", "DAKAR, SENEGAL \u00b7 MIGRATION", "Migrant boat sinks: 4 dead", "A pirogue capsized off the coast; rescuers search."),
]
cardw = (CW - 16) // 5
card_scene_h = 52
rows_y = [368, 482]
for idx, (num, blab, bcol, tag, kick, head, dek) in enumerate(cards):
    r = idx // 5; c = idx % 5
    x = M + c * (cardw + 4); y = rows_y[r]
    card_scene(num, x, y, cardw, card_scene_h)
    banner(d, x + 3, y + 3, blab, bcol, 7)
    ftag = F(SANS_B, 6)
    tw = d.textlength(tag, font=ftag)
    d.rectangle([x + cardw - tw - 8, y + card_scene_h - 13, x + cardw - 2, y + card_scene_h - 2], fill=(10, 10, 10), outline=WHITE, width=1)
    d.text((x + cardw - tw - 5, y + card_scene_h - 11), tag, font=ftag, fill=WHITE)
    num_badge(d, x + cardw - 11, y + 11, num, r=8)
    ty = y + card_scene_h + 3
    d.text((x, ty), kick, font=F(SANS_B, 6), fill=RED); ty += 9
    ty = text_block(d, x, ty, head, F(SERIF_B, 10), INK, cardw - 2, leading=11, max_lines=3)
    text_block(d, x, ty + 1, dek, F(SANS_R, 7), INK, cardw - 2, leading=9, max_lines=2)

# ---------- BOTTOM: MAP + BRIEFS ----------
by = 598
d.line([M, by - 6, W - M, by - 6], fill=INK, width=1)
mapw = 296
d.rectangle([M, by, M + mapw, by + 168], fill=NAVY)
d.text((M + 8, by + 6), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=WHITE)
# dot-matrix world map: 56x22 land grid, lon -170..190 / lat 75..-60
LAND = [
    ".####.####.###...####..........#......###....#..#..#....",
    ".#####.#########..###..#..############################..",
    ".#####.##########..##..#.#############################..",
    "..##..###########........############################...",
    ".....#############.......###########################....",
    ".....############........##########################.....",
    ".....###########........#########################.#.....",
    "......########..........#########################.......",
    ".......#####...........##################.######........",
    "........####...........##################.####..........",
    "...........######.......##########.....#..####.#........",
    ".............#####.......########.........#.###.####....",
    ".............#####.......########..........###..####....",
    ".............#####........######...........##..####.....",
    ".............####.........######..............######....",
    ".............####..........####...............######....",
    "..............###..........###................#####.....",
    "..............##...........##.................####....#.",
    "..............##................................##...##.",
    "..............##.....................................#..",
    "..............#.........................................",
    "..............#.........................................",
]
assert all(len(row) == 56 for row in LAND)
gx, gy = M + 8, by + 28
for r, row in enumerate(LAND):
    for c, ch in enumerate(row):
        if ch == "#":
            cx, cy = gx + c * 5 + 2, gy + r * 5 + 2
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=CREAM)
pins = {1: (172, 40), 2: (207, 75), 3: (247, 70), 4: (140, 46), 5: (156, 47),
        6: (172, 58), 7: (147, 60), 8: (253, 52), 9: (237, 57), 10: (185, 69),
        11: (71, 80), 12: (276, 124), 13: (127, 79)}
for n, (px, py) in pins.items():
    num_badge(d, M + px, by + py, n, r=8)
cap = "Each number is the story with that number on this page."
text_block(d, M + 8, by + 144, cap, F(SANS_R, 8), WHITE, mapw - 16, leading=10, max_lines=2)

bx = M + mapw + 12
bw = W - M - bx
d.text((bx, by), "ALSO ON FRIDAY 20 NOVEMBER \u2014 23 MORE STORIES", font=F(SANS_B, 10), fill=RED)
briefs = [
    "14 Lviv \u2014 A strike on a railway station kills two (BBC)",
    "15 Moscow \u2014 Russia decries Estonia\u2019s border closure (Reuters)",
    "16 Berlin \u2014 School pupils strike against military service (Al Jazeera)",
    "17 London \u2014 General says UK runs cyber attacks abroad (Sky News)",
    "18 Beijing \u2014 China holds its loan rates for an 18th month (Xinhua)",
    "19 Tokyo \u2014 SoftBank shares fall more than 14% in a day (Al Jazeera)",
    "20 Ganjam \u2014 209 mm of rain falls as Akvan crosses Odisha (PTI)",
    "21 Lebanon \u2014 Israeli air strikes hit the south and the east (Anadolu)",
    "22 Yemen \u2014 Gunmen fire on a cargo ship off the coast (UKMTO)",
    "23 Abuja \u2014 Court bars new evidence against Tinubu (Channels TV)",
    "24 Kampala \u2014 Police told to enforce Ebola ban on rallies (allAfrica)",
    "25 Malawi \u2014 Fuel crisis brings night-long petrol queues (Al Jazeera)",
    "26 Africa \u2014 AfDB says 22 countries are in debt distress (allAfrica)",
    "27 Las Vegas \u2014 Russell fastest in wet Grand Prix practice (Autosport)",
    "28 New York \u2014 Nasdaq futures fall 1.6% before the bell (24/7 Wall St)",
    "29 Washington \u2014 Democrats query law firm\u2019s free work (Al Jazeera)",
    "30 Wellington \u2014 Nicholls makes 175 in a stand of 216 (ICC)",
    "31 Sydney \u2014 Australian shares fall 1.6% in the sell-off (Reuters)",
    "32 Antalya \u2014 Panama asks COP31 to cap world oil output (Anadolu)",
    "33 Antalya \u2014 EU official calls the climate draft unacceptable (RT\u00c9)",
    "34 Turin \u2014 ATP backs a plan to lift player pay past $350m (Anadolu)",
    "35 BepiColombo \u2014 A capture burn is due Saturday at Mercury (ESA)",
    "36 Boston \u2014 Early trial: a pill shrinks pancreatic tumours 60.7% \u2014 a claim (Reuters)",
]
colw = (bw - 10) // 2
bf = F(SANS_R, 8)
for i, b in enumerate(briefs):
    col = 0 if i < 12 else 1
    row = i if i < 12 else i - 12
    x = bx + col * (colw + 10)
    y = by + 18 + row * 26
    lines = wrap(d, b, bf, colw)
    for j, ln in enumerate(lines[:2]):
        d.text((x, y + j * 10), ln, font=bf, fill=INK)
    if row < 11 or col == 0:
        pass

# date check under map
dy = by + 176
d.rectangle([M, dy, M + mapw, dy + 118], outline=RED, width=2)
d.text((M + 7, dy + 5), "DATE CHECK", font=F(SANS_B, 10), fill=RED)
dc = "Left out as Thursday 19 November\u2019s news: the three-leader declaration in Shenzhen, Anthropic\u2019s IPO pricing, the World Court\u2019s ruling on Myanmar and GTA VI\u2019s midnight launch. Older still, not shown: the Riyadh tower attack and Voyager 1\u2019s light-day (18 Nov)."
text_block(d, M + 7, dy + 22, dc, F(SANS_R, 8), INK, mapw - 14, leading=11)

# briefs bottom note aligned under briefs columns
ny = by + 18 + 12 * 26 + 4
d.text((bx, ny), "All briefs are dated Friday 20 November 2026.", font=F(SERIF_I, 9), fill=NAVY)

# ---------- FOOTER ----------
fy = 972
d.line([M, fy, W - M, fy], fill=INK, width=2)
foot_l = "Every story here happened, or was first reported, on Friday 20 November 2026. Officials\u2019 counts are attributed."
text_block(d, M, fy + 6, foot_l, F(SANS_B, 8), INK, 640, leading=10, max_lines=2)
foot_r = "Sources named beside each story \u00b7 original drawings"
frr = F(SANS_R, 8)
d.text((W - M - d.textlength(foot_r, font=frr), fy + 6), foot_r, font=frr, fill=GREY)

# light deterministic grain on the paper only (fixed seed -> byte-identical reruns)
import numpy as np
arr = np.asarray(img).astype(np.int16)
noise = np.random.RandomState(20261120).randint(-2, 3, size=arr.shape[:2])[..., None]
mask = np.all(arr == np.array(PAPER), axis=2)[..., None]
img = Image.fromarray(np.clip(arr + np.where(mask, noise, 0), 0, 255).astype(np.uint8))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, format="PNG", optimize=True)
print("wrote", out, os.path.getsize(out))
