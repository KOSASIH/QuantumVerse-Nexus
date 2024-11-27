import hashlib
import random
from collections import defaultdict
from typing import List, Dict, Any

class Shard:
    def __init__(self, shard_id: int):
        self.shard_id = shard_id
        self.data = []  # Stores transactions or data for this shard
        self.nodes = []  # Nodes that are part of this shard

    def add_node(self, node: str):
        """Add a node to the shard."""
        if node not in self.nodes:
            self.nodes.append(node)

    def remove_node(self, node: str):
        """Remove a node from the shard."""
        if node in self.nodes:
            self.nodes.remove(node)

    def add_data(self, transaction: Any):
        """Add data to the shard."""
        self.data.append(transaction)

    def get_data(self) -> List[Any]:
        """Retrieve data from the shard."""
        return self.data

class ShardManager:
    def __init__(self, num_shards: int):
        self.shards: Dict[int, Shard] = {i: Shard(i) for i in range(num_shards)}
        self.node_shard_map: Dict[str, int] = {}  # Maps nodes to shards

    def assign_node_to_shard(self, node: str):
        """Assign a node to a shard based on a hash of the node's identifier."""
        shard_id = self.get_shard_id(node)
        self.shards[shard_id].add_node(node)
        self.node_shard_map[node] = shard_id

    def get_shard_id(self, node: str) -> int:
        """Get the shard ID for a given node based on hashing."""
        return int(hashlib.sha256(node.encode()).hexdigest(), 16) % len(self.shards)

    def add_transaction(self, node: str, transaction: Any):
        """Add a transaction to the appropriate shard based on the node's assignment."""
        shard_id = self.node_shard_map.get(node)
        if shard_id is not None:
            self.shards[shard_id].add_data(transaction)
        else:
            raise ValueError("Node is not assigned to any shard.")

    def get_shard_data(self, shard_id: int) -> List[Any]:
        """Retrieve data from a specific shard."""
        return self.shards[shard_id].get_data()

    def get_all_data(self) -> Dict[int, List[Any]]:
        """Retrieve data from all shards."""
        return {shard_id: shard.get_data() for shard_id, shard in self.shards.items()}

class Consensus:
    def __init__(self, shard_manager: ShardManager):
        self.shard_manager = shard_manager

    def validate_transaction(self, transaction: Any) -> bool:
        """Validate a transaction (placeholder for actual validation logic)."""
        # Implement validation logic (e.g., checking signatures, balances, etc.)
        return True

    def commit_transaction(self, node: str, transaction: Any):
        """Commit a transaction to the appropriate shard after validation."""
        if self.validate_transaction(transaction):
            self.shard_manager.add_transaction(node, transaction)
        else:
            raise ValueError("Transaction validation failed.")

def main():
    # Example usage of the sharding system
    num_shards = 4
    shard_manager = ShardManager(num_shards)
    consensus = Consensus(shard_manager)

    # Simulate nodes
    nodes = [f"node_{i}" for i in range(10)]

    # Assign nodes to shards
    for node in nodes:
        shard_manager.assign_node_to_shard(node)

    # Simulate transactions
    transactions = [f"transaction_{i}" for i in range(20)]

    # Commit transactions
    for i, transaction in enumerate(transactions):
        node = random.choice(nodes)  # Randomly select a node to commit the transaction
        try:
            consensus.commit_transaction(node, transaction)
            print(f"Transaction '{transaction}' committed by {node}.")
        except ValueError as e:
            print(e)

    # Retrieve data from all shards
    all_data = shard_manager.get_all_data()
    for shard_id, data in all_data.items():
        print(f"Shard {shard_id} data: {data}")

if __name__ == "__main__":
    main()
