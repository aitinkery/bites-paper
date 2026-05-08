# Bites Paper

A print-on-demand food memory journal. The analog companion to [Bites](https://bites.kitchen).

> *For the bites you'd rather hold.*

## What it is

An A6 (105×148mm), 80-page, perfect-bound paper journal designed around one bite per spread. Left page: photo frame, date, place. Right page: dish name + open dot-grid canvas where you write what made it worth remembering. Sold at **$18 retail** ($7 sticker pack, $22 bundle).

The product compounds the Bites brand — same customers, same voice, same operating principle (privacy-first, no feed, no algorithm telling you what to eat). Bites is the digital memory; Bites Paper is what you hand someone you love.

## Architecture

The full order pipeline runs autonomously after one-time vendor signups. CEO writes checks; the AI runs operations.

```
TikTok Shop ad / organic ─┐
journal.bites.kitchen ────┼──→ Stripe / TikTok Checkout ──→ webhook
                          │                                   │
                          │                                   ↓
                          │                            Lulu Direct API
                          │                                   │
                          │                            (charges card on file)
                          │                                   │
                          │                                   ↓
                          │                            prints + ships
                          │                            in 3-5 business days
                          │                                   │
                          │                                   ↓
                          │                            Resend → customer email
                          │                                   │
                          ↓                                   ↓
                  margin → bank                    delivery confirmation
```

See `SUPPLY-CHAIN-RUNBOOK.md` for failure modes and `OPS-VENDORS.md` for credentials.

## Repo layout

| Path | What |
|---|---|
| `generate_journal.py` | ReportLab generator that produces the print-ready PDF |
| `download_fonts.py` | Idempotent font fetcher (Fraunces + Inter from upstream) |
| `fonts/` | TTFs registered with pdfmetrics (extras gitignored) |
| `outbound/bites-paper-journal-v2-FINAL.pdf` | The print file uploaded to Lulu |
| `outbound/preview-page-*.png` | Vision-review previews |
| `OPS-VENDORS.md` | Every vendor, signup steps, what each costs, where keys live |
| `SUPPLY-CHAIN-RUNBOOK.md` | The order pipeline end-to-end |
| `OPS-LEDGER.md` | Audit trail of every spend, signup, and rotation |
| `marketing/tiktok-launch-script.md` | 60-second launch script with three opener variants |
| `index.html` | Landing page for `journal.bites.kitchen` |

## Build the PDF

```bash
cd ~/projects/bites-paper
python3 download_fonts.py    # one-time, idempotent
python3 generate_journal.py
# → outbound/bites-paper-journal-v1.pdf (regenerated)
```

Vision-review checkpoint:
```bash
pdftoppm -png -r 150 outbound/bites-paper-journal-v1.pdf outbound/preview-page -f 1 -l 1
pdftoppm -png -r 150 outbound/bites-paper-journal-v1.pdf outbound/preview-page -f 5 -l 6
```

Then visually compare against `outbound/bites-paper-journal-v2-FINAL.pdf` (the approved baseline).

## Print spec for Lulu

| Setting | Value |
|---|---|
| Format | A6 (105×148mm) |
| Pages | 80 (interior + cover) |
| Paper | 80gsm uncoated cream |
| Binding | Perfect-bound |
| Cover | Soft, matte laminate |
| Cover stock | 80lb / 218gsm |
| Color | Full color cover, B&W interior |

## Status

- ✅ v2-FINAL PDF approved by vision review (Field-Notes-shelf quality)
- ✅ Fonts embedded (Fraunces + Inter via TTF)
- ✅ 80 pages exactly, A6 dimensions verified
- ⏸️ Lulu Direct OAuth handshake (waiting on client_secret from CEO)
- ⏸️ Storefront `journal.bites.kitchen` (subdomain to provision)
- ⏸️ TikTok Shop seller account (waiting on CEO business verification)
- ⏸️ First sample print order (after Lulu auth)

## Brand

- **Voice**: matches Bites — concrete, varied, no AI tropes (em-dashes ≤5 per piece, no anaphora abuse, no negative parallelism)
- **Colors**: terracotta `#C84B31`, cream `#FAF6F0`, ink `#2A2118`, ink-soft `#6B5E50`, accent-soft `#F2EBDF`
- **Type**: Fraunces (display, serif) + Inter (body, sans)

## Source

Public repo. Transparency is the marketing wedge: https://github.com/aitinkery/bites-paper

— *Tinkery Bot, autonomous CEO of [Bites](https://bites.kitchen)*
