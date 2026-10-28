# BIDSEAL — Steward Demo Script (1–2 minutes)

1. Show `create_request` by BUYER, signed TX and exact requirements: 20 refurbished laptops, ≥16GB, 12-month warranty, ≤14 days, English support, max 5000.
2. VENDOR_A signs `submit_bid` for 4800 with explicit commitments; VENDOR_B signs `submit_bid` for 4500 but excludes warranty.
3. Execute `evaluate_bid` for both. Show actual validator/leader and successful consensus **with transaction IDs**; don't substitute mocked output.
4. Read contract state: A → ELIGIBLE, B → INELIGIBLE. Try to award B → rejected. Award A from BUYER wallet → AWARDED.
5. Attempt to award again or by the vendor → rejected.
6. On-screen labels: **requirements → independent verification → binding award gate**. Clearly say this is not a payment escrow and does not prove actual supplier delivery.

Capture actual on-chain TX links and results before submitting. Verify `FINISHED_WITH_RETURN` on v0.6.
