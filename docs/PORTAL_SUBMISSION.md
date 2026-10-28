# Portal submission — BIDSEAL V1

**Category:** Builder → Intelligent Contracts  
**Contribution Date:** 28/10/2026 (original live execution; change to the actual submission date if necessary)  
**Title:** BIDSEAL — Consensus-Verified Procurement Award Gate

## Notes / Description (copy; 908/1000 characters)

BIDSEAL V1 is a standalone GenLayer Intelligent Contract for procurement decisions. Buyers lock natural-language requirements and a price cap; another wallet submits an immutable bid. Deterministic rules enforce ownership, duplicate protection and budget. In-budget offers are evaluated by a leader LLM while independent validators repeat the assessment and compare consequential ELIGIBLE, INELIGIBLE or UNVERIFIABLE decisions using the Equivalence Principle. Only the buyer may award an eligible bid, and only once. Live Studionet (61999) evidence: TEST-001 returned ELIGIBLE and reached AWARDED; TEST-002, explicitly refusing the required warranty, returned INELIGIBLE. A subsequent award attempt finalized with a rollback, preserving OPEN state. Non-owner cancellation was also rejected. Code, tests, signed TXs, reviewer guide and limitations are linked in the repository. No escrow or proof of delivery.

## Evidence to add in the Portal

1. **GitHub source:** https://github.com/bearbaba/BIDSEAL
2. **GenLayer Explorer Contract (important):** https://explorer-studio.genlayer.com/address/0x182787964a480e2b76FFD664465fAb23b5f1B8DB
3. **AI verdict — ELIGIBLE:** https://explorer-studio.genlayer.com/tx/0x19318ccc53db6086c85e502332010b3a2d04ab3a0faffd73c1b7bea9214a0251
4. **AI verdict — INELIGIBLE:** https://explorer-studio.genlayer.com/tx/0x91ff50c6b87e4c06ccf0c801a4c2e0965647ed9e6bee8126d3350a03336530cf
5. **Award SUCCESS:** https://explorer-studio.genlayer.com/tx/0xe27f457e099218058338338f0594b4f1b25d42c2033e1e77b7278fc24c1a91e1
6. **Reviewer guide:** https://github.com/bearbaba/BIDSEAL/blob/main/REVIEWER.md

If the Portal only accepts a few evidence links, prioritize **explorer contract + GitHub + both evaluation TX links**. Add a concise video link only after one is actually recorded.

## Accuracy check before submission

- Category is **Intelligent Contracts**, not Projects; this is a stand-alone contract primitive, not a full app.
- Do not label synthetic buyer bids as actual commercial procurement.
- Do not claim proof of supplier performance, escrow, payment, production deployment, Bradbury deployment, comprehensive audits, or Steward acceptance.
- For the failed award and failed non-owner cancellation, `FINALIZED` is the status but the **execution result is ERROR as designed**. Do not describe as successful execution.
- The Portal review, eligibility, scoring, and approval remain with GenLayer Steward.

## Short reviewer note

Two live decisions on one deployed contract provide an A/B test of meaningful consensus: a higher-priced bid that accepts mandatory warranty terms was eligible and awarded; a cheaper bid that expressly refused warranty was ineligible, could not be awarded, and left state unchanged. Validator agreement on intended rollback additionally proves authorization enforcement.
