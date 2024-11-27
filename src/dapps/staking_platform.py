import json
from web3 import Web3
from eth_account import Account

class StakingPlatform:
    """A decentralized staking platform."""

    def __init__(self, web3_provider, private_key, staking_contract_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.staking_contract = self.load_contract(staking_contract_address)

    def load_contract(self, contract_address):
        """Load the smart contract ABI and create a contract instance."""
        with open('path/to/your/staking_contract_abi.json') as f:
            staking_abi = json.load(f)
        return self.web3.eth.contract(address=contract_address, abi=staking_abi)

    def stake_tokens(self, amount):
        """Stake a specified amount of tokens."""
        tx = self.staking_contract.functions.stake(self.web3.toWei(amount, 'ether')).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Staked {amount} tokens: {tx_hash.hex()}")

    def withdraw_tokens(self, amount):
        """Withdraw a specified amount of staked tokens."""
        tx = self.staking_contract.functions.withdraw(self.web3.toWei(amount, 'ether')).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Withdrew {amount} tokens: {tx_hash.hex()}")

    def claim_rewards(self):
        """Claim staking rewards."""
        tx = self.staking_contract.functions.claimRewards().buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Claimed rewards: {tx_hash.hex()}")

    def get_staked_amount(self):
        """Get the amount of tokens staked by the user."""
        try:
            staked_amount = self.staking_contract.functions.getStakedAmount(self.account.address).call()
            print(f"Staked amount: {self.web3.fromWei(staked_amount, 'ether')} tokens")
        except Exception as e:
            print(f"Error retrieving staked amount: {str(e)}")

    def get_rewards(self):
        """Get the total rewards earned by the user."""
        try:
            rewards = self.staking_contract.functions.getRewards(self.account.address).call()
            print(f"Total rewards: {self.web3.fromWei(rewards, 'ether')} tokens")
        except Exception as e:
            print(f"Error retrieving rewards: {str(e)}")

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"
    staking_contract_address = "0xYourStakingContractAddress"

    staking_platform = StakingPlatform(web3_provider, private_key, staking_contract_address)

    # Stake tokens
    staking_platform.stake_tokens(10.0)  # Stake 10 tokens

    # Withdraw tokens
    staking_platform.withdraw_tokens(5.0)  # Withdraw 5 tokens

    # Claim rewards
    staking_platform.claim_rewards()

    # Get staked amount
    staking_platform.get_staked_amount()

    # Get rewards
    staking_platform.get_rewards()
