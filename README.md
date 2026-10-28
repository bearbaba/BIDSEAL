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

## Current on-chain status (28 October 2026)

- **BIDSEAL V1 active contract:** `0x182787964a480e2b76FFD664465fAb23b5f1B8DB` on Studionet.
- **Signed `submit_bid` and `evaluate_bid`:** finalized, GenVM execution successful, consensus Accepted.
- **AI consensus decision:** `ELIGIBLE` with Equivalence Principle output `ELIGIBLE`.
- **Read check:** `get_bid` returned `found: true`, `price: 4800`, `decision: PENDING` before evaluation.
- **Signed buyer `award`:** finalized, GenVM SUCCESS, consensus Accepted; TX `0xe27f457e099218058338338f0594b4f1b25d42c2033e1e77b7278fc24c1a91e1`.
- **Finalized-state readback:** `get_request("BIDSEAL-TEST-001")` returned `AWARDED` with awarded bidder `0xD6b8A3A5eB329410D9504784812b8569afA8C2aF` (builder-provided Studio response).
- **Negative AI adjudication:** TEST-002 vendor price 4500 with explicit refusal of 12-month warranty → `INELIGIBLE` (finalized, GenVM SUCCESS, consensus Accepted, Equivalence output `INELIGIBLE`; finalized `get_bid` confirms persisted state).
- **Rejected award gate:** attempt to `award` TEST-002 produced expected `ERROR` with `[rollback] Only verified eligible bids can win`; all 5 validators agreed in the supplied Studio transaction dialog (**ACCEPTED**, not displayed as FINALIZED).
- **State preservation confirmed:** after the rejected TEST-002 award, finalized `get_request` returned `OPEN` and zero awarded bidder.
- **Still pending:** negative ownership check (vendor attempts `cancel_request`), over-budget deterministic check, reviewer demo, and optional TEST-001 post-evaluation readback.
- **Full receipts:** [Live evidence and test plan](docs/LIVE_EVIDENCE.md).

## Studio acceptance checklist

- [x] New contract deployed on Studionet using Normal (Full Consensus)
- [x] BUYER `create_request("BIDSEAL-TEST-001", requirements, 5000)`
- [x] VENDOR `submit_bid("BIDSEAL-TEST-001", 4800, terms)`
- [ ] `bid_exists(..., "0x...")` returns true
- [x] `get_bid(..., "0x...")` returns `found: true`, `decision: PENDING`
- [x] `evaluate_bid` succeeds with actual validator consensus and `ELIGIBLE`
- [x] Buyer successfully calls `award` in a signed, finalized transaction
- [x] Finalized `get_request` shows `AWARDED` with correct awarded bidder
- [x] TEST-002 contradictory warranty terms evaluated `INELIGIBLE` with signed consensus and finalized readback
- [x] TEST-002 attempted award rejected with expected execution rollback (Studio screenshot)
- [x] Confirm TEST-002 remains `OPEN` with zero awarded bidder after rejected award
- [ ] Unauthorized calls and over-budget checks

See [SECURITY.md](SECURITY.md). MIT licensed. **Do not claim production or Season 2 acceptance before live evidence.**
