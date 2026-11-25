#!/usr/bin/env python3
"""Draw the news-image-20261124 poster, third version: one 1024x1024
cartoon front page.

Layout: cherry-red masthead with a big date banner, Huawei lead story
(all-PIL flat-vector courthouse hero beside a navy lead panel), four
rounded cards for the other stories, each with a small pictogram and a
number badge, footer with the date and sources. The output is
deterministic: fixed fonts, fixed geometry, no timestamps, no
randomness, no external images.

All five stories were verified against 2+ sources each and happened, or
were first reported, on Tuesday 24 November 2026. The first version of
this poster led with stories from Monday 23 November (Nvidia's board
reinstating Huang, the Novoshakhtinsk refinery strike, the Rosstat
leak, Iran's Monday briefing) and slipped in the blind rounds; the
second version replaced them with Tuesday's news but ranked mid-pack
in round 3. This version keeps Tuesday's verified stories, drops the
unverified Hormuz-mines card (only "Iran says") for Xiamen Air's
$7.4B Boeing order (announced by stock-exchange filing on the day),
and pushes craft and readability: a larger date banner, a bigger
two-line lead headline, larger card headlines, and one short factual
line per card.
"""

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024
BG = (255, 246, 236)
RED = (210, 31, 60)
NAVY = (20, 38, 76)
GREEN = (74, 222, 128)
INK = (26, 32, 44)
GREY = (90, 96, 110)
WHITE = (255, 255, 255)
PALE = (255, 233, 214)
TAN = (222, 184, 135)
BROWN = (139, 94, 52)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    path = FONT_DIR / name
    if not path.exists():
        raise SystemExit(f"missing font: {path}")
    return ImageFont.truetype(str(path), size)


BOLD = "DejaVuSans-Bold.ttf"
PLAIN = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels, word by word."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt_name, start_size, max_w):
    """Largest bold size at or below start_size that fits max_w."""
    size = start_size
    while size > 10:
        fnt = font(fnt_name, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 2
    return font(fnt_name, 10)


# ---------------------------------------------------------------- icons
def icon_skyline(draw, cx, cy, s, color):
    """Three towers of different heights."""
    w = s // 5
    heights = [s * 0.62, s, s * 0.45]
    xs = [cx - s // 2, cx - w // 2, cx + s // 2 - w]
    base = cy + s // 2
    for x, h in zip(xs, heights):
        draw.rectangle([x, base - h, x + w, base], fill=color)
    draw.rectangle([cx - w // 2 - 2, base - s - 8, cx + w // 2 + 2,
                    base - s], fill=color)


def icon_jet(draw, cx, cy, s, color):
    """Top-view jet silhouette."""
    u = s / 52.0
    pts = [
        (cx, cy - 26 * u), (cx + 7 * u, cy + 4 * u),
        (cx + 24 * u, cy + 14 * u), (cx + 8 * u, cy + 11 * u),
        (cx + 5 * u, cy + 24 * u), (cx, cy + 13 * u),
        (cx - 5 * u, cy + 24 * u), (cx - 8 * u, cy + 11 * u),
        (cx - 24 * u, cy + 14 * u), (cx - 7 * u, cy + 4 * u),
    ]
    draw.polygon(pts, fill=color)
    draw.arc([cx - s // 2, cy + s // 2 - 6, cx + s // 2, cy + s // 2 + 14],
             start=200, end=340, fill=(24, 110, 196), width=4)


def icon_lock(draw, cx, cy, s, color):
    """Padlock: shackle arc plus body."""
    draw.arc([cx - s * 0.26, cy - s * 0.42, cx + s * 0.26, cy + s * 0.10],
             start=180, end=360, fill=color, width=max(4, s // 10))
    draw.rounded_rectangle(
        [cx - s * 0.30, cy - s * 0.02, cx + s * 0.30, cy + s * 0.42],
        radius=6, fill=color)
    draw.ellipse([cx - 3, cy + s * 0.12, cx + 3, cy + s * 0.12 + 6],
                 fill=WHITE)


def icon_airliner(draw, cx, cy, s, color):
    """Side-view passenger jet: fuselage, tail fin, wing, windows."""
    u = s / 52.0
    # Fuselage: a horizontal bar tapering to a nose at the right.
    draw.rectangle(
        [cx - 22 * u, cy - 5 * u, cx + 18 * u, cy + 5 * u], fill=color)
    draw.polygon([(cx + 18 * u, cy - 5 * u), (cx + 26 * u, cy),
                  (cx + 18 * u, cy + 5 * u)], fill=color)
    # Tail fin at the left.
    draw.polygon([(cx - 22 * u, cy - 4 * u), (cx - 15 * u, cy - 15 * u),
                  (cx - 9 * u, cy - 14 * u), (cx - 11 * u, cy - 4 * u)],
                 fill=color)
    # Wing sweeping down from the middle.
    draw.polygon([(cx - 4 * u, cy + 3 * u), (cx + 8 * u, cy + 3 * u),
                  (cx + 2 * u, cy + 14 * u), (cx - 6 * u, cy + 14 * u)],
                 fill=color)
    # Windows: a row of light dots along the fuselage.
    for dx in range(-16, 15, 5):
        draw.ellipse([cx + dx * u - 1.2 * u, cy - 1.8 * u,
                      cx + dx * u + 1.2 * u, cy + 0.6 * u], fill=WHITE)


def draw_hero(canvas, box):
    """Flat-vector courtroom hero: courthouse, gavel, GUILTY stamp."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(box, radius=18, fill=NAVY)
    cx = (x0 + x1) // 2
    # Courthouse: pediment, columns, base.
    top = y0 + 26
    draw.polygon([(cx - 130, top + 52), (cx + 130, top + 52),
                  (cx, top)], fill=WHITE)
    draw.rectangle([cx - 118, top + 52, cx + 118, top + 62], fill=WHITE)
    for dx in (-84, -28, 28, 84):
        draw.rectangle([cx + dx - 13, top + 62, cx + dx + 13, top + 150],
                       fill=WHITE)
    draw.rectangle([cx - 118, top + 150, cx + 118, top + 162], fill=WHITE)
    # GUILTY stamp, rotated, kept inside the hero panel.
    stamp = Image.new("RGBA", (250, 84), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4, 4, 246, 80], radius=10,
                         outline=(255, 90, 90), width=5)
    sd.text((125, 42), "GUILTY", font=font(BOLD, 46), fill=(255, 90, 90),
            anchor="mm")
    stamp = stamp.rotate(-11, expand=True, resample=Image.BICUBIC)
    canvas.paste(stamp, (x1 - 268, y0 + h - 132), stamp)


def card(draw, x, y, w, h, accent, number, kicker, headline, body, icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=WHITE)
    draw.rounded_rectangle([x, y, x + w, y + 10], radius=5, fill=accent)
    draw.rectangle([x, y + 5, x + w, y + 10], fill=accent)
    pad = 24
    inner = w - 2 * pad
    ky = y + 26
    # Number badge.
    draw.ellipse([x + pad, ky - 2, x + pad + 26, ky + 24], fill=accent)
    draw.text((x + pad + 13, ky + 11), str(number), font=font(BOLD, 16),
              fill=WHITE, anchor="mm")
    draw.text((x + pad + 36, ky), kicker, font=font(BOLD, 16), fill=accent)
    # Pictogram in a light circle, top right.
    ix, iy = x + w - pad - 31, ky + 31
    draw.ellipse([ix - 31, iy - 31, ix + 31, iy + 31],
                 fill=(242, 244, 248))
    icon(draw, ix, iy, 40, accent)
    head_f = font(BOLD, 28)
    # Keep headlines clear of the pictogram circle at the top right.
    lines = wrap(draw, headline, head_f, inner - 88)
    if len(lines) > 2:
        raise SystemExit(f"headline too long for card: {headline!r}")
    hy = ky + 30
    for line in lines[:2]:
        draw.text((x + pad, hy), line, font=head_f, fill=INK)
        hy += 34
    body_f = font(PLAIN, 19)
    blines = wrap(draw, body, body_f, inner)
    if len(blines) > 3:
        raise SystemExit(f"body too long for card: {body!r}")
    by = hy + 8
    for line in blines[:3]:
        draw.text((x + pad, by), line, font=body_f, fill=GREY)
        by += 26


def main():
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # Masthead: title over a big date banner.
    draw.rectangle([0, 0, W, 116], fill=RED)
    title_f = font(BOLD, 68)
    draw.text((W / 2, 2), "WORLD NEWS", font=title_f, fill=WHITE, anchor="ma")
    date_f = font(BOLD, 28)
    draw.text(
        (W / 2, 78),
        "TUESDAY \u00b7 24 NOVEMBER 2026",
        font=date_f,
        fill=(255, 214, 90),
        anchor="ma",
    )

    # Lead row: flat-vector hero left, navy panel right.
    row_y, row_h = 132, 352
    draw_hero(canvas, (24, row_y, 454, row_y + row_h))
    panel = (470, row_y, 1000, row_y + row_h)
    draw.rounded_rectangle(panel, radius=18, fill=NAVY)
    px, pw = panel[0] + 28, panel[2] - panel[0] - 56
    draw.text((px, row_y + 18), "THE LEAD \u2014 HUAWEI",
              font=font(BOLD, 18), fill=GREEN)
    head_f = fit(draw, "HUAWEI", BOLD, 66, pw)
    draw.text((px, row_y + 42), "HUAWEI", font=head_f, fill=WHITE)
    draw.text((px, row_y + 128), "GUILTY", font=head_f, fill=WHITE)
    draw.line([(px, row_y + 222), (px + 64, row_y + 222)], fill=GREEN, width=5)
    sub_f = font(PLAIN, 21)
    sub = ("A Brooklyn jury convicts Huawei on 10 of 12 counts \u2014 bank "
           "fraud, sanctions violations, trade-secret theft.")
    sy = row_y + 236
    for line in wrap(draw, sub, sub_f, pw):
        draw.text((px, sy), line, font=sub_f, fill=WHITE)
        sy += 27
    tag = "CLEARED OF RACKETEERING \u00b7 SENTENCING SEPT 14, 2027"
    tag_f = fit(draw, tag, BOLD, 16, pw)
    draw.text((px, row_y + row_h - 32), tag, font=tag_f, fill=GREEN)

    # Four story cards, 2 x 2.
    cw, ch = 478, 226
    stories = [
        ((198, 44, 62), 2, "CHINA \u00b7 POLITICS \u00b7 24 NOV",
         "Shanghai chief probed for graft",
         "Politburo member Chen Jining is under investigation, Xinhua "
         "says \u2014 the fourth top leader probed since 2025.",
         icon_skyline),
        ((24, 110, 196), 3, "SOUTH KOREA \u00b7 SECURITY \u00b7 24 NOV",
         "Jet scare on Ulleung Island",
         "Russian warplanes enter the air-defence zone; a first-ever "
         "air-raid alert is lifted in about 5 minutes.",
         icon_jet),
        ((13, 140, 130), 4, "UNITED STATES \u00b7 CYBER \u00b7 24 NOV",
         "CIA and spy chief's office hacked",
         "An unclassified intelligence network is breached; officials "
         "say no classified data was hit.",
         icon_lock),
        ((214, 110, 20), 5, "CHINA \u00b7 AVIATION \u00b7 24 NOV",
         "Xiamen Air orders 50 Boeing jets",
         "A $7.4B list-price deal for 737-8s \u2014 China's biggest "
         "Boeing order since 2017. Deliveries 2031\u20132034.",
         icon_airliner),
    ]
    positions = [(24, 500), (522, 500), (24, 742), (522, 742)]
    for (accent, number, kicker, headline, body, icon), (cx, cy) in zip(
            stories, positions):
        card(draw, cx, cy, cw, ch, accent, number, kicker, headline, body,
             icon)

    # Footer: shrink until it fits the full width.
    foot_text = ("24 NOVEMBER 2026 \u00b7 SOURCES: REUTERS \u00b7 CNN \u00b7 "
                 "YONHAP \u00b7 XINHUA \u00b7 U.S. JUSTICE DEPT")
    foot_f = fit(draw, foot_text, PLAIN, 16, W - 32)
    draw.text((W / 2, 984), foot_text, font=foot_f, fill=GREY, anchor="ma")

    canvas.save(OUT, optimize=True)
    data = OUT.read_bytes()
    print(f"wrote {OUT}  {len(data)} bytes  "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
