from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
from threading import Thread
import time

class Network:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for all routes
        self.port = 5000  # Default port for the node
        self.nodes = set()

        # Define routes
        self.app.add_url_rule('/chain', 'get_chain', self.get_chain, methods=['GET'])
        self.app.add_url_rule('/transactions/new', 'new_transaction', self.new_transaction, methods=['POST'])
        self.app.add_url_rule('/nodes/register', 'register_nodes', self.register_nodes, methods=['POST'])
        self.app.add_url_rule('/nodes/resolve', 'resolve_conflicts', self.resolve_conflicts, methods=['GET'])

    def start(self):
        """
        Start the Flask web server
        """
        self.app.run(host='0.0.0.0', port=self.port)

    def get_chain(self):
        """
        Get the full blockchain
        :return: JSON representation of the blockchain
        """
        response = {
            'chain': self.blockchain.get_chain(),
            'length': len(self.blockchain.chain),
        }
        return jsonify(response), 200

    def new_transaction(self):
        """
        Create a new transaction
        :return: JSON response with the index of the block that will hold the transaction
        """
        values = request.get_json()
        required = ['sender', 'recipient', 'amount']

        if not all(k in values for k in required):
            return 'Missing values', 400

        index = self.blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201

    def register_nodes(self):
        """
        Register new nodes in the network
        :return: JSON response with the list of registered nodes
        """
        values = request.get_json()
        nodes = values.get('nodes')

        if nodes is None:
            return 'Error: Please supply a valid list of nodes', 400

        for node in nodes:
            self.blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(self.blockchain.nodes),
        }
        return jsonify(response), 201

    def resolve_conflicts(self):
        """
        Consensus Algorithm: resolves conflicts by replacing our chain with the longest one in the network
        :return: JSON response indicating whether the chain was replaced
        """
        replaced = self.blockchain.resolve_conflicts()
        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': self.blockchain.chain,
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': self.blockchain.chain,
            }
        return jsonify(response), 200

    def broadcast_transaction(self, transaction):
        """
        Broadcast a new transaction to all nodes
        :param transaction: The transaction to broadcast
        """
        for node in self.nodes:
            url = f'http://{node}/transactions/new'
            try:
                requests.post(url, json=transaction)
            except requests.exceptions.RequestException as e:
                print(f"Error broadcasting transaction to {node}: {e}")

    def sync_chain(self):
        """
        Periodically sync the blockchain with other nodes
        """
        while True:
            for node in self.nodes:
                url = f'http://{node}/chain'
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        chain = response.json()['chain']
                        self.blockchain.resolve_conflicts(chain)
                except requests.exceptions.RequestException as e:
                    print(f"Error syncing with {node}: {e}")
            time.sleep(10)  # Sync every 10 seconds

# Example usage
if __name__ == "__main__":
    from core.blockchain import Blockchain

    blockchain = Blockchain()
    network = Network(blockchain)

    # Start the Flask server in a separate thread
    server_thread = Thread(target=network.start)
    server_thread.start()

    # Start syncing the chain
    network.sync_chain()
