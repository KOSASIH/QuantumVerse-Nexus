from web3 import Web3
from solcx import compile_source
import json

class DynamicContract:
    """A dynamic smart contract that supports upgradability."""

    def __init__(self, web3_provider):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.proxy_address = None
        self.implementation_address = None
        self.account = None

    def set_account(self, private_key):
        """Set the account for deploying and interacting with the contract."""
        self.account = self.web3.eth.account.from_key(private_key)

    def compile_contract(self, contract_source):
        """Compile the smart contract source code."""
        compiled_sol = compile_source(contract_source)
        contract_id, contract_interface = compiled_sol.popitem()
        return contract_interface

    def deploy_contract(self, contract_interface):
        """Deploy the implementation contract."""
        contract = self.web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }
        tx_hash = contract.constructor().transact(transaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        self.implementation_address = tx_receipt.contractAddress
        print(f"Implementation contract deployed at: {self.implementation_address}")

    def deploy_proxy(self):
        """Deploy the proxy contract that points to the implementation."""
        proxy_contract_source = '''
        pragma solidity ^0.8.0;

        contract Proxy {
            address public implementation;

            constructor(address _implementation) {
                implementation = _implementation;
            }

            fallback() external {
                address _impl = implementation;
                require(_impl != address(0), "Implementation not set");
                assembly {
                    calldatacopy(0, 0, calldatasize())
                    let result := delegatecall(gas(), _impl, 0, calldatasize(), 0, 0)
                    return(0, returndatasize())
                }
            }
        }
        '''
        contract_interface = self.compile_contract(proxy_contract_source)
        contract = self.web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }
        tx_hash = contract.constructor(self.implementation_address).transact(transaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        self.proxy_address = tx_receipt.contractAddress
        print(f"Proxy contract deployed at: {self.proxy_address}")

    def upgrade_implementation(self, new_contract_source):
        """Upgrade the implementation contract."""
        new_contract_interface = self.compile_contract(new_contract_source)
        self.deploy_contract(new_contract_interface)

        # Update the proxy to point to the new implementation
        upgrade_tx = f'''
        pragma solidity ^0.8.0;

        contract UpgradeableProxy {
            address public implementation;

            function upgrade(address newImplementation) public {
                implementation = newImplementation;
            }
        }
        '''
        upgrade_interface = self.compile_contract(upgrade_tx)
        upgrade_contract = self.web3.eth.contract(abi=upgrade_interface['abi'], address=self.proxy_address)
        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }
        tx_hash = upgrade_contract.functions.upgrade(self.implementation_address).transact(transaction)
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Proxy upgraded to new implementation at: {self.implementation_address}")

    def call_function(self, function_name, *args):
        """Call a function on the implementation contract through the proxy."""
        proxy_contract = self.web3.eth.contract(address=self.proxy_address, abi=self.compile_contract('contract_source')['abi'])
        return proxy_contract.functions[function_name](*args).call()

# Example Solidity contract source code
contract_source_v1 = '''
pragma solidity ^0.8.0 ;

contract SimpleStorageV1 {
    uint256 private storedData;

    function set(uint256 x) public {
        storedData = x;
    }

    function get() public view returns (uint256) {
        return storedData;
    }
}
'''

contract_source_v2 = '''
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

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"  # Replace with your Ethereum node URL
    private_key = "YOUR_PRIVATE_KEY"  # Replace with your private key

    # Create an instance of the dynamic contract
    dynamic_contract = DynamicContract(web3_provider)

    # Set the account for deployment
    dynamic_contract.set_account(private_key)

    # Compile and deploy the first version of the contract
    contract_interface_v1 = dynamic_contract.compile_contract(contract_source_v1)
    dynamic_contract.deploy_contract(contract_interface_v1)
    dynamic_contract.deploy_proxy()

    # Call a function to set data
    dynamic_contract.call_function('set', 42)

    # Call a function to get data
    value = dynamic_contract.call_function('get')
    print(f"Stored value in V1: {value}")

    # Upgrade to the new version of the contract
    dynamic_contract.upgrade_implementation(contract_source_v2)

    # Call the new function in V2
    dynamic_contract.call_function('increment')
    value = dynamic_contract.call_function('get')
    print(f"Stored value in V2 after increment: {value}")
