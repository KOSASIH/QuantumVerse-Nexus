import json
import requests
from web3 import Web3
from solcx import compile_source
from eth_account import Account

class ContractManager:
    """A comprehensive contract manager for deploying and interacting with smart contracts."""

    def __init__(self, web3_provider, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.contracts = {}

    def compile_contract(self, contract_source):
        """Compile the smart contract source code."""
        compiled_sol = compile_source(contract_source)
        contract_id, contract_interface = compiled_sol.popitem()
        return contract_interface

    def deploy_contract(self, contract_source, constructor_args=None):
        """Deploy a new smart contract."""
        contract_interface = self.compile_contract(contract_source)
        contract = self.web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }

        # Deploy the contract
        tx_hash = contract.constructor(*constructor_args).transact(transaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        self.contracts[contract_address] = contract_interface
        print(f"Contract deployed at: {contract_address}")
        return contract_address

    def upgrade_contract(self, contract_address, new_contract_source):
        """Upgrade an existing smart contract."""
        if contract_address not in self.contracts:
            raise Exception("Contract not found.")

        # Deploy the new version of the contract
        new_contract_interface = self.compile_contract(new_contract_source)
        new_contract = self.web3.eth.contract(abi=new_contract_interface['abi'], bytecode=new_contract_interface['bin'])

        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }

        # Deploy the new contract
        tx_hash = new_contract.constructor().transact(transaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        new_contract_address = tx_receipt.contractAddress

        # Update the contract reference
        self.contracts[new_contract_address] = new_contract_interface
        print(f"Contract upgraded to new version at: {new_contract_address}")
        return new_contract_address

    def call_function(self, contract_address, function_name, *args):
        """Call a function on a deployed contract."""
        if contract_address not in self.contracts:
            raise Exception("Contract not found.")

        contract = self.web3.eth.contract(address=contract_address, abi=self.contracts[contract_address]['abi'])
        return contract.functions[function_name](*args).call()

    def send_transaction(self, contract_address, function_name, *args):
        """Send a transaction to a contract function."""
        if contract_address not in self.contracts:
            raise Exception("Contract not found.")

        contract = self.web3.eth.contract(address=contract_address, abi=self.contracts[contract_address]['abi'])
        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }

        # Send the transaction
        tx_hash = contract.functions[function_name](*args).transact(transaction)
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Transaction sent to {function_name} on contract at {contract_address}")

    def fetch_data_from_oracle(self, url):
        """Fetch data from an external API (oracle)."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from oracle: {e}")
            return None

# Example Solidity contract source code
contract_source = '''
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private storedData;

    function set(uint256 x) public {
        storedData = x;
    }

    function get() public view returns (uint256) {
        return storedData;
    }
}
'''

# Example usage
if __name__ == "__main__":
    web3_provider = "https .your.ethereum.node"  # Replace with your Ethereum node URL
    private_key = "YOUR_PRIVATE_KEY"  # Replace with your private key

    # Create an instance of the ContractManager
    manager = ContractManager(web3_provider, private_key)

    # Deploy the SimpleStorage contract
    contract_address = manager.deploy_contract(contract_source)

    # Interact with the deployed contract
    manager.send_transaction(contract_address, 'set', 42)
    value = manager.call_function(contract_address, 'get')
    print(f"Stored value in contract: {value}")

    # Upgrade the contract with a new version (example)
    new_contract_source = '''
    pragma solidity ^0.8.0;

    contract SimpleStorageV2 {
        uint256 private storedData;

        function set(uint256 x) public {
            storedData = x;
        }

        function get() public view returns (uint256) {
            return storedData;
        }

        function increment() public {
            storedData += 1;
        }
    }
    '''
    new_contract_address = manager.upgrade_contract(contract_address, new_contract_source)

    # Interact with the upgraded contract
    manager.send_transaction(new_contract_address, 'increment')
    new_value = manager.call_function(new_contract_address, 'get')
    print(f"New stored value in upgraded contract: {new_value}")

    # Fetch data from an oracle
    oracle_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    oracle_data = manager.fetch_data_from_oracle(oracle_url)
    if oracle_data and 'ethereum' in oracle_data:
        eth_price = oracle_data['ethereum']['usd']
        print(f"Fetched Ethereum price from oracle: {eth_price}")
