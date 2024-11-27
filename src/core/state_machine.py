import json
from enum import Enum, auto
from collections import defaultdict

class State(Enum):
    INITIALIZED = auto()
    PENDING = auto()
    EXECUTING = auto()
    COMPLETED = auto()
    FAILED = auto()

class Event(Enum):
    CREATE_TRANSACTION = auto()
    EXECUTE_TRANSACTION = auto()
    COMPLETE_TRANSACTION = auto()
    FAIL_TRANSACTION = auto()

class StateMachine:
    def __init__(self):
        self.state = State.INITIALIZED
        self.transaction_history = []
        self.event_handlers = {
            Event.CREATE_TRANSACTION: self.handle_create_transaction,
            Event.EXECUTE_TRANSACTION: self.handle_execute_transaction,
            Event.COMPLETE_TRANSACTION: self.handle_complete_transaction,
            Event.FAIL_TRANSACTION: self.handle_fail_transaction,
        }

    def handle_event(self, event, data=None):
        if event in self.event_handlers:
            self.event_handlers[event](data)
        else:
            raise Exception(f"Unhandled event: {event}")

    def handle_create_transaction(self, data):
        if self.state != State.INITIALIZED:
            raise Exception("Cannot create transaction in the current state.")
        self.state = State.PENDING
        transaction = {
            "id": data["id"],
            "sender": data["sender"],
            "recipient": data["recipient"],
            "amount": data["amount"],
            "status": "Pending"
        }
        self.transaction_history.append(transaction)
        print(f"Transaction created: {transaction}")

    def handle_execute_transaction(self, data):
        if self.state != State.PENDING:
            raise Exception("Cannot execute transaction in the current state.")
        self.state = State.EXECUTING
        transaction = self.get_transaction(data["id"])
        if transaction:
            transaction["status"] = "Executing"
            print(f"Executing transaction: {transaction}")
            # Simulate execution logic here
            self.handle_event(Event.COMPLETE_TRANSACTION, {"id": data["id"]})
        else:
            self.handle_event(Event.FAIL_TRANSACTION, {"id": data["id"]})

    def handle_complete_transaction(self, data):
        if self.state != State.EXECUTING:
            raise Exception("Cannot complete transaction in the current state.")
        self.state = State.COMPLETED
        transaction = self.get_transaction(data["id"])
        if transaction:
            transaction["status"] = "Completed"
            print(f"Transaction completed: {transaction}")

    def handle_fail_transaction(self, data):
        if self.state in [State.EXECUTING, State.PENDING]:
            self.state = State.FAILED
            transaction = self.get_transaction(data["id"])
            if transaction:
                transaction["status"] = "Failed"
                print(f"Transaction failed: {transaction}")

    def get_transaction(self, transaction_id):
        for transaction in self.transaction_history:
            if transaction["id"] == transaction_id:
                return transaction
        return None

    def get_state(self):
        return self.state

    def get_transaction_history(self):
        return json.dumps(self.transaction_history, indent=4)

# Example usage
if __name__ == "__main__":
    state_machine = StateMachine()

    # Create a transaction
    state_machine.handle_event(Event.CREATE_TRANSACTION, {
        "id": 1,
        "sender": "0x123",
        "recipient": "0x456",
        "amount": 100
    })

    # Execute the transaction
    state_machine.handle_event(Event.EXECUTE_TRANSACTION, {"id": 1})

    # Print transaction history
    print("Transaction History:")
    print(state_machine.get_transaction_history())

    # Attempt to complete the transaction
    state_machine.handle_event(Event.COMPLETE_TRANSACTION, {"id": 1})

    # Print final state
    print(f"Final State: {state_machine.get_state()}")
