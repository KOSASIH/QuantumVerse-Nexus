import unittest
from security import Security

class TestSecurity(unittest.TestCase):
    def test_hash_password(self):
        """Test password hashing."""
        password = "securePassword123"
        hashed = Security.hash_password(password)
        self.assertNotEqual(hashed, password)  # Hashed password should not equal the original
        self.assertEqual(hashed, Security.hash_password(password))  # Same password should hash to the same value

    def test_validate_email(self):
        """Test email validation."""
        valid_email = "test@example.com"
        invalid_email = "invalid-email"

        self.assertTrue(Security.validate_email(valid_email))
        self.assertFalse(Security.validate_email(invalid_email))

    def test_generate_token(self):
        """Test token generation."""
        token = Security.generate_token()
        self.assertEqual(len(token), 64)  # 32 bytes = 64 hex characters

        # Test generating a token of a different length
        short_token = Security.generate_token(16)
        self.assertEqual(len(short_token), 32)  # 16 bytes = 32 hex characters

if __name__ == '__main__':
    unittest.main()
