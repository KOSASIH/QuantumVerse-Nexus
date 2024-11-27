import hashlib
import json
from web3 import Web3

class InteroperabilityProtocols:
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

    def atomic_swap(self, chain_a, chain_b, amount_a, amount_b, recipient_b, secret):
        """Perform an atomic swap between two chains."""
        secret_hash = self.hash_secret(secret)

        # Lock asset on chain A
        self.send_transaction(chain_a, 'lockAsset', amount_a, recipient_b, secret_hash)

        # Lock asset on chain B
        self.send_transaction(chain_b, 'lockAsset', amount_b, recipient_b, secret_hash)

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

    def hash_secret(self, secret):
        """Hash the secret using SHA-256."""
        return hashlib.sha256(secret.encode()).hexdigest()

    def cross_chain_message(self, from_chain, to_chain, message):
        """Send a message from one chain to another."""
        # This is a simplified example; actual implementation may vary based on the protocol used
        self.send_transaction(from_chain, 'sendMessage', message)
        # Assume the receiving chain has a function to handle incoming messages
        self.send_transaction(to_chain, 'receiveMessage', message)

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

    protocols = InteroperabilityProtocols(chain_configs)

    # Example: Perform an atomic swap
    protocols.atomic_swap('chain_a', 'chain_b', 1, 1, '0xRecipientAddress', 'your_secret')
    print("Atomic swap executed between chain A and chain B.")

    # Example: Send a cross-chain message
    protocols.cross_chain_message('chain_a', 'chain_b', 'Hello from Chain A!')
    print("Cross-chain message sent from chain A to chain B.")
