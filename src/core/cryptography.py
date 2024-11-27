import hashlib
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import AES, PKCS1_OAEP
from base64 import b64encode, b64decode

class Cryptography:
    def __init__(self):
        self.key_pair = self.generate_key_pair()

    def generate_key_pair(self):
        """
        Generate a new RSA key pair
        :return: RSA key pair
        """
        key = RSA.generate(2048)
        return key

    def get_public_key(self):
        """
        Get the public key from the RSA key pair
        :return: Public key in PEM format
        """
        return self.key_pair.publickey().export_key()

    def sign_message(self, message):
        """
        Sign a message using the private key
        :param message: The message to sign
        :return: The signature
        """
        message_hash = SHA256.new(message.encode())
        signature = pkcs1_15.new(self.key_pair).sign(message_hash)
        return b64encode(signature).decode()

    def verify_signature(self, message, signature):
        """
        Verify a message signature
        :param message: The original message
        :param signature: The signature to verify
        :return: True if valid, False otherwise
        """
        message_hash = SHA256.new(message.encode())
        try:
            pkcs1_15.new(self.key_pair.publickey()).verify(message_hash, b64decode(signature))
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def hash_data(data):
        """
        Create a SHA-256 hash of the given data
        :param data: Data to hash
        :return: SHA-256 hash
        """
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def encrypt_aes(data, key):
        """
        Encrypt data using AES encryption
        :param data: Data to encrypt
        :param key: AES key (must be 16, 24, or 32 bytes long)
        :return: Encrypted data
        """
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return b64encode(cipher.nonce + tag + ciphertext).decode()

    @staticmethod
    def decrypt_aes(encrypted_data, key):
        """
        Decrypt AES-encrypted data
        :param encrypted_data: Encrypted data
        :param key: AES key
        :return: Decrypted data
        """
        raw_data = b64decode(encrypted_data)
        nonce, tag, ciphertext = raw_data[:16], raw_data[16:32], raw_data[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()

    @staticmethod
    def generate_aes_key():
        """
        Generate a random AES key
        :return: AES key
        """
        return os.urandom(32)  # 256-bit key

# Example usage
if __name__ == "__main__":
    crypto = Cryptography()
    message = "Hello, QuantumVerse!"
    
    # Signing a message
    signature = crypto.sign_message(message)
    print(f"Signature: {signature}")

    # Verifying the signature
    is_valid = crypto.verify_signature(message, signature)
    print(f"Is the signature valid? {is_valid}")

    # Hashing data
    hashed_data = crypto.hash_data(message)
    print(f"Hashed Data: {hashed_data}")

    # AES Encryption
    aes_key = Cryptography.generate_aes_key()
    encrypted_data = crypto.encrypt_aes(message, aes_key)
    print(f"Encrypted Data: {encrypted_data}")

    # AES Decryption
    decrypted_data = crypto.decrypt_aes(encrypted_data, aes_key)
    print(f"Decrypted Data: {decrypted_data}")
