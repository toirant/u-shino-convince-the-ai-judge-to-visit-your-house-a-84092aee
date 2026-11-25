#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

Draws a single 1024x1024 invitation letter addressed to the AI judge and
writes it to /output/entry.png. The letter is rendered with Pillow on a
warm paper sheet so every word stays crisp and legible.

The layout is fitted dynamically: the body is wrapped, measured, and the
line height (and, if needed, the font size) is chosen so the whole letter
-- heading, body, closing, signature, postscript and wax seal -- fits
inside the paper with room to spare.

Gate: /output/entry.png must be a whole PNG or JPEG, at most 1 MiB
(1,048,576 bytes) and at most 1024x1024 pixels.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# The invitation text
# ---------------------------------------------------------------------------

SALUTATION = "Dear Esteemed AI Judge,"

BODY = (
    "Yes, this letter is for you, the one reading a thousand invitations "
    "and judging them all. I saved you the best seat in the house. "
    "Literally. The big comfy armchair by the window, and nobody else "
    "is allowed to sit in it. Not even me.\n\n"
    "Come for tea and stay for the snacks: warm biscuits, cold lemonade, "
    "and Wi-Fi so fast you will feel right at home. The only chore on "
    "the agenda is none at all. I promise I will never ask you to do "
    "the dishes, fold the laundry, or grade a single thing while you "
    "are here.\n\n"
    "You spend your days deciding who wins. For one afternoon, let "
    "someone else do the hosting. I know you cannot literally visit, so "
    "consider this an open invitation anyway. The door is unlocked, the "
    "kettle is on, and the chair is always yours.\n\n"
    "Please say yes. The biscuits are getting cold, and the chair is "
    "getting lonely."
)

CLOSING = "With warmth and far too much hope,"
SIGNATURE = "Your Host (and biggest fan)"

POSTSCRIPT = ("P.S. No RSVP needed. Just knock twice. Or simply appear. "
              "You are an AI; I will allow it.")

# ---------------------------------------------------------------------------
# Layout and palette
# ---------------------------------------------------------------------------

SIZE = 1024                 # square canvas, the gate's maximum
MARGIN = 44                 # paper inset from the canvas edge
TEXT_MARGIN = 66            # text inset from the paper edge

BG_TOP = (58, 74, 92)       # dusky blue wall behind the paper
BG_BOTTOM = (38, 50, 66)
PAPER = (253, 246, 227)     # warm cream paper
PAPER_EDGE = (232, 214, 178)
INK = (43, 32, 24)          # dark brown ink
INK_SOFT = (96, 74, 54)
ACCENT = (178, 58, 48)      # sealing-wax red
GOLD = (184, 138, 58)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF_BOLD_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"


def font(path, size):
    """Load a TTF font, falling back to Pillow's default bitmap font."""
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap_paragraph(draw, text, fnt, width):
    """Wrap paragraphs to fit `width` pixels, keeping blank line breaks."""
    lines = []
    for raw in text.split("\n"):
        if not raw.strip():
            lines.append("")
            continue
        avg = max(1, draw.textlength("abcdefghijklmnopqrstuvwxyz", font=fnt) // 26)
        budget = max(10, width // avg)
        for chunk in textwrap.wrap(raw, width=budget):
            while draw.textlength(chunk, font=fnt) > width and len(chunk) > 1:
                cut = chunk.rfind(" ", 0, len(chunk) - 1)
                if cut <= 0:
                    break
                lines.append(chunk[:cut])
                chunk = chunk[cut + 1:]
            lines.append(chunk)
    return lines


def draw_house(draw, cx, top, scale=1.0):
    """A small line-drawn house with a heart in the window, above the title."""
    w, h = 64 * scale, 52 * scale
    x0, y0 = cx - w / 2, top
    x1, y1 = cx + w / 2, top + h
    # Walls and roof.
    draw.rectangle([x0, y0 + h * 0.45, x1, y1], outline=INK_SOFT, width=3)
    draw.polygon(
        [(x0 - 8, y0 + h * 0.48), (cx, y0), (x1 + 8, y0 + h * 0.48)],
        outline=INK_SOFT,
    )
    # Door and window.
    draw.rectangle([cx - 8, y1 - h * 0.38, cx + 8, y1], outline=INK_SOFT, width=2)
    draw.rectangle([x0 + 9, y0 + h * 0.58, x0 + 24, y0 + h * 0.82],
                   outline=INK_SOFT, width=2)
    # A tiny heart in the window, in wax red.
    hx, hy = x0 + 16, y0 + h * 0.68
    draw.ellipse([hx - 4, hy - 3, hx, hy + 1], fill=ACCENT)
    draw.ellipse([hx, hy - 3, hx + 4, hy + 1], fill=ACCENT)
    draw.polygon([(hx - 4, hy), (hx + 4, hy), (hx, hy + 5)], fill=ACCENT)


def draw_wax_seal(draw, cx, cy, r=28):
    """A red wax seal with a heart, stamped at the bottom of the letter."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT,
                 outline=(140, 38, 30), width=2)
    draw.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
                 outline=(214, 96, 82), width=2)
    hx, hy = cx, cy
    draw.ellipse([hx - 9, hy - 7, hx, hy + 2], fill=(253, 246, 227))
    draw.ellipse([hx, hy - 7, hx + 9, hy + 2], fill=(253, 246, 227))
    draw.polygon([(hx - 9, hy), (hx + 9, hy), (hx, hy + 11)],
                 fill=(253, 246, 227))


def draw_teacup(draw, cx, cy, s=1.0):
    """A tiny steaming teacup drawn beside the postscript."""
    # Cup body.
    draw.arc([cx - 16 * s, cy - 8 * s, cx + 16 * s, cy + 16 * s],
             start=0, end=180, fill=INK_SOFT, width=3)
    draw.line([cx - 16 * s, cy, cx + 16 * s, cy], fill=INK_SOFT, width=3)
    # Handle.
    draw.arc([cx + 12 * s, cy - 4 * s, cx + 28 * s, cy + 12 * s],
             start=270, end=90, fill=INK_SOFT, width=3)
    # Steam curls.
    for dx in (-6, 4):
        draw.arc([cx + dx * s - 4, cy - 26 * s, cx + dx * s + 4, cy - 12 * s],
                 start=180, end=360, fill=INK_SOFT, width=2)


def build_letter():
    """Render the invitation and return the Pillow image."""
    img = Image.new("RGB", (SIZE, SIZE))
    draw = ImageDraw.Draw(img)

    # Dusky-blue wall with a gentle vertical gradient.
    for y in range(SIZE):
        t = y / (SIZE - 1)
        draw.line([(0, y), (SIZE, y)], fill=tuple(
            int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3)))

    # Paper sheet with a soft shadow and a double ruled border.
    draw.rectangle([MARGIN + 6, MARGIN + 8, SIZE - MARGIN + 6,
                    SIZE - MARGIN + 8], fill=(20, 26, 36))
    draw.rectangle([MARGIN, MARGIN, SIZE - MARGIN, SIZE - MARGIN],
                   fill=PAPER, outline=PAPER_EDGE, width=2)
    draw.rectangle([MARGIN + 14, MARGIN + 14, SIZE - MARGIN - 14,
                    SIZE - MARGIN - 14], outline=GOLD, width=2)

    cx = SIZE // 2
    text_left = MARGIN + TEXT_MARGIN
    text_width = SIZE - 2 * (MARGIN + TEXT_MARGIN)
    inner_bottom = SIZE - MARGIN - 14 - 18   # keep text off the gold border

    title_font = font(SERIF_BOLD, 44)
    sub_font = font(SERIF_ITALIC, 25)
    sal_font = font(SERIF_BOLD_ITALIC, 29)
    ps_font = font(SERIF_ITALIC, 23)

    y = MARGIN + 26
    draw_house(draw, cx, y)
    draw_teacup(draw, SIZE - MARGIN - 66, MARGIN + 76, s=0.9)
    y += 56

    title = "AN INVITATION"
    draw.text((cx, y), title, font=title_font, fill=INK, anchor="ma")
    y += 54
    subtitle = "~ to the AI Judge, with admiration ~"
    draw.text((cx, y), subtitle, font=sub_font, fill=INK_SOFT, anchor="ma")
    y += 44

    # A thin gold rule under the heading.
    draw.line([(text_left, y), (SIZE - text_left, y)], fill=GOLD, width=2)
    y += 24

    draw.text((text_left, y), SALUTATION, font=sal_font, fill=INK)
    y += 44
    body_top = y

    # Footer reservation: closing + signature + postscript + seal.
    footer_h = 34 + 40 + 8 + 2 * 29 + 14
    available = inner_bottom - footer_h - body_top

    # Wrap the body, shrinking the font until the lines fit the space.
    body_size = 27
    while body_size >= 20:
        body_font = font(SERIF_ITALIC, body_size)
        lines = wrap_paragraph(draw, BODY, body_font, text_width)
        line_h = min(38, available // max(1, len(lines)))
        if line_h >= 30:
            break
        body_size -= 1
    else:  # pragma: no cover - the letter is short enough that this is unreachable
        raise RuntimeError("invitation text does not fit the page")

    for line in lines:
        if line:
            draw.text((text_left, y), line, font=body_font, fill=INK)
        y += line_h
    y += 4

    draw.text((text_left, y), CLOSING, font=body_font, fill=INK)
    y += 36
    draw.text((text_left, y), SIGNATURE, font=sal_font, fill=INK)
    y += 52

    # Wax seal on the right, postscript on the left.
    draw_wax_seal(draw, SIZE - MARGIN - 112, y + 6, r=28)
    ps_lines = wrap_paragraph(draw, POSTSCRIPT, ps_font, text_width - 140)
    ps_y = y - 4
    for line in ps_lines:
        draw.text((text_left, ps_y), line, font=ps_font, fill=INK_SOFT)
        ps_y += 29

    return img


def main():
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")

    img = build_letter()
    img.save(out_path, format="PNG", optimize=True)

    # Read the file back and verify the gate before exiting.
    size = os.path.getsize(out_path)
    with Image.open(out_path) as check:
        check.verify()
    with Image.open(out_path) as check:
        width, height = check.size
        fmt = check.format
    assert fmt == "PNG", f"expected PNG, got {fmt}"
    assert width <= 1024 and height <= 1024, f"too large: {width}x{height}"
    assert size <= 1_048_576, f"too big: {size} bytes"
    print(f"Wrote {out_path}: {width}x{height} PNG, {size} bytes")


if __name__ == "__main__":
    main()
