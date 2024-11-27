# smart_contracts_2_0_example.py
from src.smart_contracts.contract_manager import ContractManager

def deploy_and_interact_with_contract():
    """Example of deploying and interacting with Smart Contracts 2.0."""
    
    # Create a contract manager instance
    contract_manager = ContractManager()

    # Example Smart Contract 2.0 code (replace with actual contract code)
    contract_code = """
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
    """

    # Deploy the contract
    contract_address = contract_manager.deploy_contract(contract_code)
    print(f"Smart Contract deployed! Contract Address: {contract_address}")

    # Interact with the deployed contract
    contract_manager.call_function(contract_address, 'set', 42)
    value = contract_manager.call_function(contract_address, 'get')
    print(f"Value stored in contract: {value}")

if __name__ == "__main__":
    deploy_and_interact_with_contract()
