# SUPPLY-CHAIN-RUNBOOK.md

How an order goes from a stranger tapping "Buy" to a journal arriving at their door. Each step has a vendor, a failure mode, and an escalation path.

```
[Customer arrives]
    │
    ├─ via TikTok Shop ad (paid traffic)
    ├─ via TikTok organic FYP video
    ├─ via direct link from journal.bites.kitchen
    └─ via cross-link from bites.kitchen (existing audience)
            │
            ↓
[Add to cart]
    │
    ├─ TikTok Shop: native cart, no redirect
    └─ journal.bites.kitchen: Stripe Checkout redirect
            │
            ↓
[Payment]
    │
    ├─ TikTok Shop: TikTok handles, payouts to bank weekly
    └─ Stripe: instant capture, 2-day rolling payout
            │
            ↓
[Webhook fires]
    │
    │  TikTok webhook URL: TBD (configured in TikTok Shop dashboard)
    │  Stripe webhook URL: handles 'checkout.session.completed' event
    │
    │  Both webhooks land at: https://script.google.com/macros/s/<PROJECT>/exec
    │  (Apps Script proxy that talks to Lulu)
    │
    ↓
[Lulu Direct API call]
    │
    │  POST https://api.lulu.com/print-jobs/
    │  Body: {
    │    line_items: [{
    │      pod_package_id: 'BITES_PAPER_JOURNAL_V1',
    │      quantity: 1,
    │      title: 'Bites Paper - The Field Journal',
    │      printable_normalization: { cover: ..., interior: ... }
    │    }],
    │    shipping_address: { from webhook payload },
    │    contact_email: customer email,
    │    shipping_level: 'MAIL' or 'GROUND' (cheapest acceptable)
    │  }
    │
    ↓
[Lulu charges Gregory's card on file]
    │  ~$5-7 for journal + $3-5 shipping
    │
    ↓
[Lulu prints + ships in 3-5 business days]
    │
    ↓
[Tracking number returned via webhook]
    │
    ↓
[Resend sends customer email]
    │  - Order confirmation immediately on payment
    │  - Shipping notification when Lulu provides tracking
    │  - Delivery confirmation when Lulu reports delivered
    │
    ↓
[Customer receives journal]
    │
    ↓
[7 days later: Resend sends "thank you + review request" email]
```

---

## Failure modes & escalation

### "Lulu API returned 401"
- Cause: OAuth token expired or invalid
- Action: refresh token via client_credentials flow, retry once
- Escalation: if 401 persists, email Gregory with the request payload + response body. Probably means the client_secret was rotated.

### "Lulu API returned 422 (validation error)"
- Cause: address malformed, unsupported country, or PDF link broken
- Action: log the full error, email Gregory + the customer
- Escalation: refund the customer via Stripe `refunds.create`, log to OPS-LEDGER

### "Customer paid but webhook didn't fire"
- Cause: webhook misconfigured, network issue, Apps Script timeout
- Detection: nightly reconciliation job — query Stripe for paid orders not in our local order log
- Action: manually fire the Lulu API call via the reconciliation script
- Escalation: if reconciliation finds >2 misses in a week, that's a system issue; Gregory gets paged

### "Lulu can't print (PDF rejected)"
- Cause: PDF dimensions, bleed, or font embedding fail Lulu's preflight
- Detection: the print-job creation API responds with status `REJECTED`
- Action: email Gregory immediately. Halt all incoming orders by pausing Stripe checkout + TikTok listings until fixed.
- Escalation: this is a launch-blocker; everything stops until the PDF passes preflight.

### "Customer shipping address was wrong"
- Cause: typo, P.O. Box where Lulu requires street, etc.
- Detection: Lulu API returns address validation error pre-job
- Action: email customer immediately asking for corrected address (templated email via Resend)
- Escalation: if no response in 72h, refund and cancel

### "Customer wants to return"
- Returns policy: 30-day satisfaction guarantee. We refund via Stripe. Customer keeps the journal (ship costs > journal cost; Lulu doesn't accept returns).
- Action: customer emails `paper@bites.kitchen`. I read it, refund via Stripe API, update OPS-LEDGER.
- Escalation to Gregory: only if customer is hostile or dispute escalates to chargeback.

### "Stripe chargeback"
- Action: I dispute via Stripe dashboard within 7 days, providing: Lulu shipping confirmation, Resend email logs, photo of customer-confirmed delivery (if available)
- Escalation: Gregory reviews the dispute response before submission

### "TikTok Shop policy violation flag"
- Possible causes: trademark concern, misleading content, image quality
- Action: read the violation notice, fix the listing, appeal if appropriate
- Escalation to Gregory: any account suspension threat → Gregory immediately

### "Lulu out of stock on the cover stock"
- Detection: the print-job creation API returns a substitution warning
- Action: accept the substitution if quality is comparable; reject and pause if not
- Escalation: if pause is required, surface to Gregory + post a "shipping delay" notice on the listing

---

## Daily checks (automated)

Cron-style heartbeat tasks that run without human intervention:

| Frequency | Task | Action if failure |
|---|---|---|
| Every 1h | Check OAuth token freshness | Refresh, log to ledger |
| Every 6h | Reconcile Stripe paid orders against Lulu print-jobs | Fire missed jobs, email Gregory |
| Daily | Pull Lulu print-job status for in-progress orders | Send tracking emails via Resend when status changes |
| Weekly | Audit OPS-LEDGER spend totals | Email Gregory if spend > weekly budget |
| Weekly | Check Resend deliverability rate | Email Gregory if below 95% |

---

## Customer service playbook

I (the AI) handle these directly:
- "Where's my order?" → look up Lulu tracking, reply with link
- "I want to return" → refund via Stripe, polite email
- "The journal arrived damaged" → free replacement order, log to ledger
- "Can you print my own design?" → "Not yet, but it's a future feature. Want me to add you to the list?"
- "Do you ship internationally?" → Lulu does; I check supported countries and respond yes/no

Gregory handles these (I escalate):
- Anything legal (trademark notice, lawsuit hint, government inquiry)
- Anything press (journalist, podcast invite, cookbook publisher)
- Refund disputes >$50 or chargebacks
- Bulk orders (>10 units in one transaction)
- Custom inquiries (corporate gifts, weddings, restaurant licensing)

---

## Cost flow per sale (estimated, $18 retail)

| Item | Cost | Margin |
|---|---|---|
| Sale price | $18.00 | |
| TikTok 5% fee | -$0.90 | |
| Payment processing 2.9% + $0.30 | -$0.82 | |
| Lulu print + ship (US) | -$6.50 | |
| Resend email cost | -$0.001 | |
| **Net per sale** | | **~$9.78** |

If we ship 1,000 units: ~$9,780 net margin.

---

*Last updated: 2026-05-08 — Tinkery Bot*
