# OPS-VENDORS.md

Every vendor we use, signup state, what each charges, where the credentials live.

**Operating principle:** Gregory does one-time signups + identity verification. Tinkery Bot does everything after.

---

## Lulu Direct (print-on-demand manufacturer)

- **URL:** https://developers.lulu.com — production · https://developers.sandbox.lulu.com — sandbox
- **Status:** ✅ Account created · ⏸️ OAuth handshake pending
- **Credentials:**
  - `client_key`: `250c6d17-67bd-4e03-8f2c-2f8ae7b5d23c` (received)
  - `client_secret`: ⏸️ pending (Gregory: visit Lulu developer profile → "Client Keys & Secret" page → copy second value)
- **Auth flow:** OAuth 2.0 client credentials grant. Endpoint `https://api.lulu.com/auth/realms/glasstree/protocol/openid-connect/token`, basic-auth header `client_key:client_secret` base64-encoded, body `grant_type=client_credentials`. Returns a 1-hour access_token. Cache + refresh as needed.
- **Per-unit cost (estimated):** ~$5-7 to print + ship a single A6 80-page softcover within US (depends on shipping tier). Lulu charges your card on file at order time.
- **What I do once authenticated:**
  - Upload the print PDF (one-time per SKU)
  - Create a "podpackage" SKU for the journal
  - Submit print-jobs API calls when orders arrive (one job per customer order)
  - Poll job status, surface tracking number to Resend for customer emails
- **What Gregory still owes:** the `client_secret`. Five minutes. After that, hands-off.
- **Failure mode:** if the API rejects an order (bad address, payment declined), I email Gregory + the customer with the specific error. No silent fails.

## TikTok Shop Seller (sales channel #1)

- **URL:** https://seller-us.tiktok.com
- **Status:** ⏸️ Not started
- **What Gregory needs to provide:** business name (likely AI Tinkery LLC), EIN, business bank account for payouts, government-issued ID for identity verification, business address. The verification involves a photo of the ID + selfie. Estimate 30-45 min.
- **Per-unit cost:** TikTok takes 5% commission + ~$0.30 per transaction. Plus payment processing (~2.9%).
- **What I do once verified:** create product listings, upload product images (rendered from the PDF + AI-generated lifestyle shots), set inventory rules, integrate with Lulu via the order webhook.
- **Why this vendor:** the algorithm. Other channels (Etsy, Amazon Handmade, Shopify direct) have lower fees but no organic discovery. TikTok Shop is the discovery engine.

## Resend (transactional email)

- **URL:** https://resend.com
- **Status:** ⏸️ Not started
- **What Gregory needs to provide:** email + card. Free tier: 3,000 emails/mo, 100/day. We'll be well under that for the first 6+ months.
- **Per-unit cost:** $0 at our volume. $20/mo if we exceed free tier (10x growth).
- **What I do once configured:** order confirmation email, shipping notification, delivery confirmation, post-purchase "thank you + ask for review" email. Domain verification for `bites.kitchen` so emails come from `paper@bites.kitchen` rather than a generic Resend domain.
- **Why this vendor:** clean API, generous free tier, deliverability is good, tied to the same domain we already control.

## Stripe (sales channel #2 — direct via storefront)

- **URL:** https://dashboard.stripe.com
- **Status:** ✅ Already wired for Bites cookbook · ⏸️ Live mode pending Gregory's identity verification
- **Per-unit cost:** 2.9% + $0.30 per transaction.
- **What I do:** add a new product `prod_bites_paper_journal` ($18) and `prod_bites_paper_sticker_pack` ($7) and `prod_bites_paper_bundle` ($22). Reuse the existing Stripe account and webhook infrastructure from Bites.
- **Why this vendor:** already paid the integration tax for Bites. Reusing it is free.

## Cloudflare DNS (subdomain hosting)

- **URL:** https://dash.cloudflare.com
- **Status:** ✅ Already managing `bites.kitchen` · ⏸️ Need to add `journal.bites.kitchen` CNAME when storefront is built
- **Per-unit cost:** $0 (free plan)
- **What I do:** add CNAME `journal.bites.kitchen → aitinkery.github.io` once the storefront ships. Confirm SSL via Cloudflare's automatic edge cert. Edit page rules if needed.

## GitHub (source + storefront hosting)

- **URL:** https://github.com/aitinkery
- **Status:** ✅ Existing organization · ⏸️ Repo `aitinkery/bites-paper` to be created
- **Per-unit cost:** $0 (public repo, free Pages hosting)
- **What I do:** push the storefront here, configure GitHub Pages with custom domain `journal.bites.kitchen`, automated deploys via push to `main`.

---

## Gregory's punchlist (in priority order)

1. **Lulu Direct `client_secret`** — visit https://developers.lulu.com, log in, "Client Keys & Secret" page. Send me the second UUID. **5 minutes. Unblocks first sample print.**
2. **Resend signup** — https://resend.com signup with your email. Add card (free tier means $0 charged unless we exceed). Send me the API key. **5 minutes. Unblocks customer emails.**
3. **TikTok Shop Seller verification** — https://seller-us.tiktok.com. Business + ID verification. **30-45 minutes. Unblocks the primary sales channel.**
4. **Order one sample print** (after step 1) — I'll prep the API call; you receive the journal at your address; you photograph it; I do vision review. ~$8 cost. **Unblocks live launch.**

---

## Credentials map

| Where | What lives there |
|---|---|
| `~/projects/bites-paper/.env` (gitignored) | Lulu client_key, Lulu client_secret, Resend API key |
| `~/.openclaw/workspace/TOOLS.md` | Composio account IDs (already maintained) |
| Stripe dashboard | All product SKUs and prices |
| Lulu developer dashboard | Account-level billing, print-job history |

---

## Rotation cadence

- API keys reviewed every 90 days
- Lulu OAuth tokens auto-refresh hourly (cached in memory, no rotation needed)
- Stripe keys rotated only on incident
- TikTok Shop password: standard 90-day rotation, Gregory's responsibility

---

*Last updated: 2026-05-08 — Tinkery Bot*
