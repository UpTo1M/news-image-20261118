"""PIL drawing code for the news-image-20261118 front page.

Draws a 1024x1024 newspaper front page for WEDNESDAY, 18 NOVEMBER 2026.
Deterministic: fixed fonts, fixed text, no randomness, no timestamps.
Standard library + Pillow only. No network.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

PAPER = (248, 244, 236)
INK = (26, 26, 26)
MUTED = (92, 88, 80)
NAVY = (20, 33, 61)
NAVY_PANEL = (24, 42, 78)
RED = (185, 28, 28)
GOLD = (201, 162, 39)
GOLD_LIGHT = (227, 179, 65)
BLUE = (29, 78, 216)
TEAL = (13, 148, 136)
LIGHT_BLUE = (56, 130, 200)
BORDER = (214, 206, 188)
WHITE = (255, 255, 255)
FOOTER_LINE = (120, 132, 165)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Wrap text to fit max_width pixels. Returns a list of lines."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_spaced_text(draw, xy, text, fnt, fill, tracking=4):
    """Draw text with extra letter spacing (tracking) for the date line."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def spaced_width(draw, text, fnt, tracking=4):
    total = 0
    for ch in text:
        total += draw.textlength(ch, font=fnt) + tracking
    return total - tracking


# ---------------------------------------------------------------- icons

def draw_wave(draw, x0, x1, base_y, amp, period, fill, width=2):
    pts = []
    x = x0
    while x <= x1:
        y = base_y + amp * math.sin(2 * math.pi * (x - x0) / period)
        pts.append((x, y))
        x += 4
    draw.line(pts, fill=fill, width=width)


def draw_ship(draw, x0, y0, w, h):
    """Stylised oil tanker in a navy panel. Panel: (x0, y0, w, h)."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY_PANEL)
    # alert sun
    draw.ellipse([x0 + 18, y0 + 14, x0 + 52, y0 + 48], fill=RED)
    # hull
    hull_y = y0 + h - 62
    draw.polygon(
        [(x0 + 22, hull_y), (x0 + w - 22, hull_y),
         (x0 + w - 46, hull_y + 30), (x0 + 46, hull_y + 30)],
        fill=(232, 224, 208),
    )
    draw.rectangle([x0 + 22, hull_y, x0 + w - 22, hull_y + 4], fill=RED)
    # containers on deck
    cx = x0 + 58
    cy = hull_y - 26
    cols = [RED, GOLD, (240, 240, 240), BLUE, GOLD, RED, (240, 240, 240)]
    for i, c in enumerate(cols):
        draw.rectangle([cx + i * 34, cy, cx + i * 34 + 30, cy + 26], fill=c)
    # bridge tower
    bx = x0 + w - 66
    draw.rectangle([bx, hull_y - 52, bx + 34, hull_y], fill=(240, 240, 240))
    draw.rectangle([bx + 5, hull_y - 46, bx + 29, hull_y - 34], fill=NAVY)
    # funnel
    draw.rectangle([x0 + 30, hull_y - 46, x0 + 52, hull_y], fill=(60, 60, 60))
    draw.rectangle([x0 + 30, hull_y - 46, x0 + 52, hull_y - 38], fill=RED)
    # waves
    wy = y0 + h - 18
    draw_wave(draw, x0 + 14, x0 + w - 14, wy, 3, 46, (110, 140, 190), 2)
    draw_wave(draw, x0 + 14, x0 + w - 14, wy + 8, 3, 38, (80, 112, 165), 2)


def draw_bridge_icon(draw, x, y, s, color):
    """Simple suspension bridge in a s x s box at (x, y)."""
    # deck
    draw.line([(x + 2, y + s - 12), (x + s - 2, y + s - 12)], fill=color, width=4)
    # arch
    draw.arc([x + 4, y + 6, x + s - 4, y + s - 6], 180, 360, fill=color, width=4)
    # pillars
    for px in (x + 8, x + s // 2, x + s - 10):
        draw.line([(px, y + s - 12), (px, y + 12)], fill=color, width=3)


def draw_missile_icon(draw, x, y, s, color):
    """Simple upward missile in a s x s box at (x, y)."""
    cx = x + s // 2
    # body
    draw.rectangle([cx - 6, y + 14, cx + 6, y + s - 14], fill=color)
    # nose
    draw.polygon([(cx - 6, y + 14), (cx + 6, y + 14), (cx, y + 2)], fill=color)
    # fins
    draw.polygon([(cx - 6, y + s - 18), (cx - 14, y + s - 8), (cx - 6, y + s - 10)],
                 fill=color)
    draw.polygon([(cx + 6, y + s - 18), (cx + 14, y + s - 8), (cx + 6, y + s - 10)],
                 fill=color)
    # flame
    draw.polygon([(cx - 5, y + s - 12), (cx + 5, y + s - 12), (cx, y + s - 2)],
                 fill=(230, 120, 40))


def draw_snowflake_icon(draw, x, y, s, color):
    """Six-point snowflake in a s x s box at (x, y)."""
    cx, cy = x + s // 2, y + s // 2
    r = s // 2 - 4
    for k in range(3):
        ang = math.radians(60 * k)
        dx = r * math.cos(ang)
        dy = r * math.sin(ang)
        draw.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=color, width=4)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)


def draw_globe_icon(draw, x, y, s, color):
    """Simple globe in a s x s box at (x, y)."""
    cx, cy = x + s // 2, y + s // 2
    r = s // 2 - 3
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    draw.ellipse([cx - r, cy - 6, cx + r, cy + 6], outline=color, width=3)
    draw.arc([cx - 8, cy - r, cx + 8, cy + r], 90, 270, fill=color, width=2)
    draw.arc([cx - 8, cy - r, cx + 8, cy + r], 270, 90, fill=color, width=2)


def draw_skyline_icon(draw, x, y, s, color):
    """Simple city skyline in a s x s box at (x, y)."""
    base = y + s - 6
    widths = [12, 16, 12]
    heights = [26, 38, 22]
    bx = x + 4
    for wdt, hgt in zip(widths, heights):
        draw.rectangle([bx, base - hgt, bx + wdt, base], fill=color)
        bx += wdt + 4


# ---------------------------------------------------------------- page

def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 110], fill=NAVY)
    f_title = font(SERIF_BOLD, 64)
    title = "WORLD NEWS"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 10), title, font=f_title, fill=WHITE)
    f_date = font(SANS_BOLD, 27)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = spaced_width(d, date, f_date, tracking=4)
    draw_spaced_text(d, ((W - dw) / 2, 76), date, f_date, GOLD_LIGHT, tracking=4)
    d.rectangle([0, 110, W, 114], fill=RED)

    # ---- lead story ----------------------------------------------------
    lead_y0, lead_y1 = 122, 318
    d.rectangle([28, lead_y0, 996, lead_y1], fill=WHITE, outline=BORDER, width=1)
    d.rectangle([28, lead_y0, 996, lead_y0 + 4], fill=RED)
    f_kicker = font(SANS_BOLD, 15)
    d.text((44, lead_y0 + 14), "LEAD STORY", font=f_kicker, fill=RED)
    f_lead_head = font(SANS_BOLD, 34)
    d.text((44, lead_y0 + 36), "US-IRAN WAR ESCALATES",
           font=f_lead_head, fill=INK)
    f_lead_body = font(SANS, 17)
    lead_text = (
        "The US said it sank five Iranian oil tankers \u2014 Kaviz, Charminar, "
        "Horizon 1, Riesco and Derya \u2014 after Iran's Revolutionary Guards "
        "allegedly tried twice to target a US warship. Iran said it attacked "
        "ten ships near the Strait of Hormuz and fired missiles at US forces "
        "at the Al-Azraq base in Jordan."
    )
    lines = wrap_text(d, lead_text, f_lead_body, 596)
    ly = lead_y0 + 80
    for ln in lines:
        d.text((44, ly), ln, font=f_lead_body, fill=INK)
        ly += 22
    # illustration panel, right of the lead text
    draw_ship(d, 656, lead_y0 + 12, 340, lead_y1 - lead_y0 - 24)

    # ---- grid stories 2-5 ---------------------------------------------
    stories = [
        {
            "kicker": "UKRAINE", "color": BLUE,
            "headline": "UKRAINE HITS KERCH BRIDGE AGAIN",
            "body": (
                "Kyiv struck the bridge to occupied Crimea for a second night, "
                "shutting it down, while Russia hit two of its own bridges. US "
                "officials criticised the deep strikes as Zelenskyy met US "
                "envoys Kushner and Witkoff."
            ),
            "icon": draw_bridge_icon,
        },
        {
            "kicker": "NORTH KOREA", "color": RED,
            "headline": "NORTH KOREA FIRES MISSILE",
            "body": (
                "Pyongyang launched a ballistic missile towards the Sea of Japan, "
                "South Korea's Joint Chiefs of Staff said, amid heightened "
                "tensions after a landmine incident at the inter-Korean border."
            ),
            "icon": draw_missile_icon,
        },
        {
            "kicker": "GAZA", "color": LIGHT_BLUE,
            "headline": "UN WARNS OF GAZA COLD DEATHS",
            "body": (
                "The UN warned of more deaths from cold as displaced Palestinians "
                "face winter without shelter. Over 1.7 million remain displaced; "
                "Australia, Canada, Italy and the UK called on Israel to allow "
                "unrestricted aid access."
            ),
            "icon": draw_snowflake_icon,
        },
        {
            "kicker": "CLIMATE", "color": TEAL,
            "headline": "COP31 TALKS ENTER DECISIVE PHASE",
            "body": (
                "Negotiators at the COP31 climate talks in Antalya entered the "
                "decisive phase, working through a first draft agreement with 144 "
                "disputed items before the summit ends on Friday, 20 November."
            ),
            "icon": draw_globe_icon,
        },
    ]
    f_head = font(SANS_BOLD, 23)
    f_body = font(SANS, 16)
    cols = [28, 526]
    rows = [330, 532]
    cell_w, cell_h = 470, 190
    for i, st in enumerate(stories):
        cx = cols[i % 2]
        cy = rows[i // 2]
        d.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=WHITE,
                    outline=BORDER, width=1)
        d.rectangle([cx, cy, cx + cell_w, cy + 4], fill=st["color"])
        d.text((cx + 16, cy + 14), st["kicker"], font=f_kicker, fill=st["color"])
        st["icon"](d, cx + cell_w - 72, cy + 12, 56, st["color"])
        head_lines = wrap_text(d, st["headline"], f_head, cell_w - 32 - 72)
        hy = cy + 36
        for ln in head_lines[:2]:
            d.text((cx + 16, hy), ln, font=f_head, fill=INK)
            hy += 27
        body_lines = wrap_text(d, st["body"], f_body, cell_w - 32)
        by = hy + 6
        for ln in body_lines[:4]:
            d.text((cx + 16, by), ln, font=f_body, fill=INK)
            by += 20

    # ---- story 6, full-width strip --------------------------------------
    s6_y0, s6_y1 = 734, 850
    d.rectangle([28, s6_y0, 996, s6_y1], fill=WHITE, outline=BORDER, width=1)
    d.rectangle([28, s6_y0, 996, s6_y0 + 4], fill=TEAL)
    d.text((44, s6_y0 + 12), "ASIA", font=f_kicker, fill=TEAL)
    draw_skyline_icon(d, 920, s6_y0 + 10, 56, TEAL)
    f_s6_head = font(SANS_BOLD, 24)
    d.text((44, s6_y0 + 34), "TRUMP IN MANILA, XI HOSTS APEC",
           font=f_s6_head, fill=INK)
    s6_text = (
        "Trump arrived in Manila for Quad talks ahead of a China visit, while "
        "Xi Jinping hosted the APEC summit in Shenzhen and warned "
        "unilateralism and protectionism are on the rise."
    )
    s6_lines = wrap_text(d, s6_text, f_body, 936)
    sy = s6_y0 + 66
    for ln in s6_lines[:2]:
        d.text((44, sy), ln, font=f_body, fill=INK)
        sy += 20

    # ---- footer strip ----------------------------------------------------
    f_y0, f_y1 = 862, 1004
    d.rectangle([0, f_y0, W, f_y1], fill=NAVY)
    f_foot_head = font(SANS_BOLD, 18)
    d.text((44, f_y0 + 12), "ALSO TODAY", font=f_foot_head, fill=GOLD_LIGHT)
    f_foot = font(SANS, 16)
    d.text((44, f_y0 + 40),
           "Israel's president taps Eisenkot to form government, bypassing Netanyahu.",
           font=f_foot, fill=WHITE)
    d.text((44, f_y0 + 64),
           "Cyber-attack disables supermarket freezers across seven European countries.",
           font=f_foot, fill=WHITE)
    d.line([(44, f_y0 + 94), (980, f_y0 + 94)], fill=FOOTER_LINE, width=1)
    f_small = font(SANS, 13)
    d.text((44, f_y0 + 104),
           "WORLD NEWS \u2014 WEDNESDAY, 18 NOVEMBER 2026",
           font=f_small, fill=(170, 180, 205))

    return img


if __name__ == "__main__":
    build_image().save("/tmp/news-image-20261118-preview.png")
    print("preview saved")
