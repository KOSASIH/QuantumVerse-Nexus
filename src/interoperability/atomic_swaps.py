import hashlib
import time
from web3 import Web3

class AtomicSwap:
    def __init__(self, blockchain_a_rpc, blockchain_b_rpc, contract_a_address, contract_b_address):
        self.blockchain_a = Web3(Web3.HTTPProvider(blockchain_a_rpc))
        self.blockchain_b = Web3(Web3.HTTPProvider(blockchain_b_rpc))
        self.contract_a_address = contract_a_address
        self.contract_b_address = contract_b_address

        # Load the smart contract ABI (Application Binary Interface)
        self.contract_a = self.load_contract(self.contract_a_address)
        self.contract_b = self.load_contract(self.contract_b_address)

    def load_contract(self, contract_address):
        """Load the smart contract using its address and ABI."""
        # Replace with the actual ABI of your contract
        abi = []  # Load your contract ABI here
        return self.blockchain_a.eth.contract(address=contract_address, abi=abi)

    def create_swap(self, amount_a, amount_b, recipient_b, secret):
        """Create an atomic swap."""
        secret_hash = self.hash_secret(secret)
        tx_hash_a = self.lock_asset_on_chain_a(amount_a, recipient_b, secret_hash)
        self.blockchain_a.eth.waitForTransactionReceipt(tx_hash_a)

        tx_hash_b = self.lock_asset_on_chain_b(amount_b, recipient_b, secret_hash)
        self.blockchain_b.eth.waitForTransactionReceipt(tx_hash_b)

    def lock_asset_on_chain_a(self, amount, recipient_b, secret_hash):
        """Lock the asset on blockchain A."""
        lock_function = self.contract_a.functions.lockAsset(amount, recipient_b, secret_hash)
        tx = lock_function.buildTransaction({
            'from': self.blockchain_a.eth.defaultAccount,
            'nonce': self.blockchain_a.eth.getTransactionCount(self.blockchain_a.eth.defaultAccount),
            'gas': 2000000,
            'gasPrice': self.blockchain_a.toWei('50', 'gwei')
        })
        signed_tx = self.blockchain_a.eth.account.signTransaction(tx, private_key='YOUR_PRIVATE_KEY')
        return self.blockchain_a.eth.sendRawTransaction(signed_tx.rawTransaction)

    def lock_asset_on_chain_b(self, amount, recipient_b, secret_hash):
        """Lock the asset on blockchain B."""
        lock_function = self.contract_b.functions.lockAsset(amount, recipient_b, secret_hash)
        tx = lock_function.buildTransaction({
            'from': self.blockchain_b.eth.defaultAccount,
            'nonce': self.blockchain_b.eth.getTransactionCount(self.blockchain_b.eth.defaultAccount),
            'gas': 2000000,
            'gasPrice': self.blockchain_b.toWei('50', 'gwei')
        })
        signed_tx = self.blockchain_b.eth.account.signTransaction(tx, private_key='YOUR_PRIVATE_KEY')
        return self.blockchain_b.eth.sendRawTransaction(signed_tx.rawTransaction)

    def redeem_swap(self, secret):
        """Redeem the swap on both blockchains."""
        secret_hash = self.hash_secret(secret)
        self.redeem_on_chain_a(secret)
        self.redeem_on_chain_b(secret_hash)

    def redeem_on_chain_a(self, secret):
        """Redeem the asset on blockchain A."""
        redeem_function = self.contract_a.functions.redeemAsset(secret)
        tx = redeem_function.buildTransaction({
            'from': self.blockchain_a.eth.defaultAccount,
            'nonce': self.blockchain_a.eth.getTransactionCount(self.blockchain_a.eth.defaultAccount),
            'gas': 2000000,
            'gasPrice': self.blockchain_a.toWei('50', 'gwei')
        })
        signed_tx = self.blockchain_a.eth.account.signTransaction(tx, private_key='YOUR_PRIVATE_KEY')
        return self.blockchain_a.eth.sendRawTransaction(signed_tx.rawTransaction)

    def redeem_on_chain_b(self, secret_hash):
        """Redeem the asset on blockchain B."""
        redeem_function = self.contract_b.functions.redeemAsset(secret_hash)
        tx = redeem_function.buildTransaction({
            'from': self.blockchain_b.eth.defaultAccount,
            'nonce': self.blockchain_b.eth.getTransactionCount(self.blockchain_b.eth.defaultAccount),
            'gas': 2000000,
            'gasPrice': self.blockchain_b.toWei('50', 'gwei')
        })
        signed_tx = self.blockchain_b.eth.account.signTransaction(tx, private_key='YOUR_PRIVATE_KEY')
        return self .blockchain_b.eth.sendRawTransaction(signed_tx.rawTransaction)

    def hash_secret(self, secret):
        """Hash the secret using SHA-256."""
        return hashlib.sha256(secret.encode()).hexdigest()

# Example usage
if __name__ == "__main__":
    blockchain_a_rpc = "https://blockchain-a-rpc-url"
    blockchain_b_rpc = "https://blockchain-b-rpc-url"
    contract_a_address = "0xYourContractAAddress"
    contract_b_address = "0xYourContractBAddress"

    swap = AtomicSwap(blockchain_a_rpc, blockchain_b_rpc, contract_a_address, contract_b_address)

    # Create an atomic swap
    amount_a = 1  # Amount on blockchain A
    amount_b = 1  # Amount on blockchain B
    recipient_b = "0xRecipientAddressOnB"
    secret = "your_secret"

    swap.create_swap(amount_a, amount_b, recipient_b, secret)
    print(f"Atomic swap created between blockchain A and B.")

    # Redeem the swap
    swap.redeem_swap(secret)
    print("Atomic swap redeemed successfully.")
