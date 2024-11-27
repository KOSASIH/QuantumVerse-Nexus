import hashlib
import random
import time

class Consensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains 4 leading zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: Previous Proof
        :return: New Proof
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof
        :param last_proof: Previous Proof
        :param proof: Current Proof
        :return: True if correct, False if not
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def proof_of_stake(self, stakes):
        """
        Simple Proof of Stake Algorithm:
         - Randomly select a validator based on their stake
        :param stakes: Dictionary of addresses and their stakes
        :return: Selected validator
        """
        total_stake = sum(stakes.values())
        if total_stake == 0:
            return None

        # Randomly select a validator based on their stake
        random_choice = random.uniform(0, total_stake)
        current_sum = 0
        for validator, stake in stakes.items():
            current_sum += stake
            if current_sum >= random_choice:
                return validator

    def byzantine_fault_tolerance(self, proposals):
        """
        Byzantine Fault Tolerance Algorithm:
         - Requires a supermajority (more than 2/3) agreement among nodes
        :param proposals: List of proposals from nodes
        :return: Consensus value if reached, None otherwise
        """
        proposal_count = {}
        for proposal in proposals:
            if proposal in proposal_count:
                proposal_count[proposal] += 1
            else:
                proposal_count[proposal] = 1

        # Check for supermajority
        for proposal, count in proposal_count.items():
            if count > len(self.blockchain.nodes) * 2 / 3:
                return proposal

        return None

    def resolve_conflicts(self):
        """
        Consensus Algorithm: resolves conflicts by replacing our chain with the longest one in the network
        :return: True if our chain was replaced, False if not
        """
        neighbors = self.blockchain.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.blockchain.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.blockchain.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.blockchain.chain = new_chain
            return True

        return False

    def get_current_stakes(self):
        """
        Get the current stakes of all validators for Proof of Stake
        :return: Dictionary of stakes
        """
        # This is a placeholder. In a real implementation, you would retrieve stakes from a database or state.
        return {
            'validator1': 100,
            'validator2': 200,
            'validator3': 300,
        }
