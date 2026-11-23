#!/usr/bin/env python3
"""Draw the news-image-20261122 front page: one 1024x1024 PNG.

Reads stories.json next to this file, writes entry.png next to it.
Deterministic: fixed layout, fixed strings, no clock, no randomness.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W = H = 1024
MARGIN = 28
INK = (18, 18, 18)
PAPER = (250, 247, 238)
RED = (178, 34, 34)
BLUE = (24, 62, 110)
GREY = (96, 94, 88)
LIGHT = (232, 228, 216)
GREEN = (46, 110, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_center(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def main():
    data = json.loads((HERE / "stories.json").read_text())
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN  # 968

    # ---------- Masthead ----------
    y = 26
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=INK)
    y += 10
    draw_center(d, W // 2, y, data["paper"], SERIF_B(58))
    y += 74
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=INK)
    y += 8
    d.text((MARGIN, y), data["date"], font=SANS_B(17), fill=RED)
    right = "WORLD NEWS IN ONE IMAGE"
    d.text((W - MARGIN - d.textlength(right, font=SANS_B(17)), y), right,
           font=SANS_B(17), fill=INK)
    y += 26
    d.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=INK)

    # ---------- Hero ----------
    y += 14
    hero = data["hero"]
    d.text((MARGIN, y), hero["kicker"], font=SANS_B(16), fill=RED)
    y += 26
    for line in wrap(d, hero["headline"], SERIF_B(52), inner):
        d.text((MARGIN, y), line, font=SERIF_B(52), fill=INK)
        y += 60
    y += 2
    for line in wrap(d, hero["deck"], SERIF(20), inner):
        d.text((MARGIN, y), line, font=SERIF(20), fill=(52, 52, 48))
        y += 27
    y += 8
    # numbers band
    band = "2 DAYS OVERTIME  ·  LONGEST CLIMATE SUMMIT ON RECORD  ·  ~200 NATIONS  ·  0 FOSSIL-FUEL MENTIONS"
    d.rectangle([MARGIN, y, W - MARGIN, y + 30], fill=LIGHT)
    draw_center(d, W // 2, y + 7, band, SANS_B(14), fill=BLUE)
    y += 42

    # ---------- Tiles: 5 across ----------
    gap = 10
    tw = (inner - 4 * gap) // 5  # 185
    tile_top = y
    for i, tile in enumerate(data["tiles"]):
        x = MARGIN + i * (tw + gap)
        d.line([x, tile_top, x + tw, tile_top], fill=RED, width=3)
        ty = tile_top + 8
        d.text((x, ty), tile["kicker"], font=SANS_B(11), fill=RED)
        ty += 18
        for line in wrap(d, tile["headline"], SERIF_B(19), tw):
            d.text((x, ty), line, font=SERIF_B(19), fill=INK)
            ty += 23
        ty += 3
        for line in wrap(d, tile["body"], SERIF(12.5), tw)[:6]:
            d.text((x, ty), line, font=SERIF(12.5), fill=(52, 52, 48))
            ty += 16
    y = tile_top + 218

    # ---------- Wide tile: Bitcoin ----------
    wide = data["wide"]
    d.rectangle([MARGIN, y, W - MARGIN, y + 92], outline=BLUE, width=2)
    d.text((MARGIN + 12, y + 8), wide["kicker"], font=SANS_B(12), fill=BLUE)
    d.text((MARGIN + 12, y + 26), wide["headline"], font=SERIF_B(21), fill=INK)
    for j, line in enumerate(wrap(d, wide["body"], SERIF(13), 620)[:2]):
        d.text((MARGIN + 12, y + 52 + j * 17), line, font=SERIF(13), fill=(52, 52, 48))
    # sparkline: Sat low -> Sun high
    sx, sy, sw, sh = W - MARGIN - 250, y + 10, 238, 44
    pts = [(sx + i * sw / 4, sy + sh - (v - 55.0) / 7.0 * sh)
           for i, v in enumerate([60.0, 55.1, 60.1, 59.3, 61.6])]
    d.line(pts, fill=GREEN, width=3)
    d.text((sx, sy + sh + 4), "$55.1k Sat low  →  $61.6k Sun high", font=SANS(10), fill=GREY)
    y += 104

    # ---------- IN BRIEF ----------
    d.text((MARGIN, y), "IN BRIEF", font=SANS_B(15), fill=RED)
    y += 24
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=INK)
    y += 8
    col_w = (inner - 20) // 2
    briefs = data["briefs"]
    for idx, item in enumerate(briefs):
        col = idx % 2
        row = idx // 2
        x = MARGIN + col * (col_w + 20)
        by = y + row * 34
        d.text((x, by), "▪", font=SANS_B(13), fill=RED)
        for j, line in enumerate(wrap(d, item, SERIF(12.5), col_w - 18)):
            d.text((x + 16, by + j * 16), line, font=SERIF(12.5), fill=(40, 40, 38))
            if j >= 1:
                break
    y += 3 * 34 + 6

    # ---------- Markets strip ----------
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=INK)
    y += 8
    label = "MARKETS — FRIDAY'S CLOSES (20 NOV) · MARKETS SHUT SATURDAY & SUNDAY"
    draw_center(d, W // 2, y, label, SANS_B(13), fill=BLUE)
    y += 24
    mw = inner // 8
    for i, (name, val, chg) in enumerate(data["markets"]):
        x = MARGIN + i * mw
        cx = x + mw // 2
        draw_center(d, cx, y, name, SANS_B(11), fill=GREY)
        draw_center(d, cx, y + 16, val, SANS_B(13))
        colour = GREEN if chg.startswith("+") else RED
        draw_center(d, cx, y + 33, chg, SANS_B(13), fill=colour)
    y += 56

    # ---------- Footer ----------
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=INK)
    y += 7
    foot = "Sources: AP, Reuters, UN News, ESA, CoinMarketCap  ·  The Daily Ledger — a one-page front page for Sunday, 22 November 2026"
    draw_center(d, W // 2, y, foot, SANS(11), fill=GREY)

    out = HERE / "entry.png"
    img.save(out, "PNG")
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
