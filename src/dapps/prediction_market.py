import json
from web3 import Web3
from eth_account import Account
from datetime import datetime

class PredictionMarket:
    """A decentralized prediction market."""

    def __init__(self, web3_provider, private_key, market_contract_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.market_contract = self.load_contract(market_contract_address)

    def load_contract(self, contract_address):
        """Load the smart contract ABI and create a contract instance."""
        with open('path/to/your/market_contract_abi.json') as f:
            market_abi = json.load(f)
        return self.web3.eth.contract(address=contract_address, abi=market_abi)

    def create_market(self, event_name, options):
        """Create a new prediction market."""
        tx = self.market_contract.functions.createMarket(event_name, options).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Market created for event '{event_name}': {tx_hash.hex()}")

    def place_bet(self, market_id, option_index, amount):
        """Place a bet on a specific option in a market."""
        tx = self.market_contract.functions.placeBet(market_id, option_index).buildTransaction({
            'from': self.account.address,
            'value': self.web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Bet placed on market {market_id} for option {option_index}: {tx_hash.hex()}")

    def resolve_market(self, market_id, winning_option_index):
        """Resolve a market and declare the winning option."""
        tx = self.market_contract.functions.resolveMarket(market_id, winning_option_index).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Market {market_id} resolved with winning option {winning_option_index}: {tx_hash.hex()}")

    def claim_payout(self, market_id):
        """Claim payout for a winning bet."""
        tx = self.market_contract.functions.claimPayout(market_id).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Payout claimed for market {market_id}: {tx_hash.hex()}")

    def get_market_details(self, market_id):
        """Get details of a prediction market."""
        market = self.market_contract.functions.getMarket(market_id).call()
        print(f"Market details for ID {market_id}: {market}")

    def get_all_markets(self):
        """Get all prediction markets."""
        total_markets = self.market_contract.functions.getTotalMarkets().call()
        for market_id in range(total_markets):
            self.get_market_details(market_id)

# Example usage
if __name__ == "__ main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"
    market_contract_address = "0xYourMarketContractAddress"

    prediction_market = PredictionMarket(web3_provider, private_key, market_contract_address)

    # Create a new prediction market
    prediction_market.create_market("Will it rain tomorrow?", ["Yes", "No"])

    # Place a bet on a specific option
    prediction_market.place_bet(market_id=0, option_index=0, amount=1.0)

    # Resolve the market
    prediction_market.resolve_market(market_id=0, winning_option_index=1)

    # Claim payout for a winning bet
    prediction_market.claim_payout(market_id=0)

    # Get details of a specific market
    prediction_market.get_market_details(market_id=0)

    # Get all markets
    prediction_market.get_all_markets()
