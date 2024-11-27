import re
from web3 import Web3
from solcx import compile_source

class GasOptimizer:
    """A simple gas optimizer for smart contracts."""

    def __init__(self, web3_provider):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))

    def compile_contract(self, contract_source):
        """Compile the smart contract source code."""
        compiled_sol = compile_source(contract_source)
        contract_id, contract_interface = compiled_sol.popitem()
        return contract_interface

    def check_for_storage_read_write(self, contract_source):
        """Check for unnecessary storage reads/writes."""
        storage_pattern = r'\b(?:storage|memory)\s+\w+\s*=\s*\w+\s*;\s*'
        matches = re.findall(storage_pattern, contract_source)
        if matches:
            print("Warning: Unnecessary storage reads/writes detected.")
            for match in matches:
                print(f" - {match.strip()}")
            return True
        return False

    def check_for loops(self, contract_source):
        """Check for loops that could lead to high gas costs."""
        loop_pattern = r'for\s*\(.*\)\s*{'
        matches = re.findall(loop_pattern, contract_source)
        if matches:
            print("Warning: Loops detected that may lead to high gas costs.")
            for match in matches:
                print(f" - {match.strip()}")
            return True
        return False

    def check_for_redundant_operations(self, contract_source):
        """Check for redundant operations that can be optimized."""
        redundant_pattern = r'(\w+)\s*=\s*\1\s*;'
        matches = re.findall(redundant_pattern, contract_source)
        if matches:
            print("Warning: Redundant operations detected.")
            for match in matches:
                print(f" - Redundant assignment of {match.strip()}")
            return True
        return False

    def optimize_contract(self, contract_source):
        """Perform a basic gas optimization analysis of the smart contract."""
        print("Starting gas optimization analysis...")
        issues = []

        if self.check_for_storage_read_write(contract_source):
            issues.append("Unnecessary storage reads/writes detected.")
        
        if self.check_for_loops(contract_source):
            issues.append("Loops detected that may lead to high gas costs.")
        
        if self.check_for_redundant_operations(contract_source):
            issues.append("Redundant operations detected.")

        if not issues:
            print("Optimization analysis passed: No issues found.")
        else:
            print("Optimization issues found:")
            for issue in issues:
                print(f"- {issue}")

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"
    optimizer = GasOptimizer(web3_provider)

    # Example contract source code
    contract_source = '''
    pragma solidity ^0.8.0;

    contract Example {
        uint256 public data;
        uint256[] public values;

        function setData(uint256 _data) public {
            data = _data;
            // Unnecessary storage read
            uint256 temp = data;
            values.push(temp);
        }

        function loopExample() public {
            for (uint256 i = 0; i < 10; i++) {
                values.push(i);
            }
        }

        function redundantExample() public {
            uint256 x = 5;
            x = x; // Redundant operation
        }
    }
    '''

    optimizer.optimize_contract(contract_source)
