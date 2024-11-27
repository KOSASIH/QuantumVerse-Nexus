import hashlib
import json
import os
from cryptography.fernet import Fernet

class PrivacyLayer:
    """Class to handle privacy features in the blockchain system."""
    
    def __init__(self):
        # Generate a key for encryption
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_data(self, data):
        """Encrypts the given data."""
        json_data = json.dumps(data).encode()
        encrypted_data = self.cipher.encrypt(json_data)
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        """Decrypts the given encrypted data."""
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data)

    def generate_zero_knowledge_proof(self, secret):
        """Mock implementation of a zero-knowledge proof."""
        # In a real implementation, this would generate a proof that
        # the secret is valid without revealing the secret itself.
        proof = hashlib.sha256(secret.encode()).hexdigest()
        return proof

    def verify_zero_knowledge_proof(self, secret, proof):
        """Verifies the zero-knowledge proof."""
        expected_proof = self.generate_zero_knowledge_proof(secret)
        return expected_proof == proof

# Example usage
if __name__ == "__main__":
    privacy_layer = PrivacyLayer()

    # Example transaction data
    transaction = {
        "id": "tx1",
        "amount": 100,
        "sender": "0x123",
        "recipient": "0x456"
    }

    # Encrypt the transaction data
    encrypted_transaction = privacy_layer.encrypt_data(transaction)
    print(f"Encrypted Transaction: {encrypted_transaction}")

    # Decrypt the transaction data
    decrypted_transaction = privacy_layer.decrypt_data(encrypted_transaction)
    print(f"Decrypted Transaction: {decrypted_transaction}")

    # Zero-Knowledge Proof Example
    secret = "my_secret"
    proof = privacy_layer.generate_zero_knowledge_proof(secret)
    print(f"Generated Proof: {proof}")

    # Verify the proof
    is_valid = privacy_layer.verify_zero_knowledge_proof(secret, proof)
    print(f"Is the proof valid? {is_valid}")
