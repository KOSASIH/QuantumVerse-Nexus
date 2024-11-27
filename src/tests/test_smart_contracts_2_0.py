import unittest
from smart_contracts import SmartContract

class TestSmartContract(unittest.TestCase):
    def setUp(self):
        self.contract = SmartContract()

    def test_create_account(self):
        """Test account creation."""
        self.contract.create_account("0x123")
        self.assertIn("0x123", self.contract.balances)
        self.assertEqual(self.contract.balances["0x123"], 0)

        with self.assertRaises(ValueError):
            self.contract.create_account("0x123")  # Account already exists

    def test_transfer(self):
        """Test transferring funds between accounts."""
        self.contract.create_account("0x123")
        self.contract.create_account("0x456")
        self.contract.balances["0x123"] = 100  # Set initial balance

        self.contract.transfer("0x123", "0x456", 50)
        self.assertEqual(self.contract.balances["0x123"], 50)
        self.assertEqual(self.contract.balances["0x456"], 50)

        with self.assertRaises(ValueError):
            self.contract.transfer("0x123", "0x456", 100)  # Insufficient balance

        with self.assertRaises(ValueError):
            self.contract.transfer("0x999", "0x456", 10)  # Invalid from address

        with self.assertRaises(ValueError):
            self.contract.transfer("0x123", "0x999", 10)  # Invalid to address

if __name__ == '__main__':
    unittest.main()
