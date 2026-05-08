#!/usr/bin/env python3
"""
Bites Paper Journal Generator v4 - Lulu-compliant two-file output

Lulu Pocket Book format (4.25" × 6.875"), 78 interior pages + separate cover
spread, with 0.125" bleed on every edge.

Lulu pod_package_id: 0425X0687FCSTDPB060UW444MXX
  (4.25×6.875 / Full-Color interior / Standard / Perfect-Bound /
   60# uncoated white / Matte cover)

Outputs:
  - outbound/bites-paper-interior.pdf  (78 pages, 4.5×7.125" with bleed)
  - outbound/bites-paper-cover.pdf     (1 page, ~8.99×7.125" wide spread)

Layout strategy: existing draw functions operate in TRIM coordinates
(0,0 = bottom-left of trim region). For interior pages, we translate
the canvas by (BLEED, BLEED) so trim coordinates stay valid while the
page extends 0.125" outside on every edge.
"""

from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Lulu Pocket Book dimensions
PAGE_WIDTH = 4.25 * inch    # 107.95mm trim width
PAGE_HEIGHT = 6.875 * inch  # 174.625mm trim height
PAGE_SIZE = (PAGE_WIDTH, PAGE_HEIGHT)

# Bleed: 0.125" on every edge (Lulu requirement)
BLEED = 0.125 * inch
INTERIOR_PAGE_W = PAGE_WIDTH + 2 * BLEED   # 4.5" = 11.43cm
INTERIOR_PAGE_H = PAGE_HEIGHT + 2 * BLEED  # 7.125" = 18.10cm
INTERIOR_PAGE_SIZE = (INTERIOR_PAGE_W, INTERIOR_PAGE_H)

# Cover spread: back + spine + front, with bleed on all four edges
# Spine width formula: pages/444 + 0.06 inches (Lulu's calc for 60# white)
INTERIOR_PAGE_COUNT = 78
SPINE_WIDTH = INTERIOR_PAGE_COUNT / 444 + 0.06
SPINE_W = SPINE_WIDTH * inch
COVER_SPREAD_W = (2 * BLEED) + (2 * PAGE_WIDTH) + SPINE_W
COVER_SPREAD_H = PAGE_HEIGHT + 2 * BLEED
COVER_SPREAD_SIZE = (COVER_SPREAD_W, COVER_SPREAD_H)

# Brand colors
TERRACOTTA = HexColor('#C84B31')
CREAM = HexColor('#FAF6F0')
INK = HexColor('#2A2118')
INK_SOFT = HexColor('#6B5E50')
ACCENT_SOFT = HexColor('#F2EBDF')

# Register fonts
def register_fonts():
    """Register TTF fonts for embedding"""
    pdfmetrics.registerFont(TTFont('Fraunces-Regular', 'fonts/Fraunces-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Fraunces-SemiBold', 'fonts/Fraunces-SemiBold.ttf'))
    pdfmetrics.registerFont(TTFont('Fraunces-Black', 'fonts/Fraunces-Black.ttf'))
    pdfmetrics.registerFont(TTFont('Inter-Regular', 'fonts/Inter-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Inter-Medium', 'fonts/Inter-Medium.ttf'))
    pdfmetrics.registerFont(TTFont('Inter-Bold', 'fonts/Inter-Bold.ttf'))

def draw_cover_spread(c):
    """Lulu cover spread: back-cover | spine | front-cover, all on one wide page.

    Layout (left to right on the page):
        [bleed_left][BACK COVER region][SPINE region][FRONT COVER region][bleed_right]

    The whole page is full-bleed terracotta. Back, spine, and front share
    the same color so the spine is invisible until you actually look at the
    book edge-on. Wordmark + Nº 01 sit on the FRONT COVER region. URL +
    brand mark sit on the BACK COVER region. Spine carries vertical wordmark.
    """
    # Full-bleed terracotta everywhere
    c.setFillColor(TERRACOTTA)
    c.rect(0, 0, COVER_SPREAD_W, COVER_SPREAD_H, fill=1, stroke=0)

    # Compute region X positions (left edge of each region in cover-spread coords)
    back_left = BLEED                          # back cover starts after left bleed
    back_right = BLEED + PAGE_WIDTH            # back cover trim edge
    spine_left = back_right                    # spine starts at back trim edge
    spine_right = spine_left + SPINE_W         # spine ends
    front_left = spine_right                   # front trim edge
    front_right = front_left + PAGE_WIDTH      # front cover trim ends

    # ============= FRONT COVER (right side of spread) =============
    # Save state, translate to front trim origin so existing layout math works
    c.saveState()
    c.translate(front_left, BLEED)
    _draw_front_cover_content(c)
    c.restoreState()

    # ============= BACK COVER (left side of spread) =============
    c.saveState()
    c.translate(back_left, BLEED)
    _draw_back_cover_content(c)
    c.restoreState()

    # ============= SPINE =============
    # Vertical wordmark on the spine. Only render if spine is wide enough (>0.2")
    # US convention: spine text reads TOP-TO-BOTTOM when book lies face-up
    # (i.e. when laying the book flat with front cover up and you tilt your
    # head right, the spine reads correctly). This means -90° rotation, not +90.
    if SPINE_WIDTH >= 0.2:
        c.saveState()
        spine_cx = (spine_left + spine_right) / 2
        page_cy = COVER_SPREAD_H / 2
        c.translate(spine_cx, page_cy)
        c.rotate(-90)  # was +90; corrected for US top-to-bottom spine reading
        c.setFillColor(CREAM)
        c.setFont('Fraunces-SemiBold', 7)
        c.drawCentredString(0, -2, "Bites Paper")
        c.restoreState()

    c.showPage()

def _draw_front_cover_content(c):
    """Front cover artwork - operates in trim coordinates (0,0 to PAGE_WIDTH, PAGE_HEIGHT).
    Called from draw_cover_spread after translation; safe content area only."""
    # Wordmark "Bites Paper" at optical center (~45% from top).
    # Penguin/NYRB classic position - title sits in upper-middle, void
    # below reads as page bottom margin (functional), void above is the
    # sky that the eyebrow + N° mark pierce. Tried bottom and lower-mid;
    # both read as stranded. Optical center is where books live.
    c.setFillColor(CREAM)
    c.setFont('Fraunces-Black', 32)
    wordmark_x = 15 * mm
    wordmark_y = PAGE_HEIGHT * 0.42  # ~73mm from bottom on Pocket Book
    c.drawString(wordmark_x, wordmark_y, "Bites Paper")

    # Eyebrow above with hairline rule. Rule width matches eyebrow text width
    # so it doesn't dangle past the words. The eyebrow + rule + wordmark form
    # one tight lockup rather than three floating elements.
    eyebrow = "A FIELD JOURNAL FOR FOOD MEMORY"
    c.setFont('Inter-Medium', 7)
    eyebrow_width = c.stringWidth(eyebrow, 'Inter-Medium', 7)
    rule_y = wordmark_y + 14 * mm
    c.setStrokeColor(CREAM)
    c.setLineWidth(0.4)
    c.line(wordmark_x, rule_y, wordmark_x + eyebrow_width, rule_y)
    c.drawString(wordmark_x, rule_y + 2.5 * mm, eyebrow)
    # No "Vol. 01" under the wordmark - Nº 01 in the top-right does that job already.
    # Single naming, less clutter, wordmark breathes alone.

    # Top-right balance element: "N° 01" in Fraunces italic-ish (use Regular at small size)
    c.setFont('Fraunces-Regular', 11)
    c.setFillColor(CREAM)
    c.drawRightString(PAGE_WIDTH - 15 * mm, PAGE_HEIGHT - 18 * mm, "Nº 01")

    # Tiny terracotta-on-cream spine mark in bottom-right (keep as a subtle finishing detail)
    # Single hairline horizontal rule, not three vertical bars
    c.setLineWidth(0.4)
    c.line(PAGE_WIDTH - 22 * mm, 12 * mm, PAGE_WIDTH - 15 * mm, 12 * mm)
    # NOTE: no showPage here - this draws into the front-cover region of the spread

def _draw_back_cover_content(c):
    """Back cover artwork - operates in trim coordinates after translation.
    Mirror of front: same terracotta field with cream brand mark + URL."""
    # Cream-colored brand mark + URL centered on back cover
    c.setFillColor(CREAM)
    c.setFont('Inter-Medium', 8)
    # URL centered horizontally, ~30% up from bottom
    c.drawCentredString(PAGE_WIDTH / 2, 30 * mm, "journal.bites.kitchen")

    # Single hairline rule above URL (mirrors front cover's eyebrow rule)
    c.setStrokeColor(CREAM)
    c.setLineWidth(0.4)
    rule_w = 30 * mm
    rule_x = (PAGE_WIDTH - rule_w) / 2
    c.line(rule_x, 35 * mm, rule_x + rule_w, 35 * mm)

    # Optional tagline above the rule
    c.setFillColor(CREAM)
    c.setFont('Fraunces-Regular', 9)
    c.drawCentredString(PAGE_WIDTH / 2, 40 * mm, "For the bites you'd rather hold.")

    # Issue/date line below URL - ties back cover to the front cover's Nº 01
    # Small unifying mark, doesn't disturb the restraint
    c.setFont('Inter-Medium', 6)
    c.setFillColor(CREAM)
    c.drawCentredString(PAGE_WIDTH / 2, 25 * mm, "Nº 01  ·  2026")

def draw_title_page(c):
    """Title page: Fraunces Black centered with tagline"""
    c.setFillColor(INK)
    c.setFont('Fraunces-Black', 28)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT * 0.55, "Bites Paper")
    
    c.setFont('Inter-Medium', 11)
    c.setFillColor(INK_SOFT)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT * 0.48, "The Field Journal")
    
    c.setFont('Inter-Medium', 8)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT * 0.2, "Vol. 01 · 2026")
    
    c.showPage()

def draw_belongs_to(c):
    """This journal belongs to..."""
    c.setFillColor(INK)
    c.setFont('Inter-Medium', 10)
    c.drawString(15 * mm, PAGE_HEIGHT - 30 * mm, "This journal belongs to:")
    
    # Name line
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.3)
    c.line(15 * mm, PAGE_HEIGHT - 40 * mm, PAGE_WIDTH - 15 * mm, PAGE_HEIGHT - 40 * mm)
    
    # Date line
    c.setFont('Inter-Regular', 8)
    c.setFillColor(INK_SOFT)
    c.drawString(15 * mm, PAGE_HEIGHT - 55 * mm, "Started:")
    c.line(35 * mm, PAGE_HEIGHT - 56 * mm, PAGE_WIDTH - 15 * mm, PAGE_HEIGHT - 56 * mm)
    
    c.showPage()

def draw_how_to_use(c):
    """How to use - single page with 3 ruled prompts"""
    c.setFillColor(INK)
    c.setFont('Fraunces-SemiBold', 14)
    c.drawString(15 * mm, PAGE_HEIGHT - 25 * mm, "How to use")
    
    c.setFont('Inter-Regular', 9)
    c.setFillColor(INK_SOFT)
    
    prompts = [
        "Write the dish, the rating, the price.",
        "Then write what made it worth remembering.",
        "Skip a page if you don't have a photo. The spread waits."
    ]
    
    y = PAGE_HEIGHT - 40 * mm
    line_spacing = 20 * mm
    
    for prompt in prompts:
        c.drawString(15 * mm, y, prompt)
        # Draw a ruled line below each prompt
        c.setStrokeColor(ACCENT_SOFT)
        c.setLineWidth(0.3)
        c.line(15 * mm, y - 3 * mm, PAGE_WIDTH - 15 * mm, y - 3 * mm)
        y -= line_spacing
    
    c.showPage()

def draw_bite_spread_left(c, bite_num):
    """Left page: photo frame at top, DATE, WITH, WHERE evenly distributed
    down the taller Pocket Book page. Vertical BITE Nº rail anchors right edge.
    """

    # Photo frame (60×40mm) - upper left
    frame_x = 10 * mm
    frame_y = PAGE_HEIGHT - 50 * mm
    frame_w = 60 * mm
    frame_h = 40 * mm

    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.5)
    c.rect(frame_x, frame_y, frame_w, frame_h, fill=0, stroke=1)

    # "DATE" label + handwriting line below photo - rule width unified
    # to match WITH and WHERE below (full width minus right-margin to sidebar)
    c.setFont('Inter-Medium', 7)
    c.setFillColor(INK_SOFT)
    date_y = frame_y - 8 * mm
    c.drawString(frame_x, date_y, "DATE")
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.3)
    c.line(10 * mm, date_y - 2 * mm, PAGE_WIDTH - 15 * mm, date_y - 2 * mm)

    # Vertical sidebar on right side (12mm wide)
    sidebar_x = PAGE_WIDTH - 12 * mm
    c.setStrokeColor(TERRACOTTA)
    c.setLineWidth(1)
    c.line(sidebar_x, 5 * mm, sidebar_x, PAGE_HEIGHT - 5 * mm)

    # Vertical text "BITE Nº X" running upward
    c.saveState()
    c.translate(sidebar_x + 6 * mm, PAGE_HEIGHT / 2)
    c.rotate(90)
    c.setFont('Inter-Medium', 8)
    c.setFillColor(TERRACOTTA)
    c.drawCentredString(0, 0, f"BITE Nº {bite_num}")
    c.restoreState()

    # Top group: DATE pairs with WITH (paired metadata under photo).
    # WITH placed just below DATE (~12mm gap).
    with_y = PAGE_HEIGHT - 78 * mm
    c.setFont('Inter-Medium', 7)
    c.setFillColor(INK_SOFT)
    c.drawString(10 * mm, with_y, "WITH")
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.3)
    c.line(10 * mm, with_y - 5 * mm, PAGE_WIDTH - 15 * mm, with_y - 5 * mm)

    # NOTES - fills the middle dead zone with three ruled lines.
    # Optional field for a quick line of impression.
    notes_y = PAGE_HEIGHT - 100 * mm
    c.setFont('Inter-Medium', 7)
    c.setFillColor(INK_SOFT)
    c.drawString(10 * mm, notes_y, "FIRST IMPRESSION")
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.3)
    c.line(10 * mm, notes_y - 5 * mm, PAGE_WIDTH - 15 * mm, notes_y - 5 * mm)
    c.line(10 * mm, notes_y - 12 * mm, PAGE_WIDTH - 15 * mm, notes_y - 12 * mm)

    # WHERE block at TRUE bottom margin (symmetric to photo's top margin).
    # Photo top is at 10mm from top; WHERE bottom rule is at ~15mm from bottom.
    where_y = 32 * mm
    c.setFont('Inter-Medium', 7)
    c.setFillColor(INK_SOFT)
    c.drawString(10 * mm, where_y, "WHERE")
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.3)
    c.line(10 * mm, where_y - 5 * mm, PAGE_WIDTH - 15 * mm, where_y - 5 * mm)
    c.line(10 * mm, where_y - 12 * mm, PAGE_WIDTH - 15 * mm, where_y - 12 * mm)

    c.showPage()

def draw_bite_spread_right(c, page_num):
    """Right page: DISH anchored at top, light tag line below, then DOT GRID open canvas.
    Trust-the-writer philosophy: no rating circles, no price tiers, no preset note lines.
    The writer decides what's worth saying."""

    # "DISH" eyebrow at the very top - this is the spread anchor
    y = PAGE_HEIGHT - 18 * mm
    c.setFont('Inter-Medium', 7)
    c.setFillColor(INK_SOFT)
    c.drawString(10 * mm, y, "DISH")

    # Heavy rule for the dish name (the most important field, set apart)
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.line(10 * mm, y - 4 * mm, PAGE_WIDTH - 10 * mm, y - 4 * mm)

    # Single TAGS line directly below dish (one line, not three blanks - less prescriptive)
    y -= 12 * mm
    c.setFont('Inter-Medium', 7)
    c.setFillColor(INK_SOFT)
    c.drawString(10 * mm, y, "TAGS")
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.3)
    c.line(22 * mm, y - 1 * mm, PAGE_WIDTH - 10 * mm, y - 1 * mm)

    # OPEN CANVAS: dot grid filling the remaining space.
    # Trust the writer - they decide rating, price, story, all of it in their own words.
    # Grid stops well above the page number so the folio has breathing room.
    y -= 8 * mm
    grid_top = y
    grid_bottom = 18 * mm  # was 12mm - pulled up to give the page number clean white space
    grid_left = 10 * mm
    grid_right = PAGE_WIDTH - 10 * mm
    spacing = 3.5 * mm

    c.setFillColor(INK_SOFT)
    dot_y = grid_top
    while dot_y >= grid_bottom:
        dot_x = grid_left
        while dot_x <= grid_right:
            c.circle(dot_x, dot_y, 0.25, stroke=0, fill=1)
            dot_x += spacing
        dot_y -= spacing
    
    # Page number in TERRACOTTA - ties the right page back to the left page's
    # BITE Nº rail. The spread now has a visual rhyme (red on both pages)
    # rather than feeling lopsided (left branded, right generic).
    c.setFont('Fraunces-Regular', 8)
    c.setFillColor(TERRACOTTA)
    c.drawRightString(PAGE_WIDTH - 8 * mm, 6 * mm, str(page_num))

    c.showPage()

def draw_index_page(c, page_num):
    """Index page (2 pages total, 30 lines each)"""
    c.setFillColor(INK)
    c.setFont('Fraunces-SemiBold', 12)
    if page_num == 1:
        c.drawString(15 * mm, PAGE_HEIGHT - 20 * mm, "Index")
    
    c.setFont('Inter-Regular', 7)
    c.setFillColor(INK_SOFT)
    
    # Column headers
    y = PAGE_HEIGHT - 30 * mm if page_num == 1 else PAGE_HEIGHT - 20 * mm
    c.drawString(10 * mm, y, "Dish")
    c.drawRightString(PAGE_WIDTH - 10 * mm, y, "Page")
    
    # 30 ruled lines for entries
    y -= 5 * mm
    c.setStrokeColor(ACCENT_SOFT)
    c.setLineWidth(0.3)
    
    for i in range(30):
        c.line(10 * mm, y, PAGE_WIDTH - 10 * mm, y)
        y -= 3.5 * mm
        if y < 15 * mm:
            break
    
    c.showPage()

def draw_year_in_review(c, page_num):
    """Year in review (2 pages)"""
    if page_num == 1:
        # Page 1: "Five bites I'd eat again"
        c.setFillColor(INK)
        c.setFont('Fraunces-SemiBold', 14)
        c.drawString(15 * mm, PAGE_HEIGHT - 25 * mm, "Five bites I'd eat again")
        
        y = PAGE_HEIGHT - 40 * mm
        c.setFont('Inter-Regular', 9)
        c.setFillColor(INK_SOFT)
        c.setStrokeColor(INK_SOFT)
        c.setLineWidth(0.3)
        
        for i in range(1, 6):
            c.drawString(15 * mm, y, f"{i}.")
            c.line(20 * mm, y - 2 * mm, PAGE_WIDTH - 15 * mm, y - 2 * mm)
            y -= 15 * mm
    else:
        # Page 2: "Five places I'd return to"
        c.setFillColor(INK)
        c.setFont('Fraunces-SemiBold', 14)
        c.drawString(15 * mm, PAGE_HEIGHT - 25 * mm, "Five places I'd return to")
        
        y = PAGE_HEIGHT - 40 * mm
        c.setFont('Inter-Regular', 9)
        c.setFillColor(INK_SOFT)
        c.setStrokeColor(INK_SOFT)
        c.setLineWidth(0.3)
        
        for i in range(1, 6):
            c.drawString(15 * mm, y, f"{i}.")
            c.line(20 * mm, y - 2 * mm, PAGE_WIDTH - 15 * mm, y - 2 * mm)
            y -= 15 * mm
        
        # Two reflection prompts at bottom
        y = 30 * mm
        c.setFont('Fraunces-Regular', 8)
        c.setFillColor(INK_SOFT)
        c.drawString(15 * mm, y, "What surprised you most this year?")
        y -= 10 * mm
        c.drawString(15 * mm, y, "What would you try differently next time?")
    
    c.showPage()

def draw_reflection_page(c):
    """Blank reflection page with title"""
    c.setFillColor(INK)
    c.setFont('Fraunces-SemiBold', 14)
    c.drawString(15 * mm, PAGE_HEIGHT - 25 * mm, "Notes")
    
    # 20 ruled lines
    y = PAGE_HEIGHT - 35 * mm
    c.setStrokeColor(ACCENT_SOFT)
    c.setLineWidth(0.3)
    
    for i in range(20):
        c.line(15 * mm, y, PAGE_WIDTH - 15 * mm, y)
        y -= 4.5 * mm
    
    c.showPage()

def _interior_page(c, draw_fn, *args):
    """Helper: render an interior page with bleed translation.

    Each interior page is INTERIOR_PAGE_W × INTERIOR_PAGE_H (with bleed).
    Existing draw functions assume trim coordinates (0,0 to PAGE_WIDTH,
    PAGE_HEIGHT). We translate by (BLEED, BLEED) so trim-coord drawing
    lands inside the trim area, with the bleed extending the page outside.

    Note: showPage() resets the graphics state stack, so we cannot use
    saveState/restoreState to bracket the call. Instead we translate,
    let draw_fn call its own showPage, then on the next page the canvas
    is at the origin again - we'll re-translate at the start of the
    next page.
    """
    c.translate(BLEED, BLEED)
    draw_fn(c, *args)
    # showPage() inside draw_fn already moved to next page;
    # next call to _interior_page will re-translate cleanly.

def generate_interior():
    """Generate the 78-page interior PDF with bleed.

    Front matter (4 pages): title, belongs-to, how-to, blank-spacer
    Body (60 pages): 30 bite spreads
    Back matter (14 pages): index 2, year-in-review 2, reflection 10
    Total: 78 pages (matches pod_package interior page count)
    """
    output_path = "outbound/bites-paper-interior.pdf"
    c = canvas.Canvas(output_path, pagesize=INTERIOR_PAGE_SIZE)
    c.setTitle("Bites Paper - The Field Journal (Interior)")
    c.setAuthor("Bites")

    # Front matter (4 pages)
    _interior_page(c, draw_title_page)
    _interior_page(c, draw_belongs_to)
    _interior_page(c, draw_how_to_use)
    # Blank spacer page (preserves recto-verso for the first bite spread)
    c.showPage()

    # 30 bite spreads (60 pages)
    page_counter = 5  # for visible page numbers (5 = first right page)
    for i in range(1, 31):
        _interior_page(c, draw_bite_spread_left, i)
        _interior_page(c, draw_bite_spread_right, page_counter + 1)
        page_counter += 2

    # Index (2 pages)
    for i in range(1, 3):
        _interior_page(c, draw_index_page, i)

    # Year in review (2 pages)
    for i in range(1, 3):
        _interior_page(c, draw_year_in_review, i)

    # Reflection / extra notes (10 pages padding to 78)
    for i in range(10):
        _interior_page(c, draw_reflection_page)

    c.save()
    print(f"✓ Interior: {output_path} ({c.getPageNumber() - 1} pages)")
    return c.getPageNumber() - 1

def generate_cover():
    """Generate the cover spread PDF (single wide page)."""
    output_path = "outbound/bites-paper-cover.pdf"
    c = canvas.Canvas(output_path, pagesize=COVER_SPREAD_SIZE)
    c.setTitle("Bites Paper - The Field Journal (Cover)")
    c.setAuthor("Bites")
    draw_cover_spread(c)
    c.save()
    print(f"✓ Cover: {output_path} ({COVER_SPREAD_W/inch:.4f}\" × {COVER_SPREAD_H/inch:.4f}\", spine {SPINE_WIDTH:.4f}\")")

def generate_journal():
    """Generate both Lulu-compliant PDFs."""
    register_fonts()
    pages = generate_interior()
    generate_cover()
    print(f"\n✓ Lulu submission ready:")
    print(f"  pod_package_id: 0425X0687FCSTDPB060UW444MXX")
    print(f"  page_count: {pages}")
    print(f"  interior: outbound/bites-paper-interior.pdf")
    print(f"  cover:    outbound/bites-paper-cover.pdf")
    return pages

if __name__ == "__main__":
    generate_journal()
