import json
import time
from web3 import Web3
from eth_account import Account

class LendingPlatform:
    """A decentralized lending platform with advanced features."""

    def __init__(self, web3_provider, private_key, contract_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.contract_address = contract_address
        self.contract = self.load_contract()
        self.lenders = {}
        self.borrowers = {}
        self.collateral = {}
        self.interest_rate = 0.05  # Base interest rate of 5%
        self.liquidation_threshold = 1.5  # 150% collateralization

    def load_contract(self):
        """Load the smart contract ABI and create a contract instance."""
        with open('path/to/your/contract_abi.json') as f:
            contract_abi = json.load(f)
        return self.web3.eth.contract(address=self.contract_address, abi=contract_abi)

    def deposit(self, amount):
        """Deposit assets into the lending platform."""
        address = self.account.address
        tx = self.contract.functions.deposit().buildTransaction({
            'from': address,
            'value': self.web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Deposit transaction sent: {tx_hash.hex()}")
        self.lenders[address] = self.lenders.get(address, 0) + amount

    def borrow(self, amount, collateral_amount):
        """Borrow assets against collateral."""
        address = self.account.address
        if collateral_amount < amount * self.liquidation_threshold:
            print("Insufficient collateral. You need at least 150% of the loan amount.")
            return

        tx = self.contract.functions.borrow(amount, collateral_amount).buildTransaction({
            'from': address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Borrow transaction sent: {tx_hash.hex()}")
        self.borrowers[address] = self.borrowers.get(address, 0) + amount
        self.collateral[address] = collateral_amount

    def repay(self, amount):
        """Repay borrowed assets."""
        address = self.account.address
        if address not in self.borrowers or self.borrowers[address] < amount:
            print("You cannot repay more than your borrowed amount.")
            return

        tx = self.contract.functions.repay(amount).buildTransaction({
            'from': address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Repay transaction sent: {tx_hash.hex()}")
        self.borrowers[address] -= amount

    def check_liquidation(self, address):
        """Check if the user's collateral is sufficient to cover their loan."""
        if address in self.borrowers:
            loan_amount = self.borrowers[address]
            collateral_amount = self.collateral.get(address, 0)
            if collateral_amount < loan_amount * self.liquidation_threshold:
                print(f"User  {address} is liquidated. Collateral is insufficient.")
                self.liquidate(address)

    def liquidate(self, address):
        """Liquidate the collateral of a borrower."""
        print(f"Liquidating collateral for {address}. # Here you would implement the logic to transfer the collateral to the platform or a designated address
        # This is a placeholder for the actual liquidation process
        collateral_amount = self.collateral.get(address, 0)
        print(f"Collateral of {collateral_amount} liquidated for {address}.")
        # Reset borrower's data after liquidation
        self.borrowers.pop(address, None)
        self.collateral.pop(address, None)

    def calculate_interest(self, address):
        """Calculate interest on the borrowed amount."""
        if address not in self.borrowers:
            print("No loans found for this address.")
            return 0

        interest = self.borrowers[address] * self.interest_rate
        print(f"Interest for {address}: {interest}")
        return interest

    def withdraw(self, amount):
        """Withdraw deposited assets."""
        address = self.account.address
        if address not in self.lenders or self.lenders[address] < amount:
            print("Insufficient balance to withdraw.")
            return

        tx = self.contract.functions.withdraw(amount).buildTransaction({
            'from': address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(address),
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Withdraw transaction sent: {tx_hash.hex()}")
        self.lenders[address] -= amount

    def update_interest_rate(self, new_rate):
        """Update the interest rate based on market conditions."""
        self.interest_rate = new_rate
        print(f"Interest rate updated to: {self.interest_rate}")

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"
    contract_address = "your_contract_address"

    platform = LendingPlatform(web3_provider, private_key, contract_address)

    # Simulate user actions
    platform.deposit(1000)
    platform.borrow(600, 900)  # Borrowing with sufficient collateral
    platform.calculate_interest(platform.account.address)
    platform.repay(300)
    platform.check_liquidation(platform.account.address)
    platform.withdraw(500)
