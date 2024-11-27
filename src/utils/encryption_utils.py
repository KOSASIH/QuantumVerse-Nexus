# encryption_utils.py
from cryptography.fernet import Fernet

class EncryptionUtils:
    @staticmethod
    def generate_key() -> bytes:
        """Generate a new encryption key."""
        return Fernet.generate_key()

    @staticmethod
    def encrypt_data(key: bytes, data: str) -> bytes:
        """Encrypt data using the provided key."""
        fernet = Fernet(key)
        return fernet.encrypt(data.encode())

    @staticmethod
    def decrypt_data(key: bytes, encrypted_data: bytes) -> str:
        """Decrypt data using the provided key."""
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data).decode()
