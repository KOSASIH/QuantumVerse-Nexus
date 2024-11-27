import json
from web3 import Web3
from eth_account import Account
from datetime import datetime

class Marketplace:
    """A decentralized marketplace for NFTs."""

    def __init__(self, web3_provider, private_key, nft_contract_address, marketplace_contract_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.nft_contract = self.load_contract(nft_contract_address)
        self.marketplace_contract = self.load_contract(marketplace_contract_address)
        self.listings = {}  # Store NFT listings

    def load_contract(self, contract_address):
        """Load the smart contract ABI and create a contract instance."""
        with open('path/to/your/nft_contract_abi.json') as f:
            nft_abi = json.load(f)
        with open('path/to/your/marketplace_contract_abi.json') as f:
            marketplace_abi = json.load(f)
        return self.web3.eth.contract(address=contract_address, abi=nft_abi)

    def mint_nft(self, token_uri):
        """Mint a new NFT."""
        tx = self.nft_contract.functions.mint(self.account.address, token_uri).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Mint transaction sent: {tx_hash.hex()}")

    def list_nft(self, token_id, price):
        """List an NFT for sale."""
        tx = self.marketplace_contract.functions.listNFT(token_id, self.web3.toWei(price, 'ether')).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.listings[token_id] = {'price': price, 'listed_at': datetime.now()}
        print(f"NFT {token_id} listed for {price} ETH: {tx_hash.hex()}")

    def buy_nft(self, token_id):
        """Buy an NFT."""
        if token_id not in self.listings:
            print("NFT not listed for sale.")
            return

        price = self.listings[token_id]['price']
        tx = self.marketplace_contract.functions.buyNFT(token_id).buildTransaction({
            'from': self.account.address,
            'value': self.web3.toWei(price, 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"NFT {token_id} purchased for {price} ETH: {tx_hash.hex()}")
        del self.listings[token_id]  # Remove listing after purchase

    def create_auction(self, token_id, starting_price, duration):
        """Create an auction for an NFT."""
        end_time = datetime.now().timestamp() + duration
        tx = self.marketplace_contract.functions.createAuction(token_id, self.web3.toWei(starting_price, 'ether'), end_time).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce ```python
            : self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Auction created for NFT {token_id} starting at {starting_price} ETH, ending at {end_time}: {tx_hash.hex()}")

    def bid_on_auction(self, token_id, bid_amount):
        """Place a bid on an NFT auction."""
        tx = self.marketplace_contract.functions.bid(token_id).buildTransaction({
            'from': self.account.address,
            'value': self.web3.toWei(bid_amount, 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Bid placed on NFT {token_id} for {bid_amount} ETH: {tx_hash.hex()}")

    def withdraw_royalties(self):
        """Withdraw royalties from secondary sales."""
        tx = self.marketplace_contract.functions.withdrawRoyalties().buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Royalties withdrawn: {tx_hash.hex()}")

    def get_listing(self, token_id):
        """Get details of a listed NFT."""
        if token_id in self.listings:
            listing = self.listings[token_id]
            print(f"NFT {token_id} is listed for {listing['price']} ETH, listed at {listing['listed_at']}")
        else:
            print("NFT not listed for sale.")

    def get_auction_details(self, token_id):
        """Get details of an auction."""
        auction_details = self.marketplace_contract.functions.getAuctionDetails(token_id).call()
        print(f"Auction details for NFT {token_id}: {auction_details}")

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"
    nft_contract_address = "0xYourNFTContractAddress"
    marketplace_contract_address = "0xYourMarketplaceContractAddress"

    marketplace = Marketplace(web3_provider, private_key, nft_contract_address, marketplace_contract_address)

    # Mint an NFT
    marketplace.mint_nft("https://example.com/nft_metadata.json")

    # List the NFT for sale
    marketplace.list_nft(token_id=1, price=0.1)

    # Buy the NFT
    marketplace.buy_nft(token_id=1)

    # Create an auction for an NFT
    marketplace.create_auction(token_id=2, starting_price=0.05, duration=3600)

    # Place a bid on the auction
    marketplace.bid_on_auction(token_id=2, bid_amount=0.06)

    # Withdraw royalties
    marketplace.withdraw_royalties()

    # Get listing details
    marketplace.get_listing(token_id=1)

    # Get auction details
    marketplace.get_auction_details(token_id=2)
