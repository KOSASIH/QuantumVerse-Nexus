# cross_chain_example.py
from src.interoperability.cross_chain_bridge import CrossChainBridge

def perform_cross_chain_transfer():
    """Example of performing a cross-chain asset transfer."""
    
    # Create a cross-chain bridge instance
    bridge = CrossChainBridge()

    # Example asset transfer details (replace with actual values)
    from_chain = "Ethereum"
    to_chain = "Binance Smart Chain"
    asset = "ETH"
    amount = 1.0
    recipient_address = "0xRecipientAddressOnBSC"

    # Perform the cross-chain transfer
    transfer_id = bridge.transfer_asset(from_chain, to_chain, asset, amount, recipient_address)
    print(f"Cross-chain transfer initiated! Transfer ID: {transfer_id}")

if __name__ == "__main__":
    perform_cross_chain_transfer()
