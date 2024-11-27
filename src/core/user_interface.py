import json
from typing import List, Dict, Any
from consensus_mechanisms import Block, ProofOfWork, ProofOfStake, PracticalByzantineFaultTolerance

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 4
        self.pow = ProofOfWork(difficulty=self.difficulty)
        self.pos = ProofOfStake()
        self.pbft = PracticalByzantineFaultTolerance(nodes=["NodeA", "NodeB", "NodeC", "NodeD"])
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the genesis block and add it to the chain."""
        genesis_block = Block(index=0, previous_hash="0", transactions=[])
        self.chain.append(genesis_block)

    def add_block(self, block: Block):
        """Add a block to the blockchain."""
        self.chain.append(block)

    def get_last_block(self) -> Block:
        """Get the last block in the blockchain."""
        return self.chain[-1]

    def mine_block(self, transactions: List[Dict[str, Any]]):
        """Mine a new block with the given transactions."""
        last_block = self.get_last_block()
        new_block = Block(index=len(self.chain), previous_hash=last_block.hash, transactions=transactions)
        mined_block = self.pow.mine_block(new_block)
        self.add_block(mined_block)
        print(f"Block {mined_block.index} mined with hash: {mined_block.hash}")

    def create_transaction(self, from_address: str, to_address: str, amount: float):
        """Create a new transaction."""
        transaction = {"from": from_address, "to": to_address, "amount": amount}
        return transaction

    def display_chain(self):
        """Display the entire blockchain."""
        for block in self.chain:
            print(f"Block {block.index}: Hash: {block.hash}, Transactions: {block.transactions}")

def main():
    blockchain = Blockchain()
    
    while True:
        print("\n=== Blockchain User Interface ===")
        print("1. Create Transaction")
        print("2. Mine Block")
        print("3. Display Blockchain")
        print("4. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            from_address = input("Enter sender address: ")
            to_address = input("Enter receiver address: ")
            amount = float(input("Enter amount: "))
            transaction = blockchain.create_transaction(from_address, to_address, amount)
            print(f"Transaction created: {transaction}")
        
        elif choice == '2':
            transactions = []
            num_transactions = int(input("Enter number of transactions to include in the block: "))
            for _ in range(num_transactions):
                from_address = input("Enter sender address: ")
                to_address = input("Enter receiver address: ")
                amount = float(input("Enter amount: "))
                transaction = blockchain.create_transaction(from_address, to_address, amount)
                transactions.append(transaction)
            blockchain.mine_block(transactions)
        
        elif choice == '3':
            blockchain.display_chain()
        
        elif choice == '4':
            print("Exiting the user interface.")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
