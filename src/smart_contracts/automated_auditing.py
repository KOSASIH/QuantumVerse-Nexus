import json
import re
from web3 import Web3
from solcx import compile_source
from eth_account import Account

class AutomatedAuditor:
    """A simple automated auditor for smart contracts."""

    def __init__(self, web3_provider):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))

    def compile_contract(self, contract_source):
        """Compile the smart contract source code."""
        compiled_sol = compile_source(contract_source)
        contract_id, contract_interface = compiled_sol.popitem()
        return contract_interface

    def check_reentrancy(self, contract_source):
        """Check for potential reentrancy vulnerabilities."""
        if re.search(r'call\(|send\(|transfer\(', contract_source):
            print("Warning: Potential reentrancy vulnerability detected.")
            return True
        return False

    def check_gas_limit(self, contract_source):
        """Check for functions that may exceed gas limits."""
        if re.search(r'function\s+\w+\s*\(.*\)\s*public\s*returns\s*\(.*\)', contract_source):
            print("Info: Check gas limits for public functions.")
            return True
        return False

    def check_access_control(self, contract_source):
        """Check for proper access control mechanisms."""
        if re.search(r'onlyOwner|onlyAdmin|onlyRole', contract_source):
            print("Info: Access control mechanisms found.")
            return True
        print("Warning: No access control mechanisms found.")
        return False

    def audit_contract(self, contract_source):
        """Perform a basic audit of the smart contract."""
        print("Starting audit...")
        issues = []

        if self.check_reentrancy(contract_source):
            issues.append("Potential reentrancy vulnerability detected.")
        
        if self.check_gas_limit(contract_source):
            issues.append("Check gas limits for public functions.")
        
        if not self.check_access_control(contract_source):
            issues.append("No access control mechanisms found.")

        if not issues:
            print("Audit passed: No issues found.")
        else:
            print("Audit issues found:")
            for issue in issues:
                print(f"- {issue}")

    def estimate_gas_usage(self, contract_source, function_name, *args):
        """Estimate gas usage for a specific function."""
        contract_interface = self.compile_contract(contract_source)
        contract = self.web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        # Create a transaction for gas estimation
        transaction = {
            'from': self.web3.eth.accounts[0],
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
        }

        # Estimate gas
        gas_estimate = contract.functions[function_name](*args).estimateGas(transaction)
        print(f"Estimated gas for {function_name}: {gas_estimate}")
        return gas_estimate

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    auditor = AutomatedAuditor(web3_provider)

    # Example contract source code
    contract_source = '''
    pragma solidity ^0.8.0;

    contract Example {
        uint256 public data;

        event DataUpdated(uint256 newData);

        function setData(uint256 _data) public {
            data = _data;
            emit DataUpdated(_data);
        }

        function withdraw() public {
            // Potential reentrancy issue
            payable(msg.sender).transfer(address(this).balance);
        }
    }
    '''

    auditor.audit_contract(contract_source)
    auditor.estimate_gas_usage(contract_source, 'setData', 42)
