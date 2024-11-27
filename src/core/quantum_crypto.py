import os
import numpy as np
from pqcrypto.kem import lightsaber
from pqcrypto.sign import picnic

class QuantumCrypto:
    def __init__(self):
        self.kem = lightsaber
        self.signature_scheme = picnic

    def generate_keypair(self):
        """
        Generate a key pair for the quantum-resistant KEM (Key Encapsulation Mechanism).
        
        Returns:
            tuple: (public_key, private_key)
        """
        public_key, private_key = self.kem.generate_keypair()
        return public_key, private_key

    def encrypt(self, public_key, plaintext):
        """
        Encrypt a plaintext message using the provided public key.
        
        Args:
            public_key (bytes): The public key for encryption.
            plaintext (bytes): The message to encrypt.
        
        Returns:
            tuple: (ciphertext, shared_secret)
        """
        ciphertext, shared_secret = self.kem.encrypt(public_key, plaintext)
        return ciphertext, shared_secret

    def decrypt(self, private_key, ciphertext):
        """
        Decrypt a ciphertext using the provided private key.
        
        Args:
            private_key (bytes): The private key for decryption.
            ciphertext (bytes): The ciphertext to decrypt.
        
        Returns:
            bytes: The decrypted plaintext message.
        """
        plaintext, shared_secret = self.kem.decrypt(private_key, ciphertext)
        return plaintext

    def sign(self, private_key, message):
        """
        Sign a message using the provided private key.
        
        Args:
            private_key (bytes): The private key for signing.
            message (bytes): The message to sign.
        
        Returns:
            bytes: The digital signature.
        """
        signature = self.signature_scheme.sign(private_key, message)
        return signature

    def verify(self, public_key, message, signature):
        """
        Verify a digital signature using the provided public key.
        
        Args:
            public_key (bytes): The public key for verification.
            message (bytes): The signed message.
            signature (bytes): The digital signature to verify.
        
        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        is_valid = self.signature_scheme.verify(public_key, message, signature)
        return is_valid

def main():
    # Example usage of the QuantumCrypto class
    qc = QuantumCrypto()

    # Key generation
    public_key, private_key = qc.generate_keypair()
    print("Public Key:", public_key.hex())
    print("Private Key:", private_key.hex())

    # Encrypting a message
    message = b"Hello, Quantum World!"
    ciphertext, shared_secret = qc.encrypt(public_key, message)
    print("Ciphertext:", ciphertext.hex())
    print("Shared Secret:", shared_secret.hex())

    # Decrypting the message
    decrypted_message = qc.decrypt(private_key, ciphertext)
    print("Decrypted Message:", decrypted_message)

    # Signing a message
    signature = qc.sign(private_key, message)
    print("Signature:", signature.hex())

    # Verifying the signature
    is_valid = qc.verify(public_key, message, signature)
    print("Is the signature valid?", is_valid)

if __name__ == "__main__":
    main()
