# BIDSEAL V1 — Short Steward Demo (80–100 seconds)

This script uses **real existing Studionet evidence**; record the current Studio/Explorer UI. Do not recreate synthetic `SUCCESS` overlays or imply funds have moved.

| Segment | On screen | Narration |
|---|---|---|
| 0–12 sec | BIDSEAL README, [contract address](https://explorer-studio.genlayer.com/address/0x182787964a480e2b76FFD664465fAb23b5f1B8DB), source | “BIDSEAL is a reusable procurement decision gate built as a GenLayer Intelligent Contract.” |
| 12–27 sec | `BIDSEAL-TEST-001`: buyer requirements and compliant offer | “A buyer locks mandatory specifications; a different wallet submits an immutable bid.” |
| 27–43 sec | [`evaluate_bid` → ELIGIBLE](https://explorer-studio.genlayer.com/tx/0x19318ccc53db6086c85e502332010b3a2d04ab3a0faffd73c1b7bea9214a0251); show Equivalence output | “Independent validators evaluate the natural-language obligations. The compliant offer is eligible.” |
| 43–55 sec | [Award transaction](https://explorer-studio.genlayer.com/tx/0xe27f457e099218058338338f0594b4f1b25d42c2033e1e77b7278fc24c1a91e1) and `AWARDED` readback | “The original buyer can award it only after the verified decision.” |
| 55–72 sec | TEST-002 offer says `NO hardware warranty`; [`evaluate_bid` → INELIGIBLE](https://explorer-studio.genlayer.com/tx/0x91ff50c6b87e4c06ccf0c801a4c2e0965647ed9e6bee8126d3350a03336530cf) | “A cheaper bid explicitly refuses the mandatory warranty. Consensus rejects it.” |
| 72–88 sec | Existing invalid-award transaction dialog with `[rollback]` and finalized `OPEN` state | “The contract enforces the verdict: an ineligible bidder cannot be awarded; the request remains open.” |
| 88–100 sec | Existing vendor `cancel_request` rollback; README security section | “Non-owner cancellation is also rejected. This verifies offers, not delivery or payments.” |

Reviewer evidence is also browsable without video: [REVIEWER.md](../REVIEWER.md) and [LIVE_EVIDENCE.md](LIVE_EVIDENCE.md).
