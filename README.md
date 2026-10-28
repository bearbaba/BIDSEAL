# BIDSEAL — Intelligent Procurement Verification

**BIDSEAL V1 — fresh deployment source (address-key fix, 28 October 2026)**

Standalone Intelligent Contract on GenLayer: a buyer publishes mandatory procurement requirements, a second wallet submits a binding bid, independent AI validators evaluate compliance, and only an `ELIGIBLE` bid can be awarded by the buyer. No escrow or payment functionality.

## Workflow

1. `create_request(request_id, requirements, max_price)` from BUYER.
2. `submit_bid(request_id, price, terms)` from a different wallet (VENDOR).
3. `bid_exists(request_id, bidder)` or `get_bid(request_id, bidder)` — **bidder is a string** containing the 42-character `0x` address, case-insensitive.
4. `evaluate_bid(request_id, bidder)` — **bidder is the same string**. Evaluates by LLM consensus, then records `ELIGIBLE`, `INELIGIBLE` or `UNVERIFIABLE`.
5. `award(request_id, bidder)` — buyer-only, accepted bids only. Read status using `get_request`.

`get_bid` returns `found: false` and `NOT_FOUND` when no bid exists, instead of raising an opaque RPC error.

## V1 correction

The first deployment showed successful signed `submit_bid` but a generic `gen_call: execution failed` on `get_bid` and `evaluate_bid` simulation. Exact low-level GenVM cause remains unconfirmed. This build standardizes the storage key from both wallet sender and text input to lowercase `0x...`, including GenVM `addr#...` display strings. Regression tests cover both spellings.

**Deploy a NEW instance from this file.** This replaces the broken V1 in the project workflow. Do not use `Upgrade code`: the prior contract did not register authorized upgraders, and a source change does not modify that deployed address.

## Tests

```bash
python -m unittest discover -s tests -v
```

20 local Python-shim tests are provided (16 original + 4 address regressions). **Simulated tests are not equivalent to GenVM lint, live deployment, wallet-signed transactions, or validator consensus.** Run `genvm-lint check contracts/bidseal.py` when the tool is available.

## Studio acceptance checklist

- [ ] New contract deployed on Studionet using Normal (Full Consensus)
- [ ] BUYER `create_request("BIDSEAL-FIX-001", requirements, 5000)`
- [ ] VENDOR `submit_bid("BIDSEAL-FIX-001", 4800, terms)`
- [ ] `bid_exists(..., "0x...")` returns true
- [ ] `get_bid(..., "0x...")` returns `found: true`, `decision: PENDING`
- [ ] `evaluate_bid` succeeds with actual validator consensus and `ELIGIBLE`
- [ ] Buyer awards; `get_request` shows `AWARDED`
- [ ] Unauthorized award, over-budget and contradictory terms are rejected

See [SECURITY.md](SECURITY.md). MIT licensed. **Do not claim production or Season 2 acceptance before live evidence.**
