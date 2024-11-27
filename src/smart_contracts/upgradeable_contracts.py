import json
from web3 import Web3
from solcx import compile_source
from eth_account import Account

class UpgradeableContractManager:
    """A manager for deploying and upgrading smart contracts using a proxy pattern."""

    def __init__(self, web3_provider, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = Account.from_key(private_key)
        self.contracts = {}

    def compile_contract(self, contract_source):
        """Compile the smart contract source code."""
        compiled_sol = compile_source(contract_source)
        contract_id, contract_interface = compiled_sol.popitem()
        return contract_interface

    def deploy_proxy_contract(self, implementation_address):
        """Deploy a proxy contract that delegates calls to the implementation contract."""
        contract_source = '''
        pragma solidity ^0.8.0;

        contract Proxy {
            address public implementation;

            constructor(address _implementation) {
                implementation = _implementation;
            }

            fallback() external {
                address impl = implementation;
                assembly {
                    let ptr := mload(0x40)
                    calldatacopy(ptr, 0, calldatasize())
                    let result := delegatecall(gas(), impl, ptr, calldatasize(), 0, 0)
                    let size := returndatasize()
                    returndatacopy(ptr, 0, size)
                    switch result
                    case 0 { revert(ptr, size) }
                    default { return(ptr, size) }
                }
            }

            function setImplementation(address _implementation) public {
                implementation = _implementation;
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

        # Deploy the proxy contract
        tx_hash = contract.constructor(implementation_address).transact(transaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        proxy_address = tx_receipt.contractAddress
        self.contracts[proxy_address] = contract_interface
        print(f"Proxy contract deployed at: {proxy_address}")
        return proxy_address

    def deploy_implementation_contract(self):
        """Deploy an implementation contract."""
        contract_source = '''
        pragma solidity ^0.8.0;

        contract Implementation {
            uint256 public data;

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

        # Deploy the implementation contract
        tx_hash = contract.constructor().transact(transaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        implementation_address = tx_receipt.contractAddress
        print(f"Implementation contract deployed at: {implementation_address}")
        return implementation_address

    def upgrade_contract(self, proxy_address, new_implementation_address):
        """Upgrade the implementation contract."""
        proxy_contract = self.web3.eth.contract(address=proxy_address, abi=self.contracts[proxy_address]['abi'])

        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }

        # Set the new implementation address on the proxy contract
        tx_hash = proxy_contract.functions.setImplementation(new_implementation_address).transact(transaction)
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Proxy contract upgraded to new implementation at: {new_implementation_address}")

    def set_data(self, proxy_address, new_data):
        """Set data in the implementation contract via the proxy contract."""
        proxy_contract = self.web3.eth.contract(address=proxy_address, abi=self.contracts[proxy_address]['abi'])

        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }

        # Call the setData function on the implementation contract via the proxy
        tx_hash = proxy_contract.functions.setData(new_data).transact(transaction)
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Data set to {new_data} via proxy contract.")

    def get_data(self, proxy_address):
        """Get data from the implementation contract via the proxy contract."""
        proxy_contract = self.web3.eth.contract(address=proxy_address, abi=self.contracts[proxy_address]['abi'])

        # Call the getData function on the implementation contract via the proxy
        data = proxy_contract.functions.getData().call()
        print(f"Fetched data from implementation contract: {data}")
        return data

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    private_key = "your_private_key"

    manager = UpgradeableContractManager(web3_provider, private_key)
    implementation_address = manager.deploy_implementation_contract()
    proxy_address = manager.deploy_proxy_contract(implementation_address)
    manager.set_data(proxy_address, 100)
    fetched_data = manager.get_data(proxy_address)

    # Now let's upgrade the implementation contract
    new_implementation_address = manager.deploy_implementation_contract()
    manager.upgrade_contract(proxy_address, new_implementation_address)
    manager.set_data(proxy_address, 200)
    fetched_data_after_upgrade = manager.get_data(proxy_address)
