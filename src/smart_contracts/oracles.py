import requests
import json
from web3 import Web3

class Oracle:
    """A simple oracle to fetch external data for smart contracts."""

    def __init__(self, web3_provider, contract_address, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contract_address = contract_address
        self.account = self.web3.eth.account.from_key(private_key)
        self.contract = None

    def set_contract(self, contract_abi):
        """Set the smart contract to interact with."""
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=contract_abi)

    def fetch_data(self, url):
        """Fetch data from an external API."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def send_data_to_contract(self, function_name, data):
        """Send fetched data to the smart contract."""
        if self.contract is None:
            raise Exception("Contract must be set before sending data.")

        transaction = {
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }

        # Call the function on the contract to send data
        contract_function = getattr(self.contract.functions, function_name)
        tx_hash = contract_function(data).transact(transaction)
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Data sent to contract: {data}")

# Example usage
if __name__ == "__main__":
    web3_provider = "https://your.ethereum.node"  # Replace with your Ethereum node URL
    private_key = "YOUR_PRIVATE_KEY"  # Replace with your private key
    contract_address = "YOUR_CONTRACT_ADDRESS"  # Replace with your contract address
    contract_abi = json.loads('''[
        {
            "constant": false,
            "inputs": [
                {
                    "name": "price",
                    "type": "uint256"
                }
            ],
            "name": "updatePrice",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]''')  # Replace with your contract ABI

    # Create an instance of the Oracle
    oracle = Oracle(web3_provider, contract_address, private_key)
    oracle.set_contract(contract_abi)

    # Fetch cryptocurrency price data from a public API
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    data = oracle.fetch_data(url)

    if data and 'ethereum' in data:
        price = data['ethereum']['usd']
        print(f"Fetched Ethereum price: {price}")

        # Send the fetched price to the smart contract
        oracle.send_data_to_contract('updatePrice', price)
