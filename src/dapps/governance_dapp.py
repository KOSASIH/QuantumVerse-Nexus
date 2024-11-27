import json
from web3 import Web3
from eth_account import Account
from datetime import datetime

class GovernanceDApp:
    """A decentralized governance application."""

    def __init__(self, web3_provider, private_key, governance_contract_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.governance_contract = self.load_contract(governance_contract_address)

    def load_contract(self, contract_address):
        """Load the smart contract ABI and create a contract instance."""
        with open('path/to/your/governance_contract_abi.json') as f:
            governance_abi = json.load(f)
        return self.web3.eth.contract(address=contract_address, abi=governance_abi)

    def create_proposal(self, description):
        """Create a new governance proposal."""
        tx = self.governance_contract.functions.createProposal(description).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Proposal created: {tx_hash.hex()}")

    def vote_on_proposal(self, proposal_id, support):
        """Vote on a governance proposal."""
        tx = self.governance_contract.functions.vote(proposal_id, support).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Voted on proposal {proposal_id}: {tx_hash.hex()}")

    def execute_proposal(self, proposal_id):
        """Execute a governance proposal if it has been approved."""
        tx = self.governance_contract.functions.executeProposal(proposal_id).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Executed proposal {proposal_id}: {tx_hash.hex()}")

    def get_proposal_details(self, proposal_id):
        """Get details of a governance proposal."""
        proposal = self.governance_contract.functions.getProposal(proposal_id).call()
        print(f"Proposal details for ID {proposal_id}: {proposal}")

    def get_all_proposals(self):
        """Get all proposals."""
        total_proposals = self.governance_contract.functions.getTotalProposals().call()
        for proposal_id in range(total_proposals):
            self.get_proposal_details(proposal_id)

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"
    governance_contract_address = "0xYourGovernanceContractAddress"

    governance_dapp = GovernanceDApp(web3_provider, private_key, governance_contract_address)

    # Create a new proposal
    governance_dapp.create_proposal("Increase the protocol's budget by 20%.")

    # Vote on a proposal
    governance_dapp.vote_on_proposal(proposal_id=0, support=True)

    # Execute a proposal
    governance_dapp.execute_proposal(proposal_id=0)

    # Get details of a specific proposal
    governance_dapp.get_proposal_details(proposal_id=0)

    # Get all proposals
    governance_dapp.get_all_proposals()
