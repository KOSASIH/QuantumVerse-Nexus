import json
from web3 import Web3
from eth_account import Account
from cryptography.fernet import Fernet
from datetime import datetime
import random

# Constants
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
TOKEN_CONTRACT_ADDRESS = "0xYourTokenContractAddress"
LOAN_CONTRACT_ADDRESS = "0xYourLoanContractAddress"

# Initialize Web3
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Load smart contract ABI
with open('path/to/TokenABI.json') as f:
    token_abi = json.load(f)

with open('path/to/LoanABI.json') as f:
    loan_abi = json.load(f)

# Initialize contracts
token_contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=token_abi)
loan_contract = web3.eth.contract(address=LOAN_CONTRACT_ADDRESS, abi=loan_abi)

# Encryption utility
class EncryptionUtil:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, token):
        return self.cipher.decrypt(token.encode()).decode()

# User class
class User:
    def __init__(self, private_key):
        self.account = Account.from_key(private_key)
        self.encryption_util = EncryptionUtil()

    def get_balance(self):
        return web3.fromWei(token_contract.functions.balanceOf(self.account.address).call(), 'ether')

    def deposit(self, amount):
        tx = token_contract.functions.approve(LOAN_CONTRACT_ADDRESS, web3.toWei(amount, 'ether')).buildTransaction({
            'from': self.account.address,
            'nonce': web3.eth.getTransactionCount(self.account.address),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })
        signed_tx = web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.toHex(tx_hash)

    def withdraw(self, amount):
        tx = loan_contract.functions.withdraw(web3.toWei(amount, 'ether')).buildTransaction({
            'from': self.account.address,
            'nonce': web3.eth.getTransactionCount(self.account.address),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })
        signed_tx = web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.toHex(tx_hash)

    def request_loan(self, amount, duration):
        tx = loan_contract.functions.requestLoan(web3.toWei(amount, 'ether'), duration).buildTransaction({
            'from': self.account.address,
            'nonce': web3.eth.getTransactionCount(self.account.address),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })
        signed_tx = web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.toHex(tx_hash)

    def repay_loan(self, amount):
        tx = loan_contract.functions.repayLoan(web3.toWei(amount, 'ether')).buildTransaction({
            'from': self.account.address,
            'nonce': web3.eth.getTransactionCount(self.account.address),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })
        signed_tx = web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.toHex(tx_hash)

# Oracle integration for real-world data
class Oracle:
    def __init__(self):
        self.oracle_url = "https://api.example.com/data"

    def get_interest_rate(self):
        # Simulate fetching interest rate from an external API
        return random.uniform(0.01, 0.05)  # Random interest rate between 1% and 5%

# Main banking system class
class DecentralizedBanking:
    def __init__(self):
        self.users = {}
        self.oracle = Oracle()

    def register_user(self, private_key):
        user = User(private_key)
        self.users[user.account.address] = user
        return user.account.address

    def get_user_balance(self, address):
        if address in self.users:
            return self.users[address].get_balance()
        else:
            raise ValueError("User  not registered.")

    def deposit_funds(self, address, amount):
        if address in self.users:
            return self.users[address].deposit(amount)
        else:
            raise ValueError("User  not registered.")

    def withdraw_funds(self, address, amount):
        if address in self.users:
            return self.users[address].withdraw(amount)
        else:
            raise ValueError("User  not registered.")

    def request_loan(self, address, amount, duration):
        if address in self.users:
            return self.users[address].request_loan(amount, duration)
        else:
            raise ValueError("User  not registered.")

    def repay_loan(self, address, amount):
        if address in self.users:
            return self.users[address].repay_loan(amount)
        else:
            raise ValueError("User  not registered.")

    def get_current_interest_rate(self):
        return self.oracle.get_interest_rate()

# Example usage
if __name__ == "__main__":
    # Replace with your actual private key
    private_key = "0xYourPrivateKey"
    
    # Initialize the decentralized banking system
    banking_system = DecentralizedBanking()
    
    # Register a user
    user_address = banking_system.register_user(private_key)
    print(f"User  registered: {user_address}")

    # Get user balance
    balance = banking_system.get_user_balance(user_address)
    print(f"User  balance: {balance} tokens")

    # Deposit funds
    deposit_tx = banking_system.deposit_funds(user_address, 10)
    print(f"Deposit transaction hash: {deposit_tx}")

    # Withdraw funds
    withdraw_tx = banking_system.withdraw_funds(user_address, 5)
    print(f"Withdraw transaction hash: {withdraw_tx}")

    # Request a loan
    loan_tx = banking_system.request_loan(user_address, 100, 30)  # 100 tokens for 30 days
    print(f"Loan request transaction hash: {loan_tx}")

    # Repay the loan
    repay_tx = banking_system.repay_loan(user_address, 100)
    print(f"Loan repayment transaction hash: {repay_tx}")

    # Get current interest rate
    interest_rate = banking_system.get_current_interest_rate()
    print(f"Current interest rate: {interest_rate * 100:.2f}%")
