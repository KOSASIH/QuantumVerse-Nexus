import hashlib
import json
from typing import Any, Dict, List, Tuple

class CrossChainTransaction:
    def __init__(self, sender: str, receiver: str, amount: float, source_chain: str, target_chain: str):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.source_chain = source_chain
        self.target_chain = target_chain
        self.transaction_id = self.generate_transaction_id()

    def generate_transaction_id(self) -> str:
        """Generate a unique transaction ID based on the transaction details."""
        transaction_data = f"{self.sender}{self.receiver}{self.amount}{self.source_chain}{self.target_chain}"
        return hashlib.sha256(transaction_data.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the transaction to a dictionary for serialization."""
        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "source_chain": self.source_chain,
            "target_chain": self.target_chain,
        }

class InteroperabilityManager:
    def __init__(self):
        self.chains: Dict[str, List[str]] = {}  # Maps chain names to their nodes

    def register_chain(self, chain_name: str, nodes: List[str]):
        """Register a new blockchain with its nodes."""
        self.chains[chain_name] = nodes

    def send_transaction(self, transaction: CrossChainTransaction) -> str:
        """Send a cross-chain transaction to the target chain."""
        if transaction.target_chain not in self.chains:
            raise ValueError("Target chain not registered.")

        # Simulate sending the transaction to the target chain
        print(f"Sending transaction {transaction.transaction_id} from {transaction.source_chain} to {transaction.target_chain}.")
        # Here you would implement the actual logic to send the transaction to the target chain
        return transaction.transaction_id

    def receive_transaction(self, transaction_data: Dict[str, Any]) -> bool:
        """Receive a transaction on the target chain."""
        transaction = CrossChainTransaction(**transaction_data)
        print(f"Received transaction {transaction.transaction_id} on {transaction.target_chain}.")
        # Here you would implement the logic to process the transaction
        return True

    def get_registered_chains(self) -> List[str]:
        """Get a list of registered chains."""
        return list(self.chains.keys())

def main():
    # Example usage of the interoperability protocols
    interoperability_manager = InteroperabilityManager()

    # Register two chains
    interoperability_manager.register_chain("ChainA", ["nodeA1", "nodeA2"])
    interoperability_manager.register_chain("ChainB", ["nodeB1", "nodeB2"])

    # Create a cross-chain transaction
    transaction = CrossChainTransaction(sender="Alice", receiver="Bob", amount=10.0, source_chain="ChainA", target_chain="ChainB")

    # Send the transaction
    transaction_id = interoperability_manager.send_transaction(transaction)

    # Simulate receiving the transaction on the target chain
    transaction_data = transaction.to_dict()
    interoperability_manager.receive_transaction(transaction_data)

    # List registered chains
    registered_chains = interoperability_manager.get_registered_chains()
    print(f"Registered chains: {registered_chains}")

if __name__ == "__main__":
    main()
