import json
import requests
from web3 import Web3

class CrossChainOracle:
    def __init__(self, chain_configs, oracle_address):
        self.chains = {}
        self.oracle_address = oracle_address
        for chain_name, config in chain_configs.items():
            self.chains[chain_name] = {
                'web3': Web3(Web3.HTTPProvider(config['rpc_url'])),
                'contract': self.load_contract(config['contract_address'], config['abi'])
            }

    def load_contract(self, contract_address, abi):
        """Load the smart contract using its address and ABI."""
        return Web3(Web3.HTTPProvider('')).eth.contract(address=contract_address, abi=abi)

    def fetch_external_data(self, api_url):
        """Fetch data from an external API."""
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from {api_url}")

    def relay_data_to_chain(self, chain_name, data):
        """Relay data to a specified chain."""
        chain = self.chains[chain_name]
        tx_hash = self.send_transaction(chain_name, 'updateData', data)
        return tx_hash

    def send_transaction(self, chain_name, function_name, *args):
        """Send a transaction to a specified chain."""
        chain = self.chains[chain_name]
        contract_function = getattr(chain['contract'].functions, function_name)

        tx = contract_function(*args).buildTransaction({
            'from': chain['web3'].eth.defaultAccount,
            'nonce': chain['web3'].eth.getTransactionCount(chain['web3'].eth.defaultAccount),
            'gas': 2000000,
            'gasPrice': chain['web3'].toWei('50', 'gwei')
        })

        signed_tx = chain['web3'].eth.account.signTransaction(tx, private_key='YOUR_PRIVATE_KEY')
        tx_hash = chain['web3'].eth.sendRawTransaction(signed_tx.rawTransaction)
        return tx_hash

    def update_oracle_data(self, api_url, target_chain):
        """Fetch data from an external API and relay it to a target chain."""
        external_data = self.fetch_external_data(api_url)
        tx_hash = self.relay_data_to_chain(target_chain, external_data)
        return tx_hash

# Example usage
if __name__ == "__main__":
    chain_configs = {
        'chain_a': {
            'rpc_url': 'https://chain-a-rpc-url',
            'contract_address': '0xYourContractAAddress',
            'abi': json.loads('[]')  # Load your contract ABI here
        },
        'chain_b': {
            'rpc_url': 'https://chain-b-rpc-url',
            'contract_address': '0xYourContractBAddress',
            'abi': json.loads('[]')  # Load your contract ABI here
        }
    }

    oracle_address = '0xYourOracleAddress'
    oracle = CrossChainOracle(chain_configs, oracle_address)

    # Example: Update oracle data and relay it to chain B
    api_url = 'https://api.example.com/data'
    tx_hash = oracle.update_oracle_data(api_url, 'chain_b')
    print(f"Data relayed to chain B with transaction hash: {tx_hash.hex()}")
