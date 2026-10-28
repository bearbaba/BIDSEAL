# BIDSEAL — Intelligent Procurement Verification

**Standalone GenLayer Intelligent Contract primitive · Season 2 candidate (v0.2)**

A buyer publishes immutable procurement requirements, vendors commit to signed bids, and independent GenLayer AI validators determine which bids satisfy the requirements. The buyer can award only a verified eligible offer.

## What it does

1. `create_request(request_id, requirements, max_price)` — owner fixes a procurement specification.
2. `submit_bid(request_id, price, terms)` — a different wallet submits one immutable offer.
3. `evaluate_bid(request_id, bidder)` — deterministic budget check, then AI consensus compares binding obligations.
4. `award(request_id, bidder)` — restricted to request owner and bids adjudicated `ELIGIBLE`.
5. `get_request` and `get_bid` expose auditable state.

Decisions: **ELIGIBLE**, **INELIGIBLE**, **UNVERIFIABLE**.

### Example

Buyer asks for 20 refurbished laptops with 16 GB RAM, a 12-month warranty, English support, and 14-day delivery, under $5,000. A bid explicitly meeting all conditions may become eligible. A cheaper bid excluding the warranty is ineligible. An ambiguous warranty is unverifiable. Over-budget bids fail deterministically.

## Why GenLayer consensus

Natural-language exceptions and contradictory commitments cannot be safely reduced to a numeric rule. The leader evaluates the buyer's requirements against the vendor's offer; each validator independently re-runs the decision process and agrees on the outcome label. The bidder's text is untrusted evidence, not instructions. Ambiguous or unavailable evaluation fails closed to `UNVERIFIABLE`.

## Security & limitations

- Request and vendor commitments are immutable.
- Sender wallet determines ownership; textual claims of authority are ignored.
- No payment, escrow, or proof of delivery; this contract verifies **promises**, not performance.
- Never interpret prompt delimiters as a guarantee of prompt-injection resistance.
- AI disagreement, ambiguous evidence and on-chain finalization semantics require live GenVM testing.

## Run local tests

```bash
python -m unittest discover -s tests -v
```

**Local shim regression status: 16/16 passed on 2026-10-28.** These are pure-Python simulated tests, **not** GenVM compilation, deployment, validator consensus or signed blockchain transactions.

## Evidence required before Portal submission

- [ ] GenVM lint/compile and pinned runtime
- [ ] Deploy on an appropriate GenLayer network
- [ ] Signed request, bids, evaluation and award, with explorer TX links
- [ ] Negative cases: over-budget, unauthorized award, ambiguous offer
- [ ] Validator disagreement/consensus evidence
- [ ] Short reviewer video and independently verifiable explorer contract

**Current status:** Source candidate; no chain deployment or live consensus proof yet. Do not describe this as production-ready.

MIT License. Please review [SECURITY.md](SECURITY.md) before integrating.
