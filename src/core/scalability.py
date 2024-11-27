import hashlib
import random
from collections import defaultdict

class Shard:
    def __init__(self, shard_id):
        self.shard_id = shard_id
        self.transactions = []
        self.state = {}

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def process_transactions(self):
        # Simulate processing transactions
        for transaction in self.transactions:
            self.state[transaction['id']] = transaction
        self.transactions.clear()  # Clear transactions after processing

class Sharding:
    def __init__(self, num_shards):
        self.shards = [Shard(shard_id) for shard_id in range(num_shards)]

    def get_shard_id(self, transaction):
        # Simple hash-based sharding
        return int(hashlib.sha256(transaction['id'].encode()).hexdigest(), 16) % len(self.shards)

    def add_transaction(self, transaction):
        shard_id = self.get_shard_id(transaction)
        self.shards[shard_id].add_transaction(transaction)

    def process_all_shards(self):
        for shard in self.shards:
            shard.process_transactions()

class PaymentChannel:
    def __init__(self, sender, recipient):
        self.sender = sender
        self.recipient = recipient
        self.balance = 0
        self.is_open = True

    def deposit(self, amount):
        if not self.is_open:
            raise Exception("Payment channel is closed.")
        self.balance += amount

    def withdraw(self, amount):
        if not self.is_open:
            raise Exception("Payment channel is closed.")
        if amount > self.balance:
            raise Exception("Insufficient balance.")
        self.balance -= amount

    def close_channel(self):
        self.is_open = False
        print(f"Payment channel closed between {self.sender} and {self.recipient}. Final balance: {self.balance}")

class Layer2Solution:
    def __init__(self):
        self.channels = {}

    def create_channel(self, sender, recipient):
        channel_id = f"{sender}-{recipient}-{random.randint(1000, 9999)}"
        self.channels[channel_id] = PaymentChannel(sender, recipient)
        print(f"Payment channel created: {channel_id}")
        return channel_id

    def deposit_to_channel(self, channel_id, amount):
        if channel_id not in self.channels:
            raise Exception("Channel does not exist.")
        self.channels[channel_id].deposit(amount)

    def withdraw_from_channel(self, channel_id, amount):
        if channel_id not in self.channels:
            raise Exception("Channel does not exist.")
        self.channels[channel_id].withdraw(amount)

    def close_channel(self, channel_id):
        if channel_id not in self.channels:
            raise Exception("Channel does not exist.")
        self.channels[channel_id].close_channel()
        del self.channels[channel_id]

# Example usage
if __name__ == "__main__":
    # Sharding example
    sharding = Sharding(num_shards=4)

    # Add transactions to shards
    transactions = [
        {"id": "tx1", "amount": 100, "sender": "0x123", "recipient": "0x456"},
        {"id": "tx2", "amount": 200, "sender": "0x789", "recipient": "0xabc"},
        {"id": "tx3", "amount": 150, "sender": "0xdef", "recipient": "0xghi"},
        {"id": "tx4", "id": "tx1", "amount": 300, "sender": "0xjkl", "recipient": "0xmnop"},
    ]

    for tx in transactions:
        sharding.add_transaction(tx)

    # Process all shards
    sharding.process_all_shards()

    # Layer 2 solution example
    layer2 = Layer2Solution()
    channel_id = layer2.create_channel("0x123", "0x456")
    layer2.deposit_to_channel(channel_id, 50)
    layer2.withdraw_from_channel(channel_id, 20)
    layer2.close_channel(channel_id)
