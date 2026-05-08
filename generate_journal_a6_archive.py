#!/usr/bin/env python3
"""
Bites Paper Journal Generator v1
A6 format (105×148mm), 80 pages, perfect-bound
Complete redesign: embedded fonts, tighter layout, journal-first spreads
"""

from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# A6 dimensions in points (ReportLab uses points: 1mm = 2.83465 points)
PAGE_WIDTH = 105 * mm
PAGE_HEIGHT = 148 * mm

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

def draw_cover(c):
    """Front cover: terracotta with lower-third wordmark + hairline rule directly above + N° mark"""
    c.setFillColor(TERRACOTTA)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    # Wordmark "Bites Paper" - lower third, left-aligned
    c.setFillColor(CREAM)
    c.setFont('Fraunces-Black', 32)
    wordmark_x = 15 * mm
    wordmark_y = 32 * mm
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

    c.showPage()

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
    """Left page: smaller photo frame, DATE line, vertical sidebar, WHERE fields"""
    
    # Smaller photo frame (60×40mm) - upper left
    frame_x = 10 * mm
    frame_y = PAGE_HEIGHT - 50 * mm
    frame_w = 60 * mm
    frame_h = 40 * mm
    
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.5)
    c.rect(frame_x, frame_y, frame_w, frame_h, fill=0, stroke=1)
    
    # "DATE" label + handwriting line below photo
    c.setFont('Inter-Medium', 7)
    c.setFillColor(INK_SOFT)
    date_y = frame_y - 8 * mm
    c.drawString(frame_x, date_y, "DATE")
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.3)
    c.line(frame_x, date_y - 2 * mm, frame_x + frame_w, date_y - 2 * mm)
    
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
    
    # "WHERE" fields at bottom of left page
    where_y = 30 * mm
    c.setFont('Inter-Medium', 7)
    c.setFillColor(INK_SOFT)
    c.drawString(10 * mm, where_y, "WHERE")
    
    # Two ruled lines for city/restaurant
    c.setStrokeColor(INK_SOFT)
    c.setLineWidth(0.3)
    c.line(10 * mm, where_y - 5 * mm, PAGE_WIDTH - 15 * mm, where_y - 5 * mm)
    c.line(10 * mm, where_y - 10 * mm, PAGE_WIDTH - 15 * mm, where_y - 10 * mm)
    
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

def draw_back_cover(c):
    """Back cover: brand mark + URL"""
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    # Brand mark (three vertical bars)
    mark_x = PAGE_WIDTH / 2 - 3
    mark_y = PAGE_HEIGHT / 2 + 10 * mm
    c.setStrokeColor(TERRACOTTA)
    c.setLineWidth(2)
    for i in range(3):
        c.line(mark_x + i * 4, mark_y, mark_x + i * 4, mark_y + 12)
    
    # URL
    c.setFont('Inter-Medium', 9)
    c.setFillColor(INK_SOFT)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 5 * mm, "journal.bites.kitchen")
    
    c.showPage()

def generate_journal():
    """Generate the complete 80-page journal"""
    register_fonts()
    
    output_path = "outbound/bites-paper-journal-v1.pdf"
    c = canvas.Canvas(output_path, pagesize=A6)
    
    # Metadata
    c.setTitle("Bites Paper - The Field Journal")
    c.setAuthor("Bites")
    c.setSubject("Food Memory Journal")
    
    print("Generating journal v1...")
    
    # Front cover (page 1)
    draw_cover(c)
    print("✓ Front cover")
    
    # Title page (page 2)
    draw_title_page(c)
    print("✓ Title page")
    
    # Belongs to (page 3)
    draw_belongs_to(c)
    print("✓ Belongs to page")
    
    # How to use (page 4)
    draw_how_to_use(c)
    print("✓ How to use")
    
    # 30 bite spreads (pages 5-64 = 60 pages)
    page_counter = 5
    for i in range(1, 31):
        draw_bite_spread_left(c, i)
        draw_bite_spread_right(c, page_counter + 1)
        page_counter += 2
        if i % 10 == 0:
            print(f"✓ Bite spreads {i-9}-{i}")
    
    # Index (2 pages: 65-66)
    for i in range(1, 3):
        draw_index_page(c, i)
    print("✓ Index (2 pages)")
    
    # Year in review (2 pages: 67-68)
    for i in range(1, 3):
        draw_year_in_review(c, i)
    print("✓ Year in review (2 pages)")
    
    # Reflection pages (10 pages, pads total to 80 with covers + inside-back blank)
    for i in range(10):
        draw_reflection_page(c)
    print("✓ Reflection pages (10 pages)")
    
    # Back cover (page 79-80, we'll do one page as inside back, one as actual back)
    # Inside back cover - blank cream
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    c.showPage()
    
    # Actual back cover (page 80)
    draw_back_cover(c)
    print("✓ Back cover")
    
    c.save()
    print(f"\n✓ Journal saved: {output_path}")
    print(f"  Total pages: {c.getPageNumber()}")
    print(f"  Dimensions: {PAGE_WIDTH/mm:.1f} × {PAGE_HEIGHT/mm:.1f} mm (A6)")
    return c.getPageNumber()

if __name__ == "__main__":
    generate_journal()
