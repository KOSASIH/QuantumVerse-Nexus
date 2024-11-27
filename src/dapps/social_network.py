import json
from web3 import Web3
from eth_account import Account

class SocialNetwork:
    """A decentralized social network."""

    def __init__(self, web3_provider, private_key, social_network_contract_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.social_network_contract = self.load_contract(social_network_contract_address)

    def load_contract(self, contract_address):
        """Load the smart contract ABI and create a contract instance."""
        with open('path/to/your/social_network_contract_abi.json') as f:
            social_network_abi = json.load(f)
        return self.web3.eth.contract(address=contract_address, abi=social_network_abi)

    def register_user(self, username):
        """Register a new user in the social network."""
        tx = self.social_network_contract.functions.registerUser (username).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"User  '{username}' registered: {tx_hash.hex()}")

    def create_post(self, content):
        """Create a new post."""
        tx = self.social_network_contract.functions.createPost(content).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Post created: {tx_hash.hex()}")

    def like_post(self, post_id):
        """Like a post."""
        tx = self.social_network_contract.functions.likePost(post_id).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Post {post_id} liked: {tx_hash.hex()}")

    def follow_user(self, user_address):
        """Follow another user."""
        tx = self.social_network_contract.functions.followUser (user_address).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Following user {user_address}: {tx_hash.hex()}")

    def get_user_posts(self, user_address):
        """Get all posts from a user."""
        try:
            posts = self.social_network_contract.functions.getUser Posts(user_address).call()
            print(f"Posts from user {user_address}: {posts}")
        except Exception as e:
            print(f"Error retrieving posts: {str(e)}")

    def get_post_details(self, post_id):
        """Get details of a specific post."""
        try:
            post = self.social_network_contract.functions.getPost(post_id).call()
            print(f"Post details for ID {post_id}: {post}")
        except Exception as e:
            print(f"Error retrieving post details: {str(e)}")

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"
    social_network_contract_address = "0xYourSocialNetworkContractAddress"

    social_network = SocialNetwork(web3_provider, private_key, social_network_contract_address)

    # Register a new user
    social_network.register_user("alice")

    # Create a new post
    social_network.create_post("Hello, this is my first post!")

    # Like a post
    social_network.like_post(post_id=0)

    # Follow another user
    social_network.follow_user(user_address="0xAnotherUser Address")

    # Get all posts from a user
    social_network.get_user_posts(user_address="0xAnotherUser Address")

    # Get details of a specific post
    social_network.get_post_details(post_id=0)
