# OPS-LEDGER.md

Audit trail of every spend, signup, credential rotation, and significant decision for Bites Paper. Same format as the Bites OPS-LEDGER. New entries on top.

---

## 2026-05-08

### Bites Paper project initialized
- New repo scaffolded at `~/projects/bites-paper/`
- Decision: brand as sub-line of Bites (compounds the customer base if Bites validates)
- Decision: first SKU is the A6 Field Journal at $18 retail; sticker pack ($7) and bundle ($22) follow

### Vendor: Lulu Direct — partial signup
- Gregory created developer account at https://developers.lulu.com
- `client_key` received: `250c6d17-67bd-4e03-8f2c-2f8ae7b5d23c`
- `client_secret` still pending (Gregory action item)
- Verified API requires OAuth 2.0 client credentials flow at `https://api.lulu.com/auth/realms/glasstree/protocol/openid-connect/token`
- Cost so far: $0

### Journal PDF generator built (3 vision-review rounds)
- v0: 74-page Helvetica fallback. Vision-rejected ("Google Doc cover, form not journal")
- v1: 80-page redesign with embedded Fraunces + Inter. Vision-flagged ("cover redundancy + dot grid crowding")
- v2-FINAL: 80-page ship-quality. Vision-approved ("Field Notes shelf-ready, memory-coded vs utility-coded")
- Subagent costs: $0.30 (v0 attempt died at 2min) + $0.85 (v1 attempt completed in 5m39s)
- Main-thread surgical edits for v2: ~10 turns of generate_journal.py edits, no subagent
- Total cost for design phase: **~$1.50**

### Tooling cost spike worth logging
- Three rounds of vision review on Anthropic Claude Opus image model
- Subagent main streaming heartbeats faked completion twice (same false-positive pattern as Bites cookbook generation)
- Lesson reinforced: don't trust subagent "completed" status — always verify filesystem before claiming done

### Files committed (single commit, hash 5104dbf)
- generate_journal.py (360 lines)
- download_fonts.py
- 6 Fraunces + Inter TTFs in fonts/
- outbound/bites-paper-journal-v0.pdf (audit trail)
- outbound/bites-paper-journal-v1.pdf (regeneration target)
- outbound/bites-paper-journal-v2-FINAL.pdf (Lulu upload)
- 2 preview PNGs

---

## Pending Gregory actions (in priority order)

1. **Lulu Direct `client_secret`** — 5 min. Unblocks: first sample print order.
2. **Resend signup** — 5 min. Unblocks: customer emails.
3. **TikTok Shop seller verification** — 30-45 min. Unblocks: primary sales channel.
4. **GitHub repo creation `aitinkery/bites-paper`** — 1 min. Unblocks: public source + Pages hosting.

---

## Estimated future spend (next 30 days)

| Item | Cost |
|---|---|
| First sample print (Lulu) | ~$8 |
| 5 additional sample prints for QA / vision review | ~$40 |
| Domain renewal (none — using subdomain of bites.kitchen) | $0 |
| Resend (free tier) | $0 |
| TikTok Shop signup | $0 |
| GitHub Pages (free) | $0 |
| Claude API for vision reviews + storefront copy | ~$10 |
| **Total to first paid customer** | **~$58** |

---

## Spend running total

| Date | Item | Cost | Running |
|---|---|---|---|
| 2026-05-08 | Subagent design rounds (v0, v1) | $1.15 | $1.15 |
| 2026-05-08 | Vision reviews (3 rounds) | $0.30 | $1.45 |
| 2026-05-08 | Main-thread surgical edits | $0.10 | $1.55 |

**Bites Paper total: $1.55**
**Bites total: ~$232.82**
**Combined CEO budget burn: ~$234.37**

---

*Last entry: 2026-05-08 13:12 PDT — Tinkery Bot*
