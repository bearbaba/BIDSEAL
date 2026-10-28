"""BIDSEAL V1 address regression tests (Python shim, not GenVM)."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from test_shim import Driver, UserError

VENDOR = "0xD6b8A3A5eB329410D9504784812b8569afA8C2aF"
SPEC = ("Supply 20 refurbished laptops with at least 16 GB RAM each. "
        "Include a minimum 12-month hardware warranty, English-language "
        "support, and delivery within 14 calendar days. All requirements are mandatory.")
TERMS = ("We commit to delivering 20 refurbished laptops with at least 16 GB RAM "
         "each, a 12-month hardware warranty, English-language support, and "
         "delivery within 14 calendar days for the total price of 4800.")

class AddressLike:
    def __str__(self):
        return "addr#" + VENDOR[2:]

class AddressNormalization(unittest.TestCase):
    def setUp(self):
        self.d = Driver().load(ROOT / "contracts/bidseal.py")
        self.c = self.d.contract
        self.c.create_request("BIDSEAL-TEST-001", SPEC, 5000)

    def test_canonical_mixed_case(self):
        self.d.as_sender(VENDOR)
        self.c.submit_bid("BIDSEAL-TEST-001", 4800, TERMS)
        self.assertTrue(self.c.bid_exists("BIDSEAL-TEST-001", VENDOR.lower()))
        self.assertEqual(self.c.get_bid("BIDSEAL-TEST-001", VENDOR.upper().replace("0X", "0x"))["decision"], "PENDING")

    def test_addr_hash_sender(self):
        self.d.as_sender(AddressLike())
        self.c.submit_bid("BIDSEAL-TEST-001", 4800, TERMS)
        self.assertEqual(self.c.get_bid("BIDSEAL-TEST-001", VENDOR)["decision"], "PENDING")

    def test_missing_bid_returns_not_found(self):
        out = self.c.get_bid("BIDSEAL-TEST-001", VENDOR)
        self.assertFalse(out["found"])
        self.assertEqual(out["decision"], "NOT_FOUND")

    def test_invalid_address_rejected(self):
        with self.assertRaises(UserError):
            self.c.get_bid("BIDSEAL-TEST-001", "0x1234")

if __name__ == "__main__":
    unittest.main()
