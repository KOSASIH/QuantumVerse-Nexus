# deploy_contract.py
from src.smart_contracts.contract_manager import ContractManager

def deploy_example_contract():
    """Deploy an example smart contract."""
    # Create a contract manager instance
    contract_manager = ContractManager()

    # Example contract code (replace with actual contract code)
    contract_code = """
    pragma solidity ^0.8.0;

    contract ExampleContract {
        string public message;

        constructor(string memory initialMessage) {
            message = initialMessage;
        }

        function setMessage(string memory newMessage) public {
            message = newMessage;
        }
    }
    """

    # Deploy the contract
    contract_address = contract_manager.deploy_contract(contract_code, "Hello, World!")
    print(f"Contract deployed! Contract Address: {contract_address}")

if __name__ == "__main__":
    deploy_example_contract()
