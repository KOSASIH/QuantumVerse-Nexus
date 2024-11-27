import json
from web3 import Web3
from eth_account import Account
from datetime import datetime

class InsuranceProtocol:
    """A decentralized insurance protocol."""

    def __init__(self, web3_provider, private_key, insurance_contract_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.insurance_contract = self.load_contract(insurance_contract_address)
        self.policies = {}  # Store policies

    def load_contract(self, contract_address):
        """Load the smart contract ABI and create a contract instance."""
        with open('path/to/your/insurance_contract_abi.json') as f:
            insurance_abi = json.load(f)
        return self.web3.eth.contract(address=contract_address, abi=insurance_abi)

    def create_policy(self, policy_id, premium, coverage_amount, duration):
        """Create a new insurance policy."""
        tx = self.insurance_contract.functions.createPolicy(
            policy_id,
            self.web3.toWei(premium, 'ether'),
            self.web3.toWei(coverage_amount, 'ether'),
            duration
        ).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.policies[policy_id] = {
            'premium': premium,
            'coverage_amount': coverage_amount,
            'duration': duration,
            'created_at': datetime.now(),
            'status': 'active'
        }
        print(f"Policy {policy_id} created: {tx_hash.hex()}")

    def submit_claim(self, policy_id, claim_amount):
        """Submit a claim against a policy."""
        if policy_id not in self.policies:
            print("Policy does not exist.")
            return

        tx = self.insurance_contract.functions.submitClaim(policy_id, self.web3.toWei(claim_amount, 'ether')).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Claim submitted for policy {policy_id}: {tx_hash.hex()}")

    def approve_claim(self, policy_id, claim_id):
        """Approve a claim."""
        tx = self.insurance_contract.functions.approveClaim(policy_id, claim_id).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Claim {claim_id} approved for policy {policy_id}: {tx_hash.hex()}")

    def reject_claim(self, policy_id, claim_id):
        """Reject a claim."""
        tx = self.insurance_contract.functions.rejectClaim(policy_id, claim_id).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Claim {claim_id} rejected for policy {policy_id}: {tx_hash.hex()}")

    defwithdraw_payout(self, policy_id, claim_id):
        """Withdraw payout for an approved claim."""
        tx = self.insurance_contract.functions.withdrawPayout(policy_id, claim_id).buildTransaction({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Payout withdrawn for claim {claim_id} on policy {policy_id}: {tx_hash.hex()}")

    def get_policy_details(self, policy_id):
        """Get details of an insurance policy."""
        if policy_id in self.policies:
            policy = self.policies[policy_id]
            print(f"Policy {policy_id}: {policy}")
        else:
            print("Policy does not exist.")

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"
    insurance_contract_address = "0xYourInsuranceContractAddress"

    insurance_protocol = InsuranceProtocol(web3_provider, private_key, insurance_contract_address)

    # Create a new insurance policy
    insurance_protocol.create_policy(policy_id=1, premium=0.01, coverage_amount=1, duration=365)

    # Submit a claim
    insurance_protocol.submit_claim(policy_id=1, claim_amount=0.5)

    # Approve a claim
    insurance_protocol.approve_claim(policy_id=1, claim_id=1)

    # Withdraw payout
    insurance_protocol.withdraw_payout(policy_id=1, claim_id=1)

    # Get policy details
    insurance_protocol.get_policy_details(policy_id=1)
