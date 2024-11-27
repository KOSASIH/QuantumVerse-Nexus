import json
from web3 import Web3
from eth_account import Account

class NFTMarketplace:
    """A decentralized NFT marketplace."""

    def __init__(self, web3_provider, private_key, nft_marketplace_contract_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.nft_marketplace_contract = self.load_contract(nft_marketplace_contract_address)

    def load_contract(self, contract_address):
        """Load the smart contract ABI and create a contract instance."""
        with open('path/to/your/nft_marketplace_contract_abi.json') as f:
            nft_marketplace_abi = json.load(f)
        return self.web3.eth.contract(address=contract_address, abi=nft_marketplace_abi)

    def mint_nft(self, name, description, image_url):
        """Mint a new NFT."""
        tx = self.nft_marketplace_contract.functions.mintNFT(name, description, image_url).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"NFT minted: {tx_hash.hex()}")

    def list_nft_for_sale(self, nft_id, price):
        """List an NFT for sale."""
        tx = self.nft_marketplace_contract.functions.listNFTForSale(nft_id, price).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"NFT {nft_id} listed for sale: {tx_hash.hex()}")

    def buy_nft(self, nft_id):
        """Buy an NFT."""
        tx = self.nft_marketplace_contract.functions.buyNFT(nft_id).buildTransaction({
            'from': self.account.address,
            'value': self.web3.toWei('1', 'ether'),  # Assuming the price is 1 ETH
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"NFT {nft_id} bought: {tx_hash.hex()}")

    def get_nft_details(self, nft_id):
        """Get details of an NFT."""
        try:
            nft = self.nft_marketplace_contract.functions.getNFT(nft_id).call()
            print(f"NFT details for ID {nft_id}: {nft}")
        except Exception as e:
            print(f"Error retrieving NFT details: {str(e)}")

    def get_all_nfts(self):
        """Get all NFTs in the marketplace."""
        try:
            nfts = self.nft_marketplace_contract.functions.getAllNFTs().call()
            print(f"All NFTs: {nfts}")
        except Exception as e:
            print(f"Error retrieving all NFTs: {str(e)}")

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"
    nft_marketplace_contract_address = "0xYourNFTMarketplaceContractAddress"

    nft_marketplace = NFTMarketplace(web3_provider, private_key, nft_marketplace_contract_address)

    # Mint a new NFT
    nft_marketplace.mint_nft("My NFT", "This is my NFT", "https://example.com/image.png")

    # List an NFT for sale
    nft_marketplace.list_nft_for_sale(nft_id=0, price=1.0)

    # Buy an NFT
    nft_marketplace.buy_nft(nft_id=0)

    # Get details of an NFT
    nft_marketplace.get_nft_details(nft_id=0)

    # Get all NFTs
    nft_marketplace.get_all_nfts()
