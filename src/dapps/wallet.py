import json
from web3 import Web3
from eth_account import Account

class MultiSigWallet:
    """A multi-signature wallet implementation."""

    def __init__(self, web3_provider, owners, required_signatures):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.owners = owners  # List of owner addresses
        self.required_signatures = required_signatures
        self.transactions = {}  # Store transactions
        self.approvals = {}  # Store approvals for each transaction
        self.transaction_count = 0  # Count of transactions

    def create_transaction(self, to, value):
        """Create a new transaction."""
        if not self.is_owner(self.web3.eth.defaultAccount):
            raise Exception("Only owners can create transactions.")

        self.transaction_count += 1
        transaction_id = self.transaction_count
        self.transactions[transaction_id] = {
            'to': to,
            'value': value,
            'executed': False
        }
        self.approvals[transaction_id] = set()  # Set to track approvals
        print(f"Transaction created: ID {transaction_id}, To: {to}, Value: {value} ETH")
        return transaction_id

    def approve_transaction(self, transaction_id):
        """Approve a transaction."""
        if not self.is_owner(self.web3.eth.defaultAccount):
            raise Exception("Only owners can approve transactions.")

        if transaction_id not in self.transactions:
            raise Exception("Transaction does not exist.")

        if self.web3.eth.defaultAccount in self.approvals[transaction_id]:
            raise Exception("Transaction already approved by this owner.")

        self.approvals[transaction_id].add(self.web3.eth.defaultAccount)
        print(f"Transaction ID {transaction_id} approved by {self.web3.eth.defaultAccount}")

        if len(self.approvals[transaction_id]) >= self.required_signatures:
            self.execute_transaction(transaction_id)

    def execute_transaction(self, transaction_id):
        """Execute a transaction if enough approvals are received."""
        if transaction_id not in self.transactions:
            raise Exception("Transaction does not exist.")

        transaction = self.transactions[transaction_id]
        if transaction['executed']:
            raise Exception("Transaction already executed.")

        # Execute the transaction
        tx = {
            'to': transaction['to'],
            'value': self.web3.toWei(transaction['value'], 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.web3.eth.defaultAccount),
        }
        signed_tx = self.web3.eth.account.signTransaction(tx, self.web3.eth.defaultAccount.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        transaction['executed'] = True
        print(f"Transaction ID {transaction_id} executed: {tx_hash.hex()}")

    def is_owner(self, address):
        """Check if the address is an owner of the wallet."""
        return address in self.owners

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    owners = ["owner_address_1", "owner_address_2", "owner_address_3"]
    required_signatures = 2  # Number of required signatures to execute a transaction

    wallet = MultiSigWallet(web3_provider, owners, required_signatures)

    # Set the default account for the wallet (for demonstration purposes)
    wallet.web3.eth.defaultAccount = "owner_address_1"  # Change to the address of the owner

    # Create a transaction
    tx_id = wallet.create_transaction("recipient_address", 0.1)

    # Approve the transaction from different owners
    wallet.web3.eth.defaultAccount = "owner_address_2"
    wallet.approve_transaction(tx_id)

    wallet.web3.eth.defaultAccount = "owner_address_1"
    wallet.approve_transaction(tx_id)
