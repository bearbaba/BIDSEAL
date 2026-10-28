# BIDSEAL V1 — Live Studionet acceptance evidence

This document records blockchain transaction details supplied by the project builder on **28 October 2026**, pending independent explorer cross-check. This is evidence for the **new BIDSEAL V1 instance** (after the address-key bugfix), not the superseded broken instance.

## Contract

- Network: GenLayer Studionet (chain ID `61999`)
- Contract address: `0x182787964a480e2b76FFD664465fAb23b5f1B8DB`
- Studio import: https://studio.genlayer.com/?import-contract=0x182787964a480e2b76FFD664465fAb23b5f1B8DB
- Buyer wallet: `0x4C7cb73aC8F8999af21cfc9fF4cF2333a9508Dcb`
- Vendor wallet: `0xD6b8A3A5eB329410D9504784812b8569afA8C2aF`
- Request: `BIDSEAL-TEST-001`
- Budget: 5000; vendor offered 4800.

## Live checks

| Operation | Outcome | Evidence |
|---|---|---|
| Deploy new instance | Contract imported and usable | Studio import above; deployment transaction hash not captured here |
| `create_request` by buyer | FINALIZED, GenVM SUCCESS, consensus Accepted | Transaction screenshot shared by builder; hash shown beginning `0xcda4f1d384ec806...` |
| `submit_bid` by vendor | FINALIZED, GenVM SUCCESS, consensus Accepted | `0xb50296ad3aff364af014d9a47665443ac666392b0e922db838ba53b128e9faf4` |
| `get_bid` view | `found: true`, `price: 4800`, `decision: PENDING` | Studio response supplied by builder |
| `evaluate_bid` by vendor | FINALIZED, GenVM SUCCESS, consensus Accepted, return `ELIGIBLE` | `0x19318ccc53db6086c85e502332010b3a2d04ab3a0faffd73c1b7bea9214a0251` |
| Equivalence Principle output | `ELIGIBLE` | Recorded in evaluation transaction details |
| `award` by original buyer | FINALIZED, GenVM SUCCESS, consensus Accepted; input bidder matches evaluated vendor | `0xe27f457e099218058338338f0594b4f1b25d42c2033e1e77b7278fc24c1a91e1` (buyer `0x4C7cb73aC8F8999af21cfc9fF4cF2333a9508Dcb`; 2026-10-28 19:41:55 local) |
| Finalized `get_request` readback after award | `state: AWARDED`; `awarded_bidder: 0xD6b8A3A5eB329410D9504784812b8569afA8C2aF`; owner and budget match | Studio response provided by builder on 28 Oct 2026; read call TX not applicable |
| TEST-002 `create_request` (buyer) | FINALIZED, GenVM SUCCESS, consensus Accepted; mandatory 12-month warranty, max price 5000 | `0x814808648593fe47d6d8d31c09894f83e826af97017cc3ebb719c5397c8bec72` |
| TEST-002 `submit_bid` (vendor) | FINALIZED, GenVM SUCCESS; price 4500, explicit NO hardware warranty | `0x624706106d0bfa8f264b73288f36c22c4a35b589d89925faecc684d081e2af90` |
| TEST-002 `evaluate_bid` (vendor) | FINALIZED, GenVM SUCCESS, consensus Accepted; return `INELIGIBLE` and Equivalence Principle `INELIGIBLE` | `0x91ff50c6b87e4c06ccf0c801a4c2e0965647ed9e6bee8126d3350a03336530cf` |
| TEST-002 finalized `get_bid` | `found: true`, `price: 4500`, `decision: INELIGIBLE` | Readback supplied by builder on 28 Oct 2026 |

The evaluation was executed in **Normal** mode with **5 initial validators** and **0 rotations**; the supplied explorer view reports `Accepted` consensus, `SUCCESS` execution, and an Equivalence Principle output of `ELIGIBLE`. This supports the actual AI adjudication flow and successful signed buyer-award transaction, **not** every possible attack/consensus disagreement outcome. A finalized-state `get_request` readback has confirmed `AWARDED` and the exact vendor address.

## Two contrasting live AI judgments

- **TEST-001 (compliant offer):** price 4800; all mandatory terms explicitly committed; AI verdict `ELIGIBLE`; buyer award finalized; state readback `AWARDED`.
- **TEST-002 (noncompliant offer):** price 4500; express warranty refusal; AI verdict `INELIGIBLE`; finalized view confirms persisted decision. This demonstrates that the AI decision gate is not merely a price comparison.

## Required to complete V1 review

- [ ] Confirm `get_bid` from finalized state now returns `decision: ELIGIBLE`
- [x] Buyer wallet called `award("BIDSEAL-TEST-001", "0xD6b8A3A5eB329410D9504784812b8569afA8C2aF")`; signed call finalized and returned success (TX above)
- [x] Confirm `get_request` state `AWARDED` and awarded bidder matches vendor (Studio Finalized readback)
- [ ] Unauthorized `award` rejected
- [x] Noncompliant offer receives `INELIGIBLE` on-chain (AI consensus and readback)
- [ ] Attempt to award TEST-002 is rejected and request remains `OPEN`
- [ ] Unauthorized cancellation/award and replay/duplicate attempts rejected
- [ ] Demo video and explorer cross-check

**Scope:** verifies commitments against procurement requirements. Does **not** transfer funds, enforce delivery, or guarantee external-world fulfillment.
