import json
from web3 import Web3

class MultiChainSupport:
    def __init__(self, chain_configs):
        self.chains = {}
        for chain_name, config in chain_configs.items():
            self.chains[chain_name] = {
                'web3': Web3(Web3.HTTPProvider(config['rpc_url'])),
                'contract': self.load_contract(config['contract_address'], config['abi'])
            }

    def load_contract(self, contract_address, abi):
        """Load the smart contract using its address and ABI."""
        return Web3(Web3.HTTPProvider('')).eth.contract(address=contract_address, abi=abi)

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

    def query_data(self, chain_name, function_name, *args):
        """Query data from a specified chain."""
        chain = self.chains[chain_name]
        contract_function = getattr(chain['contract'].functions, function_name)
        return contract_function(*args).call()

    def transfer_asset(self, from_chain, to_chain, amount, recipient):
        """Transfer an asset from one chain to another."""
        # Lock the asset on the from_chain
        self.send_transaction(from_chain, 'lockAsset', amount, recipient)

        # Mint the asset on the to_chain
        self.send_transaction(to_chain, 'mintAsset', amount, recipient)

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

    multi_chain = MultiChainSupport(chain_configs)

    # Example: Send a transaction to chain A
    tx_hash = multi_chain.send_transaction('chain_a', 'someFunction', 'arg1', 'arg2')
    print(f"Transaction sent to chain A: {tx_hash.hex()}")

    # Example: Query data from chain B
    data = multi_chain.query_data('chain_b', 'getDataFunction', 'arg1')
    print(f"Data from chain B: {data}")

    # Example: Transfer an asset from chain A to chain B
    multi_chain.transfer_asset('chain_a', 'chain_b', 1, '0xRecipientAddress')
    print("Asset transferred from chain A to chain B.")
