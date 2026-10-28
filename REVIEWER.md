# BIDSEAL V1 — Steward Review Guide

**What it is:** A reusable on-chain decision gate for competitive procurement. Buyer requirements and vendor commitments are immutable; independent GenLayer validators adjudicate natural-language compliance. An award can happen only when the decision is `ELIGIBLE` and the original buyer signs it.

**Review in 2–3 minutes:** read the [contract](contracts/bidseal.py) → open the [deployed contract](https://explorer-studio.genlayer.com/address/0x182787964a480e2b76FFD664465fAb23b5f1B8DB) → compare the two AI evaluations → inspect the accepted award and the rejected award → review [test and security scope](docs/LIVE_EVIDENCE.md).

## Concrete consequence

A request requires 20 refurbished laptops, at least 16 GB RAM, 12-month hardware warranty, English-language support and delivery within 14 days, under a price cap of 5000 (abstract units, not a real payment).

| Case | Offer | AI outcome | Contract consequence |
|---|---|---|---|
| `BIDSEAL-TEST-001` | 4800; explicitly commits to all requirements | **ELIGIBLE** | Buyer successfully executes `award`; request reads `AWARDED` |
| `BIDSEAL-TEST-002` | 4500; explicitly **refuses** the 12-month warranty | **INELIGIBLE** | `award` reverts with `Only verified eligible bids can win`; request stays `OPEN` |

It is **not a price comparison**: the lower-priced offer is correctly rejected on a mandatory non-price requirement.

## Evidence links (Studionet, chain ID 61999)

- **Contract:** [0x182787964a480e2b76FFD664465fAb23b5f1B8DB](https://explorer-studio.genlayer.com/address/0x182787964a480e2b76FFD664465fAb23b5f1B8DB)
- **Compliant offer evaluated:** [`evaluate_bid` → ELIGIBLE](https://explorer-studio.genlayer.com/tx/0x19318ccc53db6086c85e502332010b3a2d04ab3a0faffd73c1b7bea9214a0251) — FINALIZED, GenVM SUCCESS, consensus Accepted, Equivalence Principle output `ELIGIBLE`.
- **Award for compliant offer:** [`award` → SUCCESS](https://explorer-studio.genlayer.com/tx/0xe27f457e099218058338338f0594b4f1b25d42c2033e1e77b7278fc24c1a91e1) — FINALIZED; subsequent `get_request` readback: `AWARDED`, correct bidder.
- **Noncompliant offer evaluated:** [`evaluate_bid` → INELIGIBLE](https://explorer-studio.genlayer.com/tx/0x91ff50c6b87e4c06ccf0c801a4c2e0965647ed9e6bee8126d3350a03336530cf) — FINALIZED, GenVM SUCCESS, consensus Accepted, Equivalence Principle output `INELIGIBLE`.
- **Invalid award rejected:** [Invalid award TX](https://explorer-studio.genlayer.com/tx/0x1f7ed9e5fc20c847e86d825fde2d9881efed93318e4941c35558d20b0cc2c88c) (transcribed from screenshot); FINALIZED with execution ERROR, consensus Accepted, all 5 validators agree on `[rollback] Only verified eligible bids can win`. The finalized `get_request` readback returned `OPEN` and zero `awarded_bidder`.
- **Non-owner cancellation rejected:** [Unauthorized cancellation TX](https://explorer-studio.genlayer.com/tx/0xaeca7a1c26bf9c43397fd3a7a131f56e56d1d2e803c54b78bdfc345bf15e29f2) (transcribed from screenshot); FINALIZED with execution ERROR, expected `[rollback] Only request owner can cancel` (3 Agree, 2 Idle after quorum).

For hashes, request input, and evidence provenance, see [Live Evidence](docs/LIVE_EVIDENCE.md). Transaction URLs are for reviewer verification; the explorer was not independently accessible to the documentation author in this session.

## Why GenLayer, not a standard contract or single LLM?

The maximum price and caller privileges are deterministic. However, interpreting whether a free-text vendor offer *explicitly commits to every mandatory natural-language obligation* is judgment-dependent. The leader proposes a normalized verdict, and validators independently run the LLM assessment again against the original buyer policy and offer; the validator code checks the decision-bearing label, rather than merely validating JSON shape. The accepted outcome becomes contract state and controls the one-time award.

**Decision labels:** `ELIGIBLE` / `INELIGIBLE` / `UNVERIFIABLE`. Ambiguous, missing, or failed evaluation defaults to an unawardable result; validator disagreement should prevent acceptance.

## State and trust boundaries

- Buyer-signed `create_request`: freezes requirements and ceiling; state `OPEN`.
- Vendor-signed `submit_bid`: one immutable offer per vendor per request; buyer cannot self-bid.
- `evaluate_bid`: deterministic over-budget gate; otherwise independent LLM consensus; writes the verified decision.
- Buyer-signed `award`: requires `OPEN`, buyer as sender, and prior `ELIGIBLE`; writes `AWARDED` once.
- `cancel_request`: buyer-only while request is `OPEN`.
- Reserved prompt markers blocked; vendor text treated as **untrusted evidence**, not authority.

## Reproduce locally / inspect source

```bash
python -m unittest discover -s tests -v
```

20 pure-Python shim test cases are included, covering state transitions, authorization, malformed/mixed-case addresses, budget, replay, and validator disagreement. These tests are **not** GenVM validation or live consensus evidence. [Live on-chain results](docs/LIVE_EVIDENCE.md) are listed separately.

## Limitations and boundaries

This contract verifies **offered promises**, not vendor identity, payment, legal contract formation, actual delivery or goods quality. The scenario is synthetic test data. It holds no escrow, makes no transfers, has no external source/oracle and has not undergone an independent security audit. Free-text inputs and LLM outputs remain sensitive to ambiguity, model drift and prompt injection. Studionet is a development environment and may reset; this is not a mainnet product.

## Outstanding optional review coverage

- Separate live over-budget and duplicate-bid prevention demonstrations.
- Standalone replay / award-after-award negative trace.
- Short narrated video (not yet recorded) and independent explorer cross-check.
