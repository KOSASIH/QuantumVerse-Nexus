import hashlib
import random
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[Dict[str, Any]], nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculate the hash of the block."""
        block_string = f"{self.index}{self.previous_hash}{self.transactions}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

class ProofOfWork:
    def __init__(self, difficulty: int):
        self.difficulty = difficulty

    def mine_block(self, block: Block) -> Block:
        """Perform the mining process to find a valid hash."""
        while block.hash[:self.difficulty] != '0' * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

class ProofOfStake:
    def __init__(self):
        self.stakeholders = {}  # Maps node addresses to their stakes

    def register_stakeholder(self, node: str, stake: float):
        """Register a stakeholder with their stake."""
        self.stakeholders[node] = stake

    def elect_validator(self) -> str:
        """Elect a validator based on their stake."""
        total_stake = sum(self.stakeholders.values())
        random_choice = random.uniform(0, total_stake)
        current_sum = 0
        for node, stake in self.stakeholders.items():
            current_sum += stake
            if current_sum >= random_choice:
                return node
        return None

class PracticalByzantineFaultTolerance:
    def __init__(self, nodes: List[str]):
        self.nodes = nodes
        self.ledger = []  # Stores the confirmed transactions

    def propose_block(self, block: Block) -> bool:
        """Propose a block to the network."""
        print(f"Proposing block {block.index} with hash {block.hash}.")
        votes = self.collect_votes(block)
        if len(votes) > len(self.nodes) // 2:
            self.ledger.append(block)
            print(f"Block {block.index} has been added to the ledger.")
            return True
        return False

    def collect_votes(self, block: Block) -> List[str]:
        """Simulate collecting votes from nodes."""
        votes = []
        for node in self.nodes:
            if random.choice([True, False]):  # Randomly simulate voting
                votes.append(node)
        return votes

def main():
    # Example usage of the consensus mechanisms
    # Proof of Work
    print("=== Proof of Work ===")
    pow = ProofOfWork(difficulty=4)
    block1 = Block(index=1, previous_hash="0", transactions=[{"from": "Alice", "to": "Bob", "amount": 10}])
    mined_block1 = pow.mine_block(block1)
    print(f"Mined Block 1: {mined_block1.hash} with nonce: {mined_block1.nonce}")

    # Proof of Stake
    print("\n=== Proof of Stake ===")
    pos = ProofOfStake()
    pos.register_stakeholder("NodeA", 50)
    pos.register_stakeholder("NodeB", 30)
    pos.register_stakeholder("NodeC", 20)
    validator = pos.elect_validator()
    print(f"Validator elected: {validator}")

    # Practical Byzantine Fault Tolerance
    print("\n=== Practical Byzantine Fault Tolerance ===")
    pbft = PracticalByzantineFaultTolerance(nodes=["NodeA", "NodeB", "NodeC", "NodeD"])
    block2 = Block(index=2, previous_hash=mined_block1.hash, transactions=[{"from": "Bob", "to": "Alice", "amount": 5}])
    pbft.propose_block(block2)

if __name__ == "__main__":
    main()
