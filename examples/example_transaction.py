# example_transaction.py
from src.core.blockchain import Blockchain
from src.utils.data_validation import DataValidation

def create_transaction(from_address, to_address, amount, signature):
    """Create and send a transaction."""
    # Validate transaction data
    transaction_data = {
        'from': from_address,
        'to': to_address,
        'amount': amount,
        'signature': signature
    }

    if not DataValidation.validate_transaction_data(transaction_data):
        print("Invalid transaction data.")
        return

    # Create a blockchain instance
    blockchain = Blockchain()

    # Send the transaction
    transaction_id = blockchain.send_transaction(transaction_data)
    print(f"Transaction sent! Transaction ID: {transaction_id}")

if __name__ == "__main__":
    # Example addresses and signature (replace with actual values)
    from_address = "1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8R9S0T"
    to_address = "0T9S8R7Q6P5O4N3M2L1K0J9I8H7G6F5E4D3C2B1A"
    amount = 10.0
    signature = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"

    create_transaction(from_address, to_address, amount, signature)
