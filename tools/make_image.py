#!/usr/bin/env python3
"""Draw a 1024x1024 photo-led news poster for Friday 20 November 2026.

Everything is drawn in code with PIL: a sunset summit-skyline scene
dominates the top, with the six stories as captioned strips below.
Deterministic: fixed geometry, fixed colours, no timestamps, no network.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 10)


def main():
    img = Image.new("RGB", (W, H), (247, 243, 234))
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.text((36, 12), "THE DAILY HORIZON", font=font(SERIF, 34),
           fill=(18, 22, 48))
    date_txt = "Friday, 20 November 2026"
    df = font(SANS_BOLD, 20)
    d.text((W - 36 - d.textlength(date_txt, font=df), 22), date_txt,
           font=df, fill=(150, 40, 30))
    d.rectangle([36, 62, W - 36, 65], fill=(18, 22, 48))

    # ---------- scene panel: sunset sky ----------
    px0, py0, px1, py1 = 36, 74, W - 36, 640
    top_col = (22, 28, 74)
    mid_col = (196, 82, 88)
    hor_col = (255, 158, 74)
    horizon_y = 500
    for y in range(py0, horizon_y):
        t = (y - py0) / (horizon_y - py0)
        col = lerp(top_col, mid_col, t) if t < 0.55 else lerp(
            mid_col, hor_col, (t - 0.55) / 0.45)
        d.line([(px0, y), (px1, y)], fill=col)
    # sun with soft glow (high in the sky, clear of the skyline)
    sx, sy = 830, 175
    d.ellipse([sx - 80, sy - 80, sx + 80, sy + 80], fill=(255, 172, 84))
    d.ellipse([sx - 54, sy - 54, sx + 54, sy + 54], fill=(255, 214, 130))
    # a few birds
    for bx, by, s in ((180, 180, 16), (240, 150, 12), (300, 195, 14),
                      (620, 140, 12), (860, 200, 15)):
        d.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340,
              fill=(30, 32, 60), width=3)
        d.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340,
              fill=(30, 32, 60), width=3)

    # ---------- skyline silhouettes (deterministic) ----------
    rng = random.Random(20261120)
    # far row
    x = px0
    while x < px1:
        bw = rng.randint(46, 92)
        bh = rng.randint(90, 210)
        d.rectangle([x, horizon_y - bh, x + bw, horizon_y],
                    fill=(74, 62, 96))
        x += bw + rng.randint(4, 18)
    # near row, darker, with lit windows
    x = px0
    while x < px1:
        bw = rng.randint(56, 104)
        bh = rng.randint(150, 290)
        d.rectangle([x, horizon_y - bh, x + bw, horizon_y],
                    fill=(16, 18, 42))
        for _ in range(bw * bh // 2600):
            wx = x + rng.randint(6, max(7, bw - 12))
            wy = horizon_y - bh + rng.randint(8, max(9, bh - 16))
            d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 196, 90))
        x += bw + rng.randint(2, 10)
    # one tall tapered tower left of centre
    tx0, tx1 = 430, 500
    d.polygon([(tx0, horizon_y), (tx0 + 8, 250), (tx1 - 8, 250),
               (tx1, horizon_y)], fill=(12, 14, 34))
    d.polygon([(tx0 + 26, 250), (tx0 + 34, 214), (tx1 - 34, 214),
               (tx1 - 26, 250)], fill=(12, 14, 34))
    d.rectangle([tx0 + 32, 196, tx1 - 32, 214], fill=(12, 14, 34))
    for wy in range(270, horizon_y - 10, 26):
        d.rectangle([tx0 + 14, wy, tx0 + 20, wy + 9], fill=(255, 196, 90))
        d.rectangle([tx1 - 20, wy + 12, tx1 - 14, wy + 21],
                    fill=(255, 196, 90))

    # ---------- foreground: three flagpoles on the ground band ----------
    gy0, gy1 = 500, 640
    d.rectangle([px0, gy0, px1, gy1], fill=(14, 16, 36))
    d.rectangle([px0, gy0, px1, gy0 + 3], fill=(150, 40, 30))
    poles = [150, 512, 874]
    # US flag: red/white stripes, blue canton
    fx, fy = poles[0], 396
    d.rectangle([fx, fy, fx + 3, gy0], fill=(200, 200, 200))
    for i in range(7):
        d.rectangle([fx + 3, fy + 8 + i * 9, fx + 83, fy + 17 + i * 9],
                    fill=(178, 34, 52) if i % 2 == 0 else (240, 240, 240))
    d.rectangle([fx + 3, fy + 8, fx + 35, fy + 35], fill=(30, 48, 110))
    # China flag: red field, yellow stars
    fx = poles[1]
    d.rectangle([fx, fy, fx + 3, gy0], fill=(200, 200, 200))
    d.rectangle([fx + 3, fy + 8, fx + 83, fy + 71], fill=(222, 41, 16))
    d.ellipse([fx + 10, fy + 15, fx + 24, fy + 29], fill=(255, 222, 0))
    for sx2, sy2 in ((fx + 34, fy + 16), (fx + 42, fy + 26),
                     (fx + 40, fy + 38), (fx + 30, fy + 40)):
        d.ellipse([sx2, sy2, sx2 + 7, sy2 + 7], fill=(255, 222, 0))
    # Russia flag: white / blue / red bands
    fx = poles[2]
    d.rectangle([fx, fy, fx + 3, gy0], fill=(200, 200, 200))
    for i, c in enumerate(((240, 240, 240), (0, 57, 166), (213, 0, 50))):
        d.rectangle([fx + 3, fy + 8 + i * 21, fx + 83, fy + 29 + i * 21],
                    fill=c)
    # caption on the ground band
    d.text((64, 516), "THE FIRST THREE-WAY SUMMIT",
           font=font(SANS_BOLD, 21), fill=(255, 190, 90))
    hl = "Trump, Xi and Putin meet in Shenzhen"
    hf = fit_font(d, hl, SANS_BOLD, 40, px1 - px0 - 56)
    d.text((64, 544), hl, font=hf, fill=(255, 255, 255))
    sub = "Joint peace declaration signed \u2014 further nuclear-risk talks pledged"
    sf = fit_font(d, sub, SANS, 22, px1 - px0 - 56)
    d.text((64, 592), sub, font=sf, fill=(210, 210, 220))

    # ---------- six captioned story strips ----------
    stories = [
        ("SUMMIT", (150, 40, 30),
         "Trump, Xi and Putin hold first three-way summit in Shenzhen",
         "Joint peace declaration signed; further nuclear-risk talks pledged."),
        ("COURT", (18, 60, 120),
         "World Court: Myanmar committed genocide against the Rohingya",
         "First such ruling against a state, judges find."),
        ("KYIV", (120, 30, 30),
         "Russia hits Kyiv hours after declaration; 8 killed",
         "Overnight missile and drone attack strikes power facilities."),
        ("MARKETS", (20, 90, 60),
         "Anthropic soars on Nasdaq debut amid broad AI sell-off",
         "Shares close near $97, 17% above the $83 offer; S&P 500 down ~2%, Nikkei down 4.8%."),
        ("RIYADH", (140, 90, 10),
         "Houthi missile damages Riyadh\u2019s tallest tower",
         "Saudi PIF tower struck in the capital\u2019s financial district."),
        ("SENATE", (30, 70, 110),
         "US Senate passes energy and data-centre reform bill",
         "Bipartisan measure aims to speed up energy projects."),
    ]
    y = 652
    for tag, chip_col, head, kick in stories:
        d.rectangle([36, y, 66, y + 30], fill=chip_col)
        tf = fit_font(d, tag, SANS_BOLD, 11, 42)
        d.text((36, y + 34), tag, font=tf, fill=chip_col)
        hf2 = fit_font(d, head, SANS_BOLD, 23, W - 36 - 84)
        d.text((84, y + 2), head, font=hf2, fill=(18, 22, 48))
        kf = fit_font(d, kick, SANS, 16, W - 36 - 84)
        d.text((84, y + 30), kick, font=kf, fill=(90, 90, 96))
        y += 60
        if y < 1010:
            d.line([(36, y - 2), (W - 36, y - 2)], fill=(210, 205, 190))
    d.rectangle([36, 1014, W - 36, 1016], fill=(18, 22, 48))

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
