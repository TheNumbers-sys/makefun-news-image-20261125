from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 1024
PAPER = (247, 244, 235)
INK = (22, 25, 27)
RED = (176, 41, 34)
MUTED = (95, 91, 84)
OUT = os.path.join(os.path.dirname(__file__), "entry.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def measured_wrap(draw, text, face, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = word if not line else line + " " + word
        candidate_box = draw.textbbox((0, 0), candidate, font=face)
        if candidate_box[2] - candidate_box[0] <= max_width:
            line = candidate
        else:
            if not line:
                raise ValueError("A word exceeds its text column")
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, xy, text, face, max_width, fill=INK, gap=4, max_height=None):
    x, y = xy
    lines = measured_wrap(draw, text, face, max_width)
    box = draw.textbbox((0, 0), "Ag", font=face)
    line_h = box[3] - box[1]
    total_h = len(lines) * line_h + (len(lines) - 1) * gap
    if max_height is not None and total_h > max_height:
        raise ValueError(f"Text block overflows: {text!r} ({total_h}>{max_height})")
    for line in lines:
        bbox = draw.textbbox((x, y), line, font=face)
        measured = draw.textbbox((0, 0), line, font=face)
        line_width = measured[2] - measured[0]
        if bbox[2] > x + max_width or line_width > max_width:
            raise ValueError(f"Text line overflows width: {line!r}")
        draw.text((x, y), line, font=face, fill=fill)
        y += line_h + gap
    return y


def centered(draw, cx, y, text, face, fill=INK):
    box = draw.textbbox((0, 0), text, font=face)
    w = box[2] - box[0]
    if w > SIZE - 80:
        raise ValueError(f"Centered text too wide: {text!r}")
    draw.text((cx - w / 2, y), text, font=face, fill=fill)


def tanker_motif(draw):
    # A simple oil tanker, smoke plume and mine, drawn entirely with PIL shapes.
    draw.line((726, 249, 974, 249), fill=RED, width=2)
    draw.polygon([(738, 287), (951, 287), (931, 323), (758, 323)], fill=INK)
    draw.rectangle((782, 272, 899, 287), fill=INK)
    draw.rectangle((868, 255, 882, 272), fill=INK)
    draw.rectangle((895, 259, 908, 272), fill=INK)
    draw.line((879, 254, 879, 238), fill=INK, width=4)
    draw.ellipse((866, 220, 891, 246), fill=(190, 187, 178))
    draw.ellipse((875, 201, 904, 232), fill=(208, 205, 197))
    draw.ellipse((887, 181, 916, 213), fill=(225, 222, 214))
    draw.ellipse((926, 265, 958, 297), outline=RED, width=4)
    draw.line((942, 260, 942, 253), fill=RED, width=3)
    draw.line((922, 274, 916, 270), fill=RED, width=3)
    draw.line((962, 274, 968, 270), fill=RED, width=3)
    draw.text((742, 336), "HORMUZ · SCHEMATIC", font=font("DejaVuSans-Bold.ttf", 14), fill=MUTED)


def panel(draw, x, y, w, h, title, body):
    draw.rectangle((x, y, x + w, y + h), outline=INK, width=2)
    draw.rectangle((x, y, x + 8, y + h), fill=RED)
    title_font = font("DejaVuSans-Bold.ttf", 24)
    body_font = font("DejaVuSans.ttf", 17)
    ty = draw_wrapped(draw, (x + 20, y + 11), title, title_font, w - 36, gap=2, max_height=58)
    draw_wrapped(draw, (x + 20, ty + 6), body, body_font, w - 36, gap=3,
                 max_height=(y + h - 9) - (ty + 6))


im = Image.new("RGB", (SIZE, SIZE), PAPER)
d = ImageDraw.Draw(im)

# Masthead and date banner.
d.rectangle((34, 25, 990, 134), outline=INK, width=3)
centered(d, SIZE / 2, 35, "THE WORLD IN ONE DAY", font("DejaVuSans-Bold.ttf", 48))
d.rectangle((34, 91, 990, 134), fill=RED)
centered(d, SIZE / 2, 96, "WEDNESDAY 25 NOVEMBER 2026", font("DejaVuSans-Bold.ttf", 27), PAPER)

# Lead story.
d.rectangle((34, 150, 990, 398), outline=INK, width=3)
d.text((51, 160), "LEAD STORY", font=font("DejaVuSans-Bold.ttf", 17), fill=RED)
lead_font = font("DejaVuSans-Bold.ttf", 44)
draw_wrapped(d, (51, 185), "TANKERS HIT IN STRAIT OF HORMUZ", lead_font, 660,
             gap=1, max_height=104)
lead_body = "Iran's Revolutionary Guard says two oil tankers struck naval mines, exploded and caught fire in the Strait of Hormuz"
draw_wrapped(d, (51, 300), lead_body, font("DejaVuSans.ttf", 19), 650, gap=4, max_height=83)
tanker_motif(d)

# Second story.
d.rectangle((34, 412, 990, 542), outline=INK, width=2)
d.rectangle((34, 412, 44, 542), fill=RED)
d.text((56, 421), "HOUTHIS STRIKE SAUDI REFINERY", font=font("DejaVuSans-Bold.ttf", 30), fill=INK)
second = "Yemen's Houthis say they attacked Saudi Arabia's Ras Tanura oil refinery; a Houthi strike on a Riyadh skyscraper injured 11"
draw_wrapped(d, (56, 462), second, font("DejaVuSans.ttf", 19), 910, gap=3, max_height=65)

# Six desk briefs in a three-row grid.
briefs = [
    ("ISRAEL KILLS HAMAS SECURITY CHIEF", "Israeli military kills Hamas colonel Mohammad Abuelouf, head of its interior security service, in Gaza"),
    ("RUSSIA STRIKES ODESA", "Russian strike on Ukraine's Odesa region kills 2 and injures 3, including a child; Kyiv apartment block hit, 2 injured"),
    ("490,334 RUSSIAN SOLDIERS DEAD", "Leaked Russian statistics analysed by the BBC put Russian military deaths since 2022 at at least 490,334"),
    ("SUDAN DRONE STRIKES KILL 19", "Rapid Support Forces drone strikes kill 19 civilians and wound 20 in two Sudanese cities"),
    ("SHENZHOU 24 DOCKS", "China's Shenzhou 24 docks at its space station carrying Pakistan's first astronaut, the first foreign crew member"),
    ("HUAWEI CONVICTED IN US TRIAL", "US federal court finds Huawei guilty of trade-secrets conspiracy and bank fraud over its Iran business"),
]
grid_x, grid_y, gap_x, gap_y = 34, 554, 18, 12
panel_w, panel_h = 464, 132
for i, (title, body) in enumerate(briefs):
    col, row = i % 2, i // 2
    panel(d, grid_x + col * (panel_w + gap_x), grid_y + row * (panel_h + gap_y),
          panel_w, panel_h, title, body)

# Secondary bottom digest.
strip_y = 986
d.line((34, strip_y - 8, 990, strip_y - 8), fill=RED, width=3)
also = "ALSO: Pope Leo XIV warns COP31 climate talks failed to reach a deal; Australia and Solomon Islands sign treaty barring foreign military bases; Bangladesh raises garment workers' minimum wage 36% to $139"
draw_wrapped(d, (40, strip_y), also, font("DejaVuSans.ttf", 13), 944, fill=INK,
             gap=1, max_height=35)

# Check the bottom digest's full text box remains inside the image canvas.
digest_lines = measured_wrap(d, also, font("DejaVuSans.ttf", 13), 944)
digest_font = font("DejaVuSans.ttf", 13)
digest_h = len(digest_lines) * (d.textbbox((0, 0), "Ag", font=digest_font)[3] -
                                d.textbbox((0, 0), "Ag", font=digest_font)[1]) + len(digest_lines) - 1
if strip_y + 35 > SIZE:
    raise ValueError("Bottom digest leaves canvas")
if strip_y + digest_h > SIZE:
    raise ValueError("Bottom digest text exceeds canvas")
im.save(OUT, format="PNG", optimize=True)
print(f"Wrote {OUT}: {im.size[0]}x{im.size[1]}")
