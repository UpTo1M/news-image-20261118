"""PIL drawing code for the news-image-20261118 front page (dense rebuild).

Draws a 1024x1024 newspaper front page for WEDNESDAY, 18 NOVEMBER 2026
with 36 real, verified stories across 6 continents, plus 3 footer briefs.
Deterministic: fixed fonts, fixed text, no randomness, no timestamps.
Standard library + Pillow only. No network.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

PAPER = (248, 244, 236)
INK = (26, 26, 26)
MUTED = (78, 74, 66)
NAVY = (20, 33, 61)
RED = (185, 28, 28)
GOLD = (201, 162, 39)
GOLD_LIGHT = (227, 179, 65)
BLUE = (29, 78, 216)
TEAL = (13, 148, 136)
ORANGE = (194, 94, 10)
PURPLE = (109, 40, 217)
GREEN = (21, 128, 61)
BORDER = (214, 206, 188)
LIGHT_LINE = (228, 221, 205)
WHITE = (255, 255, 255)
FOOTER_LINE = (120, 132, 165)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width, max_lines=None):
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
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim the last line so it fits with an ellipsis
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + " ..."
    return lines


def draw_spaced_text(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with extra letter spacing (tracking)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def spaced_width(draw, text, fnt, tracking=3):
    total = 0
    for ch in text:
        total += draw.textlength(ch, font=fnt) + tracking
    return total - tracking


# ---------------------------------------------------------------- data
# 36 real, verified stories from Wednesday, 18 November 2026.
# Lead (Gulf tankers) is drawn separately; the grid holds the other 35.

LEAD = {
    "kicker": "LEAD  \u2014  GULF WAR",
    "headline": "US SINKS FIVE IRANIAN TANKERS",
    "body": (
        "Washington destroyed five Iranian oil tankers \u2014 Kaviz, "
        "Charminar, Horizon 1, Riesco and Derya \u2014 after the Guards twice "
        "tried to hit a US warship. Iran hit back at ten ships near Hormuz "
        "and fired missiles at US forces in Jordan. Oil topped $100."
    ),
}

# (region, color, [(headline, summary), ...]) in column order.
COLUMNS = [
    [
        ("MIDDLE EAST", RED, [
            ("US STRIKES QESHM; IRAN HITS BAHRAIN",
             "US jets hit an IRGC missile site on Qeshm Island; Iran fired drones at Bahrain and Kuwait."),
            ("UN WARNS OF GAZA COLD DEATHS",
             "Four nations demand Israel open aid access as 1.7m displaced face winter without shelter."),
            ("GAZA CEASEFIRE \u2018MAY COLLAPSE\u2019",
             "Board of Peace warns the truce will fail without urgent action to shore it up."),
            ("EISENKOT TAPPED TO LEAD ISRAEL",
             "President Herzog asks the ex-army chief to form a government, bypassing Netanyahu."),
            ("YEMEN CALLS HOUTHIS TERRORISTS",
             "Parliament designates the group a terrorist organisation as it presses toward Aden."),
        ]),
        ("EUROPE", BLUE, [
            ("UKRAINE HITS KERCH BRIDGE AGAIN",
             "Second-night strike collapses the road arch into the strait; two killed, traffic halted."),
            ("RUSSIA POUNDS KYIV BRIDGES",
             "Record 1,441 Ukrainian drones downed in a day as Moscow hits the capital's crossings."),
            ("US SCOLDS KYIV ON DEEP STRIKES",
             "Washington criticises the attacks; Germany pushes back as peace talks continue."),
            ("146,000 PROTEST IN FRANCE",
             "Fourth weekend of demonstrations over living costs as unions strike nationwide."),
            ("5.3 QUAKE SHAKES ROMANIA",
             "A magnitude 5.3 earthquake strikes the country; no major damage reported."),
            ("GAS TANKER HIT IN BLACK SEA",
             "LPG carrier Gas Husky struck off Bulgaria; all 19 crew members rescued."),
            ("RUSSIAN PLANE CRASH KILLS 19",
             "Military aircraft goes down in Siberia's Kemerovo region."),
        ]),
    ],
    [
        ("ASIA", TEAL, [
            ("NORTH KOREA FIRES MISSILE",
             "Pyongyang launches a ballistic missile toward the Sea of Japan amid a landmine row."),
            ("XI, PUTIN AND TRUMP MEET IN SHENZHEN",
             "The three leaders gather at APEC for a first-ever trilateral summit on Thursday."),
            ("TRUMP MEETS QUAD IN MANILA",
             "Quad leaders discuss maritime security and cyber threats; Modi joins ASEAN talks."),
            ("CYCLONE AKVAN BEARS DOWN ON INDIA",
             "Storm heads for Andhra Pradesh landfall on 20 Nov; heavy rain over Odisha."),
            ("DHONI RETIRES FROM IPL",
             "India great ends a 19-year playing career and becomes Chennai's mentor."),
            ("INDIA WIN 10TH SAFF TITLE",
             "India beat Pakistan 2-1 in the final for a record tenth championship."),
            ("COP31 ENTERS DECISIVE PHASE",
             "Antalya climate talks deadlocked on finance, with 144 disputed items in the draft."),
        ]),
        ("AFRICA", ORANGE, [
            ("EBOLA TOPS 11,000 CASES IN CONGO",
             "Outbreak has killed more than 5,400; cases spread to Kenya, Uganda and Nigeria."),
            ("WHO APPROVES TWO EBOLA VACCINES",
             "Trials green-lit for vaccines designed for the Bundibugyo strain."),
            ("UGANDA ORDERS EBOLA QUARANTINE",
             "21-day quarantine for citizens returning from DR Congo."),
            ("NIGERIA PROBES SUSPECTED CASES",
             "Two suspected Ebola cases isolated in the northeast; contact tracing under way."),
            ("ERITREA BORDER CLASHES FLARE",
             "Fighting near the border raises fears of a wider war in Tigray."),
        ]),
    ],
    [
        ("AMERICAS", (30, 58, 138), [
            ("PELTOLA WINS ALASKA SENATE SEAT",
             "Democrat flips the seat; party reaches 56 seats in the Senate."),
            ("US LOSES MEASLES-FREE STATUS",
             "Elimination status ends after 26 years as cases pass 5,400, a 40-year high."),
            ("NVIDIA BEATS FORECASTS",
             "Chipmaker's shares jump 4% after hours as sales double year on year."),
            ("FUNDS DUMP TECH AT RECORD PACE",
             "BofA survey: tech exposure cut most since 2006; 52% expect AI capex cuts."),
            ("ANTHROPIC TO LIST ON NASDAQ",
             "AI lab set for a stock market debut on 19 November."),
            ("TRUMP: DIRTY-BOMB REPORT TAKEN SERIOUSLY",
             "President says the US is looking into a report of an Iranian dirty-bomb plot."),
        ]),
        ("OCEANIA & CULTURE", PURPLE, [
            ("CYCLONE XAVIER HITS COOK ISLANDS",
             "Category 5 storm brings gusts of 315 km/h to the Northern Cook Islands."),
            ("FIJI DECLARES DROUGHT DISASTER",
             "National disaster declared over an El Ni\u00f1o-driven drought."),
            ("FELA KUTI ENTERS ROCK HALL OF FAME",
             "Nigerian icon becomes the first African inducted into the Rock Hall."),
            ("CRICKET AUSTRALIA OPENS SANDPAPERGATE FORUM",
             "Players invited to share accounts after fresh claims by Usman Khawaja."),
            ("PATTINSON IS THE NEW JAMES BOND",
             "British actor named as the next 007."),
        ]),
    ],
]

FOOTER_BRIEFS = [
    "World Court to rule on the Myanmar genocide case on Thursday.",
    "Five EU states plan migrant return hubs in Rwanda.",
    "South Korea raises its 2027 growth forecast to 3.9%.",
]


# ---------------------------------------------------------------- page

def draw_region_header(d, x, y, w, name, color):
    """Small region header: coloured square + name + rule line."""
    d.rectangle([x, y + 2, x + 10, y + 12], fill=color)
    f = font(SANS_BOLD, 13)
    d.text((x + 16, y), name, font=f, fill=color)
    d.line([(x + 16 + d.textlength(name, font=f) + 8, y + 7),
            (x + w, y + 7)], fill=LIGHT_LINE, width=1)
    return y + 20


def draw_story(d, x, y, w, headline, summary):
    """One story cell. Returns the y just below it."""
    f_head = font(SANS_BOLD, 14)
    f_body = font(SANS, 11)
    head_lines = wrap_text(d, headline, f_head, w, max_lines=2)
    hy = y
    for ln in head_lines:
        d.text((x, hy), ln, font=f_head, fill=INK)
        hy += 17
    body_lines = wrap_text(d, summary, f_body, w, max_lines=2)
    by = hy + 1
    for ln in body_lines:
        d.text((x, by), ln, font=f_body, fill=MUTED)
        by += 14
    return by


def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 84], fill=NAVY)
    f_title = font(SERIF_BOLD, 42)
    title = "WORLD FRONT PAGE"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 8), title, font=f_title, fill=WHITE)
    f_date = font(SANS_BOLD, 20)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = spaced_width(d, date, f_date, tracking=3)
    draw_spaced_text(d, ((W - dw) / 2, 54), date, f_date, GOLD_LIGHT, tracking=3)
    d.rectangle([0, 84, W, 88], fill=RED)

    # ---- continents strip ----------------------------------------------
    f_strip = font(SANS_BOLD, 13)
    strip = "36 STORIES  \u2022  MIDDLE EAST  \u2022  EUROPE  \u2022  ASIA  \u2022  AFRICA  \u2022  AMERICAS  \u2022  OCEANIA"
    sw = d.textlength(strip, font=f_strip)
    d.text(((W - sw) / 2, 96), strip, font=f_strip, fill=NAVY)
    d.line([(16, 116), (1008, 116)], fill=BORDER, width=1)

    # ---- lead story ----------------------------------------------------
    lead_y0, lead_y1 = 124, 232
    d.rectangle([16, lead_y0, 1008, lead_y1], fill=WHITE, outline=BORDER, width=1)
    d.rectangle([16, lead_y0, 1008, lead_y0 + 4], fill=RED)
    f_kicker = font(SANS_BOLD, 13)
    d.text((30, lead_y0 + 12), LEAD["kicker"], font=f_kicker, fill=RED)
    f_lead_head = font(SANS_BOLD, 30)
    d.text((30, lead_y0 + 32), LEAD["headline"], font=f_lead_head, fill=INK)
    f_lead_body = font(SANS, 14)
    lead_lines = wrap_text(d, LEAD["body"], f_lead_body, 948, max_lines=2)
    ly = lead_y0 + 68
    for ln in lead_lines:
        d.text((30, ly), ln, font=f_lead_body, fill=INK)
        ly += 18

    # ---- story grid ----------------------------------------------------
    grid_y0 = 240
    grid_y1 = 922
    col_x = [16, 351, 686]
    col_w = 322
    f_region = font(SANS_BOLD, 13)
    for ci, regions in enumerate(COLUMNS):
        x = col_x[ci]
        y = grid_y0
        for name, color, stories in regions:
            y = draw_region_header(d, x, y, col_w, name, color)
            for headline, summary in stories:
                y = draw_story(d, x, y, col_w, headline, summary)
                y += 7
                # light divider between stories
                d.line([(x, y - 3), (x + col_w, y - 3)], fill=LIGHT_LINE, width=1)
            y += 2
        # thin vertical divider between columns
        if ci < 2:
            d.line([(x + col_w + 6, grid_y0), (x + col_w + 6, grid_y1)],
                   fill=BORDER, width=1)

    # ---- footer ---------------------------------------------------------
    f_y0, f_y1 = 930, 1018
    d.rectangle([0, f_y0, W, f_y1], fill=NAVY)
    f_foot_head = font(SANS_BOLD, 14)
    d.text((30, f_y0 + 8), "ALSO TODAY", font=f_foot_head, fill=GOLD_LIGHT)
    f_foot = font(SANS, 13)
    fy = f_y0 + 28
    for b in FOOTER_BRIEFS:
        d.text((30, fy), "\u2022  " + b, font=f_foot, fill=WHITE)
        fy += 18

    return img


if __name__ == "__main__":
    build_image().save("/tmp/news-image-20261118-rebuild-preview.png")
    print("preview saved")
