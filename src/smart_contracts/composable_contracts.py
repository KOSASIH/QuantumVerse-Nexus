import json
from web3 import Web3
from solcx import compile_source
from eth_account import Account

class ComposableContractManager:
    """A manager for deploying and interacting with composable smart contracts."""

    def __init__(self, web3_provider, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.contracts = {}

    def compile_contract(self, contract_source):
        """Compile the smart contract source code."""
        compiled_sol = compile_source(contract_source)
        contract_id, contract_interface = compiled_sol.popitem()
        return contract_interface

    def deploy_storage_contract(self):
        """Deploy a simple storage contract."""
        contract_source = '''
        pragma solidity ^0.8.0;

        contract Storage {
            uint256 private data;

            event DataUpdated(uint256 newData);

            function setData(uint256 _data) public {
                data = _data;
                emit DataUpdated(_data);
            }

            function getData() public view returns (uint256) {
                return data;
            }
        }
        '''
        contract_interface = self.compile_contract(contract_source)
        contract = self.web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }

        # Deploy the storage contract
        tx_hash = contract.constructor().transact(transaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        storage_address = tx_receipt.contractAddress
        self.contracts[storage_address] = contract_interface
        print(f"Storage contract deployed at: {storage_address}")
        return storage_address

    def deploy_composer_contract(self, storage_address):
        """Deploy a composer contract that interacts with the storage contract."""
        contract_source = f'''
        pragma solidity ^0.8.0;

        interface IStorage {{
            function setData(uint256 _data) external;
            function getData() external view returns (uint256);
        }}

        contract Composer {{
            IStorage public storageContract;

            constructor(address _storageAddress) {{
                storageContract = IStorage(_storageAddress);
            }}

            function updateData(uint256 _data) public {{
                storageContract.setData(_data);
            }}

            function fetchData() public view returns (uint256) {{
                return storageContract.getData();
            }}
        }}
        '''
        contract_interface = self.compile_contract(contract_source)
        contract = self.web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }

        # Deploy the composer contract
        tx_hash = contract.constructor(storage_address).transact(transaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        composer_address = tx_receipt.contractAddress
        self.contracts[composer_address] = contract_interface
        print(f"Composer contract deployed at: {composer_address}")
        return composer_address

    def update_storage_data(self, composer_address, new_data):
        """Update data in the storage contract via the composer contract."""
        composer_contract = self.web3.eth.contract(address=composer_address, abi=self.contracts[composer_address]['abi'])

        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }

        # Call the updateData function on the composer contract
        tx_hash = composer_contract.functions.updateData(new_data).transact(transaction)
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Data updated to {new_data} via composer contract.")

    def fetch_storage_data(self, composer_address):
        """Fetch data from the storage contract via the composer contract."""
        composer_contract = self.web3.eth.contract(address=com poser_address, abi=self.contracts[composer_address]['abi'])

        # Call the fetchData function on the composer contract
        data = composer_contract.functions.fetchData().call()
        print(f"Fetched data from storage contract: {data}")
        return data

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"

    manager = ComposableContractManager(web3_provider, private_key)
    storage_address = manager.deploy_storage_contract()
    composer_address = manager.deploy_composer_contract(storage_address)
    manager.update_storage_data(composer_address, 42)
    fetched_data = manager.fetch_storage_data(composer_address)
