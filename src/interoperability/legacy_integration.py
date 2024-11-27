import sqlite3
import json
from web3 import Web3

class LegacyIntegration:
    def __init__(self, db_path, blockchain_rpc, contract_address):
        self.db_path = db_path
        self.blockchain = Web3(Web3.HTTPProvider(blockchain_rpc))
        self.contract_address = contract_address
        self.contract = self.load_contract(self.contract_address)

    def load_contract(self, contract_address):
        """Load the smart contract using its address and ABI."""
        # Replace with the actual ABI of your contract
        abi = []  # Load your contract ABI here
        return self.blockchain.eth.contract(address=contract_address, abi=abi)

    def read_from_legacy_db(self, query):
        """Read data from the legacy SQL database."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        return rows

    def write_to_legacy_db(self, query, params):
        """Write data to the legacy SQL database."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()

    def sync_data_to_blockchain(self, data):
        """Sync data from the legacy system to the blockchain."""
        for record in data:
            # Assuming record is a tuple and we want to store it in the blockchain
            tx_hash = self.store_on_blockchain(record)
            self.blockchain.eth.waitForTransactionReceipt(tx_hash)

    def store_on_blockchain(self, record):
        """Store a record on the blockchain."""
        # Replace with the actual function name in your smart contract
        store_function = self.contract.functions.storeData(record[0], record[1])  # Example for two fields
        tx = store_function.buildTransaction({
            'from': self.blockchain.eth.defaultAccount,
            'nonce': self.blockchain.eth.getTransactionCount(self.blockchain.eth.defaultAccount),
            'gas': 2000000,
            'gasPrice': self.blockchain.toWei('50', 'gwei')
        })
        signed_tx = self.blockchain.eth.account.signTransaction(tx, private_key='YOUR_PRIVATE_KEY')
        return self.blockchain.eth.sendRawTransaction(signed_tx.rawTransaction)

    def fetch_data_from_blockchain(self):
        """Fetch data from the blockchain."""
        # Replace with the actual function name in your smart contract
        data = self.contract.functions.getAllData().call()
        return data

# Example usage
if __name__ == "__main__":
    db_path = "path/to/your/legacy_database.db"
    blockchain_rpc = "https://your-blockchain-rpc-url"
    contract_address = "0xYourContractAddress"

    integration = LegacyIntegration(db_path, blockchain_rpc, contract_address)

    # Read data from the legacy database
    query = "SELECT * FROM your_table"
    legacy_data = integration.read_from_legacy_db(query)
    print("Data from legacy database:", legacy_data)

    # Sync data to the blockchain
    integration.sync_data_to_blockchain(legacy_data)
    print("Data synced to blockchain.")

    # Fetch data from the blockchain
    blockchain_data = integration.fetch_data_from_blockchain()
    print("Data from blockchain:", blockchain_data)
